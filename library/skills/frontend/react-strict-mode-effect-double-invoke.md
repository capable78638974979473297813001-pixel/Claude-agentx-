---
id: react-strict-mode-effect-double-invoke
area: frontend
topic: react
task: survive-strict-mode-setup
title: React StrictMode runs effect setup twice in development
description: Use when a useEffect under StrictMode finishes at count 2 without cleanup and at 1 when cleanup decrements.
triggers:
  - useEffect runs twice
  - StrictMode double invoking
  - React development effect cleanup
  - subscription count is 2
aliases:
  - react
  - strictmode
  - useeffect
related:
  - react-19-ref-as-prop
  - node-unhandled-rejection-is-not-thrown
sources:
  - https://react.dev/reference/react/StrictMode
commands:
  - node library/examples/react-strict-mode-effect-double-invoke/check.mjs
---

# React StrictMode runs effect setup twice in development

The StrictMode reference says functions run "twice in development." This check renders a probe under `StrictMode` with React 19.1.1. An effect that only does `calls.count += 1` finishes at 2. The same effect that returns a cleanup doing `calls.count -= 1` finishes at 1. The development remount runs setup, then cleanup, then setup, so the decrement cancels the first increment and one increment remains.

## Incorrect

```js file=library/examples/react-strict-mode-effect-double-invoke/incorrect.mjs
import React from "react";

export function Probe({ calls }) {
  React.useEffect(() => {
    calls.count += 1;
  }, [calls]);
  return null;
}
```

## Correct

```js file=library/examples/react-strict-mode-effect-double-invoke/correct.mjs
import React from "react";

export function Probe({ calls }) {
  React.useEffect(() => {
    calls.count += 1;
    return () => {
      calls.count -= 1;
    };
  }, [calls]);
  return null;
}
```

## Verify

Run `node library/examples/react-strict-mode-effect-double-invoke/check.mjs`.

## Sources

- https://react.dev/reference/react/StrictMode
