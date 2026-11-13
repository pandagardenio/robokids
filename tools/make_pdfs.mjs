// Turn the printable pages in web/print/ into PDFs (A4 and US Letter).
// Run from the repo root after `python3 tools/build_site.py`:
//
//     node tools/make_pdfs.mjs
//
// Needs Playwright with Chromium (`npm install playwright && npx playwright install chromium`).
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const printDir = path.join(root, "web", "print");
const pages = ["book", "journal", "poster", "certificate", "grown-ups"];
const formats = { a4: "A4", letter: "Letter" };

const browser = await chromium.launch();
const page = await browser.newPage();
for (const name of pages) {
  await page.goto(pathToFileURL(path.join(printDir, `${name}.html`)).href, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  for (const [suffix, format] of Object.entries(formats)) {
    const out = path.join(printDir, `robokids-${name}-${suffix}.pdf`);
    await page.pdf({
      path: out,
      format,
      landscape: name === "certificate",
      printBackground: true,
      margin: { top: "12mm", bottom: "12mm", left: "12mm", right: "12mm" },
    });
    console.log("wrote", path.relative(root, out));
  }
}
await browser.close();
