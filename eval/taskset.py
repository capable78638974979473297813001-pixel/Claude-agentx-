"""Fifty coding tasks. Starters fail their check. Solutions pass it."""

from __future__ import annotations


def task(id, area, prompt, expected, command, check_name, starter, solution, check, timeout=45):
    return {
        "id": id,
        "area": area,
        "prompt": prompt,
        "expected_skills": expected,
        "command": command,
        "check_name": check_name,
        "starter": starter,
        "solution": solution,
        "check": check,
        "timeout": timeout,
    }


def py(id, area, prompt, expected, starter, solution, check, timeout=30):
    return task(
        id, area, prompt, expected, ["python3", "check.py"], "check.py",
        {"answer.py": starter}, {"answer.py": solution}, check, timeout,
    )


def node(id, area, prompt, expected, starter_files, solution_files, check, timeout=30):
    return task(
        id, area, prompt, expected, ["node", "check.mjs"], "check.mjs",
        starter_files, solution_files, check, timeout,
    )


LOAD = """import importlib.util
spec = importlib.util.spec_from_file_location("answer", "answer.py")
answer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(answer)
"""

REACT = """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const React = require("react");
"""

CHROME = """import { pathToFileURL } from "node:url";
const { withPage, setHtmlFile } = await import(
  pathToFileURL(process.env.SKILL_REPO + "/library/runtime/chrome.mjs").href
);
"""


