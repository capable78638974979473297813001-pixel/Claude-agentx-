---
id: node-mock-timers-do-not-advance-alone
area: testing
topic: node
task: tick-mocked-timers
title: node:test mock.timers does not fire a timer until tick()
description: Use when a test enables mock timers, a 5000ms timeout never runs, and the assertion sees the flag still false.
triggers:
  - mock.timers.tick
  - setTimeout does not fire
  - node:test mock timers
  - ExperimentalWarning timers
aliases:
  - node
  - test
  - timers
related:
  - node-unhandled-rejection-is-not-thrown
  - node-22-type-stripping-is-experimental
sources:
  - https://nodejs.org/docs/latest-v22.x/api/test.html#mocktimerstickmilliseconds
commands:
  - node library/examples/node-mock-timers-do-not-advance-alone/check.mjs
---

# node:test mock.timers does not fire a timer until tick()

`mock.timers.enable({ apis: ['setTimeout'] })` replaces `setTimeout`. The clock does not move with wall time. A callback scheduled for 5000ms stays pending until `mock.timers.tick(5000)`. The Node.js test runner docs for `tick` say it advances the mocked clock by that many milliseconds.

Enabling the mock and then awaiting a real `setTimeout(resolve, 10)` will not flush the mocked 5000ms timer. The incorrect helper returns before the flag flips. `tick(5000)` runs the callback and the flag becomes true.

Node 22 prints `ExperimentalWarning` for this API. Assert on the flag, not on an empty stderr. `tick` only advances timers you enabled; a `setInterval` left out of `apis` still uses the real clock.

## Incorrect

```js file=library/examples/node-mock-timers-do-not-advance-alone/incorrect.mjs
export function schedule(flag) {
  setTimeout(() => {
    flag.fired = true;
  }, 5000);
}
```

## Correct

```js file=library/examples/node-mock-timers-do-not-advance-alone/correct.mjs
import { mock } from "node:test";

export function advance() {
  mock.timers.tick(5000);
}
```

## Verify

Run `node library/examples/node-mock-timers-do-not-advance-alone/check.mjs`.

## Sources

- https://nodejs.org/docs/latest-v22.x/api/test.html#mocktimerstickmilliseconds
