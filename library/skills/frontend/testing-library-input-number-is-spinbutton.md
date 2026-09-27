---
id: testing-library-input-number-is-spinbutton
area: frontend
topic: testing-library
task: query-number-input-by-role
title: An input type=number has role spinbutton, not textbox
description: Use when getByRole(container, 'textbox') throws for a labeled number input that is clearly in the document.
triggers:
  - Unable to find an accessible element with the role textbox
  - input type number role
  - spinbutton
  - getByRole textbox number
aliases:
  - testing-library
  - aria
  - input
related:
  - testing-library-byrole-name-is-exact
  - wcag-contrast-below-4-5-fails-aa
sources:
  - https://www.w3.org/TR/html-aam-1.0/#el-input-number
  - https://testing-library.com/docs/queries/byrole
commands:
  - node library/examples/testing-library-input-number-is-spinbutton/check.mjs
---

# An input type=number has role spinbutton, not textbox

The HTML Accessibility API Mapping says `input type=number` exposes role `spinbutton`, not `textbox`. `@testing-library/dom` 10.4.0 follows that mapping. `getByRole(container, "textbox")` on `<label>Amount <input type="number" /></label>` throws `Unable to find an accessible element with the role "textbox"`.

`getByRole(container, "spinbutton", { name: "Amount" })` returns that input. The accessible name comes from the label text. Querying `textbox` will also miss `input type=range` and will match `type=text`, `type=search`, and `textarea` instead.

When the query throws, read the role in the Testing Library error dump before adding a test id.

## Incorrect

```js file=library/examples/testing-library-input-number-is-spinbutton/incorrect.mjs
import { getByRole } from "@testing-library/dom";

export function amount(container) {
  return getByRole(container, "textbox");
}
```

## Correct

```js file=library/examples/testing-library-input-number-is-spinbutton/correct.mjs
import { getByRole } from "@testing-library/dom";

export function amount(container) {
  return getByRole(container, "spinbutton", { name: "Amount" });
}
```

## Verify

Run `node library/examples/testing-library-input-number-is-spinbutton/check.mjs`.

## Sources

- https://www.w3.org/TR/html-aam-1.0/#el-input-number
- https://testing-library.com/docs/queries/byrole
