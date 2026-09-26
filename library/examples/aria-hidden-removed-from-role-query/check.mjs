import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.resolve(here, "../../package.json"));
const { JSDOM } = require("jsdom");
const html = `<div aria-hidden="true"><button>Save</button></div>`;

async function load(name) {
  return import(pathToFileURL(path.join(here, name)).href);
}

const dom = new JSDOM(html);
const texts = [...dom.window.document.querySelectorAll("button")].map((node) => node.textContent.trim());
if (texts.join(",") !== "Save") throw new Error(texts.join(","));
let threw = false;
try {
  (await load("incorrect.mjs")).saveButton(dom.window.document.body);
} catch (error) {
  if (!String(error.message).includes('name "Save"')) throw error;
  threw = true;
}
if (!threw) throw new Error("aria-hidden button was exposed");
console.log("incorrect: observed", 'name "Save"');
const node = (await load("correct.mjs")).saveButton(dom.window.document.body);
if (node.textContent.trim() !== "Save") throw new Error(node.textContent);
console.log("correct: ok", node.textContent.trim());
