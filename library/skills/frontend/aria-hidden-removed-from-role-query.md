---
id: aria-hidden-removed-from-role-query
area: frontend
topic: accessibility
task: query-hidden-from-accessibility-tree
title: getByRole skips a button inside aria-hidden
description: Use when getByRole cannot find a button that is in the DOM because an ancestor has aria-hidden=true.
triggers:
  - aria-hidden getByRole
  - Unable to find button inside aria-hidden
  - getByRole hidden true
  - accessibility tree skips aria-hidden
aliases:
  - aria
  - testing-library
  - a11y
related:
  - testing-library-byrole-name-is-exact
  - wcag-contrast-below-4-5-fails-aa
sources:
  - https://www.w3.org/TR/wai-aria-1.2/#aria-hidden
  - https://testing-library.com/docs/queries/byrole
commands:
  - node library/examples/aria-hidden-removed-from-role-query/check.mjs
---

# getByRole skips a button inside aria-hidden

`aria-hidden="true"` removes the subtree from the accessibility tree. `@testing-library/dom` 10.4.0 follows that. `getByRole(container, "button", { name: "Save" })` on `<div aria-hidden="true"><button>Save</button></div>` throws `Unable to find an accessible element with the role "button" and name "Save"`. The button is still in `querySelectorAll`.

`{ hidden: true }` includes elements the accessibility tree hides. With that option the same query returns the button whose text is `Save`. The byrole docs list `hidden` as the flag for that. The WAI-ARIA definition of `aria-hidden` is the reason the default query skips it.

`querySelectorAll("button")` on that container still returns one button whose text is `Save`. The default role query is what skips it. This check is the `aria-hidden` ancestor case.

## Incorrect

```js file=library/examples/aria-hidden-removed-from-role-query/incorrect.mjs
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../package.json"));
const { getByRole } = require("@testing-library/dom");

export function saveButton(container) {
  return getByRole(container, "button", { name: "Save" });
}
```

## Correct

```js file=library/examples/aria-hidden-removed-from-role-query/correct.mjs
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../package.json"));
const { getByRole } = require("@testing-library/dom");

export function saveButton(container) {
  return getByRole(container, "button", { name: "Save", hidden: true });
}
```

## Verify

Run `node library/examples/aria-hidden-removed-from-role-query/check.mjs`.

## Sources

- https://www.w3.org/TR/wai-aria-1.2/#aria-hidden
- https://testing-library.com/docs/queries/byrole
