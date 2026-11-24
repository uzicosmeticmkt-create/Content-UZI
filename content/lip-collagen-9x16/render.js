// Renders the 9:16 assets in this folder. Needs Node, Playwright (Chromium) and ffmpeg.
//   node render.js poster              -> uzi-lip-collagen-9x16.png
//   node render.js video               -> uzi-lip-collagen-13-extracts-9x16.mp4 (30 fps, H.264)
//   node render.js still <sec> <out>   -> one frame of the video, for checking
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const path = require("path");

const W = 1080, H = 1920, FPS = 30;
const here = (f) => path.join(__dirname, f);

async function open(file) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto("file://" + here(file));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  return { browser, page };
}

async function poster() {
  const { browser, page } = await open("poster.html");
  await page.screenshot({ path: here("uzi-lip-collagen-9x16.png") });
  await browser.close();
}

async function still(t, out) {
  const { browser, page } = await open("video.html");
  await page.evaluate((s) => window.render(s), Number(t));
  await page.screenshot({ path: out });
  await browser.close();
}

async function video() {
  const out = here("uzi-lip-collagen-13-extracts-9x16.mp4");
  const { browser, page } = await open("video.html");
  const duration = await page.evaluate(() => window.DURATION);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-r", String(FPS), "-movflags", "+faststart", out],
    { stdio: ["pipe", "inherit", "inherit"] });
  const frames = Math.round(duration * FPS);
  for (let i = 0; i < frames; i++) {
    await page.evaluate((s) => window.render(s), i / FPS);
    const buf = await page.screenshot({ type: "png" });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % 60 === 0) process.stdout.write(`frame ${i}/${frames}\n`);
  }
  ff.stdin.end();
  await new Promise((r, j) => ff.on("close", (c) => (c === 0 ? r() : j(new Error("ffmpeg exit " + c)))));
  await browser.close();
  console.log("wrote", out);
}

const [cmd, a, b] = process.argv.slice(2);
({ poster, video, still: () => still(a, b) })[cmd]?.().catch((e) => { console.error(e); process.exit(1); })
  ?? console.log("usage: node render.js poster | video | still <sec> <out.png>");
