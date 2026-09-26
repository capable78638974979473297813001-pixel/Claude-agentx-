---
id: node-22-type-stripping-is-experimental
area: languages
topic: node
task: run-typescript-with-strip-types
title: Node 22 runs .ts only with --experimental-strip-types
description: Use when node sample.ts throws SyntaxError on a type annotation, or when strip-types prints the value and an ExperimentalWarning.
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

# Node 22 runs .ts only with --experimental-strip-types

Node.js 22.14 type stripping is documented as experimental. `const count: number = 2` in `sample.ts` is a syntax error to plain `node`. The spawn without the flag exits with `SyntaxError`.

`node --experimental-strip-types sample.ts` prints `2`. Stderr contains `ExperimentalWarning`. A check that treats any stderr as failure will reject a run that actually printed the value.

Strip-types erases annotations. It does not type-check, and it refuses TypeScript features that are not erasable (enums, parameter properties, namespaces that emit code). Those still need a compiler. The flag name and the warning are the 22.x behavior in the docs linked above; later Node lines may flip the default, so read the page for the version you run.

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
