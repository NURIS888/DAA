# Minimum Depth of Binary Tree

LeetCode: https://leetcode.com/problems/minimum-depth-of-binary-tree/

## 1. Problem

I need the number of nodes on the **shortest** path from the root down to
a **leaf** (a node with no children). The important word is *leaf*: a node
that has only one child is not the end of a path.

## 2. Approach

I used breadth-first search (`min_depth`), going through the tree level
by level.

1. Put `(root, 1)` into a queue.
2. Take the front item. If that node is a leaf, return its depth right
   away — BFS visits all nodes on level `d` before any node on level
   `d + 1`, so the first leaf I see is the closest one.
3. Otherwise put its existing children into the queue with `depth + 1`.

I also wrote a corrected recursive version (`min_depth_dfs`) to compare.

### Trace — `[3, 9, 20, null, null, 15, 7]`

```
    3
   / \
  9   20
     /  \
    15   7
```

| Step | Pop | Leaf? | Queue after |
|------|-----|-------|-------------|
| 1 | (3, 1) | no | [(9,2), (20,2)] |
| 2 | (9, 2) | **yes** → return 2 | — |

Answer **2**. BFS stopped without ever touching 15 or 7.

### Trace — right-skewed `[2, null, 3, null, 4, null, 5, null, 6]`

```
2
 \
  3
   \
    4
     \
      5
       \
        6
```

Queue goes `(2,1)` → `(3,2)` → `(4,3)` → `(5,4)` → `(6,5)`. Only node 6 is
a leaf, so the answer is **5**.

### Challenges

My first attempt (kept as `min_depth_wrong`) was a copy of max depth with
`min` instead of `max`:

```python
return 1 + min(min_depth(root.left), min_depth(root.right))
```

On the skewed tree above it returns **1** instead of 5. The reason: at
node 2 the left child is `None`, which returns 0, and `min(0, ...)` = 0, so
the answer becomes 1 + 0. But a missing child is not a leaf — there is no
path ending there. The fix in the recursive version is: if one child is
missing, only follow the other one; use `min` only when both children
exist.

That bug pushed me to BFS, because BFS checks "is this a leaf?" directly
and has no such trap. Test cases I added because of this bug: the skewed
tree and `[1, 2]` (root has one child, answer 2, not 1).

## 3. Time Complexity

**Time Complexity: O(n)** in the worst case, where `n` is the number of
nodes.

Each node is added to the queue and removed from it at most once, with
O(1) work each time (`deque` makes `popleft` O(1)). In the worst case
(e.g. the skewed tree, or when the only leaves are on the last level) BFS
has to visit every node before finding a leaf. In good cases it is much
faster: it stops at the first leaf's level and never explores deeper.

**Space Complexity: O(w)**, where `w` is the maximum number of nodes in one
level held in the queue at once. For a complete tree the last level can be
about n/2 nodes, so the worst case is O(n). For a skewed tree it is O(1).

## 4. Reflection / Improvement

- **More efficient approach?** Not asymptotically — in the worst case
  every node must be checked, so O(n) is required.
- **Trade-off between my two versions:** DFS always explores the *whole*
  tree, even if there is a leaf at depth 2 and the other side is 10 000
  nodes deep. BFS stops early, so in practice it is the better choice
  here. DFS uses O(h) memory, BFS uses O(w); which is smaller depends on
  the tree's shape.
- **Improved complexity:** O(n) worst case either way; BFS is
  O(nodes up to the first leaf's level) in the best case.
