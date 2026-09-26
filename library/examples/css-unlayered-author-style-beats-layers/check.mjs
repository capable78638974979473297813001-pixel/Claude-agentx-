import path from "node:path";
import { fileURLToPath } from "node:url";
import { setHtmlFile, withPage } from "../../runtime/chrome.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
await withPage(async (page) => {
  await setHtmlFile(page, path.join(here, "incorrect.html"));
  const lost = await page.$eval("#title", (el) => getComputedStyle(el).color);
  if (lost !== "rgb(255, 0, 0)") throw new Error(lost);
  console.log("incorrect: observed", lost);
  await setHtmlFile(page, path.join(here, "correct.html"));
  const won = await page.$eval("#title", (el) => getComputedStyle(el).color);
  if (won !== "rgb(0, 0, 255)") throw new Error(won);
  console.log("correct: ok", won);
});
