# Convert Sorted Array to Binary Search Tree

LeetCode: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/

## 1. Problem

I get an array of numbers sorted from smallest to largest. I have to
build a binary search tree containing exactly these numbers, and the tree
must be **height-balanced**: at every node, the heights of the left and
right subtrees may differ by at most 1. Several different trees can be
correct; any one of them is accepted.

## 2. Approach

Key idea: in a sorted array, the **middle** element splits the numbers
into two halves of (almost) equal size — everything left of it is smaller,
everything right of it is bigger. That is exactly what a balanced BST
root needs.

`sorted_array_to_bst` uses a helper `build(lo, hi)` that builds a tree
from `nums[lo..hi]`:

1. If `lo > hi`, this part of the array is empty → return `None`.
2. Take `mid = (lo + hi) // 2` and make `nums[mid]` the node.
3. Build the left subtree from `nums[lo..mid-1]` and the right subtree
   from `nums[mid+1..hi]` in the same way.

I pass two indices instead of cutting the list into new lists, so the
array is never copied.

### Trace — `nums = [-10, -3, 0, 5, 9]`

Indices: `0:-10  1:-3  2:0  3:5  4:9`

| Call | Range of values | mid | Node | Left call | Right call |
|------|-----------------|-----|------|-----------|------------|
| build(0, 4) | [-10, -3, 0, 5, 9] | 2 | **0** | build(0, 1) | build(3, 4) |
| build(0, 1) | [-10, -3] | 0 | **-10** | build(0, -1) → None | build(1, 1) |
| build(1, 1) | [-3] | 1 | **-3** | None | None |
| build(3, 4) | [5, 9] | 3 | **5** | build(3, 2) → None | build(4, 4) |
| build(4, 4) | [9] | 4 | **9** | None | None |

Result:

```
        0
       / \
    -10   5
      \    \
      -3    9
```

Level order `[0, -10, 5, null, -3, null, 9]`. Left and right subtrees of
the root both have height 2, so the tree is balanced. Reading it in order
(left, node, right) gives back `-10, -3, 0, 5, 9`, so it is a valid BST.
(LeetCode's example shows `[0, -3, 9, -10, null, 5]` — that's what you get
when you round `mid` up instead of down. Both are accepted.)

### Trace — `nums = [1, 2, 3, 4, 5, 6, 7]`

mid = 4 → root 4; left half `[1, 2, 3]` → root 2 with children 1, 3; right
half `[5, 6, 7]` → root 6 with children 5, 7. A perfect tree of height 3.

### Challenges

- **Brute force that doesn't work.** My first idea was to take an
  ordinary BST and insert the numbers one by one, in the given order
  (`insert_one_by_one`). Because the input is sorted, every new number is
  bigger than all the numbers before it, so it always goes to the right.
  For `[1..7]` I got a "chain" of height **7** instead of 3 — a valid BST,
  but completely unbalanced, so the answer is rejected. The order of
  insertion decides the shape of the tree, and sorted order is the worst
  possible.
- **Picking the root.** That failure made me think about which number
  should be at the top. The middle number is the only choice that leaves
  the same amount of numbers on both sides, and the same reasoning works
  again inside each half — which led to the recursive solution.
- **Slicing.** My first recursive version (`sorted_array_to_bst_slicing`)
  used `nums[:mid]` and `nums[mid+1:]`. It gives the right tree, but every
  slice *copies* part of the array, which costs extra time and memory (see
  section 3). Switching to `lo`/`hi` indices removed the copying.
- **Off-by-one errors.** With indices, it's easy to use `mid` instead of
  `mid - 1` for the left half; then `build(0, 0)` keeps calling itself
  with the same range and never stops. The stop condition `lo > hi` and
  excluding `mid` from both halves fixed this.
- **How I tested:** because many trees are correct, I didn't compare
  against one fixed answer. Instead, my test checks two properties: (1) the
  in-order traversal equals the input array, which proves it's a valid BST
  with all the numbers, and (2) every node is height-balanced. I ran this
  on small arrays, an even-length array, a single element, an empty array,
  and 100 numbers (height 7, the minimum possible, since 2⁷ = 128 ≥ 100).

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the length of the array.

Each call of `build` creates exactly one node, and every array element
becomes a node exactly once, so there are `n` calls that create nodes
(plus about `n + 1` calls that just return `None` for an empty range).
Every call does constant work: compute `mid`, create one node, make two
calls. n × O(1) = O(n).

The slicing version is **O(n log n)**: at every level of the recursion,
the slices together copy almost the whole array (O(n) per level), and
there are about log n levels.

**Space Complexity: O(log n)** extra, plus O(n) for the tree itself
(which is the answer, so it is required). The recursion goes as deep as
the tree is tall, and because the tree is balanced, its height is about
log₂ n. So at most about log n calls are on the stack at once. (The
slicing version also needs O(n) extra memory for the copies.)

## 4. Reflection / Improvement

- **More efficient approach?** Not in time: the output has `n` nodes, and
  creating them takes at least O(n). My solution already reaches that.
- **What could change:** the recursion could be replaced by an iterative
  version that uses an explicit stack of `(node, lo, hi)` tasks; it does
  the same work but avoids Python's recursion limit. This only matters for
  huge inputs, because the recursion depth is just log n (about 20 for a
  million numbers).
- **Improved complexity:** stays O(n) time and O(log n) extra space — the
  current solution is already optimal; the main improvement was going
  from slicing (O(n log n)) to indices (O(n)).
