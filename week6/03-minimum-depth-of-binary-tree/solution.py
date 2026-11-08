# Minimum Depth of Binary Tree
# https://leetcode.com/problems/minimum-depth-of-binary-tree/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def min_depth(root: Optional[TreeNode]) -> int:
    """
    Breadth-first search, level by level, starting from the root.
    The first leaf I meet is on the shallowest level, so I can return its
    depth immediately without looking at the rest of the tree.
    """
    if root is None:
        return 0

    queue = deque([(root, 1)])          # (node, depth of that node)
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth                # first leaf = closest leaf
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0  # never reached for a non-empty tree


def min_depth_dfs(root: Optional[TreeNode]) -> int:
    """
    Recursive version. The trap: if one child is missing, that side is
    NOT a path to a leaf, so I must ignore it instead of taking min(0, ...).
    """
    if root is None:
        return 0
    if root.left is None:
        return 1 + min_depth_dfs(root.right)
    if root.right is None:
        return 1 + min_depth_dfs(root.left)
    return 1 + min(min_depth_dfs(root.left), min_depth_dfs(root.right))


def min_depth_wrong(root: Optional[TreeNode]) -> int:
    """My first (incorrect) attempt, kept to show why it fails."""
    if root is None:
        return 0
    return 1 + min(min_depth_wrong(root.left), min_depth_wrong(root.right))


# LeetCode entry point
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        return min_depth(root)


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
        ([3, 9, 20, None, None, 15, 7], 2),
        ([2, None, 3, None, 4, None, 5, None, 6], 5),   # right-skewed
        ([], 0),
        ([1], 1),
        ([1, 2], 2),                                    # root is not a leaf
        ([1, 2, 3, 4, None, None, None, 5], 2),
    ]

    all_ok = True
    for values, expected in test_cases:
        root = build_tree(values)
        r1 = min_depth(root)
        r2 = min_depth_dfs(root)
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values} -> bfs={r1}, dfs={r2} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")

    wrong = min_depth_wrong(build_tree([2, None, 3, None, 4, None, 5, None, 6]))
    print(f"\nFirst wrong attempt on the skewed tree gives {wrong} instead of 5")
