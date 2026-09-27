import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const result = spawnSync(
  process.execPath,
  ["--experimental-strip-types", path.join(here, "sample.ts")],
  { encoding: "utf8" },
);
if (result.status !== 0) {
  throw new Error(result.stderr);
}
if (!result.stdout.includes("2")) {
  throw new Error(result.stdout);
}
if (!result.stderr.includes("ExperimentalWarning")) {
  throw new Error(result.stderr);
}
console.log("correct: ok");
