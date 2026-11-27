# Week 8 — Solve and Analyze (Binary Search Trees)

Three LeetCode binary search tree problems. Each folder has its own
`solution.py` (runnable, with test cases in `__main__`) and its own
`README.md` with the problem in my own words, a step-by-step trace, the
challenges and failed attempts, time and space complexity, and possible
improvements.

| # | Problem | Approach | Time | Space |
|---|---------|----------|------|-------|
| 1 | [Search in a Binary Search Tree](./01-search-in-a-binary-search-tree/) | walk one path, go left/right by comparison | O(h) | O(1) |
| 2 | [Range Sum of BST](./02-range-sum-of-bst/) | DFS that skips out-of-range subtrees | O(n) worst, ≈ O(h + k) | O(h) |
| 3 | [Convert Sorted Array to BST](./03-convert-sorted-array-to-bst/) | middle element as root, recurse on halves | O(n) | O(log n) |

`n` = number of nodes, `h` = height of the tree, `k` = number of values
inside the range.

## Running

```bash
for f in */solution.py; do python3 "$f"; done
```

Each file prints `OK`/`FAIL` per test and `ALL PASSED` at the end. Every
file also contains a `Solution` class with the exact LeetCode method name,
so it can be pasted into LeetCode directly.
