# Manual review

Seed `random.Random(20260926)`, 30 of 43 verified skills. The review looked at the prose (the code fences are the programs the validator runs).

## Sample

- backend/go-http-shutdown-blocks-on-handler
- apis/if-match-rejects-stale-update
- apis/idempotency-key-replays-stored-response
- refactoring/python-generator-second-pass-empty
- docs/python-warnings-stacklevel
- languages/python-closure-late-binding
- debugging/python-exception-context-chaining
- testing/node-mock-timers-do-not-advance-alone
- databases/sqlite-foreign-keys-require-pragma
- frontend/testing-library-byrole-name-is-exact
- languages/node-22-type-stripping-is-experimental
- frontend/css-container-query-ignores-viewport
- languages/go-1-22-loop-var-per-iteration
- languages/rust-temporary-dropped-while-borrowed
- vcs/git-abbrev-ref-is-head-when-detached
- frontend/svelte-5-export-let-invalid-in-runes
- languages/python-unboundlocalerror-on-assignment
- devops/github-actions-unquoted-run-script
- languages/javascript-array-sort-lexicographic
- security/sql-fstring-interpolates-untrusted-input
- databases/sqlite-unindexed-lookup-plans-scan
- frontend/css-unlayered-author-style-beats-layers
- frontend/react-19-ref-as-prop
- cli/argparse-options-after-positionals
- frontend/html-enter-implicitly-submits-form
- security/hmac-compare-digest-for-secrets
- backend/node-http-client-hangs-without-end
- frontend/react-index-key-sticks-dom-state
- frontend/vue-3-5-destructured-props-stay-bound
- devops/git-describe-fails-on-shallow-clone

## Fixes from this pass

- Generator note claimed `len()` consumes a generator. It raises `TypeError`. The sentence now says that.
- `warnings.warn` mentioned `stacklevel=0`, which this check did not run. That sentence is gone.
- Go loop note claimed `go run main.go` outside a module. The check ran `go run .`. The note now says only that.
- React 19 note claimed class-component ref behavior that this check did not render. That sentence is gone.
- Form note claimed a two-field form does not submit. The measured case is one field. The extra sentence is gone.
- SQLite plan note described a non-covering `SEARCH` plan that this check did not print. The note now sticks to the `COVERING` plan that was printed.

No sampled skill was dropped. The other 13 of that 43 were not in this sample; they still have to pass `validate`.

## Skills added after the sample

The seed drew 30 of the 43 skills that existed for that review. These seven were written later, after the same checks: an incorrect example and a correct example were run on this machine, and the prose stays inside what those runs printed. They were not part of the random sample.

- frontend/react-stale-state-updater
- frontend/history-pushstate-skips-popstate
- frontend/css-import-must-precede-rules
- frontend/formdata-omits-disabled-fields
- frontend/aria-hidden-removed-from-role-query
- frontend/package-json-type-module-rejects-require
- frontend/offsetheight-in-loop-forces-layout

Sentences that were not in those runs were left out: a `.cjs` `require` path, `readonly` versus `disabled`, `hashchange`, `display: none`, and restarting the interval by listing `count` in the effect dependency array.
