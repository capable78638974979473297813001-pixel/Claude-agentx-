---
id: package-json-type-module-rejects-require
area: frontend
topic: build
task: load-cjs-when-type-is-module
title: package.json "type": "module" makes require a ReferenceError in .js files
description: Use when a frontend build or Node script throws require is not defined in ES module scope after adding type module.
triggers:
  - require is not defined in ES module scope
  - type module package.json
  - ERR_REQUIRE_ESM
  - .js treated as ES module
aliases:
  - node
  - esm
  - package.json
related:
  - node-22-type-stripping-is-experimental
  - javascript-array-sort-lexicographic
sources:
  - https://nodejs.org/api/packages.html#type
commands:
  - node library/examples/package-json-type-module-rejects-require/check.mjs
---

# package.json "type": "module" makes require a ReferenceError in .js files

Node's package `type` field, documented on the packages page, decides how `.js` files in that package are parsed. `"type": "module"` parses `.js` as ESM. `require` is not defined there. Node 22.14 exits with `ReferenceError: require is not defined in ES module scope` and the hint that the file is ESM because of the extension and `package.json`.

The same directory's `correct.mjs` uses `import path from "node:path"` and prints `b` for `path.basename("/a/b")`. The check spawns `node incorrect.js` in that directory and requires a non-zero status whose stderr contains that ReferenceError. The `package.json` that sets `"type": "module"` is the file beside `incorrect.js`.

## Package

```json file=library/examples/package-json-type-module-rejects-require/package.json
{
  "type": "module"
}
```

## Incorrect

```js file=library/examples/package-json-type-module-rejects-require/incorrect.js
console.log(require("node:path").basename("/a/b"));
```

## Correct

```js file=library/examples/package-json-type-module-rejects-require/correct.mjs
import path from "node:path";

console.log(path.basename("/a/b"));
```

## Verify

Run `node library/examples/package-json-type-module-rejects-require/check.mjs`.

## Sources

- https://nodejs.org/api/packages.html#type
