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

  await page.setContent(
    `<form id="find"><input id="q" name="q" /><button type="button">Go</button></form>`,
    { waitUntil: "domcontentloaded" },
  );
  await page.evaluate(() => {
    window.__submits = 0;
    document.getElementById("find").addEventListener("submit", (event) => {
      event.preventDefault();
      window.__submits += 1;
    });
  });
  await page.focus("#q");
  await page.keyboard.press("Enter");
  const withButton = await page.evaluate(() => window.__submits);
  if (withButton !== 1) throw new Error(`type=button submits=${withButton}`);
  const synthetic = await page.evaluate(() => {
    window.__submits = 0;
    document.getElementById("q").dispatchEvent(
      new KeyboardEvent("keydown", { key: "Enter", bubbles: true, cancelable: true }),
    );
    return window.__submits;
  });
  if (synthetic !== 0) throw new Error(`synthetic submits=${synthetic}`);

  const good = await submits(page, "correct.html");
  if (good !== 0) throw new Error(`preventDefault still submitted=${good}`);
  console.log("correct: ok", good);
});
