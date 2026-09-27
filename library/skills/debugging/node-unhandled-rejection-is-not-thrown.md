---
id: node-unhandled-rejection-is-not-thrown
area: debugging
topic: node
task: await-or-catch-rejection
title: try/catch does not see a rejected Promise you did not await
description: Use when a try block calls Promise.reject, the catch never runs, and unhandledRejection later reports nope.
triggers:
  - unhandledRejection
  - try catch missed promise
  - fell-through
  - await rejected promise
aliases:
  - node
  - promise
  - rejection
related:
  - node-mock-timers-do-not-advance-alone
  - react-strict-mode-effect-double-invoke
sources:
  - https://nodejs.org/api/process.html#event-unhandledrejection
commands:
  - node library/examples/node-unhandled-rejection-is-not-thrown/check.mjs
---

# try/catch does not see a rejected Promise you did not await

`try { Promise.reject(new Error("nope")) }` does not throw on Node 22. The rejection is scheduled. The function returns `fell-through`, and `process.on("unhandledRejection")` later receives the error whose message is `nope`. Node's `unhandledRejection` event is the documented hook for that path.

`await` inside the `try` turns the rejection into a throw, and `catch` returns `nope`. The check waits 30ms after the bare `Promise.reject` so the `unhandledRejection` listener can record `nope`.

## Incorrect

```js file=library/examples/node-unhandled-rejection-is-not-thrown/incorrect.mjs
export function fire() {
  try {
    Promise.reject(new Error("nope"));
    return "fell-through";
  } catch {
    return "caught";
  }
}
```

## Correct

```js file=library/examples/node-unhandled-rejection-is-not-thrown/correct.mjs
export async function fire() {
  try {
    await Promise.reject(new Error("nope"));
    return "fell-through";
  } catch (error) {
    return error.message;
  }
}
```

## Verify

Run `node library/examples/node-unhandled-rejection-is-not-thrown/check.mjs`.

## Sources

- https://nodejs.org/api/process.html#event-unhandledrejection
