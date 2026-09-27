import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const { withPage } = await import(pathToFileURL(path.resolve(here, "../../runtime/chrome.mjs")).href);

async function pops(page, name) {
  await page.goto(pathToFileURL(path.join(here, name)).href, { waitUntil: "domcontentloaded" });
  await new Promise((resolve) => setTimeout(resolve, 100));
  return page.evaluate(() => window.__pops);
}

await withPage(async (page) => {
  const bad = await pops(page, "incorrect.html");
  if (bad !== 0) throw new Error(String(bad));
  console.log("incorrect: observed", bad);
  const good = await pops(page, "correct.html");
  if (good !== 1) throw new Error(String(good));
  console.log("correct: ok", good);
});
