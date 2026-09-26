import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.resolve(here, "../../package.json"));
const React = require("react");
const { act } = require("react");
const { mock } = await import("node:test");
const { installDom, render } = await import(pathToFileURL(path.resolve(here, "../../runtime/react-harness.mjs")).href);

installDom();
mock.timers.enable({ apis: ["setInterval"] });

async function read(modPath) {
  const mod = await import(pathToFileURL(modPath).href);
  const root = await render(React.createElement(mod.Counter));
  await act(async () => {
    mock.timers.tick(3000);
  });
  const text = document.getElementById("n").textContent;
  root.unmount();
  return text;
}

const bad = await read(path.join(here, "incorrect.mjs"));
if (bad !== "1") throw new Error(bad);
console.log("incorrect: observed", bad);
const good = await read(path.join(here, "correct.mjs"));
if (good !== "3") throw new Error(good);
console.log("correct: ok", good);
