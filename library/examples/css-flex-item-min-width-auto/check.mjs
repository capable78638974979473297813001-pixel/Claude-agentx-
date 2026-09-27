import path from "node:path";
import { fileURLToPath } from "node:url";
import { setHtmlFile, withPage } from "../../runtime/chrome.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
await withPage(async (page) => {
  await setHtmlFile(page, path.join(here, "incorrect.html"));
  const bad = await page.$eval("#row", (el) => ({
    client: el.clientWidth,
    scroll: el.scrollWidth,
  }));
  if (bad.scroll <= bad.client) throw new Error(JSON.stringify(bad));
  console.log("incorrect: observed", JSON.stringify(bad));
  await setHtmlFile(page, path.join(here, "correct.html"));
  const good = await page.$eval("#row", (el) => ({
    client: el.clientWidth,
    scroll: el.scrollWidth,
  }));
  if (good.scroll > good.client) throw new Error(JSON.stringify(good));
  console.log("correct: ok", JSON.stringify(good));
});
