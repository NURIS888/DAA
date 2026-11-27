# Search in a Binary Search Tree

LeetCode: https://leetcode.com/problems/search-in-a-binary-search-tree/

## 1. Problem

I'm given the root of a binary search tree (BST) and a number `val`. I
have to find the node whose value equals `val` and return it — which also
means returning the whole subtree under it. If no such node exists, I
return `None`.

In a BST every value in a node's left subtree is smaller than the node,
and every value in its right subtree is bigger. That rule is what makes
this problem easy to do fast.

## 2. Approach

I walk down from the root with a single pointer (`search_bst`):

1. If the current node's value equals `val` → found, return the node.
2. If `val` is smaller → it can only be in the left subtree, so go left.
3. If `val` is bigger → it can only be in the right subtree, so go right.
4. If I fall off the tree (`None`) → the value isn't there, return `None`.

At every node I throw away one whole side of the tree, so I never need to
come back up. That's why a simple loop is enough — no recursion, no stack.

### Trace — `root = [4, 2, 7, 1, 3]`, `val = 2`

```
      4
     / \
    2   7
   / \
  1   3
```

| Step | current | Compare | Move |
|------|---------|---------|------|
| 1 | 4 | 2 < 4 | go left |
| 2 | 2 | 2 == 2 | **found** → return node 2 |

Returned subtree: `[2, 1, 3]`. Only 2 nodes were checked; 7, 1 and 3 were
never looked at.

### Trace — same tree, `val = 5`

| Step | current | Compare | Move |
|------|---------|---------|------|
| 1 | 4 | 5 > 4 | go right |
| 2 | 7 | 5 < 7 | go left |
| 3 | None | — | **not found** → return `None` |

### Challenges

- **First attempt — brute force.** I first solved it like an ordinary
  binary tree (`search_bst_brute_force`): check the node, then search the
  whole left subtree, then the whole right subtree. It is correct and it
  passes the tests, but it ignores the BST order completely. For
  `val = 7` it searches through 2, 1 and 3 before even reaching 7. In the
  worst case it visits all `n` nodes.
- **Realising one side can be skipped.** Writing the tree out on paper
  made it obvious: if I'm looking for 7 and the root is 4, nothing on the
  left (all < 4) can be 7. After that, the solution became a loop.
- **Equal case first.** I first wrote the `<` and `>` checks and forgot
  the `==` case, so the loop walked *past* the target until it hit `None`
  and always returned "not found". Checking `==` first fixed it.
- **Tests:** value in the middle, value missing, value at the root, value
  at a leaf, empty tree, and a left-skewed BST (the worst case). I ran
  both versions on every test to check they agree.

## 3. Time Complexity

**Time Complexity: O(h)**, where `h` is the height of the tree.

Each loop step moves exactly one level down, and the work per step is one
or two comparisons (O(1)). The walk can't go deeper than the tree is tall,
so there are at most `h` steps.

- Balanced BST: `h ≈ log₂ n` → **O(log n)**. For 1 000 000 nodes that's
  about 20 steps.
- Skewed BST (like a linked list, e.g. numbers inserted in sorted order):
  `h = n` → **O(n)** in the worst case.

The brute-force version is O(n) every time, because it can visit every
node regardless of shape.

**Space Complexity: O(1)**. The loop only keeps one pointer (`current`).
The returned node is part of the existing tree, so nothing new is built.
(A recursive version of the same idea would use O(h) space for the call
stack.)

## 4. Reflection / Improvement

- **More efficient approach?** For a given tree, no: following one path
  from the root is the minimum — you can't know where the value is without
  comparing along that path.
- **What would need to change:** the weak point is the tree's *shape*. If
  the tree were kept balanced while it is built (a self-balancing BST such
  as an AVL tree or a red-black tree), its height would always stay about
  `log n`.
- **Improved complexity:** guaranteed **O(log n)** search, even in the
  worst case, instead of O(n) for a skewed tree.
