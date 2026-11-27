# Convert Sorted Array to Binary Search Tree
# https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/

from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sorted_array_to_bst(nums: List[int]) -> Optional[TreeNode]:
    """
    The middle element of a sorted array is the perfect root:
    half of the numbers are smaller (they go left), half are bigger
    (they go right). Doing the same thing again on each half gives
    subtrees whose sizes differ by at most 1, so the tree is balanced.

    I pass index boundaries (lo, hi) instead of slicing the list, so no
    copies of the array are made.
    """

    def build(lo, hi):
        if lo > hi:                  # empty part of the array
            return None
        mid = (lo + hi) // 2
        node = TreeNode(nums[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(nums) - 1)


def sorted_array_to_bst_slicing(nums: List[int]) -> Optional[TreeNode]:
    """My first version: same idea, but with list slicing (copies the array)."""
    if not nums:
        return None
    mid = len(nums) // 2
    node = TreeNode(nums[mid])
    node.left = sorted_array_to_bst_slicing(nums[:mid])
    node.right = sorted_array_to_bst_slicing(nums[mid + 1:])
    return node


def insert_one_by_one(nums: List[int]) -> Optional[TreeNode]:
    """
    A brute-force idea that does NOT work: insert the numbers in the given
    (sorted) order into an ordinary BST. Every new number is bigger than
    all previous ones, so it always goes right -> a chain, not balanced.
    """
    root = None
    for x in nums:
        if root is None:
            root = TreeNode(x)
            continue
        cur = root
        while True:
            if x < cur.val:
                if cur.left is None:
                    cur.left = TreeNode(x)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = TreeNode(x)
                    break
                cur = cur.right
    return root


# LeetCode entry point
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        return sorted_array_to_bst(nums)


# ---------- Helpers used only for local testing ----------

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


def inorder(root):
    return inorder(root.left) + [root.val] + inorder(root.right) if root else []


def height(root):
    return 0 if root is None else 1 + max(height(root.left), height(root.right))


def is_balanced(root):
    if root is None:
        return True
    return abs(height(root.left) - height(root.right)) <= 1 and is_balanced(root.left) and is_balanced(root.right)


if __name__ == "__main__":
    # Many balanced answers are accepted by LeetCode, so I check the
    # properties instead of one exact shape:
    #   1. inorder traversal gives back the original sorted array (valid BST)
    #   2. the tree is height-balanced
    test_cases = [
        [-10, -3, 0, 5, 9],
        [1, 3],
        [0],
        [1, 2, 3, 4, 5, 6, 7],
        list(range(100)),
        [],
    ]

    all_ok = True
    for nums in test_cases:
        root = sorted_array_to_bst(nums)
        ok = inorder(root) == nums and is_balanced(root)
        root2 = sorted_array_to_bst_slicing(nums)
        ok &= inorder(root2) == nums and is_balanced(root2)
        all_ok &= ok
        shown = nums if len(nums) <= 10 else f"[0..{len(nums) - 1}]"
        print(f"{shown} -> {tree_to_list(root) if len(nums) <= 10 else '...'} "
              f"height={height(root)} [{'OK' if ok else 'FAIL'}]")
    print("ALL PASSED" if all_ok else "SOME FAILED")

    chain = insert_one_by_one([1, 2, 3, 4, 5, 6, 7])
    print(f"\nInsert-one-by-one on [1..7]: height={height(chain)}, balanced={is_balanced(chain)} "
          f"(middle method: height={height(sorted_array_to_bst([1, 2, 3, 4, 5, 6, 7]))})")
