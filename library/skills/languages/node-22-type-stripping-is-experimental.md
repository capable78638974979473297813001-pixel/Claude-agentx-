---
id: node-22-type-stripping-is-experimental
area: languages
topic: node
task: run-typescript-with-strip-types
title: Node.js 22.14.0 needs --experimental-strip-types to run this .ts file
description: Use when node sample.ts on Node.js 22.14.0 throws SyntaxError, and --experimental-strip-types prints 2 plus ExperimentalWarning.
triggers:
  - node SyntaxError type annotation
  - --experimental-strip-types
  - type stripping ExperimentalWarning
  - node 22 typescript
aliases:
  - node
  - typescript
  - strip-types
related:
  - javascript-array-sort-lexicographic
  - node-mock-timers-do-not-advance-alone
sources:
  - https://nodejs.org/docs/latest-v22.x/api/typescript.html#type-stripping
commands:
  - node library/examples/node-22-type-stripping-is-experimental/check.mjs
---

# Node.js 22.14.0 needs --experimental-strip-types to run this .ts file

This check ran on Node.js 22.14.0. `const count: number = 2` in `sample.ts` is a `SyntaxError` under plain `node`. The spawn without the flag exits non-zero, and the combined output includes `SyntaxError` or `Unexpected token`.

`node --experimental-strip-types sample.ts` prints `2`. Stderr contains `ExperimentalWarning`. A check that treats any stderr as failure will reject a run that printed the value.

The type-stripping page linked below was fetched as the Node.js v22.23.3 docs. Its history lines say `v22.18.0` "Type stripping is enabled by default" and "Type stripping no longer emits an experimental warning." This check was not run on 22.18.0. The same page says "no type checking is performed."

## Sample

```ts file=library/examples/node-22-type-stripping-is-experimental/sample.ts
const count: number = 2;
console.log(count);
```

## Incorrect

```js file=library/examples/node-22-type-stripping-is-experimental/incorrect.mjs
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
```

## Correct

```js file=library/examples/node-22-type-stripping-is-experimental/correct.mjs
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
```

## Verify

Run `node library/examples/node-22-type-stripping-is-experimental/check.mjs`.

## Sources

- https://nodejs.org/docs/latest-v22.x/api/typescript.html#type-stripping
