---
id: react-index-key-sticks-dom-state
area: frontend
topic: react
task: key-list-rows-by-identity
title: An index key keeps DOM state on the position, not the row
description: Use when a typed value or focus stays on the wrong row after a list is sorted, filtered, or reversed.
triggers:
  - index as key
  - input value sticks after reorder
  - key={index}
  - list reorder loses the wrong row
aliases:
  - react
  - reconciliation
  - key
related:
  - cursor-page-needs-unique-tie-break
  - react-19-ref-as-prop
sources:
  - https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key
commands:
  - node library/examples/react-index-key-sticks-dom-state/check.mjs
---

# An index key keeps DOM state on the position, not the row

React matches list children by `key`. The rendering-lists page says the key must identify the item among siblings, not its current index. An index key is stable for a given position, so React reuses the DOM node at that position when the data moves.

Measured with React 19.1.1 and uncontrolled inputs: items `['a','b']`, the first input's value set to `EDITED`, then the list rendered as `['b','a']`. With `key={index}` the values are `EDITED,b`. With `key={item}` they are `b,EDITED`. The edited DOM state followed the index, not the letter `a`. The check expects `b,EDITED`.

## Incorrect

```js file=library/examples/react-index-key-sticks-dom-state/incorrect.mjs
import React from "react";

export function List({ items }) {
  return React.createElement(
    "div",
    null,
    items.map((item, index) =>
      React.createElement("input", { key: index, defaultValue: item }),
    ),
  );
}
```

## Correct

```js file=library/examples/react-index-key-sticks-dom-state/correct.mjs
import React from "react";

export function List({ items }) {
  return React.createElement(
    "div",
    null,
    items.map((item) =>
      React.createElement("input", { key: item, defaultValue: item }),
    ),
  );
}
```

## Verify

Run `node library/examples/react-index-key-sticks-dom-state/check.mjs`.

## Sources

- https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key
