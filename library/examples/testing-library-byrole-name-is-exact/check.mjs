import { JSDOM } from "jsdom";
import { saveButton as badSave } from "./incorrect.mjs";
import { saveButton as goodSave } from "./correct.mjs";

const dom = new JSDOM("<button>Save <span>draft</span></button>");
const body = dom.window.document.body;
let missed = false;
try {
  badSave(body);
} catch (error) {
  if (!String(error.message).includes('name "Save"')) throw error;
  missed = true;
}
if (!missed) throw new Error("name Save matched Save draft");
console.log("incorrect: observed", 'name "Save"');
const node = goodSave(body);
if (!node.textContent.includes("draft")) throw new Error(node.textContent);
console.log("correct: ok", node.textContent.trim());
