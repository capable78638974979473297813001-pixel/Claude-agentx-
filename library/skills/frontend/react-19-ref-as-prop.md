---
id: react-19-ref-as-prop
area: frontend
topic: react
task: forward-ref-to-host
title: React 19 function components take ref as a prop
description: Use when a parent ref stays null on a function component that used to need forwardRef, or when element.ref warns after a React 19 upgrade.
triggers:
  - forwardRef is no longer necessary
  - ref as a prop
  - Accessing element.ref is no longer supported
  - React 19 ref callback null
aliases:
  - react
  - react 19
  - forwardref
  - jsx
related:
  - react-strict-mode-effect-double-invoke
  - react-index-key-sticks-dom-state
sources:
  - https://react.dev/blog/2024/12/05/react-19
  - https://react.dev/blog/2024/04/25/react-19-upgrade-guide
commands:
  - node library/examples/react-19-ref-as-prop/check.mjs
---

# React 19 function components take ref as a prop

The React 19 release post from December 5, 2024 says new function components will no longer need `forwardRef`. The upgrade guide says to read `element.props.ref` instead of `element.ref`, and it quotes the warning `Accessing element.ref is no longer supported. ref is now a regular prop.` This check does not render that warning. It measures the ref callback.

The failure this check measures: a function that destructures only `label` and renders an input without passing `ref` never invokes the parent's ref callback, so the callback stays `null`. Putting `ref` on `React.createElement("input", { ref })` makes that callback receive an `INPUT` node. The check is that `tagName`.

## Incorrect

```js file=library/examples/react-19-ref-as-prop/incorrect.mjs
import React from "react";

export function Field({ label }) {
  return React.createElement("input", { "aria-label": label });
}
```

## Correct

```js file=library/examples/react-19-ref-as-prop/correct.mjs
import React from "react";

export function Field({ label, ref }) {
  return React.createElement("input", { "aria-label": label, ref });
}
```

## Verify

Run `node library/examples/react-19-ref-as-prop/check.mjs`.

## Sources

- https://react.dev/blog/2024/12/05/react-19
- https://react.dev/blog/2024/04/25/react-19-upgrade-guide
