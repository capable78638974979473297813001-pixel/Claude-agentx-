---
id: css-flex-item-min-width-auto
area: frontend
topic: css
task: let-flex-item-shrink
title: A flex item's min-width:auto refuses to shrink below its content
description: Use when a flex row scrolls or spills even though the item has flex: 1 1 auto and the container has a fixed width.
triggers:
  - flex item overflow nowrap
  - min-width auto flex
  - scrollWidth greater than clientWidth
  - flex shrink ignored
aliases:
  - css
  - flexbox
  - min-width
related:
  - css-unlayered-author-style-beats-layers
  - css-container-query-ignores-viewport
sources:
  - https://www.w3.org/TR/css-flexbox-1/#min-size-auto
commands:
  - node library/examples/css-flex-item-min-width-auto/check.mjs
---

# A flex item's min-width:auto refuses to shrink below its content

The flexbox spec's automatic minimum size sets `min-width: auto` on a flex item to its content size. `flex: 1 1 auto` is allowed to shrink, but not below that minimum. `white-space: nowrap` makes the minimum the full unwrapped string.

Here the row is `width: 100px`, the label is `flex: 0 0 auto` at 40px, and the value is `UNBREAKABLE_TOKEN_VALUE` with `white-space: nowrap`. The row's `scrollWidth` is greater than its `clientWidth` of 100. The flex item will not compress the token.

`min-width: 0` (and `overflow: hidden` so the text can be clipped) replaces the automatic minimum. After that the row's `scrollWidth` is no longer greater than 100. `overflow: hidden` alone, without `min-width: 0`, does not change the automatic minimum. `min-width: 0` on the flex container instead of the item also misses the item that is refusing to shrink.

## Incorrect

```html file=library/examples/css-flex-item-min-width-auto/incorrect.html
<style>
  #row { display: flex; width: 100px; }
  #label { width: 40px; flex: 0 0 auto; }
  #value { flex: 1 1 auto; white-space: nowrap; }
</style>
<div id="row"><span id="label">Id</span><span id="value">UNBREAKABLE_TOKEN_VALUE</span></div>
```

## Correct

```html file=library/examples/css-flex-item-min-width-auto/correct.html
<style>
  #row { display: flex; width: 100px; }
  #label { width: 40px; flex: 0 0 auto; }
  #value { flex: 1 1 auto; min-width: 0; white-space: nowrap; overflow: hidden; }
</style>
<div id="row"><span id="label">Id</span><span id="value">UNBREAKABLE_TOKEN_VALUE</span></div>
```

## Verify

Run `node library/examples/css-flex-item-min-width-auto/check.mjs`.

## Sources

- https://www.w3.org/TR/css-flexbox-1/#min-size-auto
