# Binary Tree Postorder Traversal
# https://leetcode.com/problems/binary-tree-postorder-traversal/

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def postorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Postorder = Left subtree, then Right subtree, then Node.

    Trick: if I read Left-Right-Node backwards I get Node-Right-Left,
    which is just preorder with the children swapped. That one is easy
    with a stack (push LEFT first so RIGHT is popped first).
    So I build Node-Right-Left and reverse it at the end.
    """
    if root is None:
        return []

    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    result.reverse()
    return result


def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """Straightforward recursive version, used to cross-check."""
    result = []

    def visit(node):
        if node is None:
            return
        visit(node.left)
        visit(node.right)
        result.append(node.val)

    visit(root)
    return result


# LeetCode entry point
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        return postorder_iterative(root)


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
        ([1, None, 2, 3], [3, 2, 1]),
        ([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9], [4, 6, 7, 5, 2, 9, 8, 3, 1]),
        ([], []),
        ([1], [1]),
    ]

    all_ok = True
    for values, expected in test_cases:
        root = build_tree(values)
        r1 = postorder_iterative(root)
        r2 = postorder_recursive(root)
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values} -> iterative={r1}, recursive={r2} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")
