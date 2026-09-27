---
id: react-stale-state-updater
area: frontend
topic: react
task: update-state-from-interval
title: An interval that closes over count sticks at 1
description: Use when a setInterval or setTimeout inside useEffect keeps writing the same count because the effect deps are empty.
triggers:
  - setInterval stale state
  - setCount count + 1 stays 1
  - functional setState updater
  - useEffect empty deps interval
aliases:
  - react
  - usestate
  - setinterval
related:
  - react-strict-mode-effect-double-invoke
  - react-index-key-sticks-dom-state
sources:
  - https://react.dev/reference/react/useState#updating-state-based-on-the-previous-state
commands:
  - node library/examples/react-stale-state-updater/check.mjs
---

# An interval that closes over count sticks at 1

`useState`'s setter can take the next value or a function of the previous value. The React useState reference says to use the function form when the next value depends on the previous one. An effect with `[]` closes over the `count` from the first render, which is 0.

This check uses React 19.1.1 and `mock.timers`. `setInterval(() => setCount(count + 1), 1000)` with empty deps, then `tick(3000)`, leaves the text at `1`. The first tick writes 1. Later ticks still see `count` as 0 and write 1 again.

`setCount((value) => value + 1)` reads the value React has stored. The same three ticks end at `3`. The effect still has `[]`, so it does not resubscribe. The updater is what changes. The check enables `setInterval` mocks before `render`, then calls `tick(3000)` inside `act`. Unmount can print an `act(...)` warning on stderr. The check still exits 0 when stdout has both phrases.

## Incorrect

```js file=library/examples/react-stale-state-updater/incorrect.mjs
import React from "react";

export function Counter() {
  const [count, setCount] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setCount(count + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return React.createElement("span", { id: "n" }, String(count));
}
```

## Correct

```js file=library/examples/react-stale-state-updater/correct.mjs
import React from "react";

export function Counter() {
  const [count, setCount] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setCount((value) => value + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return React.createElement("span", { id: "n" }, String(count));
}
```

## Verify

Run `node library/examples/react-stale-state-updater/check.mjs`.

## Sources

- https://react.dev/reference/react/useState#updating-state-based-on-the-previous-state
