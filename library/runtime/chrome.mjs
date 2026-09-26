import puppeteer from "puppeteer-core";
import { readFileSync } from "node:fs";

const executablePath = process.env.CHROME_PATH || "/usr/bin/google-chrome";

export async function withPage(fn) {
  const browser = await puppeteer.launch({
    executablePath,
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
  });
  try {
    const page = await browser.newPage();
    return await fn(page);
  } finally {
    await browser.close();
  }
}

export async function setHtmlFile(page, file) {
  const html = readFileSync(file, "utf8");
  await page.setContent(html, { waitUntil: "domcontentloaded" });
}
