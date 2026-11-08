# Sum of Left Leaves

LeetCode: https://leetcode.com/problems/sum-of-left-leaves/

## 1. Problem

Add up the values of all **left leaves**: nodes that have no children
*and* are the left child of their parent. A tree that is just a root has
no left leaves (the root has no parent).

## 2. Approach

The hard part is that a node knows whether it is a leaf but has no idea
whether it is a left child. So I pass that information down as a flag:

1. `walk(root, is_left=False)` — the root is not a left child.
2. At a `None` node, return 0.
3. At a leaf, return its value if `is_left` is `True`, else 0.
4. Otherwise return `walk(left, True) + walk(right, False)`.

### Trace — `[3, 9, 20, null, null, 15, 7]`

```
    3
   / \
  9   20
     /  \
    15   7
```

| Call | is_left | Leaf? | Returns |
|------|---------|-------|---------|
| walk(9) | True | yes | **9** |
| walk(15) | True | yes | **15** |
| walk(7) | False | yes | 0 (right leaf) |
| walk(20) | False | no | 15 + 0 = 15 |
| walk(3) | False | no | 9 + 15 = **24** |

Answer: **24**.

### Trace — `[1, 2, 3, 4, 5]`

```
      1
     / \
    2   3
   / \
  4   5
```

walk(4, True) = 4, walk(5, False) = 0, so walk(2) = 4 (node 2 is a left
child but not a leaf, so it adds nothing itself). walk(3, False) = 0
(right leaf). Total: **4**.

### Challenges

- My first attempt (`sum_of_left_leaves_wrong`) added `root.left.val` for
  every node that had a left child. On `[1, 2, 3, 4, 5]` it returned **6**
  (2 + 4) instead of 4, because node 2 is a left child but not a leaf. I
  had only tested the first example, where every left child happened to be
  a leaf, so the bug was hidden until I tried a bigger tree.
- Another variant I thought about: checking from the parent,
  "is `node.left` a leaf?". That also works, but the flag version felt
  simpler because every call handles only itself.
- Edge cases tested: single node `[1]` (answer 0 — the root must not
  count), a left leaf deep inside the *right* subtree `[1, null, 2, 3]`
  (answer 3), and the empty tree.

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes.

Every node is visited exactly once and each visit is O(1): a leaf check
and one addition.

**Space Complexity: O(h)** for the recursion stack: O(log n) for a
balanced tree, O(n) for a skewed one. The flag is one boolean per call.

## 4. Reflection / Improvement

- **More efficient approach?** Not in time: any node could be a left leaf,
  so all of them must be checked. O(n) is optimal.
- **What to change:** an iterative BFS/DFS with a queue or stack of
  `(node, is_left)` pairs avoids the recursion limit for very deep trees.
  Morris traversal could reduce extra space further.
- **Improved complexity:** O(n) time; O(1) extra space with Morris
  traversal, or O(h)/O(w) with an explicit stack/queue.
