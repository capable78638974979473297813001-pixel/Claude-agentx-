import path from "node:path";
import { fileURLToPath } from "node:url";
import { setHtmlFile, withPage } from "../../runtime/chrome.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

async function submits(page, file) {
  await setHtmlFile(page, path.join(here, file));
  await page.evaluate(() => {
    window.__submits = 0;
    document.getElementById("find").addEventListener("submit", (event) => {
      event.preventDefault();
      window.__submits += 1;
    });
  });
  await page.focus("#q");
  await page.keyboard.press("Enter");
  return page.evaluate(() => window.__submits);
}

await withPage(async (page) => {
  const bad = await submits(page, "incorrect.html");
  if (bad !== 1) throw new Error(`single-field form submits=${bad}`);
  console.log("incorrect: observed", bad);
  const good = await submits(page, "correct.html");
  if (good !== 0) throw new Error(`preventDefault still submitted=${good}`);
  console.log("correct: ok", good);
});
