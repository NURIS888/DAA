# Range Sum of BST

LeetCode: https://leetcode.com/problems/range-sum-of-bst/

## 1. Problem

I'm given the root of a binary search tree and two numbers `low` and
`high`. I need to add up the values of all nodes that lie between them,
including `low` and `high` themselves, and return the total.

## 2. Approach

Depth-first search that uses the BST order to **skip** parts of the tree
that can't contain any value in the range (`range_sum_bst`):

1. `None` → contributes 0.
2. `node.val < low` → the node is too small, and so is its entire left
   subtree (everything there is even smaller). Only the **right** subtree
   can still have values in range, so I search only there.
3. `node.val > high` → the node is too big, and so is its entire right
   subtree. Only the **left** subtree can help.
4. Otherwise the node is in range: add `node.val` and search **both**
   sides.

### Trace — `root = [10, 5, 15, 3, 7, null, 18]`, `low = 7`, `high = 15`

```
        10
       /  \
      5    15
     / \     \
    3   7     18
```

| Call | Value vs [7, 15] | Action | Returns |
|------|------------------|--------|---------|
| sum(10) | in range | 10 + sum(5) + sum(15) | |
| sum(5) | 5 < 7 | skip 5 **and its left subtree (3)**, go right | |
| sum(7) | in range | 7 + sum(None) + sum(None) | **7** |
| → sum(5) returns | | | 7 |
| sum(15) | in range | 15 + sum(None) + sum(18) | |
| sum(18) | 18 > 15 | skip 18 and its right side, go left | sum(None) = 0 |
| → sum(15) returns | | | 15 |
| → sum(10) returns | | 10 + 7 + 15 | **32** |

Answer **32**. Node 3 was never visited.

### Challenges

- **First attempt — brute force.** I visited every node and added it if
  `low <= val <= high` (`range_sum_brute_force`). It works for any binary
  tree, but it never uses the BST order, so it always visits all `n`
  nodes, even when the range only covers a tiny part of the tree.
- **Wrong pruning.** Then I tried to "skip" out-of-range nodes like this
  (`range_sum_wrong`):

  ```python
  if root is None or root.val < low or root.val > high:
      return 0
  ```

  On the same tree with range `[3, 7]` it returned **0** instead of 15.
  The root 10 is bigger than 7, so the function stopped immediately — but
  3, 5 and 7 are all *below* 10, in its left subtree. My mistake was
  thinking "out-of-range node" means "out-of-range subtree". Only **one
  side** of an out-of-range node can be skipped; the other side must still
  be searched. That's exactly the difference between my wrong version and
  cases 2 and 3 of the final one.
- **Tests:** the LeetCode examples, a range covering everything, a range
  covering nothing (`[11, 14]` → 0), a single node, and the case above
  where the root itself is out of range. I compared the pruned version
  against the brute-force one on every test.

## 3. Time Complexity

**Time Complexity: O(n)** in the worst case, where `n` is the number of
nodes. Better in practice: about **O(h + k)**, where `h` is the tree height
and `k` the number of nodes inside the range.

Why:
- Every node is visited at most once with O(1) work, so it can never be
  worse than O(n). If the range covers the whole tree, all `n` nodes are
  in range and must be added, so O(n) is reached.
- When the range is small, the search only goes into a subtree that can
  still contain in-range values. The nodes visited are the `k` in-range
  ones, plus the out-of-range nodes along the two "border" paths (the path
  towards `low` and the path towards `high`), each at most `h` long. That
  gives roughly O(h + k) visits.

The brute-force version is always O(n), no matter how small the range is.

**Space Complexity: O(h)** for the recursion stack: O(log n) for a
balanced tree, O(n) for a skewed one. I only keep one running sum per call.

## 4. Reflection / Improvement

- **More efficient approach?** For a single query on a plain BST, O(h + k)
  is already close to the best you can do, since all `k` in-range values
  have to be added.
- **What would need to change:** if many range queries are asked on the
  same tree, I could store in every node the **sum of its whole subtree**
  (an "augmented" BST). Then a fully in-range subtree is added in one step
  instead of being walked node by node; the answer is
  `sum(values ≤ high) − sum(values < low)`, and each of those is found by
  walking a single root-to-leaf path. Keeping the tree balanced
  (AVL / red-black) keeps that path short.
- **Improved complexity:** **O(h)** per query, i.e. **O(log n)** on a
  balanced tree, independent of how many values are in the range. Cost: an
  extra number per node, updated on every insert/delete.
