import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

const bad = spawnSync(process.execPath, [path.join(here, "incorrect.js")], { encoding: "utf8" });
if (bad.status === 0 || !String(bad.stderr).includes("require is not defined in ES module scope")) {
  throw new Error(bad.stderr || bad.stdout);
}
console.log("incorrect: observed", "require is not defined in ES module scope");

const good = spawnSync(process.execPath, [path.join(here, "correct.mjs")], { encoding: "utf8" });
if (good.status !== 0 || good.stdout.trim() !== "b") {
  throw new Error(good.stderr || good.stdout);
}
console.log("correct: ok", good.stdout.trim());
