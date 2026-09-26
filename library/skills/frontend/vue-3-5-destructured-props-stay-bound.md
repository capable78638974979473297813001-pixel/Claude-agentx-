---
id: vue-3-5-destructured-props-stay-bound
area: frontend
topic: vue
task: keep-destructured-props-reactive
title: Vue 3.5 keeps a defineProps destructure bound; a plain const does not
description: Use when a child copies props.count into a const and keeps rendering the old number after the parent updates the prop.
triggers:
  - destructured props lose reactivity
  - defineProps count stays 1
  - vue 3.5 reactive props destructure
  - $props.count
aliases:
  - vue
  - props
  - reactivity
related:
  - svelte-5-export-let-invalid-in-runes
  - react-19-ref-as-prop
sources:
  - https://blog.vuejs.org/posts/vue-3-5
commands:
  - node library/examples/vue-3-5-destructured-props-stay-bound/check.mjs
---

# Vue 3.5 keeps a defineProps destructure bound; a plain const does not

Vue 3.5's compiler treats `const { count = 0 } = defineProps(...)` as a props binding, not a one-time JavaScript destructure. The compiler bindings map for that component is `{count: "props"}`, and the template render code reads `$props.count`. The Vue 3.5 release post describes this reactive props destructure.

A hand-written `const count = props.count` on a reactive object does the ordinary snapshot. After `props.count = 4` the reader still returns 1. That is the bug people reintroduce when they "simplify" the compiler output or when they destructure a `props` object passed into a plain function.

The default `= 0` in the destructure is the missing-prop default. It does not freeze the value. Read `count` in the template, or call a computed that reads the prop, instead of storing the number in a local `const`.

## Incorrect

```js file=library/examples/vue-3-5-destructured-props-stay-bound/incorrect.mjs
import { reactive } from "vue";

export function snapshot(props) {
  const count = props.count;
  return () => count;
}
```

## Correct

```vue file=library/examples/vue-3-5-destructured-props-stay-bound/App.vue
<script setup>
const { count = 0 } = defineProps({ count: Number });
</script>
<template><span class="n">{{ count }}</span></template>
```

## Verify

Run `node library/examples/vue-3-5-destructured-props-stay-bound/check.mjs`.

## Sources

- https://blog.vuejs.org/posts/vue-3-5
