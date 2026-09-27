import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const { withPage } = await import(pathToFileURL(path.resolve(here, "../../runtime/chrome.mjs")).href);

async function color(page, name) {
  await page.goto(pathToFileURL(path.join(here, name)).href, { waitUntil: "domcontentloaded" });
  return page.$eval("#title", (el) => getComputedStyle(el).color);
}

await withPage(async (page) => {
  const bad = await color(page, "incorrect.html");
  if (bad !== "rgb(255, 0, 0)") throw new Error(bad);
  console.log("incorrect: observed", bad);
  const good = await color(page, "correct.html");
  if (good !== "rgb(0, 128, 0)") throw new Error(good);
  console.log("correct: ok", good);
});
