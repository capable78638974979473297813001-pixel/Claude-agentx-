import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const result = spawnSync(process.execPath, [path.join(here, "sample.ts")], {
  encoding: "utf8",
});
if (result.status === 0) {
  throw new Error("type syntax ran without the strip-types flag");
}
const text = `${result.stdout}\n${result.stderr}`;
if (!text.includes("Unexpected token") && !text.includes("SyntaxError")) {
  throw new Error(text);
}
console.log("incorrect: observed");
console.log(text.trim().split("\n")[0]);
