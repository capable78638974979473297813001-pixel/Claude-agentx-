import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parse, compileScript, compileTemplate } from "@vue/compiler-sfc";
import { reactive } from "vue";
import { snapshot } from "./incorrect.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const props = reactive({ count: 1 });
const read = snapshot(props);
props.count = 4;
if (read() !== 1) throw new Error(String(read()));
console.log("incorrect: observed", read());

const source = readFileSync(path.join(here, "App.vue"), "utf8");
const parsed = parse(source, { filename: "App.vue" });
const script = compileScript(parsed.descriptor, { id: "app" });
if (script.bindings.count !== "props") {
  throw new Error(JSON.stringify(script.bindings));
}
const template = compileTemplate({
  id: "app",
  filename: "App.vue",
  source: parsed.descriptor.template.content,
  compilerOptions: { bindingMetadata: script.bindings },
});
if (!template.code.includes("$props.count")) {
  throw new Error(template.code);
}
console.log("correct: ok", script.bindings.count);
