# Maximum Depth of Binary Tree

LeetCode: https://leetcode.com/problems/maximum-depth-of-binary-tree/

## 1. Problem

Given a binary tree, I need to find how many nodes are on the **longest**
path from the root down to the deepest leaf. An empty tree has depth 0, a
single node has depth 1.

## 2. Approach

I used recursion (`max_depth`), based on one observation: the depth of a
tree is **1 (the root) + the depth of its deeper subtree**.

1. If the node is `None`, return 0. This is the base case.
2. Otherwise ask the left subtree for its depth, ask the right subtree for
   its depth, and return `1 + max(left, right)`.

I also wrote a breadth-first version (`max_depth_bfs`) that counts levels
with a queue, to cross-check.

### Trace — `[3, 9, 20, null, null, 15, 7]`

```
    3
   / \
  9   20
     /  \
    15   7
```

Calls return bottom-up:

| Call | left | right | Returns |
|------|------|-------|---------|
| depth(9) | depth(None)=0 | depth(None)=0 | 1 + max(0,0) = **1** |
| depth(15) | 0 | 0 | **1** |
| depth(7) | 0 | 0 | **1** |
| depth(20) | depth(15)=1 | depth(7)=1 | 1 + 1 = **2** |
| depth(3) | depth(9)=1 | depth(20)=2 | 1 + 2 = **3** |

Answer: **3**.

BFS trace on the same tree: level 1 = `[3]`, level 2 = `[9, 20]`,
level 3 = `[15, 7]`, then the queue is empty → 3 levels.

### Challenges

- My first idea was to count *all* nodes along the way and keep a global
  counter that I increased when going down and decreased when coming back
  up. It worked, but it was messy and easy to get off-by-one. Letting each
  call *return* its own depth was much cleaner.
- I had to decide what depth `None` has. Returning 1 for `None` made every
  answer one too big; 0 is correct because an empty tree has no nodes.
- Test cases: normal tree, empty tree, a single node, and a left-skewed
  "linked list" of 5 nodes (the worst case for recursion depth).

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes.

Each node is visited exactly once, and at each node I only do a constant
amount of work (one `max` and one addition). Calls on `None` children add
at most `n + 1` extra constant-time calls, which doesn't change the order.

**Space Complexity: O(h)**, where `h` is the tree height. That is the
maximum depth of the recursion stack: O(log n) for a balanced tree, O(n)
for a skewed tree. (The BFS version uses O(w) instead, where `w` is the
widest level — up to about n/2 for a full tree.)

## 4. Reflection / Improvement

- **More efficient approach?** Not in time: to know the deepest leaf I
  must look at every node, so O(n) is the lower bound.
- **What to change:** for very deep (skewed) trees, the recursive version
  can hit Python's recursion limit (about 1000 calls). Switching to the
  iterative BFS, or an iterative DFS with a stack of `(node, depth)`
  pairs, avoids that.
- **Improved complexity:** still O(n) time; space O(h) or O(w) depending
  on the version, but without the recursion-limit risk.
