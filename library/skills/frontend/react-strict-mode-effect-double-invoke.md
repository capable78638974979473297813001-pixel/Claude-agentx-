---
id: react-strict-mode-effect-double-invoke
area: frontend
topic: react
task: survive-strict-mode-setup
title: React StrictMode runs effect setup twice in development
description: Use when a useEffect subscription, fetch, or analytics call happens twice in development and once in production.
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

In development, React's StrictMode mounts, unmounts, and mounts again so that missing effect cleanup shows up before production. The official StrictMode reference documents this extra setup/cleanup cycle. It does not mean the effect runs twice in production.

This check renders a probe under `StrictMode` with React 19.1.1. An effect that only does `calls.count += 1` finishes at 2. The same effect that returns a cleanup doing `calls.count -= 1` finishes at 1, because the development remount runs setup, cleanup, setup. If you open a socket, start a timer, or fire a request without aborting it in cleanup, development will leak the first one and the second one stays.

Fix the cleanup. Do not delete `<StrictMode>` to hide the double call.

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
