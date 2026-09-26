---
id: testing-library-byrole-name-is-exact
area: frontend
topic: testing-library
task: match-accessible-name-exactly
title: getByRole name strings are exact and case-sensitive
description: Use when getByRole cannot find a button whose visible text contains the word you searched for, such as Save inside Save draft.
triggers:
  - Found multiple elements with the role button and name
  - getByRole name exact
  - Save draft
  - accessible name case sensitive
aliases:
  - testing-library
  - getbyrole
  - accname
related:
  - testing-library-input-number-is-spinbutton
  - wcag-contrast-below-4-5-fails-aa
sources:
  - https://testing-library.com/docs/queries/byrole
commands:
  - node library/examples/testing-library-byrole-name-is-exact/check.mjs
---

# getByRole name strings are exact and case-sensitive

`getByRole` compares a string `name` with `matches`, not a substring. In `@testing-library/dom` 10.4.0, `{ name: "Save" }` does not match a button whose accessible name is `Save draft`, and `{ name: "save" }` does not match `Save`. The query throws `Unable to find an accessible element with the role "button" and name "Save"`.

The name that matches is the full accessible name, `Save draft`, including the text inside nested elements. A regex such as `/Save/` matches every button whose name contains that pattern and then throws `Found multiple elements with the role "button" and name /Save/` when two buttons qualify. The passing query uses the full name `Save draft`.

## Incorrect

```js file=library/examples/testing-library-byrole-name-is-exact/incorrect.mjs
import { getByRole } from "@testing-library/dom";

export function saveButton(container) {
  return getByRole(container, "button", { name: "Save" });
}
```

## Correct

```js file=library/examples/testing-library-byrole-name-is-exact/correct.mjs
import { getByRole } from "@testing-library/dom";

export function saveButton(container) {
  return getByRole(container, "button", { name: "Save draft" });
}
```

## Verify

Run `node library/examples/testing-library-byrole-name-is-exact/check.mjs`.

## Sources

- https://testing-library.com/docs/queries/byrole
