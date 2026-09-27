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
  - .js treated as ES module
aliases:
  - node
  - esm
  - package.json
related:
  - node-22-type-stripping-is-experimental
  - javascript-array-sort-lexicographic
sources:
  - https://nodejs.org/docs/latest-v22.x/api/packages.html#type
commands:
  - node library/examples/package-json-type-module-rejects-require/check.mjs
---

# package.json "type": "module" makes require a ReferenceError in .js files

The Node.js v22 packages page documents the `"type"` field on the nearest parent `package.json`. `"type": "module"` parses `.js` as ESM. `require` is not defined there. Node.js 22.14 exits with `ReferenceError: require is not defined in ES module scope`. The check looks for that ReferenceError string. It does not look for `ERR_REQUIRE_ESM`.

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

- https://nodejs.org/docs/latest-v22.x/api/packages.html#type
