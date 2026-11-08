# Invert Binary Tree
# https://leetcode.com/problems/invert-binary-tree/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Mirror the tree: at every node, swap the left and right children,
    then do the same inside both subtrees.

    The swap uses Python's tuple assignment, which evaluates the whole
    right-hand side first, so neither child is lost during the swap.
    """
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def invert_tree_wrong(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """My first (incorrect) attempt: two separate assignments."""
    if root is None:
        return None
    root.left = invert_tree_wrong(root.right)
    root.right = invert_tree_wrong(root.left)   # root.left was already overwritten!
    return root


# LeetCode entry point
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        return invert_tree(root)


# ---------- Helpers used only for local testing ----------

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


def tree_to_list(root):
    """Turn a tree back into LeetCode's level-order list (trailing Nones removed)."""
    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


if __name__ == "__main__":
    test_cases = [
        ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]),
        ([2, 1, 3], [2, 3, 1]),
        ([], []),
        ([1], [1]),
        ([1, 2], [1, None, 2]),
    ]

    all_ok = True
    for values, expected in test_cases:
        result = tree_to_list(invert_tree(build_tree(values)))
        ok = result == expected
        all_ok &= ok
        print(f"{values} -> {result} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")

    wrong = tree_to_list(invert_tree_wrong(build_tree([2, 1, 3])))
    print(f"\nWrong attempt on [2, 1, 3] -> {wrong} (should be [2, 3, 1])")
