# Usage: python3 render_UZI_cleansing_40s.py <SRC dir with the 6 source mp4s> <WORK dir> <OUT.mp4>
import subprocess, sys, os, json
SRC, WORK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FPS = 30
CLIPS = {1: '1_232038.mp4', 2: '2_232354.mp4', 3: '3_232415.mp4', 4: '4_232448.mp4', 5: '5_232704.mp4', 6: '6_232905.mp4'}
HDR = {1}  # clip 1 is HLG/BT.2020 10-bit; the rest are SDR BT.709
# Audio timeline (what is heard), in final order: (clip, start, end)
AUDIO = [(1, 1.55, 13.62), (1, 31.11, 34.75), (1, 111.20, 114.88), (1, 116.00, 120.15),
         (6, 0.10, 4.90), (1, 142.75, 144.75), (1, 147.00, 149.00), (1, 150.85, 158.35)]
# Video timeline (what is seen): (clip, start, end); B-roll covers parts of the audio
VIDEO = [(1, 1.55, 7.50), (4, 13.00, 16.50), (1, 11.00, 13.62), (1, 31.11, 34.75), (1, 111.20, 114.88),
         (5, 67.30, 71.43), (6, 0.10, 4.90), (1, 142.75, 144.75), (1, 147.00, 149.00), (1, 150.85, 158.35)]
f = lambda t: round(t * FPS)  # seconds -> frame index
afr = [f(e) - f(s) for _, s, e in AUDIO]; vfr = [f(e) - f(s) for _, s, e in VIDEO]
assert sum(afr) == sum(vfr), (sum(afr), sum(vfr))
total = sum(vfr) / FPS; print('total seconds', total); assert total <= 40
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
os.makedirs(WORK, exist_ok=True)
vlist = []
for i, (c, s, e) in enumerate(VIDEO):
    n = vfr[i]; ss = f(s) / FPS
    vf = 'scale=1080:1920:flags=lanczos,'
    vf += ('colorspace=all=bt709:iall=bt2020:itrc=bt2020-10:fast=0:format=yuv420p' if c in HDR else 'format=yuv420p')
    vf += f',fps={FPS},setsar=1'
    out = f'{WORK}/v{i:02d}.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{ss:.4f}', '-i', f'{SRC}/{CLIPS[c]}', '-an', '-vf', vf, '-frames:v', str(n),
         '-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out])
    vlist.append(out); print('video', i, c, s, e, n, 'frames', flush=True)
open(f'{WORK}/vlist.txt', 'w').write(''.join(f"file '{p}'\n" for p in vlist))
# Audio: cut each piece with 20 ms fade-in / 30 ms fade-out, then join
inputs, fc, labels = [], [], []
for i, (c, s, e) in enumerate(AUDIO):
    d = afr[i] / FPS; ss = f(s) / FPS
    inputs += ['-ss', f'{ss:.4f}', '-t', f'{d + 0.5:.4f}', '-i', f'{SRC}/{CLIPS[c]}']
    fc.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d:.4f},asetpts=PTS-STARTPTS,'
              f'afade=t=in:d=0.02,afade=t=out:st={d - 0.03:.4f}:d=0.03[a{i}]')
    labels.append(f'[a{i}]')
fc.append(''.join(labels) + f'concat=n={len(AUDIO)}:v=0:a=1[aout]')
run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[aout]', '-c:a', 'pcm_s16le', f'{WORK}/audio_raw.wav'])
# Two-pass loudness normalisation to -14 LUFS (social video standard)
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f'{WORK}/audio_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                   capture_output=True, text=True)
j = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1]); print('loudness in', j['input_i'], 'LUFS')
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
run(['ffmpeg', '-v', 'error', '-y', '-i', f'{WORK}/audio_raw.wav', '-af', ln + ',aresample=48000', '-c:a', 'pcm_s16le', f'{WORK}/audio_norm.wav'])
# Final: join video pieces, re-encode once, mux audio
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{WORK}/vlist.txt', '-i', f'{WORK}/audio_norm.wav',
     '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-maxrate', '10M', '-bufsize', '20M', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
     '-r', str(FPS), '-g', '60', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
     '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT])
print('wrote', OUT)
