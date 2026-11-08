# Path Sum

LeetCode: https://leetcode.com/problems/path-sum/

## 1. Problem

Given a binary tree and a number `targetSum`, I must answer whether there
is a path that starts at the root, ends at a **leaf**, and whose node
values add up exactly to `targetSum`. Values can be negative.

## 2. Approach

Recursive depth-first search where I carry "how much is still missing".

1. If the node is `None`, return `False` (no path through nothing).
2. Subtract the node's value: `remaining = target - node.val`.
3. If the node is a leaf, the path is complete: return `remaining == 0`.
4. Otherwise try the left subtree, then the right subtree with `remaining`
   as the new target. Return `True` if either one works. Python's `or`
   short-circuits, so if the left side already found a path the right side
   is never searched.

### Trace — `[5, 4, 8, 11, null, 13, 4, 7, 2, null, null, null, 1]`, target 22

```
        5
       / \
      4   8
     /   / \
    11  13  4
   / \       \
  7   2       1
```

| Node | remaining after subtracting | Leaf? | Result |
|------|-----------------------------|-------|--------|
| 5 | 22 − 5 = 17 | no | go left |
| 4 | 17 − 4 = 13 | no | go left |
| 11 | 13 − 11 = 2 | no | go left |
| 7 | 2 − 7 = −5 | yes | False → try right |
| 2 | 2 − 2 = **0** | yes | **True** |

`True` bubbles back up through 11, 4 and 5. The right subtree (8, 13, 4, 1)
is never visited. Path: 5 → 4 → 11 → 2.

### Trace — `[1, 2, 3]`, target 5

1 → remaining 4. Left leaf 2 → 4 − 2 = 2 ≠ 0. Right leaf 3 → 4 − 3 = 1 ≠ 0.
Both fail → **False**.

### Challenges

My first attempt (`has_path_sum_wrong`) checked the sum when reaching
`None` instead of when reaching a leaf:

```python
if root is None:
    return target_sum == 0
```

It gave wrong answers in two cases:

- `[1, 2]`, target 1 → returned **True**. Node 1 has a left child (2) but
  its *right* child is `None`. Going right, remaining is 0 at `None`, so it
  said "found". But 1 is not a leaf, so `1` alone is not a root-to-leaf
  path. Correct answer: False.
- Empty tree, target 0 → returned **True**, but an empty tree has no paths
  at all. Correct answer: False.

Moving the check to "is this node a leaf?" fixed both. I also added a test
with negative values (`[-2, null, -3]`, target −5) to make sure I don't
stop early when the running sum goes "past" the target — with negatives
you can't prune like that.

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes.

In the worst case (no valid path, or it is the last one checked) every node
is visited once, doing O(1) work: one subtraction and one leaf check. The
short-circuit can make it faster, but not in the worst case.

**Space Complexity: O(h)**, where `h` is the height of the tree, for the
recursion stack. O(log n) for a balanced tree, O(n) for a skewed one. I
never store the path itself, only one integer per call.

## 4. Reflection / Improvement

- **More efficient approach?** No better time is possible in general: a
  path could end at any leaf, and because values can be negative there is
  no safe way to skip a subtree early. So O(n) is optimal.
- **What could change:** an iterative version with a stack of
  `(node, remaining)` pairs would avoid Python's recursion limit on very
  deep trees.
- **Improved complexity:** same O(n) time and O(h) space; only the
  recursion-limit risk goes away.
