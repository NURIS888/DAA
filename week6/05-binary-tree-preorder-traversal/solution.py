# Binary Tree Preorder Traversal
# https://leetcode.com/problems/binary-tree-preorder-traversal/

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Preorder = Node, then Left subtree, then Right subtree.

    I keep a stack of nodes still to visit. Pop a node, record it, then
    push its children. A stack is last-in-first-out, so I push RIGHT first
    and LEFT second: that way the left child is popped (visited) first.
    """
    if root is None:
        return []

    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """Straightforward recursive version, used to cross-check the stack one."""
    result = []

    def visit(node):
        if node is None:
            return
        result.append(node.val)
        visit(node.left)
        visit(node.right)

    visit(root)
    return result


# LeetCode entry point
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        return preorder_iterative(root)


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
        ([1, None, 2, 3], [1, 2, 3]),
        ([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9], [1, 2, 4, 5, 6, 7, 3, 8, 9]),
        ([], []),
        ([1], [1]),
    ]

    all_ok = True
    for values, expected in test_cases:
        root = build_tree(values)
        r1 = preorder_iterative(root)
        r2 = preorder_recursive(root)
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values} -> iterative={r1}, recursive={r2} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")
