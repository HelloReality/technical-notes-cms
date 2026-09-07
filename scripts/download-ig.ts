// Download all Instagram carousel images from the collected URLs.
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { join } from "path";

const outDir = join(process.cwd(), "downloads", "instagram-DcdSiAhFbh0");
mkdirSync(outDir, { recursive: true });

const raw = readFileSync("/tmp/ig_urls_raw.txt", "utf8").trim();
// The file contains the JSON string result from agent-browser eval,
// wrapped in double quotes with escaped content. Parse it.
let urls: string[];
try {
  urls = JSON.parse(JSON.parse(raw));
} catch {
  // Fallback: the file might already be a plain JSON array
  urls = JSON.parse(raw);
}

console.log(`Found ${urls.length} images to download`);

let ok = 0;
let fail = 0;
for (let i = 0; i < urls.length; i++) {
  const url = urls[i];
  const num = String(i + 1).padStart(2, "0");
  // Extract a short id from the URL for the filename
  const match = url.match(/\/(\d+_\d+_\d+)_n\.webp/);
  const id = match ? match[1].slice(0, 20) : `img`;
  const filename = `${num}_${id}.webp`;
  const filepath = join(outDir, filename);
  try {
    const res = await fetch(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        Accept: "image/webp,image/*,*/*",
      },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buf = await res.arrayBuffer();
    writeFileSync(filepath, Buffer.from(buf));
    console.log(`  ✓ ${num}/${urls.length} ${filename} (${(buf.byteLength / 1024).toFixed(0)} KB)`);
    ok++;
  } catch (err) {
    console.error(`  ✗ ${num}/${urls.length} ${filename}: ${err instanceof Error ? err.message : "failed"}`);
    fail++;
  }
}

console.log(`\nDone: ${ok} downloaded, ${fail} failed → ${outDir}`);
