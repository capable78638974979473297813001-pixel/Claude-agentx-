import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const { withPage, setHtmlFile } = await import(
  pathToFileURL(path.resolve(here, "../../runtime/chrome.mjs")).href
);

async function measure(name) {
  return withPage(async (page) => {
    await setHtmlFile(page, path.join(here, name));
    const metrics = await page.metrics();
    const reads = await page.evaluate(() => window.__reads);
    return { layout: metrics.LayoutCount, reads };
  });
}

const bad = await measure("incorrect.html");
if (bad.layout !== 81 || bad.reads !== 1440) throw new Error(JSON.stringify(bad));
console.log("incorrect: observed", bad.layout);
const good = await measure("correct.html");
if (good.layout !== 2 || good.reads !== 1440) throw new Error(JSON.stringify(good));
console.log("correct: ok", good.layout);
