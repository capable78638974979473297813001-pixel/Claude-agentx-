---
id: mobile-safe-area-fallback-only-if-undefined
area: mobile
topic: css
task: use-env-safe-area-fallback
title: env(safe-area-inset-top, 12px) is 0px when the variable exists
description: Use when a fallback padding inside env() is ignored and the header sits under the status bar, or the fallback appears on desktop unexpectedly.
triggers:
  - safe-area-inset-top fallback ignored
  - env() padding-top 0px
  - safe area inset fallback
  - env no-such-inset 12px
aliases:
  - css
  - safe-area
  - env
related:
  - css-container-query-ignores-viewport
  - css-flex-item-min-width-auto
sources:
  - https://www.w3.org/TR/css-env-1/#safe-area-insets
commands:
  - node library/examples/mobile-safe-area-fallback-only-if-undefined/check.mjs
---

# env(safe-area-inset-top, 12px) is 0px when the variable exists

`env(safe-area-inset-top, 12px)` uses 12px only when the variable is missing. CSS Environment Variables defines the UA insets `safe-area-inset-*`. In this headless Chrome they exist and are 0, so computed `padding-top` is `0px`. The fallback never runs.

`env(no-such-inset, 12px)` is a name the UA does not define, so the same engine computes `padding-top: 12px`. The check reads those two computed values. The fallback runs only for the undefined name.

## Incorrect

```html file=library/examples/mobile-safe-area-fallback-only-if-undefined/incorrect.html
<style>
  #pad { padding-top: env(safe-area-inset-top, 12px); }
</style>
<div id="pad"></div>
```

## Correct

```html file=library/examples/mobile-safe-area-fallback-only-if-undefined/correct.html
<style>
  #pad { padding-top: env(no-such-inset, 12px); }
</style>
<div id="pad"></div>
```

## Verify

Run `node library/examples/mobile-safe-area-fallback-only-if-undefined/check.mjs`.

## Sources

- https://www.w3.org/TR/css-env-1/#safe-area-insets
