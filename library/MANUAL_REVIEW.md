# Manual review

Stratified sample of 30 of the 50 verified skills. Seed `random.Random(20260926)`.

Draw: sort area names, sort skill ids inside each area, shuffle each area list, take one id from every area, shuffle what remains, and draw until the sample has 30. All 16 areas are in the sample.

The review read the prose against the bar. A sentence had to match a command that was run, a number or error that command printed, or a quoted line from the cited source. Filler and unrun advice were removed. No sampled skill was deleted. Each one still has an incorrect result and a fix that the example command prints.

## Sample

- apis/idempotency-key-replays-stored-response
- apis/cursor-page-needs-unique-tie-break
- architecture/transactional-outbox-commit-with-row
- backend/node-http-client-hangs-without-end
- cli/argparse-options-after-positionals
- databases/sqlite-null-comparisons-are-unknown
- databases/sqlite-foreign-keys-require-pragma
- debugging/python-exception-context-chaining
- debugging/node-unhandled-rejection-is-not-thrown
- devops/github-actions-unquoted-run-script
- docs/python-warnings-stacklevel
- frontend/formdata-omits-disabled-fields
- frontend/react-19-ref-as-prop
- frontend/vue-3-5-destructured-props-stay-bound
- frontend/offsetheight-in-loop-forces-layout
- frontend/html-enter-implicitly-submits-form
- frontend/aria-hidden-removed-from-role-query
- frontend/react-index-key-sticks-dom-state
- frontend/css-import-must-precede-rules
- frontend/svelte-5-export-let-invalid-in-runes
- languages/javascript-array-sort-lexicographic
- languages/go-nil-pointer-stored-in-interface
- languages/java-21-switch-null-throws
- mobile/mobile-safe-area-fallback-only-if-undefined
- performance/n-plus-one-query-per-row
- refactoring/python-generator-second-pass-empty
- security/hmac-compare-digest-for-secrets
- security/sql-fstring-interpolates-untrusted-input
- testing/node-mock-timers-do-not-advance-alone
- vcs/git-abbrev-ref-is-head-when-detached

## Fixes from this pass

- Idempotency: removed the unmeasured tenant-key map and the crash-before-response paragraph. The check is `calls == 2` versus one stored body.
- Outbox: removed the unmeasured worker and double-send sentences. The check counts `orders=1` / `outbox=0` versus both `0`.
- Generator: removed unmeasured `len()`, generator-expression, and database sentences. The check is `['a', 'b']` then `[]`.
- `Array.prototype.sort`: removed the unmeasured boolean compare and the `slice` mutation sentence. The check joins `[10, 2, 1]` as `1,10,2` and `1,2,10`.
- SQL f-string: removed the unmeasured identifier allow-list paragraph. The payload is `' OR '1'='1`.
- NULL comparison: removed the unmeasured `NOT IN` paragraph. The rows are ids `2` versus `2` and `3`.
- N+1: removed the unmeasured `SQLITE_MAX_VARIABLE_NUMBER` figures. The trace lengths are `3` and `1`.
- GitHub Actions: the correct script in the check is `echo "$MSG"`. The unquoted `$MSG` sentence is gone.
- Exception chaining: removed `raise ... from None` and traceback-banner lines the check does not read. The check reads `__context__` and `__cause__`.
- Unhandled rejection: removed the unmeasured `.catch` sentence. The listener records `nope` after `30` ms.
- `warnings.warn`: removed the unmeasured decorator sentence. The filenames are `incorrect.py` and `check.py`.
- argparse: removed the unmeasured `REMAINDER` paragraph. The check now also requires stderr `unrecognized arguments: --flag` and exit code `2`.
- Keyset cursor: removed the unmeasured `OFFSET` sentence. Page size `1` returns `[1, 3]` versus `[1, 2]`.
- Foreign keys: removed the unmeasured connection-pool sentence. The check reads `PRAGMA foreign_keys`.
- Java 21 switch: removed the unmeasured `--release 17` sentence. The check uses `javac --release 21` and stdout `npe` versus `missing`.
- Go nil interface: removed the unmeasured `*MyError` sentence. The programs print `typed-nil` and `nil` for a nil `*int`.
- Safe area: removed the unmeasured `max()` recipe. Computed padding is `0px` versus `12px`.
- Svelte: removed the unmeasured `css: 'none'` sentence.
- Vue 3.5: removed the unmeasured computed sentence. The snapshot stays `1` after `props.count = 4`.
- React 19 ref: removed the unmeasured instruction to skip `forwardRef` on every component. The callback stays `null` or receives `INPUT`.
- CSS `@import`: removed the unmeasured data-URL and `setContent` sentences. The file URL colors are `rgb(255, 0, 0)` and `rgb(0, 128, 0)`.
- List keys: removed the unmeasured "only safe when never reordered" rule. The values are `EDITED,b` versus `b,EDITED`.
- Node HTTP: removed the unmeasured `ECONNRESET` crash and the early `response.end` sentence. The client resolves `timeout` at `200` ms, and `end()` returns `ok`.
- Form Enter: `<button type="button">Go</button>` still submits (`1`), and a synthetic `KeyboardEvent` stays at `0`. Those two assertions are now in the example check, next to `preventDefault()` yielding `0`.
- Mock timers: the check records `ExperimentalWarning` on the process `warning` event. The unmeasured `setInterval` sentence is gone. `setImmediate` leaves the `5000` ms flag `false` until `tick(5000)`.

`validate` now rejects banned filler phrases, near-duplicate bodies, example code under 60 characters, and a body whose long prose sentences are mostly unanchored advice.

## Earlier pass

The same seed, drawn as 30 of the 43 skills that existed then, fixed six inaccurate sentences: generator `len()` is a `TypeError` rather than a consuming call (that `len()` sentence was later removed because this check does not call it), `stacklevel=0`, `go run main.go` outside a module, class-component refs, a two-field form, and a non-covering SQLite `SEARCH` plan.

The other 20 skills were not in this draw. They still have to pass `validate`.
