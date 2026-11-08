# Binary Tree Paths

LeetCode: https://leetcode.com/problems/binary-tree-paths/

## 1. Problem

List every path that goes from the root down to a leaf, written as a
string like `"1->2->5"`. The order of the paths doesn't matter.

## 2. Approach

Depth-first search that carries the path text built so far
(`binary_tree_paths`, used for LeetCode):

1. At a node, build `path = path_so_far + "->" + value` (or just the value
   for the root, when `path_so_far` is empty).
2. If the node is a leaf, the path is complete → add it to the answer.
3. Otherwise continue into the left and right children with `path`.

Strings are immutable in Python, so each call gets its own copy of the
path and I never have to "undo" anything when going back up.

### Trace — `[1, 2, 3, null, 5]`

```
    1
   / \
  2   3
   \
    5
```

| Call | path_so_far | path | Leaf? | paths |
|------|-------------|------|-------|-------|
| walk(1) | "" | "1" | no | [] |
| walk(2) | "1" | "1->2" | no | [] |
| walk(None) (left of 2) | — | — | return | [] |
| walk(5) | "1->2" | "1->2->5" | **yes** | ["1->2->5"] |
| walk(3) | "1" | "1->3" | **yes** | ["1->2->5", "1->3"] |

Result: **["1->2->5", "1->3"]**.

### Challenges

- My first version added the path when the node was `None` instead of
  checking for a leaf. On `[1, 2]` it produced `["1->2", "1->2", "1"]`:
  each leaf was added twice (once for each `None` child), and the root was
  added as a path because its right child is `None` even though it is not
  a leaf. Checking "both children are `None`" before recursing fixed it.
- Formatting the arrow: at first every path started with `"->"`
  (`"->1->2"`). I fixed it by not adding an arrow when the path so far is
  empty. Negative values (`-1->-3`) work because I use `str(val)`.
- I also wrote a backtracking version (see section 4) and checked that
  both give the same answers on all tests.

## 3. Time Complexity

**Time Complexity: O(n · h)**, where `n` is the number of nodes and `h`
the tree height. Worst case O(n²).

Every node is visited once, but at each node I build a new string
`path_so_far + "->" + value`, and building a string costs time
proportional to its length, which is up to the node's depth (at most `h`).
So the total is the sum of all node depths, which is at most `n · h`.
For a balanced tree that is O(n log n); for a skewed tree (`h = n`) it is
O(n²) in the worst case. The output itself also has size up to
(number of leaves) × h, so some of this cost can't be avoided.

**Space Complexity: O(h²)** for the recursion stack in the worst case —
`h` active calls, each holding a string of length up to `h` — plus the
output. Counting just the call depth it is O(h).

## 4. Reflection / Improvement

- **More efficient approach?** Yes, for the work done on inner nodes.
- **What to change:** use **backtracking** with one shared list
  (`binary_tree_paths_backtracking` in `solution.py`): append the value
  when going down, `pop()` it when coming back up, and only call
  `"->".join(...)` at a leaf. Inner nodes then cost O(1) instead of
  O(depth), and only leaves pay for building a string.
- **Improved complexity:** O(n + L · h) time, where `L` is the number of
  leaves — that is just the time to visit the tree plus the size of the
  output, which is the best possible. Extra space drops to O(h) (one
  shared list + call stack).
