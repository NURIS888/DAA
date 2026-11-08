# Binary Tree Inorder Traversal

LeetCode: https://leetcode.com/problems/binary-tree-inorder-traversal/

## 1. Problem

I get the root of a binary tree and must return the values of all nodes in
**inorder**: first everything in the left subtree, then the node itself,
then everything in the right subtree. This rule applies at every node, not
just the root. The follow-up asks to do it without recursion.

## 2. Approach

I wrote two versions in `solution.py`.

**Recursive (`inorder_recursive`)** — a direct translation of the rule:
`visit(left)`, record `node.val`, `visit(right)`. An empty node returns
immediately.

**Iterative (`inorder_iterative`, used for LeetCode)** — I replace the
call stack with my own list:

1. From the current node, go left as far as possible, pushing every node.
2. When I hit `None`, pop the top node. Everything to its left is already
   done, so I record it.
3. Jump to that node's right child and repeat step 1.
4. Stop when there is no current node and the stack is empty.

### Trace — `[1, null, 2, 3]`

```
1
 \
  2
 /
3
```

| Step | Action | Stack (bottom→top) | current | Result |
|------|--------|--------------------|---------|--------|
| 1 | push 1, go left → None | [1] | None | [] |
| 2 | pop 1, record, go right | [] | 2 | [1] |
| 3 | push 2, go left → 3 | [2] | 3 | [1] |
| 4 | push 3, go left → None | [2, 3] | None | [1] |
| 5 | pop 3, record, go right → None | [2] | None | [1, 3] |
| 6 | pop 2, record, go right → None | [] | None | [1, 3, 2] |
| 7 | stack empty and current None → stop | | | **[1, 3, 2]** |

### Trace — left-skewed `[3, 2, null, 1]`

The inner loop pushes 3, 2, 1 in one go. Then the pops come out as 1, 2, 3,
each with no right child, so the result is `[1, 2, 3]`.

### Challenges

- In my first iterative attempt I wrote `while stack:` as the outer loop
  condition. It broke immediately: at the start the stack is empty (I
  haven't pushed the root yet), so the loop never ran. Also, after popping
  the last node the stack is empty but I may still have a right subtree to
  visit. The correct condition is `current is not None or stack`.
- I also tried recording the value when *pushing* the node. That gives
  preorder, not inorder, because a node gets recorded before its left
  subtree. The value must be recorded at *pop* time.
- I tested both versions on the same inputs (normal, empty, one node,
  skewed) to check they always agree.

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes.

Every node is pushed onto the stack exactly once and popped exactly once,
and each push/pop/append is O(1). The inner `while` loop looks nested, but
across the whole run it pushes each node only once, so the total work is
still proportional to `n`, not `n²`.

**Space Complexity: O(h)** extra, where `h` is the height of the tree
(plus O(n) for the output list, which is required anyway). The stack holds
at most one path from the root down, so O(log n) for a balanced tree and
O(n) for a skewed one. The recursive version uses the same O(h), just on
the call stack.

## 4. Reflection / Improvement

- **More efficient approach?** Time cannot beat O(n) because every value
  has to be output. Space can be improved.
- **What to change:** *Morris traversal*. Instead of a stack, it
  temporarily makes the right-most node of each left subtree point back to
  the current node (a "thread"), uses that link to come back up, and then
  removes it, so the tree is restored at the end.
- **Improved complexity:** O(n) time, **O(1)** extra space.
