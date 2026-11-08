# Merge Two Binary Trees
# https://leetcode.com/problems/merge-two-binary-trees/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def merge_trees(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Walk both trees at the same time, position by position.
      - If one side is empty, the other side's whole subtree is the answer
        for this position: I reuse it as-is, no need to go deeper.
      - If both exist, add root2's value into root1 and merge the children.
    root1 is modified in place and returned.
    """
    if root1 is None:
        return root2
    if root2 is None:
        return root1

    root1.val += root2.val
    root1.left = merge_trees(root1.left, root2.left)
    root1.right = merge_trees(root1.right, root2.right)
    return root1


# LeetCode entry point
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        return merge_trees(root1, root2)


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
        ([1, 3, 2, 5], [2, 1, 3, None, 4, None, 7], [3, 4, 5, 5, 4, None, 7]),
        ([1], [1, 2], [2, 2]),
        ([], [1, 2], [1, 2]),
        ([1, 2], [], [1, 2]),
        ([], [], []),
    ]

    all_ok = True
    for v1, v2, expected in test_cases:
        result = tree_to_list(merge_trees(build_tree(v1), build_tree(v2)))
        ok = result == expected
        all_ok &= ok
        print(f"{v1} + {v2} -> {result} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")
