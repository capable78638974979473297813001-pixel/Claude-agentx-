import React from "react";
import { installDom, render } from "../../runtime/react-harness.mjs";
import { Field as BadField } from "./incorrect.mjs";
import { Field as GoodField } from "./correct.mjs";

installDom();

let badNode = null;
let root = await render(React.createElement(BadField, {
  label: "Name",
  ref: (node) => {
    badNode = node;
  },
}));
if (badNode) throw new Error("ignored ref was attached");
console.log("incorrect: observed", badNode);
root.unmount();

let goodNode = null;
root = await render(React.createElement(GoodField, {
  label: "Name",
  ref: (node) => {
    goodNode = node;
  },
}));
if (!goodNode || goodNode.tagName !== "INPUT") throw new Error(String(goodNode));
console.log("correct: ok", goodNode.tagName);
root.unmount();
