# Week 6 — Solve and Analyze (Binary Trees)

Ten LeetCode binary-tree problems. Each folder has its own `solution.py`
(runnable, with test cases in `__main__`) and its own `README.md` with the
problem in my own words, a step-by-step trace, the challenges / failed
attempts, time and space complexity, and possible improvements.

| # | Problem | Approach | Time | Space |
|---|---------|----------|------|-------|
| 1 | [Binary Tree Inorder Traversal](./01-binary-tree-inorder-traversal/) | iterative stack (+ recursive) | O(n) | O(h) |
| 2 | [Maximum Depth of Binary Tree](./02-maximum-depth-of-binary-tree/) | recursive DFS (+ BFS) | O(n) | O(h) |
| 3 | [Minimum Depth of Binary Tree](./03-minimum-depth-of-binary-tree/) | BFS, stop at first leaf | O(n) | O(w) |
| 4 | [Path Sum](./04-path-sum/) | DFS with remaining sum | O(n) | O(h) |
| 5 | [Binary Tree Preorder Traversal](./05-binary-tree-preorder-traversal/) | stack, push right then left | O(n) | O(h) |
| 6 | [Binary Tree Postorder Traversal](./06-binary-tree-postorder-traversal/) | reversed Node-Right-Left | O(n) | O(h) |
| 7 | [Invert Binary Tree](./07-invert-binary-tree/) | recursive swap | O(n) | O(h) |
| 8 | [Binary Tree Paths](./08-binary-tree-paths/) | DFS carrying path string | O(n·h) | O(h²) |
| 9 | [Sum of Left Leaves](./09-sum-of-left-leaves/) | DFS with `is_left` flag | O(n) | O(h) |
| 10 | [Merge Two Binary Trees](./10-merge-two-binary-trees/) | simultaneous recursion, reuse subtrees | O(min(n₁, n₂)) | O(min(h₁, h₂)) |

`n` = number of nodes, `h` = height of the tree, `w` = widest level.

## Running

```bash
for f in */solution.py; do python3 "$f"; done
```

Each file prints `OK`/`FAIL` per test and `ALL PASSED` at the end. Every
file also contains a `Solution` class with the exact LeetCode method name,
so it can be pasted into LeetCode directly.
