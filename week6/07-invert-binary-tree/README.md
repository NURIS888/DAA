# Invert Binary Tree

LeetCode: https://leetcode.com/problems/invert-binary-tree/

## 1. Problem

Turn a binary tree into its mirror image: everything that was on the left
should end up on the right and vice versa, at every level. Return the
root of the changed tree.

## 2. Approach

Recursive: mirroring a tree = swap the root's two children, and mirror
each of those children too.

1. If the node is `None`, return `None`.
2. Mirror the right subtree and the left subtree.
3. Put the mirrored right subtree on the left and the mirrored left on the
   right, in **one** tuple assignment:
   `root.left, root.right = invert(root.right), invert(root.left)`.
   Python evaluates the whole right-hand side first, so both original
   children are read before either is overwritten.
4. Return the node.

### Trace — `[4, 2, 7, 1, 3, 6, 9]`

```
Before:            After:
     4                  4
   /   \              /   \
  2     7            7     2
 / \   / \          / \   / \
1   3 6   9        9   6 3   1
```

Order in which calls finish (bottom-up):

| Call | What happens | Subtree after |
|------|--------------|---------------|
| invert(9), (6), (3), (1) | leaves: both children `None`, swap does nothing | same |
| invert(7) | left ← mirrored 9, right ← mirrored 6 | 7(9, 6) |
| invert(2) | left ← mirrored 3, right ← mirrored 1 | 2(3, 1) |
| invert(4) | left ← subtree 7(9,6), right ← subtree 2(3,1) | 4(7(9,6), 2(3,1)) |

Level order of the result: **[4, 7, 2, 9, 6, 3, 1]** ✓

### Challenges

My first attempt (`invert_tree_wrong`) used two separate lines:

```python
root.left = invert(root.right)
root.right = invert(root.left)   # bug
```

On `[2, 1, 3]` it returned `[2, 3, 3]` instead of `[2, 3, 1]`. After the
first line, `root.left` already points to node 3, so the second line
mirrors node 3 *again* and puts it on the right too. Node 1 is lost.
Fixes: either save the old left child in a temporary variable first, or
use tuple assignment (what I did).

Other tests: empty tree (returns `None` → `[]`), single node, and `[1, 2]`
(a lone left child must move to the right → `[1, null, 2]`). To compare
trees I wrote `tree_to_list`, which converts a tree back into LeetCode's
level-order list.

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes.

Each node is visited exactly once and at each node I do one swap, which is
O(1). There are also about `n + 1` calls on `None` children, each O(1).

**Space Complexity: O(h)** for the recursion stack, where `h` is the tree
height: O(log n) balanced, O(n) skewed. The tree is changed in place, so no
new nodes are created.

## 4. Reflection / Improvement

- **More efficient approach?** No — every node's children must be swapped,
  so every node must be visited: O(n) is optimal.
- **What to change:** an iterative version with a queue (BFS) or stack:
  pop a node, swap its children, push the children. It avoids Python's
  recursion limit on very deep trees.
- **Improved complexity:** O(n) time either way; BFS uses O(w) space
  (widest level) instead of O(h).
