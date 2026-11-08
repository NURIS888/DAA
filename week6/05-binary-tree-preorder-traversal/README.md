# Binary Tree Preorder Traversal

LeetCode: https://leetcode.com/problems/binary-tree-preorder-traversal/

## 1. Problem

Return all values of a binary tree in **preorder**: the node first, then
its whole left subtree, then its whole right subtree — at every node.
The follow-up asks for a non-recursive solution.

## 2. Approach

Iterative, with a stack (`preorder_iterative`, used for LeetCode):

1. Start with the root on the stack.
2. Pop a node and record its value (the "node first" part).
3. Push its **right** child, then its **left** child. Because a stack is
   last-in-first-out, the left child comes out next, so the whole left
   subtree is finished before the right child is popped.
4. Repeat until the stack is empty.

A recursive version (`preorder_recursive`) is included to cross-check.

### Trace — `[1, 2, 3, 4, 5, null, 8, null, null, 6, 7, 9]`

```
        1
       / \
      2   3
     / \   \
    4   5   8
       / \  /
      6  7 9
```

| Step | Pop | Record | Push (right, then left) | Stack (bottom→top) |
|------|-----|--------|-------------------------|--------------------|
| 0 | — | — | 1 | [1] |
| 1 | 1 | 1 | 3, 2 | [3, 2] |
| 2 | 2 | 2 | 5, 4 | [3, 5, 4] |
| 3 | 4 | 4 | — | [3, 5] |
| 4 | 5 | 5 | 7, 6 | [3, 7, 6] |
| 5 | 6 | 6 | — | [3, 7] |
| 6 | 7 | 7 | — | [3] |
| 7 | 3 | 3 | 8 | [8] |
| 8 | 8 | 8 | 9 | [9] |
| 9 | 9 | 9 | — | [] |

Result: **[1, 2, 4, 5, 6, 7, 3, 8, 9]**. Notice how node 3 waits at the
bottom of the stack the whole time the left subtree is processed.

### Challenges

- My first iterative version pushed **left first, then right** (the
  "natural" reading order). On `[1, 2, 3]` it gave `[1, 3, 2]` — the right
  subtree came out first because it was pushed last. Swapping the push
  order fixed it. This was the main lesson: with a stack, push in the
  *reverse* of the order you want to visit.
- I also tried using a queue (`deque.popleft`) instead of a stack. That
  gives level order (`1, 2, 3, 4, 5, 8, ...`), not preorder — preorder
  needs to go *deep* first, which is what a stack does.
- Testing: I compared the iterative and recursive outputs on every test
  case, including the empty tree (must return `[]`, so I check for `None`
  before pushing the root).

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes.

Each node is pushed once and popped once, and each pop does O(1) work
(append the value, at most two pushes). So the total work is a constant
times `n`.

**Space Complexity: O(h)** extra in a typical tree (plus the O(n) output
list). The stack holds the nodes along the current path plus the right
siblings waiting on that path, which is at most about one node per level
(height `h`) plus one. Skewed tree → O(n), balanced → O(log n).

## 4. Reflection / Improvement

- **More efficient approach?** Time is already optimal — every node must
  be output, so O(n) is the minimum.
- **What to change:** Morris preorder traversal uses temporary "thread"
  pointers from the right-most node of each left subtree back to the
  current node, so it can climb back up without a stack, and removes the
  threads afterwards.
- **Improved complexity:** O(n) time, **O(1)** extra space.
