# Binary Tree Paths
# https://leetcode.com/problems/binary-tree-paths/

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def binary_tree_paths(root: Optional[TreeNode]) -> List[str]:
    """
    Depth-first walk that carries the path built so far as a string.
    At each node I append "->value". When I reach a leaf the string is
    a complete root-to-leaf path, so I save it.
    """
    paths = []

    def walk(node, path_so_far):
        if node is None:
            return
        path = path_so_far + "->" + str(node.val) if path_so_far else str(node.val)
        if node.left is None and node.right is None:
            paths.append(path)
            return
        walk(node.left, path)
        walk(node.right, path)

    walk(root, "")
    return paths


def binary_tree_paths_backtracking(root: Optional[TreeNode]) -> List[str]:
    """
    Improved version: one shared list of values, push on the way down,
    pop on the way back up ("backtracking"). A string is only built
    when a leaf is reached.
    """
    paths = []
    stack = []

    def walk(node):
        if node is None:
            return
        stack.append(str(node.val))
        if node.left is None and node.right is None:
            paths.append("->".join(stack))
        else:
            walk(node.left)
            walk(node.right)
        stack.pop()

    walk(root)
    return paths


# LeetCode entry point
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        return binary_tree_paths(root)


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
        ([1, 2, 3, None, 5], ["1->2->5", "1->3"]),
        ([1], ["1"]),
        ([1, 2], ["1->2"]),               # only ONE path, not two
        ([-1, 2, -3], ["-1->2", "-1->-3"]),
        ([1, 2, 3, 4, 5, 6, 7], ["1->2->4", "1->2->5", "1->3->6", "1->3->7"]),
    ]

    all_ok = True
    for values, expected in test_cases:
        root = build_tree(values)
        r1 = binary_tree_paths(root)
        r2 = binary_tree_paths_backtracking(root)
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values} -> {r1} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")
