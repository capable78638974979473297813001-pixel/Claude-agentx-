---
id: history-pushstate-skips-popstate
area: frontend
topic: routing
task: listen-for-real-navigations
title: history.pushState does not fire popstate
description: Use when a client router updates the URL with pushState and a popstate listener never runs until the user hits Back.
triggers:
  - pushState popstate not fired
  - history.back popstate
  - client router misses pushState
  - popstate count stays 0
aliases:
  - history
  - popstate
  - routing
related:
  - html-enter-implicitly-submits-form
  - css-container-query-ignores-viewport
sources:
  - https://html.spec.whatwg.org/multipage/nav-history-apis.html#event-popstate
commands:
  - node library/examples/history-pushstate-skips-popstate/check.mjs
---

# history.pushState does not fire popstate

The HTML spec's `popstate` event fires when the user traverses the session history, including `history.back()`. `history.pushState` adds an entry and changes the URL, and it does not fire `popstate`. A listener that waits for `popstate` to render the next view stays at 0 after `pushState({ step: 1 }, "", "#a")`.

In headless Chrome that page's `__pops` is 0 after a 100ms wait. The page that pushes `#a`, then `#b`, then calls `history.back()` reaches 1. Update the view in the function that calls `pushState`. Keep the `popstate` listener for Back and Forward. This check counts `popstate` only.

## Incorrect

```html file=library/examples/history-pushstate-skips-popstate/incorrect.html
<p id="n">0</p>
<script>
  window.__pops = 0;
  addEventListener("popstate", () => {
    window.__pops += 1;
  });
  history.pushState({ step: 1 }, "", "#a");
  document.getElementById("n").textContent = String(window.__pops);
</script>
```

## Correct

```html file=library/examples/history-pushstate-skips-popstate/correct.html
<p id="n">0</p>
<script>
  window.__pops = 0;
  addEventListener("popstate", () => {
    window.__pops += 1;
    document.getElementById("n").textContent = String(window.__pops);
  });
  history.pushState({ step: 1 }, "", "#a");
  history.pushState({ step: 2 }, "", "#b");
  history.back();
</script>
```

## Verify

Run `node library/examples/history-pushstate-skips-popstate/check.mjs`.

## Sources

- https://html.spec.whatwg.org/multipage/nav-history-apis.html#event-popstate
