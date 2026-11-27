# Search in a Binary Search Tree
# https://leetcode.com/problems/search-in-a-binary-search-tree/

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Walk down from the root and use the BST rule at every step:
    everything in the left subtree is smaller, everything in the right
    subtree is bigger. So at each node there is only ONE side where the
    value can be, and I never need to come back up.
    """
    current = root
    while current is not None:
        if val == current.val:
            return current
        if val < current.val:
            current = current.left
        else:
            current = current.right
    return None


def search_bst_brute_force(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    My first version: search the whole tree like an ordinary binary tree,
    ignoring the BST order. Correct, but it may visit every node.
    """
    if root is None:
        return None
    if root.val == val:
        return root
    found = search_bst_brute_force(root.left, val)
    if found:
        return found
    return search_bst_brute_force(root.right, val)


# LeetCode entry point
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        return search_bst(root, val)


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
        ([4, 2, 7, 1, 3], 2, [2, 1, 3]),
        ([4, 2, 7, 1, 3], 5, []),            # not in the tree
        ([4, 2, 7, 1, 3], 4, [4, 2, 7, 1, 3]),  # value is the root
        ([4, 2, 7, 1, 3], 7, [7]),           # value is a leaf
        ([], 1, []),                         # empty tree
        ([5, 4, None, 3, None, 2, None, 1], 1, [1]),  # left-skewed BST
    ]

    all_ok = True
    for values, val, expected in test_cases:
        root = build_tree(values)
        r1 = tree_to_list(search_bst(root, val))
        r2 = tree_to_list(search_bst_brute_force(root, val))
        ok = r1 == expected and r2 == expected
        all_ok &= ok
        print(f"{values}, val={val} -> {r1} (expected {expected}) [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")
