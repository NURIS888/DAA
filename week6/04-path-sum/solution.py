# Path Sum
# https://leetcode.com/problems/path-sum/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """
    Walk down the tree and subtract each node's value from the target.
    "Remaining" is how much the rest of the path still has to add up to.
    When I stand on a LEAF, the path is complete: it works only if the
    remaining amount is exactly that leaf's value.
    """
    if root is None:
        return False

    remaining = target_sum - root.val
    if root.left is None and root.right is None:
        return remaining == 0

    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)


def has_path_sum_wrong(root: Optional[TreeNode], target_sum: int) -> bool:
    """My first (incorrect) attempt: it checks at None instead of at a leaf."""
    if root is None:
        return target_sum == 0
    remaining = target_sum - root.val
    return has_path_sum_wrong(root.left, remaining) or has_path_sum_wrong(root.right, remaining)


# LeetCode entry point
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        return has_path_sum(root, targetSum)


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
        ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22, True),
        ([1, 2, 3], 5, False),
        ([], 0, False),             # empty tree has no paths at all
        ([1, 2], 1, False),         # "1" alone is not root-to-leaf: 1 has a child
        ([1, 2], 3, True),
        ([-2, None, -3], -5, True),  # negative values
    ]

    all_ok = True
    for values, target, expected in test_cases:
        result = has_path_sum(build_tree(values), target)
        ok = result == expected
        all_ok &= ok
        print(f"{values}, target={target} -> {result} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")

    print(f"\nWrong attempt on [1, 2], target=1 -> {has_path_sum_wrong(build_tree([1, 2]), 1)} (should be False)")
    print(f"Wrong attempt on [], target=0 -> {has_path_sum_wrong(build_tree([]), 0)} (should be False)")
