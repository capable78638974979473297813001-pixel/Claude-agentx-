import { sortNumbers as badSort } from "./incorrect.mjs";
import { sortNumbers as goodSort } from "./correct.mjs";

const bad = badSort([10, 2, 1]);
if (bad.join(",") !== "1,10,2") {
  throw new Error(bad.join(","));
}
console.log("incorrect: observed", bad.join(","));

const good = goodSort([10, 2, 1]);
if (good.join(",") !== "1,2,10") {
  throw new Error(good.join(","));
}
console.log("correct: ok", good.join(","));
