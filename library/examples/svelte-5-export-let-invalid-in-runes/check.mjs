import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { compile } from "svelte/compiler";
import { render } from "svelte/server";

const here = path.dirname(fileURLToPath(import.meta.url));
const badSource = readFileSync(path.join(here, "incorrect.svelte"), "utf8");
try {
  compile(badSource, { filename: "incorrect.svelte", generate: "server" });
  throw new Error("export let compiled in runes mode");
} catch (error) {
  if (error.code !== "legacy_export_invalid") throw error;
  console.log("incorrect: observed", error.code);
}

const goodSource = readFileSync(path.join(here, "correct.svelte"), "utf8");
const compiled = compile(goodSource, { filename: "correct.svelte", generate: "server" });
const file = path.resolve(here, "../../node_modules/.skill-svelte-app.js");
const { writeFileSync } = await import("node:fs");
writeFileSync(file, compiled.js.code);
const mod = await import(file);
const html = render(mod.default, { props: { count: 7 } });
if (!html.body.includes(">7<")) throw new Error(html.body);
console.log("correct: ok", 7);
