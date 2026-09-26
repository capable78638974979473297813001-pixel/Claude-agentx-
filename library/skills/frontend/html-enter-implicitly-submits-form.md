---
id: html-enter-implicitly-submits-form
area: frontend
topic: html
task: stop-implicit-form-submit
title: Enter in a one-field form submits, and type=button does not stop it
description: Use when pressing Enter in a search box fires submit even though the form has no submit button, or a type=button failed to block it.
triggers:
  - implicit form submission
  - Enter submits single input
  - type=button does not block submit
  - keydown Enter preventDefault
aliases:
  - html
  - forms
  - enter
related:
  - idempotency-key-replays-stored-response
  - if-match-rejects-stale-update
sources:
  - https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission
commands:
  - node library/examples/html-enter-implicitly-submits-form/check.mjs
---

# Enter in a one-field form submits, and type=button does not stop it

The HTML spec's implicit submission fires when the user hits Enter in a text field and the form has one text-like control, even if there is no submit button. A real key press from Puppeteer on this one-field form increments the submit count to 1. A synthetic `KeyboardEvent` dispatched from script does not, because implicit submission is tied to the user activation path, not to an untrusted event.

`type="button"` on a second control does not block that path. The spec only treats certain controls (submit buttons, and more than one blocking field when there is no submit button) as changing implicit submission. Adding `<button type="button">` next to the text field still submits.

`keydown` on the field with `event.key === "Enter"` and `preventDefault()` drops the count to 0. That is the lever when a one-field search box must not navigate.

## Incorrect

```html file=library/examples/html-enter-implicitly-submits-form/incorrect.html
<form id="find">
  <input id="q" name="q" />
</form>
```

## Correct

```html file=library/examples/html-enter-implicitly-submits-form/correct.html
<form id="find">
  <input id="q" name="q" />
</form>
<script>
  document.getElementById("q").addEventListener("keydown", (event) => {
    if (event.key === "Enter") event.preventDefault();
  });
</script>
```

## Verify

Run `node library/examples/html-enter-implicitly-submits-form/check.mjs`.

## Sources

- https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#implicit-submission
