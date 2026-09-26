import React from "react";
import { act } from "react";
import { installDom, render } from "../../runtime/react-harness.mjs";
import { List as BadList } from "./incorrect.mjs";
import { List as GoodList } from "./correct.mjs";

installDom();

async function valuesAfterReorder(List) {
  const root = await render(React.createElement(List, { items: ["a", "b"] }));
  document.querySelector("input").value = "EDITED";
  await act(async () => {
    root.render(React.createElement(List, { items: ["b", "a"] }));
  });
  const values = [...document.querySelectorAll("input")].map((node) => node.value);
  root.unmount();
  return values;
}

const bad = await valuesAfterReorder(BadList);
if (bad.join(",") !== "EDITED,b") throw new Error(bad.join(","));
console.log("incorrect: observed", bad.join(","));

const good = await valuesAfterReorder(GoodList);
if (good.join(",") !== "b,EDITED") throw new Error(good.join(","));
console.log("correct: ok", good.join(","));