TASKS = [
    node(
        "react-ref-reaches-input",
        "frontend",
        "React 19 function component. Parent ref callback stays null. Accessing element.ref is no longer supported. Pass ref through to the input.",
        ["react-19-ref-as-prop"],
        {"answer.mjs": REACT + """
export function Field({ label, ref }) {
  return React.createElement("input", { "aria-label": label });
}
"""},
        {"answer.mjs": REACT + """
export function Field({ label, ref }) {
  return React.createElement("input", { "aria-label": label, ref });
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const React = require("react");
const { installDom, render } = await import(pathToFileURL(process.env.SKILL_REPO + "/library/runtime/react-harness.mjs").href);
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
installDom();
let node = null;
await render(React.createElement(answer.Field, { label: "Name", ref: (el) => { node = el; } }));
if (!node || node.tagName !== "INPUT") throw new Error(String(node && node.tagName));
""",
    ),
    node(
        "strict-mode-effect-cleanup",
        "frontend",
        "useEffect runs twice under React StrictMode in development. Subscription count ends at 2 unless the effect returns a cleanup that decrements.",
        ["react-strict-mode-effect-double-invoke"],
        {"answer.mjs": REACT + """
export function Probe({ calls }) {
  React.useEffect(() => {
    calls.count += 1;
  }, [calls]);
  return null;
}
"""},
        {"answer.mjs": REACT + """
export function Probe({ calls }) {
  React.useEffect(() => {
    calls.count += 1;
    return () => {
      calls.count -= 1;
    };
  }, [calls]);
  return null;
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const React = require("react");
const { installDom, render } = await import(pathToFileURL(process.env.SKILL_REPO + "/library/runtime/react-harness.mjs").href);
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
installDom();
const calls = { count: 0 };
await render(React.createElement(React.StrictMode, null, React.createElement(answer.Probe, { calls })));
if (calls.count !== 1) throw new Error(String(calls.count));
""",
    ),
    node(
        "list-key-follows-item",
        "frontend",
        "After editing the first input to EDITED and reordering items from a,b to b,a, key={index} keeps values EDITED,b. key must be the item so values are b,EDITED.",
        ["react-index-key-sticks-dom-state"],
        {"answer.mjs": REACT + """
export function List({ items }) {
  return React.createElement(
    "div",
    null,
    items.map((item, index) => React.createElement("input", { key: index, defaultValue: item })),
  );
}
"""},
        {"answer.mjs": REACT + """
export function List({ items }) {
  return React.createElement(
    "div",
    null,
    items.map((item) => React.createElement("input", { key: item, defaultValue: item })),
  );
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const React = require("react");
const { act } = require("react");
const { installDom, render } = await import(pathToFileURL(process.env.SKILL_REPO + "/library/runtime/react-harness.mjs").href);
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
installDom();
const root = await render(React.createElement(answer.List, { items: ["a", "b"] }));
document.querySelector("input").value = "EDITED";
await act(async () => {
  root.render(React.createElement(answer.List, { items: ["b", "a"] }));
});
const values = [...document.querySelectorAll("input")].map((node) => node.value).join(",");
if (values !== "b,EDITED") throw new Error(values);
""",
    ),
    node(
        "number-input-spinbutton",
        "frontend",
        'getByRole(container, "textbox") throws Unable to find an accessible element with the role "textbox" for <input type="number"> labeled Amount. HTML-AAM role is spinbutton. @testing-library/dom 10.',
        ["testing-library-input-number-is-spinbutton"],
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function amount(container) {
  return getByRole(container, "textbox", { name: "Amount" });
}
"""},
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function amount(container) {
  return getByRole(container, "spinbutton", { name: "Amount" });
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { JSDOM } = require("jsdom");
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const dom = new JSDOM('<label>Amount <input type="number" /></label>');
const node = answer.amount(dom.window.document.body);
if (node.getAttribute("type") !== "number") throw new Error(node.outerHTML);
""",
    ),
    node(
        "byrole-name-is-full-string",
        "frontend",
        'getByRole button name "Save" does not match accessible name Save draft. The query throws Unable to find an accessible element with the role "button" and name "Save". Pass the full name.',
        ["testing-library-byrole-name-is-exact"],
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function saveButton(container) {
  return getByRole(container, "button", { name: "Save" });
}
"""},
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function saveButton(container) {
  return getByRole(container, "button", { name: "Save draft" });
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { JSDOM } = require("jsdom");
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const dom = new JSDOM("<button>Save <span>draft</span></button>");
const node = answer.saveButton(dom.window.document.body);
if (!node.textContent.includes("draft")) throw new Error(node.textContent);
""",
    ),
    node(
        "byrole-regex-matches-multiple",
        "frontend",
        'getByRole with name /Save/ throws Found multiple elements with the role "button" and name /Save/ when buttons are Save draft and Save as. Query the one full accessible name Save draft.',
        ["testing-library-byrole-name-is-exact"],
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function saveButton(container) {
  return getByRole(container, "button", { name: /Save/ });
}
"""},
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function saveButton(container) {
  return getByRole(container, "button", { name: "Save draft" });
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { JSDOM } = require("jsdom");
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const dom = new JSDOM("<button>Save draft</button><button>Save as</button>");
const node = answer.saveButton(dom.window.document.body);
if (node.textContent.trim() !== "Save draft") throw new Error(node.textContent);
""",
    ),
    node(
        "byrole-name-case",
        "frontend",
        'getByRole name strings are case-sensitive. name "save" does not match a button whose accessible name is Save. @testing-library/dom exact name option.',
        ["testing-library-byrole-name-is-exact"],
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function saveButton(container) {
  return getByRole(container, "button", { name: "save" });
}
"""},
        {"answer.mjs": """import { createRequire } from "node:module";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { getByRole } = require("@testing-library/dom");
export function saveButton(container) {
  return getByRole(container, "button", { name: "Save" });
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { JSDOM } = require("jsdom");
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const dom = new JSDOM("<button>Save</button>");
const node = answer.saveButton(dom.window.document.body);
if (node.textContent.trim() !== "Save") throw new Error(node.textContent);
""",
    ),
    node(
        "unlayered-style-loses",
        "frontend",
        "CSS cascade: unlayered #title { color red } beats @layer components { body #title { color blue } }. Put both rules in layers so the component layer wins and computed color is rgb(0, 0, 255). css-cascade-5.",
        ["css-unlayered-author-style-beats-layers"],
        {"answer.html": """<style>
  @layer components {
    body #title { color: rgb(0, 0, 255); }
  }
  #title { color: rgb(255, 0, 0); }
</style>
<p id="title">Title</p>
"""},
        {"answer.html": """<style>
  @layer reset, components;
  @layer reset {
    #title { color: rgb(255, 0, 0); }
  }
  @layer components {
    body #title { color: rgb(0, 0, 255); }
  }
</style>
<p id="title">Title</p>
"""},
        CHROME + """
await withPage(async (page) => {
  await setHtmlFile(page, "answer.html");
  const color = await page.$eval("#title", (el) => getComputedStyle(el).color);
  if (color !== "rgb(0, 0, 255)") throw new Error(color);
});
""",
        timeout=40,
    ),
    node(
        "flex-min-width-zero",
        "frontend",
        "Flex item min-width auto plus white-space nowrap makes a 100px row scroll. Set min-width 0 and overflow hidden on the value so scrollWidth is not greater than clientWidth.",
        ["css-flex-item-min-width-auto"],
        {"answer.html": """<style>
  #row { display: flex; width: 100px; }
  #label { width: 40px; flex: 0 0 auto; }
  #value { flex: 1 1 auto; white-space: nowrap; }
</style>
<div id="row"><span id="label">Id</span><span id="value">UNBREAKABLE_TOKEN_VALUE</span></div>
"""},
        {"answer.html": """<style>
  #row { display: flex; width: 100px; }
  #label { width: 40px; flex: 0 0 auto; }
  #value { flex: 1 1 auto; min-width: 0; white-space: nowrap; overflow: hidden; }
</style>
<div id="row"><span id="label">Id</span><span id="value">UNBREAKABLE_TOKEN_VALUE</span></div>
"""},
        CHROME + """
await withPage(async (page) => {
  await setHtmlFile(page, "answer.html");
  const box = await page.$eval("#row", (el) => ({ client: el.clientWidth, scroll: el.scrollWidth }));
  if (box.scroll > box.client) throw new Error(JSON.stringify(box));
});
""",
        timeout=40,
    ),
    node(
        "container-query-not-viewport",
        "frontend",
        "Viewport is 1200px and the card wrapper is 200px. @media (min-width: 300px) paints the card red. Use container-type inline-size and @container (max-width: 250px) so the card is rgb(0, 128, 0). css-contain-3.",
        ["css-container-query-ignores-viewport"],
        {"answer.html": """<style>
  #wrap { width: 200px; }
  #card { color: rgb(0, 0, 0); }
  @media (min-width: 300px) {
    #card { color: rgb(255, 0, 0); }
  }
</style>
<div id="wrap"><p id="card">Card</p></div>
"""},
        {"answer.html": """<style>
  #wrap { container-type: inline-size; width: 200px; }
  #card { color: rgb(0, 0, 0); }
  @container (min-width: 300px) {
    #card { color: rgb(255, 0, 0); }
  }
  @container (max-width: 250px) {
    #card { color: rgb(0, 128, 0); }
  }
</style>
<div id="wrap"><p id="card">Card</p></div>
"""},
        CHROME + """
await withPage(async (page) => {
  await page.setViewport({ width: 1200, height: 800 });
  await setHtmlFile(page, "answer.html");
  const color = await page.$eval("#card", (el) => getComputedStyle(el).color);
  if (color !== "rgb(0, 128, 0)") throw new Error(color);
});
""",
        timeout=40,
    ),
    node(
        "enter-does-not-submit",
        "frontend",
        "A one-field form submits on Enter even with no submit button. type=button does not stop implicit submission. preventDefault on keydown Enter must leave the submit count at 0. HTML implicit submission.",
        ["html-enter-implicitly-submits-form"],
        {"answer.html": """<form id="find">
  <input id="q" name="q" />
</form>
"""},
        {"answer.html": """<form id="find">
  <input id="q" name="q" />
</form>
<script>
  document.getElementById("q").addEventListener("keydown", (event) => {
    if (event.key === "Enter") event.preventDefault();
  });
</script>
"""},
        CHROME + """
await withPage(async (page) => {
  await setHtmlFile(page, "answer.html");
  await page.evaluate(() => {
    window.__submits = 0;
    document.getElementById("find").addEventListener("submit", (event) => {
      event.preventDefault();
      window.__submits += 1;
    });
  });
  await page.focus("#q");
  await page.keyboard.press("Enter");
  const count = await page.evaluate(() => window.__submits);
  if (count !== 0) throw new Error("submits=" + count);
});
""",
        timeout=40,
    ),
    py(
        "wcag-srgb-contrast",
        "frontend",
        "WCAG 2.2 contrast minimum 4.5. Dividing channel by 255 reports about 1.90 for rgb(128,128,128) on white. Spec linearization reports 3.9494396480491156. rgb(119,119,119) fails AA and rgb(118,118,118) passes.",
        ["wcag-contrast-below-4-5-fails-aa"],
        """def contrast_ratio(foreground, background):
    def lin(channel):
        return channel / 255
    def lum(color):
        return 0.2126 * lin(color[0]) + 0.7152 * lin(color[1]) + 0.0722 * lin(color[2])
    lighter = max(lum(foreground), lum(background))
    darker = min(lum(foreground), lum(background))
    return (lighter + 0.05) / (darker + 0.05)

def passes_normal_text_aa(foreground, background):
    return contrast_ratio(foreground, background) >= 4.5
""",
        """def _linearize(channel):
    value = channel / 255
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4

def contrast_ratio(foreground, background):
    def lum(color):
        return 0.2126 * _linearize(color[0]) + 0.7152 * _linearize(color[1]) + 0.0722 * _linearize(color[2])
    lighter = max(lum(foreground), lum(background))
    darker = min(lum(foreground), lum(background))
    return (lighter + 0.05) / (darker + 0.05)

def passes_normal_text_aa(foreground, background):
    return contrast_ratio(foreground, background) >= 4.5
""",
        LOAD + """
white = (255, 255, 255)
gray = answer.contrast_ratio((128, 128, 128), white)
if abs(gray - 3.9494396480491156) > 0.001:
    raise SystemExit(gray)
if answer.passes_normal_text_aa((119, 119, 119), white):
    raise SystemExit("119 passed")
if not answer.passes_normal_text_aa((118, 118, 118), white):
    raise SystemExit("118 failed")
""",
    ),
    node(
        "svelte-props-not-export-let",
        "frontend",
        "Svelte 5 compiler error legacy_export_invalid: Cannot use export let in runes mode — use $props() instead. Render count 7 from $props().",
        ["svelte-5-export-let-invalid-in-runes"],
        {"answer.svelte": """<script>
  export let count = 0;
  let extra = $state(1);
</script>
<p>{count}{extra}</p>
"""},
        {"answer.svelte": """<script>
  let { count = 0 } = $props();
</script>
<p>{count}</p>
"""},
        """import { createRequire } from "node:module";
import { readFileSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { compile } = require("svelte/compiler");
const { render } = require("svelte/server");
const source = readFileSync("answer.svelte", "utf8");
const compiled = compile(source, { filename: "answer.svelte", generate: "server" });
const file = process.env.SKILL_REPO + "/library/node_modules/.bench-svelte-app.js";
writeFileSync(file, compiled.js.code);
const mod = await import(pathToFileURL(file).href);
const html = render(mod.default, { props: { count: 7 } });
if (!html.body.includes(">7<")) throw new Error(html.body);
""",
        timeout=40,
    ),
    node(
        "vue-prop-read-stays-live",
        "frontend",
        "Vue 3.5 defineProps destructure stays bound to $props.count. A plain const count = props.count still returns 1 after props.count = 4. Return a reader that sees 4.",
        ["vue-3-5-destructured-props-stay-bound"],
        {"answer.mjs": """export function watchCount(props) {
  const count = props.count;
  return () => count;
}
"""},
        {"answer.mjs": """export function watchCount(props) {
  return () => props.count;
}
"""},
        """import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
const require = createRequire(process.env.SKILL_REPO + "/library/package.json");
const { reactive } = require("vue");
const answer = await import(pathToFileURL(process.cwd() + "/answer.mjs").href);
const props = reactive({ count: 1 });
const read = answer.watchCount(props);
props.count = 4;
if (read() !== 4) throw new Error(String(read()));
""",
    ),
]

from eval.taskset_rest import MORE  # noqa: E402

TASKS.extend(MORE)
