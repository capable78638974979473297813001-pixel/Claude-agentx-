---
id: node-http-client-hangs-without-end
area: backend
topic: node
task: end-the-http-request
title: A Node http request that never calls end() stays open
description: Use when a client writes a body, the server never responds, and the socket sits until a timeout.
triggers:
  - http.request timeout without end
  - request.write never finishes
  - server waits for request end
  - ECONNRESET after destroy
aliases:
  - node
  - http
  - request
related:
  - go-http-shutdown-blocks-on-handler
  - path-join-allows-traversal
sources:
  - https://nodejs.org/api/http.html#requestenddata-encoding-callback
commands:
  - node library/examples/node-http-client-hangs-without-end/check.mjs
---

# A Node http request that never calls end() stays open

`http.request` sends headers when you `write`, and it finishes the body only when you `end`. A server that waits for the request `end` event before `response.end("ok")` will never answer a client that writes and then waits.

The incomplete client hits its own `setTimeout` of `200` ms, calls `request.destroy()`, and resolves `timeout`. It writes `"{}"` and never calls `end`. The example installs `request.on("error", () => {})` before that timer. `request.end()` on the same server returns the body `ok`. The server writes that body from the request `end` listener.

## Incorrect

```js file=library/examples/node-http-client-hangs-without-end/incorrect.mjs
import http from "node:http";

export function post(port) {
  return new Promise((resolve) => {
    const request = http.request({ hostname: "127.0.0.1", port, method: "POST" }, (response) => {
      response.resume();
      response.on("end", () => resolve("response"));
    });
    request.on("error", () => {});
    request.setTimeout(200, () => {
      request.destroy();
      resolve("timeout");
    });
    request.write("{}");
  });
}
```

## Correct

```js file=library/examples/node-http-client-hangs-without-end/correct.mjs
import http from "node:http";

export function post(port) {
  return new Promise((resolve, reject) => {
    const request = http.request({ hostname: "127.0.0.1", port, method: "POST" }, (response) => {
      const chunks = [];
      response.on("data", (chunk) => chunks.push(chunk));
      response.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    });
    request.on("error", reject);
    request.write("{}");
    request.end();
  });
}
```

## Verify

Run `node library/examples/node-http-client-hangs-without-end/check.mjs`.

## Sources

- https://nodejs.org/api/http.html#requestenddata-encoding-callback
