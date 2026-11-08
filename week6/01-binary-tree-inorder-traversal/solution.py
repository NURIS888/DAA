# Binary Tree Inorder Traversal
# https://leetcode.com/problems/binary-tree-inorder-traversal/

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """
    Inorder = Left subtree, then Node, then Right subtree.

    A small helper walks the tree: go all the way into the left subtree,
    write down the current value, then walk the right subtree.
    An empty subtree (None) simply contributes nothing.
    """
    result = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        result.append(node.val)
        visit(node.right)

    visit(root)
    return result


def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Same order, but with my own stack instead of the call stack
    (this is the LeetCode follow-up).

    1. Slide left from the current node, pushing every node on the way.
    2. When I can't go further left, pop a node: everything to its left
       is already done, so I record it.
    3. Move into its right subtree and repeat.
    """
    result = []
    stack = []
    current = root

    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right

    return result


# LeetCode entry point
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        return inorder_iterative(root)


# ---------- Helper used only for local testing ----------

def build_tree(values):
    """Build a tree from LeetCode's level-order list, e.g. [1, None, 2, 3]."""
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
        ([1, None, 2, 3], [1, 3, 2]),
        ([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9], [4, 2, 6, 5, 7, 1, 3, 9, 8]),
        ([], []),
        ([1], [1]),
        ([3, 2, None, 1], [1, 2, 3]),           # left-skewed
    ]

    all_ok = True
    for values, expected in test_cases:
        root = build_tree(values)
        r1 = inorder_recursive(root)
        r2 = inorder_iterative(root)
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values} -> recursive={r1}, iterative={r2} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")
