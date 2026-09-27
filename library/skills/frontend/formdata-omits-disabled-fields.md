---
id: formdata-omits-disabled-fields
area: frontend
topic: forms
task: submit-successful-controls-only
title: FormData skips a disabled field that querySelectorAll still sees
description: Use when a disabled input is missing from the POST body, or a hand-built payload still sends it.
triggers:
  - FormData omits disabled
  - disabled input not submitted
  - successful controls
  - querySelectorAll includes disabled
aliases:
  - html
  - formdata
  - forms
related:
  - html-enter-implicitly-submits-form
  - idempotency-key-replays-stored-response
sources:
  - https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#constructing-the-form-data-set
commands:
  - node library/examples/formdata-omits-disabled-fields/check.mjs
---

# FormData skips a disabled field that querySelectorAll still sees

The form data set is built from successful controls. A disabled field is not successful, so it is absent from `new FormData(form)`. Walking `querySelectorAll("#f input")` and appending every name still includes the disabled field.

The form has `name=a` enabled and `name=b` disabled. The selector walk produces the key list `a,b`. `FormData` produces `a`. The check loads each file with `page.goto` on a `file:` URL and reads `window.__keys`. There is no submit button in the markup, and `FormData` is constructed with the form only.

## Incorrect

```html file=library/examples/formdata-omits-disabled-fields/incorrect.html
<form id="f">
  <input name="a" value="1" />
  <input name="b" value="2" disabled />
</form>
<script>
  const data = new URLSearchParams();
  for (const input of document.querySelectorAll("#f input")) {
    data.append(input.name, input.value);
  }
  window.__keys = [...data.keys()].join(",");
</script>
```

## Correct

```html file=library/examples/formdata-omits-disabled-fields/correct.html
<form id="f">
  <input name="a" value="1" />
  <input name="b" value="2" disabled />
</form>
<script>
  window.__keys = [...new FormData(document.getElementById("f")).keys()].join(",");
</script>
```

## Verify

Run `node library/examples/formdata-omits-disabled-fields/check.mjs`.

## Sources

- https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#constructing-the-form-data-set
