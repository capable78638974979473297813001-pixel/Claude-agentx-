---
id: css-unlayered-author-style-beats-layers
area: frontend
topic: css
task: order-cascade-layers
title: An unlayered author rule beats any style inside @layer
description: Use when a more specific rule inside @layer loses to a short selector written outside every layer.
triggers:
  - unlayered style beats layer
  - @layer specificity ignored
  - body #title stays red
  - cascade layer order
aliases:
  - css
  - cascade
  - layer
related:
  - css-flex-item-min-width-auto
  - css-container-query-ignores-viewport
sources:
  - https://www.w3.org/TR/css-cascade-5/#cascade-sort
commands:
  - node library/examples/css-unlayered-author-style-beats-layers/check.mjs
---

# An unlayered author rule beats any style inside @layer

Cascade Layers sort before specificity. CSS Cascading and Inheritance Level 5 puts unlayered author styles after every layered author style, so a one-id selector written outside `@layer` beats a longer selector inside a layer.

The losing stylesheet puts `body #title { color: rgb(0, 0, 255) }` in `@layer components` and then `#title { color: rgb(255, 0, 0) }` with no layer. In headless Chrome the computed color is `rgb(255, 0, 0)`. Specificity 0,1,1 never gets a chance to beat 0,1,0 because the unlayered declaration is in a later cascade bucket.

The working stylesheet declares `@layer reset, components` and puts both rules inside those layers. The component layer is later, so `body #title` wins and the computed color is `rgb(0, 0, 255)`.

## Incorrect

```html file=library/examples/css-unlayered-author-style-beats-layers/incorrect.html
<style>
  @layer components {
    body #title { color: rgb(0, 0, 255); }
  }
  #title { color: rgb(255, 0, 0); }
</style>
<p id="title">Title</p>
```

## Correct

```html file=library/examples/css-unlayered-author-style-beats-layers/correct.html
<style>
  @layer reset, components;
  @layer reset {
    #title { color: rgb(255, 0, 0); }
  }
  @layer components {
    body #title { color: rgb(0, 0, 255); }
  }
</style>
<p id="title">Title</p>
```

## Verify

Run `node library/examples/css-unlayered-author-style-beats-layers/check.mjs`.

## Sources

- https://www.w3.org/TR/css-cascade-5/#cascade-sort
