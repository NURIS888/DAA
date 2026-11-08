# Sum of Left Leaves
# https://leetcode.com/problems/sum-of-left-leaves/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sum_of_left_leaves(root: Optional[TreeNode]) -> int:
    """
    A node only knows whether it is a leaf; it does not know whether it
    is a LEFT child. So I pass that information down: is_left is True
    only when I step into node.left.

    A node counts when it is a leaf AND is_left is True.
    The root is called with is_left=False, so a lone root never counts.
    """

    def walk(node, is_left):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return node.val if is_left else 0
        return walk(node.left, True) + walk(node.right, False)

    return walk(root, False)


def sum_of_left_leaves_wrong(root: Optional[TreeNode]) -> int:
    """My first (incorrect) attempt: sums every LEFT CHILD, leaf or not."""
    if root is None:
        return 0
    total = root.left.val if root.left else 0
    return total + sum_of_left_leaves_wrong(root.left) + sum_of_left_leaves_wrong(root.right)


# LeetCode entry point
class Solution:
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
        return sum_of_left_leaves(root)


# ---------- Helper used only for local testing ----------

def build_tree(values):
    """Build a tree from LeetCode's level-order list."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    test_cases = [
        ([3, 9, 20, None, None, 15, 7], 24),   # 9 + 15
        ([1], 0),                              # root is not a left leaf
        ([1, 2, 3, 4, 5], 4),                  # 2 is a left child but NOT a leaf
        ([1, None, 2, 3], 3),                  # left leaf deep in the right subtree
        ([], 0),
    ]

    all_ok = True
    for values, expected in test_cases:
        result = sum_of_left_leaves(build_tree(values))
        ok = result == expected
        all_ok &= ok
        print(f"{values} -> {result} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")

    print(f"\nWrong attempt on [1, 2, 3, 4, 5] -> {sum_of_left_leaves_wrong(build_tree([1, 2, 3, 4, 5]))} (should be 4)")
