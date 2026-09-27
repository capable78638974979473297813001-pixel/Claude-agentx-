import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const { withPage } = await import(pathToFileURL(path.resolve(here, "../../runtime/chrome.mjs")).href);

async function keys(page, name) {
  await page.goto(pathToFileURL(path.join(here, name)).href, { waitUntil: "domcontentloaded" });
  return page.evaluate(() => window.__keys);
}

await withPage(async (page) => {
  const bad = await keys(page, "incorrect.html");
  if (bad !== "a,b") throw new Error(bad);
  console.log("incorrect: observed", bad);
  const good = await keys(page, "correct.html");
  if (good !== "a") throw new Error(good);
  console.log("correct: ok", good);
});
