---
name: performance-profiling
description: Measure before optimizing - benchmarks, profilers, complexity analysis, caching of pure functions, and batch processing. Use when something is slow, when running large scenario grids or batch tax computations, or before adding caches.
---

# Performance

1. Define the target (e.g. 10k returns/minute) and measure current state with a benchmark.
2. Profile (`python -m cProfile -s cumtime`, `py-spy`, browser devtools). Optimize the top frame, not a guess.
3. Algorithmic wins first (O(n²) → O(n log n)), then data structures, then micro-optimizations.
4. Pure functions can be memoized on (facts hash, ruleset hash); tax engines built pure get this free.
5. Batch: load rulesets once; parallelize per return across processes.
6. Re-measure and record numbers in the handoff.
