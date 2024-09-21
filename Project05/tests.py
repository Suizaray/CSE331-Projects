"""
Project 5
CSE 331 SS24
Authors: Gabriel Sotelo, Hank Murdock, Joel Nataren, Aaron Elkin, Divyalakshmi Varadha, Ethan Cook
tests.py
"""

import unittest
import random
import types
from solution import Node, AVLTree, BinarySearchTree, HuffmanTree, build_tree_with_stocks, prune, \
    make_stock_from_dictionary, User, recommend_stock


class BSTTests(unittest.TestCase):

    def test_insert_bst(self):
        """
        (1) Test inserting to empty tree
        final structure:
            1
        """
        bst = BinarySearchTree()
        bst.insert(bst.origin, 1)
        self.assertEqual(1, bst.size)
        self.assertEqual(1, bst.origin.value)
        self.assertEqual(0, bst.origin.height)
        self.assertEqual(None, bst.origin.left)
        self.assertEqual(None, bst.origin.right)

        """
        (2) Test inserting to cause imbalance tree on left
        final structure:
               10
              /
             5
            /
           1
          /
        -1
        """
        bst = BinarySearchTree()
        for value in [10, 5, 1, -1]:
            bst.insert(bst.origin, value)
        self.assertEqual(4, bst.size)
        self.assertEqual(10, bst.origin.value)
        self.assertEqual(3, bst.origin.height)
        self.assertEqual(5, bst.origin.left.value)
        self.assertEqual(2, bst.origin.left.height)
        self.assertEqual(1, bst.origin.left.left.value)
        self.assertEqual(1, bst.origin.left.left.height)
        self.assertEqual(-1, bst.origin.left.left.left.value)
        self.assertEqual(0, bst.origin.left.left.left.height)
        self.assertEqual(None, bst.origin.right)
        """
        (3) Test inserting to cause imbalance tree on left
        final structure:
             10
            /  \
           1    12
                 \
                  13
                   \
                   14
                    \
                    15
        """
        bst = BinarySearchTree()
        for value in [10, 12, 13, 14, 15, 1]:
            bst.insert(bst.origin, value)
        self.assertEqual(6, bst.size)
        self.assertEqual(10, bst.origin.value)
        self.assertEqual(4, bst.origin.height)
        self.assertEqual(1, bst.origin.left.value)
        self.assertEqual(0, bst.origin.left.height)

        self.assertEqual(12, bst.origin.right.value)
        self.assertEqual(3, bst.origin.right.height)
        self.assertEqual(13, bst.origin.right.right.value)
        self.assertEqual(2, bst.origin.right.right.height)
        self.assertEqual(14, bst.origin.right.right.right.value)
        self.assertEqual(1, bst.origin.right.right.right.height)
        self.assertEqual(15, bst.origin.right.right.right.right.value)
        self.assertEqual(0, bst.origin.right.right.right.right.height)

        """
        (4) Test inserting to complex tree (no rotating)
        final structure:
                        10
                    /        \
                  7           19
                /             / \
               4            13   35
              /  \           \   /   
             1    6          17 25
        """
        bst = BinarySearchTree()
        for value in [10, 7, 4, 19, 35, 25, 13, 17, 1, 6]:
            bst.insert(bst.origin, value)

        self.assertEqual(10, bst.size)
        # Height 3
        self.assertEqual(10, bst.origin.value)
        self.assertEqual(3, bst.origin.height)

        # Height 2
        self.assertEqual(7, bst.origin.left.value)
        self.assertEqual(2, bst.origin.left.height)
        self.assertEqual(19, bst.origin.right.value)
        self.assertEqual(2, bst.origin.right.height)

        # Height 1
        self.assertEqual(4, bst.origin.left.left.value)
        self.assertEqual(1, bst.origin.left.left.height)
        self.assertEqual(13, bst.origin.right.left.value)
        self.assertEqual(1, bst.origin.right.left.height)
        self.assertEqual(35, bst.origin.right.right.value)
        self.assertEqual(1, bst.origin.right.right.height)

        # Height 0
        self.assertEqual(1, bst.origin.left.left.left.value)
        self.assertEqual(0, bst.origin.left.left.left.height)
        self.assertEqual(6, bst.origin.left.left.right.value)
        self.assertEqual(0, bst.origin.left.left.right.height)
        self.assertEqual(17, bst.origin.right.left.right.value)
        self.assertEqual(0, bst.origin.right.left.right.height)
        self.assertEqual(25, bst.origin.right.right.left.value)
        self.assertEqual(0, bst.origin.right.right.left.height)

    def test_remove_bst(self):
        # visualize this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        # ensure empty tree is properly handled
        bst = BinarySearchTree()
        self.assertIsNone(bst.remove(bst.origin, 0))

        """
        (1) test removal all left side (not trigger rotation)
        initial structure:
            2
           / \
          1   3
         /     \
        0       4
        final structure (removing 1, 0):
            2
             \
              3
               \
                4
        """
        bst = BinarySearchTree()
        for value in [2, 1, 3, 0, 4]:
            bst.insert(bst.origin, value)
        self.assertEqual(5, bst.size)

        bst.remove(bst.origin, 1)  # one child removal
        self.assertEqual(0, bst.origin.left.value)

        bst.remove(bst.origin, 0)  # zero child removal, will need rebalancing
        self.assertEqual(3, bst.size)
        self.assertEqual(2, bst.origin.value)
        self.assertEqual(2, bst.origin.height)
        self.assertEqual(3, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(4, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)
        self.assertIsNone(bst.origin.left)

        """
        (2) test removal all right side (not trigger rotation)
        initial structure:
            3
           / \
          2   4
         /     \
        1       5
        final structure (removing 4, 5):
            3
           /
          2   
         /     
        1       
        """
        bst = BinarySearchTree()
        for value in [3, 2, 4, 1, 5]:
            bst.insert(bst.origin, value)

        bst.remove(bst.origin, 4)  # one child removal
        self.assertEqual(5, bst.origin.right.value)

        bst.remove(bst.origin, 5)  # zero child removal, will need rebalancing
        self.assertEqual(3, bst.size)
        self.assertEqual(3, bst.origin.value)
        self.assertEqual(2, bst.origin.height)
        self.assertEqual(2, bst.origin.left.value)
        self.assertEqual(1, bst.origin.left.height)
        self.assertEqual(1, bst.origin.left.left.value)
        self.assertEqual(0, bst.origin.left.left.height)
        self.assertIsNone(bst.origin.right)

        """
        (3) test simple 2-child removal
        initial structure:
          2
         / \
        1   3
        final structure (removing 2):
         1 
          \
           3
        """
        bst = BinarySearchTree()
        for value in [2, 1, 3]:
            bst.insert(bst.origin, value)

        # two child removal (predecessor is in the left subtree)
        bst.remove(bst.origin, 2)
        self.assertEqual(2, bst.size)
        self.assertEqual(1, bst.origin.value)
        self.assertEqual(1, bst.origin.height)
        self.assertEqual(3, bst.origin.right.value)
        self.assertEqual(0, bst.origin.right.height)
        self.assertIsNone(bst.origin.left)

        """
        (5) test compounded 2-child removal
        initial structure:
              4
           /     \
          2       6
         / \     / \
        1   3   5   7
        intermediate structure (removing 2, 6):
            4
           / \
          1   5
           \   \
            3   7
        final structure (removing 4)
            3
           / \
          1   5
               \
                7        
        """
        bst = BinarySearchTree()
        for i in [4, 2, 6, 1, 3, 5, 7]:
            bst.insert(bst.origin, i)
        bst.remove(bst.origin, 2)  # two child removal
        self.assertEqual(1, bst.origin.left.value)

        bst.remove(bst.origin, 6)  # two child removal
        self.assertEqual(5, bst.origin.right.value)

        bst.remove(bst.origin, 4)  # two child removal
        self.assertEqual(4, bst.size)
        self.assertEqual(3, bst.origin.value)
        self.assertEqual(2, bst.origin.height)
        self.assertEqual(1, bst.origin.left.value)
        self.assertEqual(0, bst.origin.left.height)
        self.assertEqual(5, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(7, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)

        """
        (6) test removal of intermediate node with 1 children
        Initial structure:
                4
               / \
              3   6
             /   / \
            2   5   7
           / 
          0   
        Final structure (removing 3):
                4
               / \
              2   6
             /   / \
            0   5   7          
        """
        bst = BinarySearchTree()
        for i in [4, 6, 3, 2, 0, 5, 7]:
            bst.insert(bst.origin, i)
        bst.remove(bst.origin, 3)

        self.assertEqual(6, bst.size)
        self.assertEqual(4, bst.origin.value)
        self.assertEqual(2, bst.origin.height)

        self.assertEqual(2, bst.origin.left.value)
        self.assertEqual(1, bst.origin.left.height)
        self.assertEqual(4, bst.origin.left.parent.value)

        self.assertEqual(0, bst.origin.left.left.value)
        self.assertEqual(0, bst.origin.left.left.height)
        self.assertEqual(2, bst.origin.left.left.parent.value)

        self.assertEqual(6, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(4, bst.origin.right.parent.value)

        self.assertEqual(5, bst.origin.right.left.value)
        self.assertEqual(0, bst.origin.right.left.height)
        self.assertEqual(6, bst.origin.right.left.parent.value)

        self.assertEqual(7, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)
        self.assertEqual(6, bst.origin.right.right.parent.value)

        """
        (7) test removal of intermediate node with 2 children
        Initial structure:
                 7  
               /   \
              4     9
             / \   / \
            2  5   8  10
           / \  \        
          1   3  6
        Final structure (removing 4):
                  7  
               /    \
              3      9
             / \    / \
            2   5   8  10
           /     \
          1       6
        """
        bst = BinarySearchTree()
        for i in [7, 4, 9, 2, 5, 8, 10, 1, 3, 6]:
            bst.insert(bst.origin, i)
        a = str(bst)
        print(a)
        bst.remove(bst.origin, 4)

        self.assertEqual(9, bst.size)
        self.assertEqual(7, bst.origin.value)
        self.assertEqual(3, bst.origin.height)

        self.assertEqual(3, bst.origin.left.value)
        self.assertEqual(2, bst.origin.left.height)
        self.assertEqual(7, bst.origin.left.parent.value)

        self.assertEqual(2, bst.origin.left.left.value)
        self.assertEqual(1, bst.origin.left.left.height)
        self.assertEqual(3, bst.origin.left.left.parent.value)

        self.assertEqual(1, bst.origin.left.left.left.value)
        self.assertEqual(0, bst.origin.left.left.left.height)
        self.assertEqual(2, bst.origin.left.left.left.parent.value)

        self.assertEqual(5, bst.origin.left.right.value)
        self.assertEqual(1, bst.origin.left.right.height)
        self.assertEqual(3, bst.origin.left.right.parent.value)

        self.assertEqual(6, bst.origin.left.right.right.value)
        self.assertEqual(0, bst.origin.left.right.right.height)
        self.assertEqual(5, bst.origin.left.right.right.parent.value)

        self.assertEqual(9, bst.origin.right.value)
        self.assertEqual(1, bst.origin.right.height)
        self.assertEqual(7, bst.origin.right.parent.value)

        self.assertEqual(8, bst.origin.right.left.value)
        self.assertEqual(0, bst.origin.right.left.height)
        self.assertEqual(9, bst.origin.right.left.parent.value)

        self.assertEqual(10, bst.origin.right.right.value)
        self.assertEqual(0, bst.origin.right.right.height)
        self.assertEqual(9, bst.origin.right.right.parent.value)

    def test_search(self):

        # ensure empty tree is properly handled
        bst = BinarySearchTree()
        self.assertIsNone(bst.search(bst.origin, 0))

        """
        (1) search small basic tree
        tree structure
          1
         / \
        0   3
           / \
          2   4
        """
        bst = BinarySearchTree()
        numbers = [1, 0, 3, 2, 4]
        for num in numbers:
            bst.insert(bst.origin, num)
        # search existing numbers
        for num in numbers:
            node = bst.search(bst.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        # search non-existing numbers and ensure parent of where value would go is returned
        pairs = [(-1, 0), (0.5, 0), (5, 4), (2.5, 2),
                 (3.5, 4), (-1e5, 0), (1e5, 4)]
        for target, closest in pairs:
            node = bst.search(bst.origin, target)
            self.assertIsInstance(node, Node)
            self.assertEqual(closest, node.value)

        """(2) search large random tree"""
        random.seed(331)
        bst = BinarySearchTree()
        numbers = {random.randint(-1000, 1000) for _ in range(1000)}
        for num in numbers:
            bst.insert(bst.origin, num)
        for num in numbers:
            # search existing number
            node = bst.search(bst.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)

            # if this node is a leaf, search non-existing numbers around it
            # to ensure it is returned as the parent of where new insertions would go
            if node.left is None and node.right is None:
                node = bst.search(bst.origin, num + 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)
                node = bst.search(bst.origin, num - 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)


class AVLTreeTests(unittest.TestCase):

    def test_rotate(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.right_rotate(avl.origin))
        self.assertIsNone(avl.left_rotate(avl.origin))

        """
        (1) test basic right
        initial structure:
            3
           /
          2
         /
        1
        final structure:
          2
         / \
        1   3
        """
        avl.origin = Node(3)
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.size = 3

        node = avl.right_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        # root has no parent
        self.assertEqual(2, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        # root left value and parent
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)

        # left leaf should have no children
        self.assertIsNone(avl.origin.left.left)
        self.assertIsNone(avl.origin.left.right)

        # root right value and parent
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        # right leaf should have no children
        self.assertIsNone(avl.origin.right.right)
        self.assertIsNone(avl.origin.right.left)

        """
        (2) test basic left
        initial structure:
        1
         \
          2
           \
            3
        final structure:
          2
         / \
        1   3
        """
        avl = AVLTree()
        avl.origin = Node(1)
        avl.origin.right = Node(2, parent=avl.origin)
        avl.origin.right.right = Node(3, parent=avl.origin.right)
        avl.size = 3

        node = avl.left_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        # root has no parent
        self.assertEqual(2, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        # root left value and parent
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)

        # left leaf should have no children
        self.assertIsNone(avl.origin.left.left)
        self.assertIsNone(avl.origin.left.right)

        # root right value and parent
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        # right leaf should have no children
        self.assertIsNone(avl.origin.right.right)
        self.assertIsNone(avl.origin.right.left)

        """
        (3) test intermediate right, rotating at origin
        initial structure:
              7
             / \
            3   10
           / \
          2   4
         /
        1 
        final structure:
            3
           / \
          2   7
         /   / \
        1   4   10
        """
        avl = AVLTree()
        avl.origin = Node(7)
        avl.origin.left = Node(3, parent=avl.origin)
        avl.origin.left.left = Node(2, parent=avl.origin.left)
        avl.origin.left.left.left = Node(1, parent=avl.origin.left.left)
        avl.origin.left.right = Node(4, parent=avl.origin.left)
        avl.origin.right = Node(10, parent=avl.origin)

        node = avl.right_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)
        self.assertIsNone(avl.origin.left.right)

        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left)
        self.assertIsNone(avl.origin.left.left.right)

        self.assertEqual(7, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(avl.origin.right, avl.origin.right.left.parent)
        self.assertIsNone(avl.origin.right.left.left)
        self.assertIsNone(avl.origin.right.left.right)

        self.assertEqual(10, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)
        self.assertIsNone(avl.origin.right.right.right)

        """
        (4) test intermediate left, rotating at origin
        initial structure:
          7
         /  \
        3   10
           /   \
          9    11
                 \
                  12
        final structure:
        	10
           /  \
          7   11
         / \    \
        3   9    12
        """
        avl = AVLTree()
        avl.origin = Node(7)
        avl.origin.left = Node(3, parent=avl.origin)
        avl.origin.right = Node(10, parent=avl.origin)
        avl.origin.right.left = Node(9, parent=avl.origin.right)
        avl.origin.right.right = Node(11, parent=avl.origin.right)
        avl.origin.right.right.right = Node(12, parent=avl.origin.right.right)

        node = avl.left_rotate(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(10, node.value)

        self.assertEqual(10, avl.origin.value)
        self.assertIsNone(avl.origin.parent)
        # assert node10.value == 10 and not node10.parent

        self.assertEqual(7, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)
        # assert node7.value == 7 and node7.parent == node10

        self.assertEqual(3, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left)
        self.assertIsNone(avl.origin.left.left.right)
        # assert node3.value == 3 and node3.parent == node7 and not (
        #     node3.left or node3.right)

        self.assertEqual(9, avl.origin.left.right.value)
        self.assertEqual(avl.origin.left, avl.origin.left.right.parent)
        self.assertIsNone(avl.origin.left.right.left)
        self.assertIsNone(avl.origin.left.right.right)
        # assert node9.value == 9 and node9.parent == node7 and not (
        #     node9.left or node9.right)

        self.assertEqual(11, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)
        self.assertIsNone(avl.origin.right.left)
        # assert node11.value == 11 and node11.parent == node10 and not node11.left

        self.assertEqual(12, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)
        self.assertIsNone(avl.origin.right.right.right)
        # assert node12.value == 12 and node12.parent == node11 and not (
        #     node12.left or node12.right)

        """
        (5) test advanced right, rotating not at origin
        initial structure:
        		10
        	   /  \
        	  5	   11
        	 / \     \
        	3	7    12
           / \
          2   4
         /
        1
        final structure:
              10
             /  \
            3    11
           / \     \
          2   5     12
         /   / \
        1   4   7
        """
        avl = AVLTree()
        avl.origin = Node(10)
        avl.origin.right = Node(11, parent=avl.origin)
        avl.origin.right.right = Node(12, parent=avl.origin.right)
        avl.origin.left = Node(5, parent=avl.origin)
        avl.origin.left.right = Node(7, parent=avl.origin.left)
        avl.origin.left.left = Node(3, parent=avl.origin.left)
        avl.origin.left.left.right = Node(4, parent=avl.origin.left.left)
        avl.origin.left.left.left = Node(2, parent=avl.origin.left.left)
        avl.origin.left.left.left.left = Node(
            1, parent=avl.origin.left.left.left)

        node = avl.right_rotate(avl.origin.left)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(10, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        self.assertEqual(3, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)

        self.assertEqual(2, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.right)

        self.assertEqual(5, avl.origin.left.right.value)
        self.assertEqual(avl.origin.left, avl.origin.left.right.parent)

        self.assertEqual(1, avl.origin.left.left.left.value)
        self.assertEqual(avl.origin.left.left,
                         avl.origin.left.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left.left)
        self.assertIsNone(avl.origin.left.left.left.right)

        self.assertEqual(4, avl.origin.left.right.left.value)
        self.assertEqual(avl.origin.left.right,
                         avl.origin.left.right.left.parent)
        self.assertIsNone(avl.origin.left.right.left.left)
        self.assertIsNone(avl.origin.left.right.left.right)

        self.assertEqual(7, avl.origin.left.right.right.value)
        self.assertEqual(avl.origin.left.right,
                         avl.origin.left.right.right.parent)
        self.assertIsNone(avl.origin.left.right.right.left)
        self.assertIsNone(avl.origin.left.right.right.right)

        self.assertEqual(11, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)
        self.assertIsNone(avl.origin.right.left)

        self.assertEqual(12, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)
        self.assertIsNone(avl.origin.right.right.right)

        """
        (6) test advanced left, rotating not at origin
        initial structure:
        	3
           / \
          2   10
         /   /  \
        1   5   12
               /  \
              11   13
                     \
                      14
        final structure:
        	3
           / \
          2   12
         /   /  \
        1   10   13
           /  \    \
          5   11   14
        """
        avl = AVLTree()
        avl.origin = Node(3)
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.right = Node(10, parent=avl.origin)
        avl.origin.right.left = Node(5, parent=avl.origin.right)
        avl.origin.right.right = Node(12, parent=avl.origin.right)
        avl.origin.right.right.left = Node(11, parent=avl.origin.right.right)
        avl.origin.right.right.right = Node(13, parent=avl.origin.right.right)
        avl.origin.right.right.right.right = Node(
            14, parent=avl.origin.right.right.right)

        node = avl.left_rotate(avl.origin.right)
        self.assertIsInstance(node, Node)
        self.assertEqual(12, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertIsNone(avl.origin.parent)

        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(avl.origin, avl.origin.left.parent)
        self.assertIsNone(avl.origin.left.right)

        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(avl.origin.left, avl.origin.left.left.parent)
        self.assertIsNone(avl.origin.left.left.left)
        self.assertIsNone(avl.origin.left.left.right)

        self.assertEqual(12, avl.origin.right.value)
        self.assertEqual(avl.origin, avl.origin.right.parent)

        self.assertEqual(10, avl.origin.right.left.value)
        self.assertEqual(avl.origin.right, avl.origin.right.left.parent)

        self.assertEqual(5, avl.origin.right.left.left.value)
        self.assertEqual(avl.origin.right.left,
                         avl.origin.right.left.left.parent)
        self.assertIsNone(avl.origin.right.left.left.left)
        self.assertIsNone(avl.origin.right.left.left.right)

        self.assertEqual(11, avl.origin.right.left.right.value)
        self.assertEqual(avl.origin.right.left,
                         avl.origin.right.left.right.parent)
        self.assertIsNone(avl.origin.right.left.right.left)
        self.assertIsNone(avl.origin.right.left.right.right)

        self.assertEqual(13, avl.origin.right.right.value)
        self.assertEqual(avl.origin.right, avl.origin.right.right.parent)
        self.assertIsNone(avl.origin.right.right.left)

        self.assertEqual(14, avl.origin.right.right.right.value)
        self.assertEqual(avl.origin.right.right,
                         avl.origin.right.right.right.parent)
        self.assertIsNone(avl.origin.right.right.right.left)
        self.assertIsNone(avl.origin.right.right.right.right)

    def test_balance_factor(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertEqual(0, avl.balance_factor(avl.origin))

        """
        (1) test on balanced tree
        structure:
          2
         / \
        1   3
        """
        avl.origin = Node(2)
        avl.origin.height = 1
        avl.origin.left = Node(1, parent=avl.origin)
        avl.origin.left.height = 0
        avl.origin.right = Node(3, parent=avl.origin)
        avl.origin.right.height = 0
        avl.size = 3

        self.assertEqual(0, avl.balance_factor(avl.origin))
        self.assertEqual(0, avl.balance_factor(avl.origin.left))
        self.assertEqual(0, avl.balance_factor(avl.origin.right))

        """
        (2) test on unbalanced left
        structure:
            3
           /
          2
         /
        1
        """
        avl = AVLTree()
        avl.origin = Node(3)
        avl.origin.height = 2
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.height = 1
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.left.left.height = 0
        avl.size = 3

        self.assertEqual(2, avl.balance_factor(avl.origin))
        self.assertEqual(1, avl.balance_factor(avl.origin.left))
        self.assertEqual(0, avl.balance_factor(avl.origin.left.left))

        """
        (2) test on unbalanced right
        structure:
        1
         \
          2
           \
            3
        """
        avl = AVLTree()
        avl.origin = Node(1)
        avl.origin.height = 2
        avl.origin.right = Node(2, parent=avl.origin)
        avl.origin.right.height = 1
        avl.origin.right.right = Node(3, parent=avl.origin.right)
        avl.origin.right.right.height = 0
        avl.size = 3

        self.assertEqual(-2, avl.balance_factor(avl.origin))
        self.assertEqual(-1, avl.balance_factor(avl.origin.right))
        self.assertEqual(0, avl.balance_factor(avl.origin.right.right))

    def test_rebalance(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.rebalance(avl.origin))

        """
        (1) test balanced tree (do nothing)
        initial and final structure:
          2
         / \
        1   3
        since pointers are already tested in rotation testcase, only check values and heights
        """
        avl.origin = Node(2)
        avl.origin.height = 1
        avl.origin.left = Node(1, parent=avl.origin)
        avl.origin.left.height = 0
        avl.origin.right = Node(3, parent=avl.origin)
        avl.origin.right.height = 0
        avl.size = 3

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        self.assertEqual(2, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (2) test left-left rebalance
        initial structure:
            4
           /
          2
         / \
        1   3
        final structure:
          2
         / \
        1   4
           /
          3
        """
        avl = AVLTree()
        avl.origin = Node(4)
        avl.origin.height = 2
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.height = 1
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.left.left.height = 0
        avl.origin.left.right = Node(3, parent=avl.origin.left)
        avl.origin.left.right.height = 0
        avl.size = 4

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(2, node.value)

        self.assertEqual(2, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(3, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)

        """
        (2) test right-right rebalance
        initial structure:
        1
         \
          3
         /  \
        2    4
        final structure:
          3
         / \
        1   4
         \
          2
        """
        avl = AVLTree()
        avl.origin = Node(1)
        avl.origin.height = 2
        avl.origin.right = Node(3, parent=avl.origin)
        avl.origin.right.height = 1
        avl.origin.right.right = Node(4, parent=avl.origin.right)
        avl.origin.right.right.height = 0
        avl.origin.right.left = Node(2, parent=avl.origin.right)
        avl.origin.right.left.height = 0
        avl.size = 4

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)
        self.assertEqual(2, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)

        """
        (4) test left-right rebalance
        initial structure:
            5
           / \
          2   6
         / \
        1   3
             \
              4
        intermediate structure:
              5
             / \
            3   6
           / \
          2   4
         /
        1
        final structure:
            3 
           / \
          2   5
         /   / \
        1   4   6
        """
        avl = AVLTree()
        avl.origin = Node(5)
        avl.origin.height = 3
        avl.origin.left = Node(2, parent=avl.origin)
        avl.origin.left.height = 2
        avl.origin.right = Node(6, parent=avl.origin)
        avl.origin.right.height = 0
        avl.origin.left.left = Node(1, parent=avl.origin.left)
        avl.origin.left.left.height = 0
        avl.origin.left.right = Node(3, parent=avl.origin.left)
        avl.origin.left.right.height = 1
        avl.origin.left.right.right = Node(4, parent=avl.origin.left.right)
        avl.origin.left.right.right.height = 0

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(3, node.value)

        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (5) test right-left rebalance
        initial structure:
          2
         / \
        1   5
           / \
          4   6
         /
        3
        intermediate structure:
          2
         / \
        1   4
           / \
          3   5
               \
                6
        final structure:
            4 
           / \
          2   5
         / \   \
        1   3   6
        """
        avl = AVLTree()
        avl.origin = Node(2)
        avl.origin.height = 3
        avl.origin.left = Node(1, parent=avl.origin)
        avl.origin.left.height = 0
        avl.origin.right = Node(5, parent=avl.origin)
        avl.origin.right.height = 2
        avl.origin.right.left = Node(4, parent=avl.origin.right)
        avl.origin.right.left.height = 1
        avl.origin.right.right = Node(6, parent=avl.origin.right)
        avl.origin.right.right.height = 0
        avl.origin.right.left.left = Node(3, parent=avl.origin.right.left)
        avl.origin.right.left.left.height = 0

        node = avl.rebalance(avl.origin)
        self.assertIsInstance(node, Node)
        self.assertEqual(4, node.value)

        self.assertEqual(4, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(3, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

    def test_insert(self):

        # visualize this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        avl = AVLTree()
        """
        (1) test insertion causing right-right rotation
        final structure
          1
         / \
        0   3
           / \
          2   4
        """
        for value in range(5):
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)

        self.assertEqual(5, avl.size)
        self.assertEqual(1, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(0, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(2, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(4, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (2) test insertion causing left-left rotation
        final structure
            3
           / \
          1   4
         / \
        0   2
        """
        avl = AVLTree()
        for value in range(4, -1, -1):
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)
        self.assertEqual(5, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)
        self.assertEqual(0, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(2, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)

        """
        (3) test insertion (with duplicates) causing left-right rotation
        initial structure:
            5
           / \
          2   6
         / \
        1   3
             \
              4
        final structure:
            3 
           / \
          2   5
         /   / \
        1   4   6
        """
        avl = AVLTree()
        for value in [5, 2, 6, 1, 3] * 2 + [4]:
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (4) test insertion (with duplicates) causing right-left rotation
        initial structure:
          2
         / \
        1   5
           / \
          4   6
         /
        3
        final structure:
            4 
           / \
          2   5
         / \   \
        1   3   6
        """
        avl = AVLTree()
        for value in [2, 1, 5, 4, 6] * 2 + [3]:
            node = avl.insert(avl.origin, value)
            self.assertIsInstance(node, Node)
        self.assertEqual(4, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(1, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(3, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)
        self.assertEqual(6, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

    def test_remove(self):

        # visualize this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.remove(avl.origin, 0))

        """
        (1) test removal causing right-right rotation
        initial structure:
            2
           / \
          1   3
         /     \
        0       4
        final structure (removing 1, 0):
          3 
         / \
        2   4
        """
        avl = AVLTree()
        for value in [2, 1, 3, 0, 4]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 1)  # one child removal
        self.assertEqual(0, avl.origin.left.value)

        avl.remove(avl.origin, 0)  # zero child removal, will need rebalancing
        self.assertEqual(3, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(4, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (2) test removal causing left-left rotation
        initial structure:
            3
           / \
          2   4
         /     \
        1       5
        final structure (removing 4, 5):
          2 
         / \
        1   3
        """
        avl = AVLTree()
        for value in [3, 2, 4, 1, 5]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 4)  # one child removal
        self.assertEqual(5, avl.origin.right.value)

        avl.remove(avl.origin, 5)  # zero child removal, will need rebalancing
        self.assertEqual(3, avl.size)
        self.assertEqual(2, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (3) test removal causing left-right rotation
        initial structure:
              5
             / \
            2   6
           / \   \
          1   3   7
         /     \
        0       4
        final structure (removing 1, 6):
            3 
           / \
          2   5
         /   / \
        0   4   7
        """
        avl = AVLTree()
        for value in [5, 2, 6, 1, 3, 7, 0, 4]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 1)  # one child removal
        self.assertEqual(0, avl.origin.left.left.value)

        avl.remove(avl.origin, 6)  # one child removal, will need rebalancing

        self.assertEqual(6, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(0, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(4, avl.origin.right.left.value)
        self.assertEqual(0, avl.origin.right.left.height)
        self.assertEqual(7, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

        """
        (4) test removal causing right-left rotation
        initial structure:
            2
           / \
          1   5
         /   / \
        0   4   6
           /     \
          3       7
        final structure (removing 6, 1):
            4 
           / \
          2   5
         / \   \
        0   3   7
        """
        avl = AVLTree()
        for value in [2, 1, 5, 0, 4, 6, 3, 7]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 6)  # one child removal
        self.assertEqual(7, avl.origin.right.right.value)

        avl.remove(avl.origin, 1)  # one child removal, will need rebalancing
        self.assertEqual(6, avl.size)
        self.assertEqual(4, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(2, avl.origin.left.value)
        self.assertEqual(1, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(7, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)
        self.assertEqual(0, avl.origin.left.left.value)
        self.assertEqual(0, avl.origin.left.left.height)
        self.assertEqual(3, avl.origin.left.right.value)
        self.assertEqual(0, avl.origin.left.right.height)

        """
        (5) test simple 2-child removal
        initial structure:
          2
         / \
        1   3
        final structure (removing 2):
         1 
          \
           3
        """
        avl = AVLTree()
        for value in [2, 1, 3]:
            avl.insert(avl.origin, value)
        avl.remove(avl.origin, 2)  # two child removal
        self.assertEqual(2, avl.size)
        self.assertEqual(1, avl.origin.value)
        self.assertEqual(1, avl.origin.height)
        self.assertEqual(3, avl.origin.right.value)
        self.assertEqual(0, avl.origin.right.height)

        """
        (5) test compounded 2-child removal
        initial structure:
              4
           /     \
          2       6
         / \     / \
        1   3   5   7
        intermediate structure (removing 2, 6):
            4
           / \
          1   5
           \   \
            3   7
        final structure (removing 4)
            3
           / \
          1   5
               \
                7        
        """
        avl = AVLTree()
        for value in [4, 2, 6, 1, 3, 5, 7]:
            avl.insert(avl.origin, value)

        avl.remove(avl.origin, 2)  # two child removal
        self.assertEqual(1, avl.origin.left.value)

        avl.remove(avl.origin, 6)  # two child removal
        self.assertEqual(5, avl.origin.right.value)

        avl.remove(avl.origin, 4)  # two child removal
        self.assertEqual(4, avl.size)
        self.assertEqual(3, avl.origin.value)
        self.assertEqual(2, avl.origin.height)
        self.assertEqual(1, avl.origin.left.value)
        self.assertEqual(0, avl.origin.left.height)
        self.assertEqual(5, avl.origin.right.value)
        self.assertEqual(1, avl.origin.right.height)
        self.assertEqual(7, avl.origin.right.right.value)
        self.assertEqual(0, avl.origin.right.right.height)

    def test_min(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.min(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        min_node = avl.min(avl.origin)
        self.assertIsInstance(min_node, Node)
        self.assertEqual(0, min_node.value)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-100, 101):
            avl.insert(avl.origin, i)
        min_node = avl.min(avl.origin)
        self.assertIsInstance(min_node, Node)
        self.assertEqual(-100, min_node.value)

        """(3) large random tree"""
        random.seed(331)
        avl = AVLTree()
        numbers = [random.randint(-1000, 1000) for _ in range(1000)]
        for num in numbers:
            avl.insert(avl.origin, num)
        min_node = avl.min(avl.origin)
        self.assertIsInstance(min_node, Node)
        self.assertEqual(min(numbers), min_node.value)

    def test_max(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.max(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        max_node = avl.max(avl.origin)
        self.assertIsInstance(max_node, Node)
        self.assertEqual(9, max_node.value)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-100, 101):
            avl.insert(avl.origin, i)
        max_node = avl.max(avl.origin)
        self.assertIsInstance(max_node, Node)
        self.assertEqual(100, max_node.value)

        """(3) large random tree"""
        random.seed(331)
        avl = AVLTree()
        numbers = [random.randint(-1000, 1000) for _ in range(1000)]
        for num in numbers:
            avl.insert(avl.origin, num)
        max_node = avl.max(avl.origin)
        self.assertIsInstance(max_node, Node)
        self.assertEqual(max(numbers), max_node.value)

    def test_search(self):

        # ensure empty tree is properly handled
        avl = AVLTree()
        self.assertIsNone(avl.search(avl.origin, 0))

        """
        (1) search small basic tree
        tree structure
          1
         / \
        0   3
           / \
          2   4
        """
        avl = AVLTree()
        numbers = [1, 0, 3, 2, 4]
        for num in numbers:
            avl.insert(avl.origin, num)
        # search existing numbers
        for num in numbers:
            node = avl.search(avl.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        # search non-existing numbers and ensure parent of where value would go is returned
        pairs = [(-1, 0), (0.5, 0), (5, 4), (2.5, 2),
                 (3.5, 4), (-1e5, 0), (1e5, 4)]
        for target, closest in pairs:
            node = avl.search(avl.origin, target)
            self.assertIsInstance(node, Node)
            self.assertEqual(closest, node.value)

        """(2) search large random tree"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(1000)}
        for num in numbers:
            avl.insert(avl.origin, num)
        for num in numbers:
            # search existing number
            node = avl.search(avl.origin, num)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)

            # if this node is a leaf, search non-existing numbers around it
            # to ensure it is returned as the parent of where new insertions would go
            if node.left is None and node.right is None:
                node = avl.search(avl.origin, num + 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)
                node = avl.search(avl.origin, num - 0.1)
                self.assertIsInstance(node, Node)
                self.assertEqual(num, node.value)

    def test_inorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.inorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.inorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = list(range(10))
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-100, 101):
            avl.insert(avl.origin, i)
        generator = avl.inorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = list(range(-100, 101))
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.inorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = sorted(numbers)
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(4) Testing tree is iterable. Hint: Implement the __iter__ function."""
        for expected_val, actual in zip(expected, avl):
            self.assertEqual(expected_val, actual.value)

    def test_preorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.preorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.preorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [3, 1, 0, 2, 7, 5, 4, 6, 8, 9]
        # avl.visualize("test2.svg")
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-20, 21):
            avl.insert(avl.origin, i)
        generator = avl.preorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-5, -13, -17, -19, -20, -18, -15, -16, -14, -9, -11,
                    -12, -10, -7, -8, -6, 11, 3, -1, -3, -4, -2, 1, 0, 2,
                    7, 5, 4, 6, 9, 8, 10, 15, 13, 12, 14, 17, 16, 19, 18,
                    20]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.preorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [527, 33, -493, -834, -933, -954, -918, -655, -720,
                    -789, -705, -650, -529, -165, -343, -422, -434,
                    -359, -312, -324, -269, -113, -142, -148, -116, -43,
                    -89, -26, 327, 220, 108, 77, 44, 101, 193, 113,
                    194, 274, 251, 224, 268, 294, 283, 316, 454, 362, 358,
                    333, 360, 431, 411, 446, 486, 485, 498, 503,
                    711, 574, 565, 529, 571, 675, 641, 687, 832, 776, 733,
                    720, 775, 784, 782, 802, 914, 860, 843, 888,
                    966, 944, 975]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

    def test_postorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.postorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.postorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [0, 2, 1, 4, 6, 5, 9, 8, 7, 3]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-20, 20):
            avl.insert(avl.origin, i)
        generator = avl.postorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-20, -18, -19, -16, -14, -15, -17, -12, -10, -11, -8, -6, -7, -9,
                    -13, -4, -2, -3, 0, 2, 1, -1, 4, 6, 5, 8, 10, 9, 7, 3, 12, 14, 13,
                    16, 19, 18, 17, 15, 11, -5]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.postorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-954, -918, -933, -789, -705, -720, -529, -650, -655, -834, -434, -359, -422, -324, -269, -312,
                    -343, -148, -116, -142, -89, -26, -43, -113, -
                    165, -493, 44, 101, 77, 113, 194, 193, 108, 224,
                    268, 251, 283, 316, 294, 274, 220, 333, 360, 358, 411, 446, 431, 362, 485, 503, 498, 486, 454,
                    327, 33, 529, 571, 565, 641, 687, 675, 574, 720, 775, 733, 782, 802, 784, 776, 843, 888, 860,
                    944, 975, 966, 914, 832, 711, 527]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

    def test_levelorder(self):

        # note: Python generators will raise a StopIteration exception when there are no items
        # left to yield, and we test for this exception to ensure each traversal yields the correct
        # number of items: https://docs.python.org/3/library/exceptions.html#StopIteration

        # ensure empty tree is properly handled and returns a StopIteration
        avl = AVLTree()
        with self.assertRaises(StopIteration):
            next(avl.levelorder(avl.origin))

        """(1) small sequential tree"""
        for i in range(10):
            avl.insert(avl.origin, i)
        generator = avl.levelorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [3, 1, 7, 0, 2, 5, 8, 4, 6, 9]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(2) large sequential tree"""
        avl = AVLTree()
        for i in range(-20, 20):
            avl.insert(avl.origin, i)
        generator = avl.levelorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [-5, -13, 11, -17, -9, 3, 15, -19, -15, -11, -7, -1, 7, 13, 17, -20, -18,
                    -16, -14, -12, -10, -8, -6, -3, 1, 5, 9, 12, 14, 16, 18, -4, -2, 0, 2,
                    4, 6, 8, 10, 19]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

        """(3) large random tree of unique numbers"""
        random.seed(331)
        avl = AVLTree()
        numbers = {random.randint(-1000, 1000) for _ in range(80)}
        for num in numbers:
            avl.insert(avl.origin, num)
        generator = avl.levelorder(avl.origin)
        self.assertIsInstance(generator, types.GeneratorType)
        expected = [527, 33, 711, -493, 327, 574, 832, -834, -165, 220, 454,
                    565, 675, 776, 914, -933, -655, -343, -113, 108, 274,
                    362, 486, 529, 571, 641, 687, 733, 784, 860, 966, -954,
                    -918, -720, -650, -422, -312, -142, -43, 77, 193, 251,
                    294, 358, 431, 485, 498, 720, 775, 782, 802, 843, 888,
                    944, 975, -789, -705, -529, -434, -359, -324, -269, -148,
                    -116, -89, -26, 44, 101, 113, 194, 224, 268, 283, 316, 333,
                    360, 411, 446, 503]
        for num in expected:
            node = next(generator)
            self.assertIsInstance(node, Node)
            self.assertEqual(num, node.value)
        with self.assertRaises(StopIteration):
            next(generator)

    def test_AVL_comprehensive(self):

        # visualize some of test in this testcase with https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
        # ensure empty tree is properly handled
        """
        First part, inserting and removing without rotation

        insert without any rotation (inserting 5, 0, 10):
          5
         / \
        1   10
        """

        def check_node_properties(current: Node, value: int = 0, height: int = 0, balance: int = 0):
            if value is None:
                self.assertIsNone(current)
                return
            self.assertEqual(value, current.value)
            self.assertEqual(height, current.height)
            self.assertEqual(balance, avl.balance_factor(current))

        avl = AVLTree()
        avl.insert(avl.origin, 5)
        avl.insert(avl.origin, 1)
        avl.insert(avl.origin, 10)
        self.assertEqual(3, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=5, height=1, balance=0)
        check_node_properties(avl.origin.left, value=1, height=0, balance=0)
        check_node_properties(avl.origin.right, value=10, height=0, balance=0)
        """
        Current AVL tree:
          5
         / \
        1   10
        After Removing 5:
          1
           \
            10
        """
        avl.remove(avl.origin, 5)
        self.assertEqual(2, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=1, height=1, balance=-1)
        check_node_properties(avl.origin.left, value=None)
        check_node_properties(avl.origin.right, value=10, height=0, balance=0)
        """
        Current AVL tree:
          1
            \
            10
        After inserting 0, 20:
          1
         /  \
        0   10
              \
               20
        """
        avl.insert(avl.origin, 0)
        avl.insert(avl.origin, 20)
        self.assertEqual(4, avl.size)
        self.assertEqual(0, avl.min(avl.origin).value)
        self.assertEqual(20, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=1, height=2, balance=-1)
        check_node_properties(avl.origin.left, value=0, height=0, balance=0)
        check_node_properties(avl.origin.right, value=10, height=1, balance=-1)
        check_node_properties(avl.origin.right.right,
                              value=20, height=0, balance=0)

        """
        Current AVL tree:
          1
         /  \
        0   10
              \
               20
        After removing 20, inserting -20 and inserting 5
             1
            /  \
           0   10
          /   /
        -20  5
        """
        avl.remove(avl.origin, 20)
        avl.insert(avl.origin, -20)
        avl.insert(avl.origin, 5)
        self.assertEqual(5, avl.size)
        self.assertEqual(-20, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=1, height=2, balance=0)
        check_node_properties(avl.origin.left, value=0, height=1, balance=1)
        check_node_properties(avl.origin.left.left,
                              value=-20, height=0, balance=0)
        check_node_properties(avl.origin.right, value=10, height=1, balance=1)
        check_node_properties(avl.origin.right.left,
                              value=5, height=0, balance=0)

        """
        Second part, inserting and removing with rotation

        inserting 5, 10:
          5
           \
            10
        """
        avl = AVLTree()
        avl.insert(avl.origin, 5)
        avl.insert(avl.origin, 10)
        self.assertEqual(2, avl.size)
        self.assertEqual(5, avl.min(avl.origin).value)
        self.assertEqual(10, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=5, height=1, balance=-1)
        check_node_properties(avl.origin.right, value=10, height=0, balance=0)
        """
        Current AVL tree:
          5
           \
            10
        After inserting 8, 9, 12
           8
         /   \
        5    10
            /  \
           9   12
        """
        avl.insert(avl.origin, 8)
        avl.insert(avl.origin, 9)
        avl.insert(avl.origin, 12)
        self.assertEqual(5, avl.size)
        self.assertEqual(5, avl.min(avl.origin).value)
        self.assertEqual(12, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=2, balance=-1)
        check_node_properties(avl.origin.right, value=10, height=1, balance=0)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.left, value=5, height=0, balance=0)

        """
        Current AVL tree:
           8
         /   \
        5    10
            /  \
           9   12
        After inserting 3, 1, 2
               8
           /       \
          3        10
         /  \     /   \
        1    5   9    12
          \
           2
        """
        avl.insert(avl.origin, 3)
        avl.insert(avl.origin, 1)
        avl.insert(avl.origin, 2)
        self.assertEqual(8, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(12, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=3, balance=1)
        check_node_properties(avl.origin.right, value=10, height=1, balance=0)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.left, value=3, height=2, balance=1)
        check_node_properties(avl.origin.left.left,
                              value=1, height=1, balance=-1)
        check_node_properties(avl.origin.left.left.right,
                              value=2, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=5, height=0, balance=0)
        """
        Current AVL tree:
               8
           /       \
          3        10
         /  \     /   \
        1    5   9    12
          \
           2
        After removing 5
               8
           /       \
          2        10
         /  \     /   \
        1    3   9    12
        """
        avl.remove(avl.origin, 5)
        self.assertEqual(7, avl.size)
        self.assertEqual(1, avl.min(avl.origin).value)
        self.assertEqual(12, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=2, balance=0)
        check_node_properties(avl.origin.right, value=10, height=1, balance=0)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.left, value=2, height=1, balance=0)
        check_node_properties(avl.origin.left.left,
                              value=1, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=3, height=0, balance=0)
        """
        Current AVL tree:
              8
           /     \
          2      10
         /  \   /   \
        1    3 9    12
        After inserting 5, 13, 0, 7, 20
               8
            /       \
           2         10
          /  \      /   \
         1    5     9    13
        /    / \        /  \
        0   3   7     12    20
        """
        avl.insert(avl.origin, 5)
        avl.insert(avl.origin, 13)
        avl.insert(avl.origin, 0)
        avl.insert(avl.origin, 7)
        avl.insert(avl.origin, 20)
        self.assertEqual(12, avl.size)
        self.assertEqual(0, avl.min(avl.origin).value)
        self.assertEqual(20, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=3, balance=0)

        check_node_properties(avl.origin.right, value=10, height=2, balance=-1)
        check_node_properties(avl.origin.right.left,
                              value=9, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=13, height=1, balance=0)
        check_node_properties(avl.origin.right.right.right,
                              value=20, height=0, balance=0)
        check_node_properties(avl.origin.right.right.left,
                              value=12, height=0, balance=0)

        check_node_properties(avl.origin.left, value=2, height=2, balance=0)
        check_node_properties(avl.origin.left.left,
                              value=1, height=1, balance=1)
        check_node_properties(avl.origin.left.left.left,
                              value=0, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=5, height=1, balance=-0)
        check_node_properties(avl.origin.left.right.right,
                              value=7, height=0, balance=0)
        check_node_properties(avl.origin.left.right.left,
                              value=3, height=0, balance=0)

        """
        Current AVL tree:
               8
            /       \
           2         10
          /  \      /   \
         1    5     9    13
        /    / \        /  \
        0   3   7     12    20
        After removing 1, 9
               8
            /       \
           2         13
          /  \      /   \
         0    5   10     20
             / \     \    
             3   7    12
        """
        avl.remove(avl.origin, 1)
        avl.remove(avl.origin, 9)
        self.assertEqual(10, avl.size)
        self.assertEqual(0, avl.min(avl.origin).value)
        self.assertEqual(20, avl.max(avl.origin).value)
        # Properties of all nodes
        check_node_properties(avl.origin, value=8, height=3, balance=0)

        check_node_properties(avl.origin.right, value=13, height=2, balance=1)
        check_node_properties(avl.origin.right.left,
                              value=10, height=1, balance=-1)
        check_node_properties(avl.origin.right.left.right,
                              value=12, height=0, balance=0)
        check_node_properties(avl.origin.right.right,
                              value=20, height=0, balance=0)

        check_node_properties(avl.origin.left, value=2, height=2, balance=-1)
        check_node_properties(avl.origin.left.left,
                              value=0, height=0, balance=0)
        check_node_properties(avl.origin.left.right,
                              value=5, height=1, balance=-0)
        check_node_properties(avl.origin.left.right.right,
                              value=7, height=0, balance=0)
        check_node_properties(avl.origin.left.right.left,
                              value=3, height=0, balance=0)

        """
        Part Three
        Everything but random, checking properties of tree only
        """
        random.seed(331)
        """
        randomly insert, and remove alphabet to avl tree
        """

        # def random_order_1(character=True):
        #     order = random.randint(0, 2)
        #     if not len(existing_value) or (order and (not character or avl.size < 26)):
        #         if character:
        #             inserted = chr(ord('a') + random.randint(0, 25))
        #             while inserted in existing_value:
        #                 inserted = chr(ord('a') + random.randint(0, 25))
        #         else:
        #             inserted = random.randint(0, 100000)
        #         avl.insert(avl.origin, inserted)
        #         existing_value[inserted] = 1
        #     else:
        #         removed = random.choice(list(existing_value.keys()))
        #         avl.remove(avl.origin, removed)
        #         existing_value.pop(removed)
        #
        # existing_value = {}
        # avl = AVLTree()
        # for _ in range(30):
        #     random_order_1()
        # self.assertEqual('a', avl.min(avl.origin).value)
        # self.assertEqual('y', avl.max(avl.origin).value)
        # # inorder test
        # expected = ['a', 'b', 'd', 'f', 'g', 'i', 'k',
        #             'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y']
        # generator = avl.inorder(avl.origin)
        # self.assertIsInstance(generator, types.GeneratorType)
        # for num in expected:
        #     node = next(generator)
        #     self.assertIsInstance(node, Node)
        #     self.assertEqual(num, node.value)
        # with self.assertRaises(StopIteration):
        #     next(generator)
        #
        # expected = ['p', 'f', 'b', 'a', 'd', 'k', 'i',
        #             'g', 'o', 't', 'r', 'q', 's', 'w', 'v', 'y']
        # generator = avl.preorder(avl.origin)
        # self.assertIsInstance(generator, types.GeneratorType)
        # for num in expected:
        #     node = next(generator)
        #     self.assertIsInstance(node, Node)
        #     self.assertEqual(num, node.value)
        # with self.assertRaises(StopIteration):
        #     next(generator)
        #
        # expected = ['a', 'd', 'b', 'g', 'i', 'o', 'k',
        #             'f', 'q', 's', 'r', 'v', 'y', 'w', 't', 'p']
        # generator = avl.postorder(avl.origin)
        # self.assertIsInstance(generator, types.GeneratorType)
        # for num in expected:
        #     node = next(generator)
        #     self.assertIsInstance(node, Node)
        #     self.assertEqual(num, node.value)
        # with self.assertRaises(StopIteration):
        #     next(generator)
        #
        # existing_value.clear()
        # avl = AVLTree()
        # for _ in range(150):
        #     random_order_1(character=False)
        # self.assertEqual(3113, avl.min(avl.origin).value)
        # self.assertEqual(99254, avl.max(avl.origin).value)
        # # inorder test
        # expected = [3113, 4842, 8476, 9661, 9691, 9849, 12004, 13818, 16748, 19125,
        #             20633, 20815, 20930, 25633, 25790, 28476, 29509, 30303, 30522,
        #             32151, 32253, 35293, 35691, 36623, 37047, 40980, 41185, 42559,
        #             43298, 44521, 44698, 45027, 46070, 46204, 46876, 49122, 51761,
        #             51864, 54480, 55579, 56007, 56230, 58594, 59094, 59240, 59245,
        #             61029, 61837, 63796, 66866, 69402, 69498, 70575, 70733, 74185,
        #             74291, 74893, 76608, 76840, 77762, 78162, 78215, 80089, 80883,
        #             85118, 86927, 88662, 91673, 94661, 94848, 98575, 99254]
        #
        # generator = avl.inorder(avl.origin)
        # self.assertIsInstance(generator, types.GeneratorType)
        # for num in expected:
        #     node = next(generator)
        #     self.assertIsInstance(node, Node)
        #     self.assertEqual(num, node.value)
        # with self.assertRaises(StopIteration):
        #     next(generator)
        #
        # expected = [49122, 35691, 20815, 9849, 4842, 3113, 9661, 8476, 9691, 19125,
        #             13818, 12004, 16748, 20633, 30303, 25790, 20930, 25633, 29509,
        #             28476, 32253, 30522, 32151, 35293, 43298, 37047, 36623, 41185,
        #             40980, 42559, 46070, 44698, 44521, 45027, 46204, 46876, 69498,
        #             58594, 54480, 51761, 51864, 56007, 55579, 56230, 59245, 59240,
        #             59094, 61837, 61029, 66866, 63796, 69402, 80883, 76840, 74185,
        #             70575, 70733, 74893, 74291, 76608, 78162, 77762, 80089, 78215,
        #             91673, 86927, 85118, 88662, 94848, 94661, 99254, 98575]
        #
        # generator = avl.preorder(avl.origin)
        # self.assertIsInstance(generator, types.GeneratorType)
        # for num in expected:
        #     node = next(generator)
        #     self.assertIsInstance(node, Node)
        #     self.assertEqual(num, node.value)
        # with self.assertRaises(StopIteration):
        #     next(generator)
        #
        # expected = [3113, 8476, 9691, 9661, 4842, 12004, 16748, 13818,
        #             20633, 19125, 9849, 25633, 20930, 28476, 29509,
        #             25790, 32151, 30522, 35293, 32253, 30303, 20815,
        #             36623, 40980, 42559, 41185, 37047, 44521, 45027,
        #             44698, 46876, 46204, 46070, 43298, 35691, 51864,
        #             51761, 55579, 56230, 56007, 54480, 59094, 59240,
        #             61029, 63796, 69402, 66866, 61837, 59245, 58594,
        #             70733, 70575, 74291, 76608, 74893, 74185, 77762,
        #             78215, 80089, 78162, 76840, 85118, 88662, 86927,
        #             94661, 98575, 99254, 94848, 91673, 80883, 69498, 49122]
        #
        # generator = avl.postorder(avl.origin)
        # self.assertIsInstance(generator, types.GeneratorType)
        # for num in expected:
        #     node = next(generator)
        #     self.assertIsInstance(node, Node)
        #     self.assertEqual(num, node.value)
        # with self.assertRaises(StopIteration):
        #     next(generator)



class StocksAVLTests(unittest.TestCase):
    def test_simple_pruning(self):
        def make_avl_a_binary_tree(avl_node: AVLTree, bst: BinarySearchTree, avl: AVLTree):
            if avl_node is not None:
                bst.insert(bst.origin,avl_node.value)
                make_avl_a_binary_tree(avl_node.left, bst, avl)
                make_avl_a_binary_tree(avl_node.right, bst, avl)
            return bst
        stocks_data = [
            {"ticker": "AAPL", "name": "Apple Inc.", "price": 150.50, "pe_ratio": 0.253,
             "market_cap": 2000000000000, "div_yield": 1.5},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "price": 2800.00, "pe_ratio": 0.307,
             "market_cap": 1800000000000, "div_yield": 0.8},
            {"ticker": "MSFT", "name": "Microsoft Corporation", "price": 320.75, "pe_ratio": 0.285,
             "market_cap": 2200000000000, "div_yield": 1.2},
            {"ticker": "INTC", "name": "Intel Corporation", "price": 50.25, "pe_ratio": 0.158,
             "market_cap": 1500000000000, "div_yield": 2.0},
            {"ticker": "CSCO", "name": "Cisco Systems Inc.", "price": 55.50, "pe_ratio": 0.202,
             "market_cap": 1600000000000, "div_yield": 1.8},
            {"ticker": "ORCL", "name": "Oracle Corporation", "price": 85.75, "pe_ratio": 0.183,
             "market_cap": 1900000000000, "div_yield": 1.0},
            {"ticker": "IBM", "name": "International Business Machines Corporation", "price": 120.00,
             "pe_ratio": 0.146, "market_cap": 1200000000000, "div_yield": 2.5},
            {"ticker": "HPQ", "name": "HP Inc.", "price": 30.50, "pe_ratio": 0.127, "market_cap": 800000000000,
             "div_yield": 3.0},
            {"ticker": "DELL", "name": "Dell Technologies Inc.", "price": 70.00, "pe_ratio": 0.221,
             "market_cap": 1000000000000, "div_yield": 1.5},
            {"ticker": "AMD", "name": "Advanced Micro Devices Inc.", "price": 120.25, "pe_ratio": 0.356,
             "market_cap": 900000000000, "div_yield": 0.7},
        ]

        # If you want to print the tree, uncomment the following lines
        # bst = BinarySearchTree()
        # bst = make_avl_a_binary_tree(stock_tree.origin, bst, stock_tree)
        # print(bst)
        """ (1) Prune with 0.35 as the threshold"""
        stock_tree = build_tree_with_stocks(stocks_data)
        prune(stock_tree, 0.35)

        self.assertEqual(make_stock_from_dictionary(stocks_data[9]), stock_tree.origin.value)
        self.assertEqual(1, stock_tree.size)

        """ (2) Prune with 0.15 as the threshold"""
        stock_tree = build_tree_with_stocks(stocks_data)
        prune(stock_tree, 0.15)


        # CSCO ticker should be origin root
        self.assertEqual(make_stock_from_dictionary(stocks_data[4]), stock_tree.origin.value)
        # Left root should be INTC
        self.assertEqual(make_stock_from_dictionary(stocks_data[3]), stock_tree.origin.left.value)
        # Left of INTC should be None
        self.assertIsNone(stock_tree.origin.left.left)
        # Right of INTC should be ORCL
        self.assertEqual(make_stock_from_dictionary(stocks_data[5]), stock_tree.origin.left.right.value)
        # Right root should be MSFT
        self.assertEqual(make_stock_from_dictionary(stocks_data[2]), stock_tree.origin.right.value)
        # Left of MSFT should be AAPL
        self.assertEqual(make_stock_from_dictionary(stocks_data[0]), stock_tree.origin.right.left.value)
        # Right of MSFT should be GOOGL
        self.assertEqual(make_stock_from_dictionary(stocks_data[1]), stock_tree.origin.right.right.value)
        # Left of GOOGL should be None
        self.assertIsNone(stock_tree.origin.right.right.left)
        # Right of GOOGL should be AMD
        self.assertEqual(make_stock_from_dictionary(stocks_data[9]), stock_tree.origin.right.right.right.value)
        # Size should be 8
        self.assertEqual(8, stock_tree.size)

        """ (3) Prune with 0.30 as the threshold"""
        stock_tree = build_tree_with_stocks(stocks_data)
        prune(stock_tree, 0.30)

        self.assertEqual(make_stock_from_dictionary((stocks_data[1])), stock_tree.origin.value) #Origin
        self.assertEqual(make_stock_from_dictionary((stocks_data[9])), stock_tree.origin.right.value) #Right
        self.assertEqual(2, stock_tree.size)

        """ (4) Prune with 0.25 as the threshold"""
        stock_tree = build_tree_with_stocks(stocks_data)
        prune(stock_tree, 0.25)

        self.assertEqual(make_stock_from_dictionary((stocks_data[2])), stock_tree.origin.value) #Origin
        self.assertEqual(make_stock_from_dictionary((stocks_data[0])), stock_tree.origin.left.value) #Left
        self.assertEqual(make_stock_from_dictionary((stocks_data[1])), stock_tree.origin.right.value) #Right
        self.assertEqual(make_stock_from_dictionary((stocks_data[9])), stock_tree.origin.right.right.value) #Right Right
        self.assertEqual(4, stock_tree.size)

    def test_advanced_pruning(self):
        stocks_data = [
            {'ticker': 'N01',
             'name': 'N01 Corporation',
             'price': 1654.4127265258749,
             'pe_ratio': 0.17350401092724566,
             'market_cap': 2267294274063,
             'div_yield': 3.0045096307110626},
            {'ticker': 'N02',
             'name': 'N02 Corporation',
             'price': 482.82853315519196,
             'pe_ratio': 0.17152063051654176,
             'market_cap': 171372734010,
             'div_yield': 3.2907737763405396},
            {'ticker': 'N03',
             'name': 'N03 Corporation',
             'price': 581.38791893488,
             'pe_ratio': 0.08288459551066929,
             'market_cap': 1986717286798,
             'div_yield': 0.21607786966669185},
            {'ticker': 'N04',
             'name': 'N04 Corporation',
             'price': 1891.4542735930377,
             'pe_ratio': 0.3809128454229713,
             'market_cap': 2944907672122,
             'div_yield': 2.0262312337867545},
            {'ticker': 'N05',
             'name': 'N05 Corporation',
             'price': 652.8451507086813,
             'pe_ratio': 0.25112666869712974,
             'market_cap': 1689339700786,
             'div_yield': 0.21920677194038607},
            {'ticker': 'N06',
             'name': 'N06 Corporation',
             'price': 2509.6588825765793,
             'pe_ratio': 0.3053576539737222,
             'market_cap': 1940191056958,
             'div_yield': 0.19868817399651695},
            {'ticker': 'N07',
             'name': 'N07 Corporation',
             'price': 2143.15203972091,
             'pe_ratio': 0.28676803512702576,
             'market_cap': 2261181399650,
             'div_yield': 0.8557945651620376},
            {'ticker': 'N08',
             'name': 'N08 Corporation',
             'price': 319.4017129424933,
             'pe_ratio': 0.3424503973392974,
             'market_cap': 1401748767126,
             'div_yield': 1.2502473309745246},
            {'ticker': 'N09',
             'name': 'N09 Corporation',
             'price': 2691.70607031262,
             'pe_ratio': 0.33805058121180187,
             'market_cap': 1370630672277,
             'div_yield': 2.357025901255805},
            {'ticker': 'N10',
             'name': 'N10 Corporation',
             'price': 2230.8832664024935,
             'pe_ratio': 0.42321079144428075,
             'market_cap': 814674949105,
             'div_yield': 0.5906366334402602},
            {'ticker': 'N11',
             'name': 'N11 Corporation',
             'price': 357.2490987603387,
             'pe_ratio': 0.3657884260141092,
             'market_cap': 1557628761256,
             'div_yield': 0.8521825161433374},
            {'ticker': 'N12',
             'name': 'N12 Corporation',
             'price': 1052.7716333702915,
             'pe_ratio': 0.35439682520540994,
             'market_cap': 342350154533,
             'div_yield': 2.2687842095947404},
            {'ticker': 'N13',
             'name': 'N13 Corporation',
             'price': 1797.0944287580485,
             'pe_ratio': 0.4532429903161907,
             'market_cap': 397586946179,
             'div_yield': 3.084759422019157},
            {'ticker': 'N14',
             'name': 'N14 Corporation',
             'price': 2835.1591240241078,
             'pe_ratio': 0.2712354891023151,
             'market_cap': 1352714680873,
             'div_yield': 1.2787248300996046},
            {'ticker': 'N15',
             'name': 'N15 Corporation',
             'price': 2995.2882082409205,
             'pe_ratio': 0.13211762553870068,
             'market_cap': 2953191880380,
             'div_yield': 1.719058820898825},
            {'ticker': 'N16',
             'name': 'N16 Corporation',
             'price': 918.5474358167464,
             'pe_ratio': 0.07555238029681377,
             'market_cap': 2819373989543,
             'div_yield': 0.9752868109377646},
            {'ticker': 'N17',
             'name': 'N17 Corporation',
             'price': 1941.571166333349,
             'pe_ratio': 0.28990873933561145,
             'market_cap': 2854727217631,
             'div_yield': 1.0313424689177402},
            {'ticker': 'N18',
             'name': 'N18 Corporation',
             'price': 2536.8937481245775,
             'pe_ratio': 0.3066066602546072,
             'market_cap': 1958546007363,
             'div_yield': 1.0427524832892638},
            {'ticker': 'N19',
             'name': 'N19 Corporation',
             'price': 1512.5244850292613,
             'pe_ratio': 0.17015543438073233,
             'market_cap': 2284977920972,
             'div_yield': 1.3090814290800088},
            {'ticker': 'N20',
             'name': 'N20 Corporation',
             'price': 2807.946967050143,
             'pe_ratio': 0.33322565400043014,
             'market_cap': 1226712524577,
             'div_yield': 0.38656080941797155},
            {'ticker': 'N21',
             'name': 'N21 Corporation',
             'price': 227.1811273505082,
             'pe_ratio': 0.40025782441822605,
             'market_cap': 2088328069303,
             'div_yield': 3.917745966338216},
            {'ticker': 'N22',
             'name': 'N22 Corporation',
             'price': 1583.7898423134332,
             'pe_ratio': 0.4818420289702342,
             'market_cap': 682201603267,
             'div_yield': 3.2730448344046135},
            {'ticker': 'N23',
             'name': 'N23 Corporation',
             'price': 2574.1872173018214,
             'pe_ratio': 0.30032141475032115,
             'market_cap': 2055767210364,
             'div_yield': 1.0009225003856774},
            {'ticker': 'N24',
             'name': 'N24 Corporation',
             'price': 1810.402826962892,
             'pe_ratio': 0.10438533983197618,
             'market_cap': 1323895799936,
             'div_yield': 0.4083951518678042},
            {'ticker': 'N25',
             'name': 'N25 Corporation',
             'price': 29.567005715079848,
             'pe_ratio': 0.15721059276390187,
             'market_cap': 1008185936265,
             'div_yield': 3.7471077010490172},
            {'ticker': 'N26',
             'name': 'N26 Corporation',
             'price': 10.002071522733045,
             'pe_ratio': 0.05398434946152874,
             'market_cap': 830767674181,
             'div_yield': 0.8767049071007951},
            {'ticker': 'N27',
             'name': 'N27 Corporation',
             'price': 2856.33510526757,
             'pe_ratio': 0.31319315631072747,
             'market_cap': 2646025319106,
             'div_yield': 2.179615451633033},
            {'ticker': 'N28',
             'name': 'N28 Corporation',
             'price': 2661.506466011475,
             'pe_ratio': 0.22666775293736197,
             'market_cap': 340887942716,
             'div_yield': 2.986102180110432},
            {'ticker': 'N29',
             'name': 'N29 Corporation',
             'price': 2406.3777674456546,
             'pe_ratio': 0.1999326108737135,
             'market_cap': 2556865736861,
             'div_yield': 3.5824781923897224},
            {'ticker': 'N30',
             'name': 'N30 Corporation',
             'price': 2100.419938952449,
             'pe_ratio': 0.28861636997763995,
             'market_cap': 2540851134423,
             'div_yield': 2.8643966035466013},
            {'ticker': 'N31',
             'name': 'N31 Corporation',
             'price': 1343.8798063702218,
             'pe_ratio': 0.14325663825116225,
             'market_cap': 2811542181478,
             'div_yield': 1.8157437576114814},
            {'ticker': 'N32',
             'name': 'N32 Corporation',
             'price': 2065.017814924486,
             'pe_ratio': 0.20911262543368142,
             'market_cap': 360359163846,
             'div_yield': 3.6093267376737086},
            {'ticker': 'N33',
             'name': 'N33 Corporation',
             'price': 2294.1976702547104,
             'pe_ratio': 0.4008227123872031,
             'market_cap': 1936755324235,
             'div_yield': 1.4002512232786648},
            {'ticker': 'N34',
             'name': 'N34 Corporation',
             'price': 2384.094810214076,
             'pe_ratio': 0.3130730999393783,
             'market_cap': 1863303865836,
             'div_yield': 1.0863978548946278},
            {'ticker': 'N35',
             'name': 'N35 Corporation',
             'price': 1179.4989837297173,
             'pe_ratio': 0.31235203701733516,
             'market_cap': 1084539233178,
             'div_yield': 3.968772613975379},
            {'ticker': 'N36',
             'name': 'N36 Corporation',
             'price': 1444.7749357519392,
             'pe_ratio': 0.4156696252698249,
             'market_cap': 1376873786868,
             'div_yield': 3.520019199818016},
            {'ticker': 'N37',
             'name': 'N37 Corporation',
             'price': 2702.399544695485,
             'pe_ratio': 0.17322659145520486,
             'market_cap': 2494489407619,
             'div_yield': 0.9536365361457597},
            {'ticker': 'N38',
             'name': 'N38 Corporation',
             'price': 2427.343657433411,
             'pe_ratio': 0.43848719032243594,
             'market_cap': 2469040876071,
             'div_yield': 3.0505368310604406},
            {'ticker': 'N39',
             'name': 'N39 Corporation',
             'price': 599.3416105360536,
             'pe_ratio': 0.3673578456971167,
             'market_cap': 1780573482717,
             'div_yield': 3.5335907121364887},
            {'ticker': 'N40',
             'name': 'N40 Corporation',
             'price': 1565.2677441538845,
             'pe_ratio': 0.09959350963731212,
             'market_cap': 2106058116969,
             'div_yield': 1.0550172905793476},
            {'ticker': 'N41',
             'name': 'N41 Corporation',
             'price': 1671.867889298196,
             'pe_ratio': 0.4684420038320561,
             'market_cap': 430322284909,
             'div_yield': 2.623334768814259},
            {'ticker': 'N42',
             'name': 'N42 Corporation',
             'price': 638.4068672963505,
             'pe_ratio': 0.20968420837529017,
             'market_cap': 749333257090,
             'div_yield': 2.535695750896249},
            {'ticker': 'N43',
             'name': 'N43 Corporation',
             'price': 2668.8599192108377,
             'pe_ratio': 0.4872972254746576,
             'market_cap': 414054694788,
             'div_yield': 1.8249113963469106},
            {'ticker': 'N44',
             'name': 'N44 Corporation',
             'price': 1039.792261542579,
             'pe_ratio': 0.43624439006961563,
             'market_cap': 2371868625423,
             'div_yield': 2.322551813339182},
            {'ticker': 'N45',
             'name': 'N45 Corporation',
             'price': 1665.762552242418,
             'pe_ratio': 0.466571095986318,
             'market_cap': 1024225636254,
             'div_yield': 2.777139716741507},
            {'ticker': 'N46',
             'name': 'N46 Corporation',
             'price': 588.5334079347349,
             'pe_ratio': 0.27293280212667037,
             'market_cap': 2746942750216,
             'div_yield': 1.4934517074224058},
            {'ticker': 'N47',
             'name': 'N47 Corporation',
             'price': 1101.954831824996,
             'pe_ratio': 0.251150958773078,
             'market_cap': 1657746815543,
             'div_yield': 0.0024807887384437066},
            {'ticker': 'N48',
             'name': 'N48 Corporation',
             'price': 2481.5645281111415,
             'pe_ratio': 0.41602475453235793,
             'market_cap': 2115332626463,
             'div_yield': 1.897852119560564},
            {'ticker': 'N49',
             'name': 'N49 Corporation',
             'price': 1357.4349950814747,
             'pe_ratio': 0.36825716679986226,
             'market_cap': 2593482485112,
             'div_yield': 3.6656806065967826},
            {'ticker': 'N50',
             'name': 'N50 Corporation',
             'price': 30.868947927189026,
             'pe_ratio': 0.06279172134133967,
             'market_cap': 703216024577,
             'div_yield': 1.9614321817561367}
        ]

        stock_tree = build_tree_with_stocks(stocks_data)

        """ (1) Prune with 0.32 as the threshold"""
        prune(stock_tree, 0.32)
        
        # N10 should be the origin
        self.assertEqual(make_stock_from_dictionary(stocks_data[9]), stock_tree.origin.value)

        # Left side of origin #
        # Left of N10 is N08
        self.assertEqual( make_stock_from_dictionary(stocks_data[7]), stock_tree.origin.left.value)
        # Left of N08 is N20
        self.assertEqual(make_stock_from_dictionary(stocks_data[19]), stock_tree.origin.left.left.value)
        # Right of N08 is N04
        self.assertEqual( make_stock_from_dictionary(stocks_data[3]), stock_tree.origin.left.right.value)
        # Left of N20 is none
        self.assertIsNone(stock_tree.origin.left.left.left)
        # Right of N20 is N09
        self.assertEqual(make_stock_from_dictionary(stocks_data[8]), stock_tree.origin.left.left.right.value)
        # N06 and N09 have no left or right
        self.assertIsNone(stock_tree.origin.left.right.left.right.right)
        self.assertIsNone(stock_tree.origin.left.right.left.left.left)
        # Left of N04 is N11
        self.assertEqual(make_stock_from_dictionary(stocks_data[10]), stock_tree.origin.left.right.left.value)
        # Right of N04 is N21
        self.assertEqual(make_stock_from_dictionary(stocks_data[20]), stock_tree.origin.left.right.right.value)
        # Left of N11 is N12
        self.assertEqual(make_stock_from_dictionary(stocks_data[11]), stock_tree.origin.left.right.left.left.value)
        # Right of N11 is N39
        self.assertEqual(make_stock_from_dictionary(stocks_data[38]), stock_tree.origin.left.right.left.right.value)
        # Left of N21 is None
        self.assertIsNone(stock_tree.origin.left.right.right.left)
        # Right of N21 is N36
        self.assertEqual(make_stock_from_dictionary(stocks_data[35]), stock_tree.origin.left.right.right.right.value)
        # N12, N39, and N36 have no children
        self.assertIsNone(stock_tree.origin.left.right.left.left.left)
        self.assertIsNone(stock_tree.origin.left.right.left.left.right)
        self.assertIsNone(stock_tree.origin.left.right.left.right.left)
        self.assertIsNone(stock_tree.origin.left.right.left.right.right)
        self.assertIsNone(stock_tree.origin.left.right.right.right.left)
        self.assertIsNone(stock_tree.origin.left.right.right.right.right)

        # Right side of origin #
        # Right of N10 is N13
        self.assertEqual(make_stock_from_dictionary(stocks_data[12]), stock_tree.origin.right.value)
        # Left of N13 is N38
        self.assertEqual(make_stock_from_dictionary(stocks_data[37]), stock_tree.origin.right.left.value)
        # Right of N13 is N22
        self.assertEqual(make_stock_from_dictionary(stocks_data[21]), stock_tree.origin.right.right.value)
        # Left of N38 is N44
        self.assertEqual(make_stock_from_dictionary(stocks_data[43]), stock_tree.origin.right.left.left.value)
        # Right of N38 is none
        self.assertIsNone(stock_tree.origin.right.left.right)
        # N44 has no left or right
        self.assertIsNone(stock_tree.origin.right.left.left.left)
        self.assertIsNone(stock_tree.origin.right.left.left.right)
        # Left of N22 is N41
        self.assertEqual(make_stock_from_dictionary(stocks_data[40]), stock_tree.origin.right.right.left.value)
        # Right of N22 is N43
        self.assertEqual(make_stock_from_dictionary(stocks_data[42]), stock_tree.origin.right.right.right.value)
        # Left of N41 is N45
        self.assertEqual(make_stock_from_dictionary(stocks_data[44]), stock_tree.origin.right.right.left.left.value)
        # Right of N41 is None
        self.assertIsNone(stock_tree.origin.right.right.left.right)
        # N45 and N43 has no left or right
        self.assertIsNone(stock_tree.origin.right.right.left.left.right)
        self.assertIsNone(stock_tree.origin.right.right.left.left.left)
        self.assertIsNone(stock_tree.origin.right.right.right.left)
        self.assertIsNone(stock_tree.origin.right.right.right.right)

        # Size should be 17
        self.assertEqual(17, stock_tree.size)

        """ (2) Prune with 0.47 as the threshold"""
        # Should prune all stocks except 2
        prune(stock_tree, 0.47);

        # Size is now 2
        self.assertEqual(2, stock_tree.size)

        # N22 is the origin
        self.assertEqual(make_stock_from_dictionary(stocks_data[21]), stock_tree.origin.value)
        # Left of N22 is None
        self.assertIsNone(stock_tree.origin.left)
        # Right of N22 is N43
        self.assertEqual(make_stock_from_dictionary(stocks_data[42]), stock_tree.origin.right.value)
        # N43 has no left or right
        self.assertIsNone(stock_tree.origin.right.left)
        self.assertIsNone(stock_tree.origin.right.right)

        """ (3) Prune with 0.52 as the threshold"""
        # Prune the rest of the stocks
        prune(stock_tree, 0.52)
        self.assertEqual(0, stock_tree.size)
    def test_recommend_stock(self):
        stocks_data = [
            {"ticker": "AAPL", "name": "Apple Inc.", "price": 150.50, "pe_ratio": 0.253,
             "market_cap": 2000000000000, "div_yield": 1.5},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "price": 2800.00, "pe_ratio": 0.307,
             "market_cap": 1800000000000, "div_yield": 0.8},
            {"ticker": "MSFT", "name": "Microsoft Corporation", "price": 320.75, "pe_ratio": 0.285,
             "market_cap": 2200000000000, "div_yield": 1.2},
            {"ticker": "INTC", "name": "Intel Corporation", "price": 50.25, "pe_ratio": 0.158,
             "market_cap": 1500000000000, "div_yield": 2.0},
            {"ticker": "CSCO", "name": "Cisco Systems Inc.", "price": 55.50, "pe_ratio": 0.202,
             "market_cap": 1600000000000, "div_yield": 1.8},
            {"ticker": "ORCL", "name": "Oracle Corporation", "price": 85.75, "pe_ratio": 0.183,
             "market_cap": 1900000000000, "div_yield": 1.0},
            {"ticker": "IBM", "name": "International Business Machines Corporation", "price": 120.00,
             "pe_ratio": 0.146, "market_cap": 1200000000000, "div_yield": 2.5},
            {"ticker": "HPQ", "name": "HP Inc.", "price": 30.50, "pe_ratio": 0.127, "market_cap": 800000000000,
             "div_yield": 3.0},
            {"ticker": "DELL", "name": "Dell Technologies Inc.", "price": 70.00, "pe_ratio": 0.221,
             "market_cap": 1000000000000, "div_yield": 1.5},
            {"ticker": "AMD", "name": "Advanced Micro Devices Inc.", "price": 120.25, "pe_ratio": 0.356,
             "market_cap": 900000000000, "div_yield": 0.7},
        ]

        stock = build_tree_with_stocks(stocks_data)

        user_buy = User(name="Divya Lakshmi", pe_ratio_threshold=0.15, div_yield_threshold=1.5)
        user_buy2 = User(name="Aaron Elkin", pe_ratio_threshold=0.3, div_yield_threshold=0.9)
        user_sell = User(name=" Hank Murdock", pe_ratio_threshold=25, div_yield_threshold=2.5)
        user_sell2 = User(name="Sebnem Onsay", pe_ratio_threshold=0.2, div_yield_threshold=2.0)
        user_strict_sell = User(name="Ethan Cook", pe_ratio_threshold=5.0, div_yield_threshold=0.01)  # no stock meets
        user_strict_buy = User(name="Joel Nataren", pe_ratio_threshold=0.1, div_yield_threshold=3.5)  # no stock meets

        # Test 1 - Recommend the correct Stock to Buy
        best_stock = recommend_stock(stock, user_buy, "buy")
        self.assertEqual("HPQ", best_stock.ticker)

        best_stock = recommend_stock(stock, user_buy2, "buy")
        self.assertEqual("HPQ", best_stock.ticker)

        # Test 2 - Recommend the correct Stock to Sell
        best_stock = recommend_stock(stock, user_sell, "sell")
        self.assertEqual("AMD", best_stock.ticker)

        best_stock = recommend_stock(stock, user_sell2, "sell")
        self.assertEqual("AMD", best_stock.ticker)

        # Test 3 - No suitable stock to Buy
        best_stock = recommend_stock(stock, user_strict_buy, "buy")
        self.assertIsNone(best_stock)

        # Test 4 - No suitable stock to Sell
        best_stock = recommend_stock(stock, user_strict_sell, "sell")
        self.assertIsNone(best_stock)


class HuffmanTreeTests(unittest.TestCase):

    def test_build(self):
        htree = HuffmanTree()

        htree.build('TotallyRandom')

        self.assertEqual({'R': '1110', 'T': '000', 'a': '110', 'd': '010', 'l': '011',
                          'm': '1011', 'n': '1010', 'o': '100', 't': '001', 'y': '1111'},
                         htree.make_char_map())

        htree.build('aljdsakvndvoeqpgvmb9511kgmnvc0wq')

        self.assertEqual(
            {'0': '01001',
             '1': '1110',
             '5': '00111',
             '9': '00110',
             'a': '1011',
             'b': '11000',
             'c': '11111',
             'd': '0010',
             'e': '01000',
             'g': '0110',
             'j': '01111',
             'k': '1000',
             'l': '01110',
             'm': '1010',
             'n': '0101',
             'o': '11110',
             'p': '11010',
             'q': '1001',
             's': '11011',
             'v': '000',
             'w': '11001'},
            htree.make_char_map())

        htree.build('1495403125039849120849018490184104810')

        self.assertEqual(
            {'0': '00',
             '1': '01',
             '2': '1100',
             '3': '11011',
             '4': '111',
             '5': '11010',
             '8': '101',
             '9': '100'},
            htree.make_char_map())

    def test_compression_decompression(self):
        htree = HuffmanTree()

        mapping, compressed = htree.compress('Totally Random And Such')

        decompressed = htree.decompress(mapping, compressed)

        self.assertEqual(decompressed, 'Totally Random And Such')

        mapping, compressed = htree.compress('aljdsakvndvoeqpgvmb9511kgmnvc0wq')

        decompressed = htree.decompress(mapping, compressed)

        self.assertEqual(decompressed, 'aljdsakvndvoeqpgvmb9511kgmnvc0wq')

        mapping, compressed = htree.compress('1495403125039849120849018490184104810')

        decompressed = htree.decompress(mapping, compressed)

        self.assertEqual(decompressed, '1495403125039849120849018490184104810')

        mapping, compressed = htree.compress("Don't mess with my password I want it back")

        decompressed = htree.decompress(mapping, compressed)

        self.assertEqual(decompressed, "Don't mess with my password I want it back")


if __name__ == '__main__':
    unittest.main()
    