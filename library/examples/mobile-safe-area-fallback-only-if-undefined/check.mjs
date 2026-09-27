import path from "node:path";
import { fileURLToPath } from "node:url";
import { setHtmlFile, withPage } from "../../runtime/chrome.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
await withPage(async (page) => {
  await setHtmlFile(page, path.join(here, "incorrect.html"));
  const defined = await page.$eval("#pad", (el) => getComputedStyle(el).paddingTop);
  if (defined !== "0px") throw new Error(defined);
  console.log("incorrect: observed", defined);
  await setHtmlFile(page, path.join(here, "correct.html"));
  const fallback = await page.$eval("#pad", (el) => getComputedStyle(el).paddingTop);
  if (fallback !== "12px") throw new Error(fallback);
  console.log("correct: ok", fallback);
});
