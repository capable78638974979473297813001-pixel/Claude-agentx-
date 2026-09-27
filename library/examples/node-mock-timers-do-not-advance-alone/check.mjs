import { mock } from "node:test";
import { schedule } from "./incorrect.mjs";
import { advance } from "./correct.mjs";

const warnings = [];
process.on("warning", (warning) => {
  warnings.push(`${warning.name}: ${warning.message}`);
});
mock.timers.enable({ apis: ["setTimeout"] });
const flag = { fired: false };
schedule(flag);
await new Promise((resolve) => setImmediate(resolve));
if (flag.fired) throw new Error("5s timer fired without tick");
console.log("incorrect: observed", flag.fired);
advance();
if (!flag.fired) throw new Error("tick did not run the timer");
console.log("correct: ok", flag.fired);
await new Promise((resolve) => setImmediate(resolve));
if (!warnings.some((line) => line.startsWith("ExperimentalWarning:"))) {
  throw new Error(warnings.join("\n") || "missing ExperimentalWarning");
}
mock.timers.reset();
