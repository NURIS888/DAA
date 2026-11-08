# Binary Tree Postorder Traversal

LeetCode: https://leetcode.com/problems/binary-tree-postorder-traversal/

## 1. Problem

Return all values of a binary tree in **postorder**: the whole left
subtree, then the whole right subtree, and the node itself **last** — at
every node. The follow-up asks for a non-recursive solution.

## 2. Approach

Postorder is the hardest of the three to do with a stack directly, because
a node has to wait until *both* children are finished. I used a trick
(`postorder_iterative`):

- Postorder is **Left → Right → Node**.
- Read backwards, that is **Node → Right → Left**.
- Node → Right → Left is just preorder with the children swapped, which is
  easy with a stack (push **left** first so **right** is popped first).

So: run that "mirrored preorder", collect the values, then reverse the
list.

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

| Step | Pop | Record | Push (left, then right) | Stack (bottom→top) |
|------|-----|--------|-------------------------|--------------------|
| 0 | — | — | 1 | [1] |
| 1 | 1 | 1 | 2, 3 | [2, 3] |
| 2 | 3 | 3 | 8 | [2, 8] |
| 3 | 8 | 8 | 9 | [2, 9] |
| 4 | 9 | 9 | — | [2] |
| 5 | 2 | 2 | 4, 5 | [4, 5] |
| 6 | 5 | 5 | 6, 7 | [4, 6, 7] |
| 7 | 7 | 7 | — | [4, 6] |
| 8 | 6 | 6 | — | [4] |
| 9 | 4 | 4 | — | [] |

Collected (Node-Right-Left): `[1, 3, 8, 9, 2, 5, 7, 6, 4]`
Reversed: **[4, 6, 7, 5, 2, 9, 8, 3, 1]** ✓ (matches the recursive version).

### Challenges

- My first idea was to reuse the preorder code and just record the value
  at a different moment. With one stack that doesn't work: when I pop a
  node I don't know if its children have already been processed, so I
  either record it too early or lose it.
- Next I tried pushing the node back on the stack together with a
  "visited" flag (`(node, False)` → push `(node, True)`, right, left). That
  works, but it was more code and harder to trace.
- Then I noticed the reverse-of-mirrored-preorder pattern by writing
  postorder of a small tree `[1, 2, 3]` → `[2, 3, 1]`, and reversing it →
  `[1, 3, 2]`, which looked like a preorder with right before left.
- Testing: compared with the recursive version on all inputs, plus empty
  and single-node trees.

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes.

Each node is pushed once and popped once with O(1) work each. The final
`reverse()` walks the result list once, which is another O(n). O(n) +
O(n) = O(n).

**Space Complexity: O(h)** extra for the stack, plus the O(n) output list.
In this mirrored-preorder pattern the stack holds about one waiting
sibling per level, so O(log n) for a balanced tree and O(n) for a skewed
one. One downside: because I reverse at the end, the full result list must
exist before any value is in the right order — the values can't be
streamed out one by one.

## 4. Reflection / Improvement

- **More efficient approach?** Time is optimal at O(n), since every value
  must be output.
- **What to change:**
  - A "true" one-stack postorder keeps a `last_visited` pointer: a node is
    recorded only when its right child is `None` or was the node just
    recorded. This avoids the reverse step and gives values in the correct
    order as they are produced.
  - Morris postorder traversal (threading, like Morris inorder) brings
    extra space down to O(1), but it is much more complicated because it
    has to output right-edge chains in reverse.
- **Improved complexity:** O(n) time, O(h) extra space with
  `last_visited`, or **O(1)** extra space with Morris.
