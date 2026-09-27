import { fire as badFire } from "./incorrect.mjs";
import { fire as goodFire } from "./correct.mjs";

const reasons = [];
process.on("unhandledRejection", (error) => {
  reasons.push(error.message);
});

const bad = badFire();
await new Promise((resolve) => setTimeout(resolve, 30));
if (bad !== "fell-through" || !reasons.includes("nope")) {
  throw new Error(JSON.stringify({ bad, reasons }));
}
console.log("incorrect: observed", bad);

const good = await goodFire();
if (good !== "nope") throw new Error(good);
console.log("correct: ok", good);
