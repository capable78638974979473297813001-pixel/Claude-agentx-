---
id: svelte-5-export-let-invalid-in-runes
area: frontend
topic: svelte
task: replace-export-let-with-props
title: Svelte 5 rejects export let once a component uses a rune
description: Use when the Svelte compiler reports legacy_export_invalid or says Cannot use export let in runes mode.
triggers:
  - legacy_export_invalid
  - Cannot use export let in runes mode
  - $props instead of export let
  - svelte 5 runes mode
aliases:
  - svelte
  - runes
  - props
related:
  - vue-3-5-destructured-props-stay-bound
  - react-19-ref-as-prop
sources:
  - https://svelte.dev/docs/svelte/legacy-export-let
  - https://svelte.dev/e/legacy_export_invalid
commands:
  - node library/examples/svelte-5-export-let-invalid-in-runes/check.mjs
---

# Svelte 5 rejects export let once a component uses a rune

Svelte 5.39.6 compiles a component in runes mode as soon as it uses a rune such as `$state`. In that mode `export let` is a compile error, code `legacy_export_invalid`, and the message starts `Cannot use export let in runes mode — use $props() instead`. The legacy props page documents the same replacement.

`export let count = 0` next to `let extra = $state(1)` fails before any HTML is produced. `let { count = 0 } = $props()` compiles. Server-side render (`generate: 'server'`) of that component with `count: 7` yields a body containing `>7<`.

Do not pass `css: 'none'` to `compile`; Svelte 5 rejects that option with `options_invalid_value`. Write the compiled module under `node_modules` (this check uses `library/node_modules/.skill-svelte-app.js`) so the generated `import ... from 'svelte'` resolves. A file written to `/tmp` cannot see the package.

## Incorrect

```svelte file=library/examples/svelte-5-export-let-invalid-in-runes/incorrect.svelte
<script>
  export let count = 0;
  let extra = $state(1);
</script>
<p>{count}{extra}</p>
```

## Correct

```svelte file=library/examples/svelte-5-export-let-invalid-in-runes/correct.svelte
<script>
  let { count = 0 } = $props();
</script>
<p>{count}</p>
```

## Verify

Run `node library/examples/svelte-5-export-let-invalid-in-runes/check.mjs`.

## Sources

- https://svelte.dev/docs/svelte/legacy-export-let
- https://svelte.dev/e/legacy_export_invalid
