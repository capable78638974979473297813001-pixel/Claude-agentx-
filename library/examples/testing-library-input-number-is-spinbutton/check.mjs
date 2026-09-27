import { JSDOM } from "jsdom";
import { amount as badAmount } from "./incorrect.mjs";
import { amount as goodAmount } from "./correct.mjs";

const dom = new JSDOM(
  '<label>Amount <input type="number" value="3" /></label>',
);
const body = dom.window.document.body;
try {
  badAmount(body);
  throw new Error("textbox query matched a number input");
} catch (error) {
  if (!String(error.message).includes('role "textbox"')) throw error;
  console.log("incorrect: observed", 'role "textbox"');
}
const node = goodAmount(body);
if (node.tagName !== "INPUT" || node.type !== "number") throw new Error(node.outerHTML);
console.log("correct: ok", node.type);
