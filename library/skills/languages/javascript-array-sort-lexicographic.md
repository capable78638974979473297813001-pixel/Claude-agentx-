---
id: javascript-array-sort-lexicographic
area: languages
topic: javascript
task: sort-numbers-numerically
title: Array.prototype.sort compares numbers as strings
description: Use when [10, 2, 1].sort() comes back as 1,10,2 and a numeric compare was omitted.
triggers:
  - array sort lexicographic
  - sort 1,10,2
  - numeric compare function
  - default sort is UTF-16
aliases:
  - javascript
  - array
  - sort
related:
  - node-22-type-stripping-is-experimental
  - testing-library-byrole-name-is-exact
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
commands:
  - node library/examples/javascript-array-sort-lexicographic/check.mjs
---

# Array.prototype.sort compares numbers as strings

`Array.prototype.sort` with no compare function converts each element to a string and orders those strings by UTF-16 code units. MDN documents that default. `[10, 2, 1].sort()` joins to `1,10,2` because `"10"` starts with `"1"` and is less than `"2"`.

A compare function `(a, b) => a - b` sorts numerically and joins to `1,2,10`. The function must return a negative number, zero, or a positive number. Returning a boolean coerces to 0 or 1 and does not order the pair in both directions.

`sort` mutates the array. Copy with `slice` before sorting when the caller still needs the original order.

## Incorrect

```js file=library/examples/javascript-array-sort-lexicographic/incorrect.mjs
export function sortNumbers(values) {
  return [...values].sort();
}
```

## Correct

```js file=library/examples/javascript-array-sort-lexicographic/correct.mjs
export function sortNumbers(values) {
  return [...values].sort((left, right) => left - right);
}
```

## Verify

Run `node library/examples/javascript-array-sort-lexicographic/check.mjs`.

## Sources

- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
