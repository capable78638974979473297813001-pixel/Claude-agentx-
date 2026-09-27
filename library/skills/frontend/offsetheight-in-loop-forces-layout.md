---
id: offsetheight-in-loop-forces-layout
area: frontend
topic: performance
task: batch-dom-writes-before-layout-read
title: Reading offsetHeight inside an append loop forces a layout per item
description: Use when a loop appends DOM nodes and reads offsetHeight, and Chrome LayoutCount climbs once per item.
triggers:
  - offsetHeight inside appendChild loop
  - LayoutCount 81 versus 2
  - forced synchronous layout
  - DocumentFragment one layout read
aliases:
  - layout
  - offsetheight
  - chrome
related:
  - css-flex-item-min-width-auto
  - n-plus-one-query-per-row
sources:
  - https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing
  - https://pptr.dev/api/puppeteer.page.metrics
commands:
  - node library/examples/offsetheight-in-loop-forces-layout/check.mjs
---

# Reading offsetHeight inside an append loop forces a layout per item

web.dev's article on layout thrashing says to avoid forced synchronous layouts: read style values, then change the document. The article reads `offsetHeight` after a style change as the example of that read. Appending a node and then reading that node's `offsetHeight` in the same loop asks the browser to lay out on every iteration.

This check uses Google Chrome 148.0.7778.96. `page.metrics().LayoutCount` is Puppeteer's Page.metrics value, documented as the total number of full or partial page layout. Eighty `appendChild` calls that each add `el.offsetHeight` into a sum report LayoutCount `81` and a sum of `1440`. Building the same 80 nodes on a `DocumentFragment`, appending that fragment once, then reading `list.offsetHeight` once reports LayoutCount `2` and the same `1440`.

`RecalcStyleCount` was not stable across repeats on this Chrome, so the check does not assert it. Both documents create 80 children. The matching height sum is what this markup produced. LayoutCount is the difference the check requires.

`page.metrics()` accumulates for the page it is called on. The check opens a new browser for the incorrect document and another for the correct document. Loading both into one page would add the counts together.

## Incorrect

```html file=library/examples/offsetheight-in-loop-forces-layout/incorrect.html
<div id="list"></div>
<script>
  const list = document.getElementById("list");
  let reads = 0;
  for (let i = 0; i < 80; i++) {
    const el = document.createElement("div");
    el.textContent = "item-" + i;
    list.appendChild(el);
    reads += el.offsetHeight;
  }
  window.__reads = reads;
</script>
```

## Correct

```html file=library/examples/offsetheight-in-loop-forces-layout/correct.html
<div id="list"></div>
<script>
  const list = document.getElementById("list");
  const frag = document.createDocumentFragment();
  for (let i = 0; i < 80; i++) {
    const el = document.createElement("div");
    el.textContent = "item-" + i;
    frag.appendChild(el);
  }
  list.appendChild(frag);
  window.__reads = list.offsetHeight;
</script>
```

## Verify

Run `node library/examples/offsetheight-in-loop-forces-layout/check.mjs`.

## Sources

- https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing
- https://pptr.dev/api/puppeteer.page.metrics
