# Merge Two Binary Trees

LeetCode: https://leetcode.com/problems/merge-two-binary-trees/

## 1. Problem

Imagine putting one binary tree on top of another. Where both trees have
a node in the same position, the merged tree gets a node with the **sum**
of the two values. Where only one tree has a node, that node (and its
whole subtree) is taken as it is. Return the root of the merged tree.

## 2. Approach

Recursion that walks both trees in the same shape at the same time:

1. If `root1` is `None`, the answer for this position is `root2` (which
   may also be `None`). I return it directly — its whole subtree is reused
   and I don't go deeper.
2. If `root2` is `None`, return `root1` the same way.
3. If both exist: `root1.val += root2.val`, then
   `root1.left = merge(root1.left, root2.left)` and the same for `right`.
4. Return `root1`. Tree 1 is updated in place and becomes the answer.

### Trace — `root1 = [1, 3, 2, 5]`, `root2 = [2, 1, 3, null, 4, null, 7]`

```
 Tree 1         Tree 2          Merged
    1              2               3
   / \            / \             / \
  3   2          1   3           4   5
 /                \   \         / \   \
5                  4   7       5   4   7
```

| Call | root1 | root2 | Action | Returns |
|------|-------|-------|--------|---------|
| merge(1, 2) | 1 | 2 | 1+2 = **3**, recurse | node 3 |
| merge(3, 1) | 3 | 1 | 3+1 = **4**, recurse | node 4 |
| merge(5, None) | 5 | None | root2 empty | node 5 (as is) |
| merge(None, 4) | None | 4 | root1 empty | node 4 (from tree 2) |
| merge(2, 3) | 2 | 3 | 2+3 = **5**, recurse | node 5 |
| merge(None, None) | None | None | root1 empty | None |
| merge(None, 7) | None | 7 | root1 empty | node 7 (from tree 2) |

Level order of the result: **[3, 4, 5, 5, 4, null, 7]** ✓

### Challenges

- My first idea was to build a brand-new tree: create a node for every
  position that exists in *either* tree, treating a missing node as value
  0. That works, but it visits every node of both trees — including big
  subtrees that exist in only one of them — and copies them one by one.
  Reusing the existing subtree when one side is `None` is simpler and does
  less work.
- I had to be careful to *assign* the recursive result back
  (`root1.left = merge(...)`). Just calling `merge(root1.left, root2.left)`
  without assigning lost the subtrees from tree 2 whenever `root1.left`
  was `None`, because the returned node was thrown away.
- Edge cases tested: one tree empty (either side), both empty, and a case
  where tree 2 is deeper than tree 1 (`[1]` + `[1, 2]` → `[2, 2]`).

## 3. Time Complexity

**Time Complexity: O(min(n₁, n₂))**, where n₁ and n₂ are the sizes of the
two trees. More precisely: O(number of positions where *both* trees have a
node).

The recursion only goes deeper when both nodes exist. As soon as one side
is `None`, it returns immediately in O(1), attaching the other subtree
without walking through it. The overlapping positions can't be more than
the smaller tree's size, so the work is bounded by min(n₁, n₂).

**Space Complexity: O(min(h₁, h₂))** for the recursion stack, where h₁, h₂
are the heights: recursion stops going deeper as soon as one tree runs
out. No new nodes are created because tree 1 is reused in place (note: the
result shares nodes with tree 2 too, so changing the result later can
change tree 2).

## 4. Reflection / Improvement

- **More efficient approach?** Not in time — every overlapping pair of
  nodes must be added, so O(overlap) is the minimum, and that is what this
  solution does.
- **What to change:** if the original trees must stay untouched, I'd have
  to create new nodes for the overlap and copy the non-overlapping
  subtrees, which raises the time to O(n₁ + n₂). An iterative version
  with a stack of node pairs would avoid the recursion limit.
- **Improved complexity:** the current O(min(n₁, n₂)) time is already
  optimal for the in-place version.
