import { mock } from "node:test";
import { schedule } from "./incorrect.mjs";
import { advance } from "./correct.mjs";

mock.timers.enable({ apis: ["setTimeout"] });
const flag = { fired: false };
schedule(flag);
await new Promise((resolve) => setImmediate(resolve));
if (flag.fired) throw new Error("5s timer fired without tick");
console.log("incorrect: observed", flag.fired);
advance();
if (!flag.fired) throw new Error("tick did not run the timer");
console.log("correct: ok", flag.fired);
mock.timers.reset();
