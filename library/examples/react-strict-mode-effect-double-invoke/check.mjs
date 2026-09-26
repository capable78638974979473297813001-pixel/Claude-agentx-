import React, { StrictMode } from "react";
import { installDom, render } from "../../runtime/react-harness.mjs";
import { Probe as BadProbe } from "./incorrect.mjs";
import { Probe as GoodProbe } from "./correct.mjs";

installDom();
const bad = { count: 0 };
let root = await render(
  React.createElement(StrictMode, null, React.createElement(BadProbe, { calls: bad })),
);
if (bad.count !== 2) throw new Error(`effect count ${bad.count}`);
console.log("incorrect: observed", bad.count);
root.unmount();

const good = { count: 0 };
root = await render(
  React.createElement(StrictMode, null, React.createElement(GoodProbe, { calls: good })),
);
if (good.count !== 1) throw new Error(`net subscriptions ${good.count}`);
console.log("correct: ok", good.count);
root.unmount();
