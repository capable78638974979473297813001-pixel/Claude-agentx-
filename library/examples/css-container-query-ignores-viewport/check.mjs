import path from "node:path";
import { fileURLToPath } from "node:url";
import { setHtmlFile, withPage } from "../../runtime/chrome.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
await withPage(async (page) => {
  await page.setViewport({ width: 1200, height: 800 });
  await setHtmlFile(page, path.join(here, "incorrect.html"));
  const bad = await page.$eval("#card", (el) => getComputedStyle(el).color);
  if (bad !== "rgb(255, 0, 0)") throw new Error(bad);
  console.log("incorrect: observed", bad);
  await setHtmlFile(page, path.join(here, "correct.html"));
  const good = await page.$eval("#card", (el) => getComputedStyle(el).color);
  if (good !== "rgb(0, 128, 0)") throw new Error(good);
  console.log("correct: ok", good);
});
