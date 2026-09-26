---
id: css-import-must-precede-rules
area: frontend
topic: css
task: place-import-before-style-rules
title: @import after a style rule is ignored
description: Use when a stylesheet @import of a color rule does nothing because a selector was written above it.
triggers:
  - @import ignored after style rule
  - green.css never applies
  - import must precede style rules
  - css import order
aliases:
  - css
  - import
  - cascade
related:
  - css-unlayered-author-style-beats-layers
  - css-flex-item-min-width-auto
sources:
  - https://www.w3.org/TR/css-cascade-5/#at-import
commands:
  - node library/examples/css-import-must-precede-rules/check.mjs
---

# @import after a style rule is ignored

CSS Cascading and Inheritance Level 5 invalidates an `@import` that follows a style rule in the same stylesheet. The browser drops that import. It does not move it above the selector.

`#title { color: rgb(255, 0, 0); }` followed by `@import url("green.css")` stays `rgb(255, 0, 0)`. `green.css` contains `#title { color: rgb(0, 128, 0); }`. With the import first and no later rule, the computed color is `rgb(0, 128, 0)`. The check loads each file with `page.goto` on a `file:` URL so the relative `green.css` resolves.

## Incorrect

```html file=library/examples/css-import-must-precede-rules/incorrect.html
<style>
  #title { color: rgb(255, 0, 0); }
  @import url("green.css");
</style>
<p id="title">Title</p>
```

## Correct

```html file=library/examples/css-import-must-precede-rules/correct.html
<style>
  @import url("green.css");
</style>
<p id="title">Title</p>
```

## Verify

Run `node library/examples/css-import-must-precede-rules/check.mjs`.

## Sources

- https://www.w3.org/TR/css-cascade-5/#at-import
