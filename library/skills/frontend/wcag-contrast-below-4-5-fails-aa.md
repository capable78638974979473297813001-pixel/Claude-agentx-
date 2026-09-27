---
id: wcag-contrast-below-4-5-fails-aa
area: frontend
topic: accessibility
task: compute-srgb-contrast
title: WCAG 2.2 contrast needs sRGB linearization, and 4.5 is a hard floor
description: Use when a gray-on-white check says the contrast passes, or when dividing channel by 255 disagrees with the WCAG ratio.
triggers:
  - contrast ratio 4.5
  - relative luminance linearize
  - rgb(119,119,119) fails AA
  - sRGB contrast
aliases:
  - wcag
  - contrast
  - a11y
related:
  - testing-library-input-number-is-spinbutton
  - testing-library-byrole-name-is-exact
sources:
  - https://www.w3.org/TR/WCAG22/#contrast-minimum
commands:
  - python3 library/examples/wcag-contrast-below-4-5-fails-aa/check.py
---

# WCAG 2.2 contrast needs sRGB linearization, and 4.5 is a hard floor

WCAG 2.2 success criterion 1.4.3 requires a contrast ratio of at least 4.5:1 for normal text. The ratio uses relative luminance after the sRGB transfer: a channel at or below 0.04045 is divided by 12.92, otherwise it is `((channel + 0.055) / 1.055) ** 2.4`, then weighted 0.2126 / 0.7152 / 0.0722.

Dividing the channel by 255 and skipping that curve reports about 1.90 for `rgb(128, 128, 128)` on white. The spec curve reports 3.9494396480491156. Black on white is 21 either way, so a black/white fixture will not catch the missing linearization.

Around the AA floor, `rgb(118, 118, 118)` on white is about 4.542 and passes `>= 4.5`. `rgb(119, 119, 119)` is about 4.478 and fails. A check that rounds to one decimal before comparing, or that uses `>` instead of `>=`, will mis-label colors that sit on that boundary.

## Incorrect

```python file=library/examples/wcag-contrast-below-4-5-fails-aa/incorrect.py
def contrast_ratio(foreground, background):
    def channel(value):
        return value / 255

    def luminance(color):
        red, green, blue = color
        return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)

    lighter = max(luminance(foreground), luminance(background))
    darker = min(luminance(foreground), luminance(background))
    return (lighter + 0.05) / (darker + 0.05)
```

## Correct

```python file=library/examples/wcag-contrast-below-4-5-fails-aa/correct.py
def _linearize(channel):
    value = channel / 255
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(color):
    red, green, blue = color
    return 0.2126 * _linearize(red) + 0.7152 * _linearize(green) + 0.0722 * _linearize(blue)


def contrast_ratio(foreground, background):
    lighter = max(relative_luminance(foreground), relative_luminance(background))
    darker = min(relative_luminance(foreground), relative_luminance(background))
    return (lighter + 0.05) / (darker + 0.05)


def passes_normal_text_aa(foreground, background):
    return contrast_ratio(foreground, background) >= 4.5
```

## Verify

Run `python3 library/examples/wcag-contrast-below-4-5-fails-aa/check.py`.

## Sources

- https://www.w3.org/TR/WCAG22/#contrast-minimum
