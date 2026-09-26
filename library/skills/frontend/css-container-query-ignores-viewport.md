---
id: css-container-query-ignores-viewport
area: frontend
topic: css
task: query-the-container-not-the-viewport
title: A @media rule follows the viewport, not the 200px card
description: Use when a sidebar card picks up a desktop @media rule while the card itself is only a couple hundred pixels wide.
triggers:
  - container query vs media query
  - card is red on a wide viewport
  - @container max-width
  - container-type inline-size
aliases:
  - css
  - container-queries
  - responsive
related:
  - css-flex-item-min-width-auto
  - mobile-safe-area-fallback-only-if-undefined
sources:
  - https://www.w3.org/TR/css-contain-3/#container-type
commands:
  - node library/examples/css-container-query-ignores-viewport/check.mjs
---

# A @media rule follows the viewport, not the 200px card

`@media (min-width: 300px)` reads the viewport. A card whose parent is `width: 200px` still matches that query when the window is 1200px, and the card paints `rgb(255, 0, 0)`.

CSS Containment Module Level 3 lets you name a containment context with `container-type: inline-size`. `@container (min-width: 300px)` then sees the 200px container and does not apply. `@container (max-width: 250px)` does apply, and the card paints `rgb(0, 128, 0)`.

The parent needs `container-type` (or `container`). A query on an element that is not a container falls through to the nearest ancestor container, which is often the viewport-sized root. Size containers also cannot depend on their own descendants for size, so do not put `container-type: inline-size` on the card you are also sizing with the query.

## Incorrect

```html file=library/examples/css-container-query-ignores-viewport/incorrect.html
<style>
  #wrap { width: 200px; }
  #card { color: rgb(0, 0, 0); }
  @media (min-width: 300px) {
    #card { color: rgb(255, 0, 0); }
  }
</style>
<div id="wrap"><p id="card">Card</p></div>
```

## Correct

```html file=library/examples/css-container-query-ignores-viewport/correct.html
<style>
  #wrap { container-type: inline-size; width: 200px; }
  #card { color: rgb(0, 0, 0); }
  @container (min-width: 300px) {
    #card { color: rgb(255, 0, 0); }
  }
  @container (max-width: 250px) {
    #card { color: rgb(0, 128, 0); }
  }
</style>
<div id="wrap"><p id="card">Card</p></div>
```

## Verify

Run `node library/examples/css-container-query-ignores-viewport/check.mjs`.

## Sources

- https://www.w3.org/TR/css-contain-3/#container-type
