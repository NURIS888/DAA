# Range Sum of BST
# https://leetcode.com/problems/range-sum-of-bst/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    """
    Depth-first walk that skips the parts of the tree that cannot
    contain any value in [low, high]:

    - node.val < low  -> this node AND its whole left subtree are too
                         small, only the right subtree can help.
    - node.val > high -> this node AND its whole right subtree are too
                         big, only the left subtree can help.
    - otherwise       -> count this node and look on both sides.
    """
    if root is None:
        return 0
    if root.val < low:
        return range_sum_bst(root.right, low, high)
    if root.val > high:
        return range_sum_bst(root.left, low, high)
    return root.val + range_sum_bst(root.left, low, high) + range_sum_bst(root.right, low, high)


def range_sum_brute_force(root: Optional[TreeNode], low: int, high: int) -> int:
    """My first version: visit every node and add it if it is in range."""
    if root is None:
        return 0
    own = root.val if low <= root.val <= high else 0
    return own + range_sum_brute_force(root.left, low, high) + range_sum_brute_force(root.right, low, high)


def range_sum_wrong(root: Optional[TreeNode], low: int, high: int) -> int:
    """A wrong pruning attempt: stops completely at an out-of-range node."""
    if root is None or root.val < low or root.val > high:
        return 0
    return root.val + range_sum_wrong(root.left, low, high) + range_sum_wrong(root.right, low, high)


# LeetCode entry point
class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        return range_sum_bst(root, low, high)


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
        ([10, 5, 15, 3, 7, None, 18], 7, 15, 32),               # 7 + 10 + 15
        ([10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10, 23),     # 6 + 7 + 10
        ([10, 5, 15, 3, 7, None, 18], 1, 100, 58),              # everything
        ([10, 5, 15, 3, 7, None, 18], 11, 14, 0),               # nothing in range
        ([10], 10, 10, 10),                                     # single node
        ([10, 5, 15, 3, 7, None, 18], 3, 7, 15),                # root out of range
    ]

    all_ok = True
    for values, low, high, expected in test_cases:
        root = build_tree(values)
        r1 = range_sum_bst(root, low, high)
        r2 = range_sum_brute_force(root, low, high)
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values}, [{low}, {high}] -> {r1} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")

    wrong = range_sum_wrong(build_tree([10, 5, 15, 3, 7, None, 18]), 3, 7)
    print(f"\nWrong pruning on [10,5,15,3,7,null,18], [3, 7] -> {wrong} (should be 15)")
