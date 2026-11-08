# Maximum Depth of Binary Tree
# https://leetcode.com/problems/maximum-depth-of-binary-tree/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: Optional[TreeNode]) -> int:
    """
    The depth of a tree is 1 (for the root itself) plus the depth of its
    deeper subtree. An empty tree has depth 0, which is what stops the
    recursion.
    """
    if root is None:
        return 0
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    return 1 + max(left_depth, right_depth)


def max_depth_bfs(root: Optional[TreeNode]) -> int:
    """
    Alternative I also tried: count levels with a queue.
    Each pass of the outer loop processes one whole level.
    """
    if root is None:
        return 0
    queue = deque([root])
    depth = 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth


# LeetCode entry point
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        return max_depth(root)


# ---------- Helper used only for local testing ----------

def build_tree(values):
    """Build a tree from LeetCode's level-order list, e.g. [3, 9, 20, None, None, 15, 7]."""
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
        ([3, 9, 20, None, None, 15, 7], 3),
        ([1, None, 2], 2),
        ([], 0),
        ([1], 1),
        ([1, 2, None, 3, None, 4, None, 5], 5),   # left-skewed "linked list"
    ]

    all_ok = True
    for values, expected in test_cases:
        root = build_tree(values)
        r1 = max_depth(root)
        r2 = max_depth_bfs(root)
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values} -> dfs={r1}, bfs={r2} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")
