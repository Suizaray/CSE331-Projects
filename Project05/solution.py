"""
Project 5
CSE 331 SS24
Authors: Hank Murdock, Joel Nataren, Aaron Elkin, Divyalakshmi Varadha, Ethan Cook
starter.py
"""
import math
import queue
from typing import TypeVar, Generator, List, Tuple, Optional
from collections import deque
import json
from queue import SimpleQueue
import heapq

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
# represents a Node object (forward-declare to use in Node __init__)
Node = TypeVar("Node")
# represents a custom type used in application
AVLWrappedDictionary = TypeVar("AVLWrappedDictionary")


class Node:
    """
    Implementation of an BST and AVL tree node.
    Do not modify.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["value", "parent", "left", "right", "height"]

    def __init__(self, value: T, parent: Node = None,
                 left: Node = None, right: Node = None) -> None:
        """
        Construct an AVL tree node.

        :param value: value held by the node object
        :param parent: ref to parent node of which this node is a child
        :param left: ref to left child node of this node
        :param right: ref to right child node of this node
        """
        self.value = value
        self.parent, self.left, self.right = parent, left, right
        self.height = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"

    def __str__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return repr(self)


####################################################################################################

class BinarySearchTree:
    """
    Implementation of an BSTree.
    Modify only below indicated line.
    """

    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty BST tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BST tree
        """
        if self.origin is None:
            return "Empty BST Tree"

        lines = pretty_print_binary_tree(self.origin, 0, False, '-')[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    def __str__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Gives the height element of the provided node or -1 is NoneType
        :param root: The node that height is retrieved from
        :return: height value
        """
        return -1 if (root is None) else root.height

    def insert(self, root: Node, val: T) -> None:
        """
        Inserts a node into the BST subtree given with the value given
        :param root: root node for the subtree that the insertion occurs in
        :param val: the value that is assigned to the new node
        """
        if root is None:
            self.origin = Node(val, parent=None)
            self.size += 1
            self.origin.height = 0
            return
        else:
            if root.value == val:
                return
            elif root.value < val:
                if root.right is None:
                    root.right = Node(val, parent=root)
                    self.size += 1
                else:
                    self.insert(root.right, val)
            else:
                if root.left is None:
                    root.left = Node(val, parent=root)
                    self.size += 1
                else:
                    self.insert(root.left, val)
            root.height = 1 + max(self.height(root.left), self.height(root.right))

    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        Removes a node from the BST subtree given if the value exists
        :param root: root of the given subtree to be removed from
        :param val: The value that is being searched for and then removed
        :return: The root node of the subtree after removal
        """
        par = None
        cur = root
        while cur:
            if cur.value == val:
                if cur.left is None and cur.right is None:  # leaf node case
                    if par is None:
                        self.origin = None

                    elif par.left == cur:
                        par.left = None
                    else:
                        par.right = None
                    self.size -= 1
                elif cur.left is None:  # right child only case
                    if par is None:
                        self.origin = cur.right
                    elif par.left == cur:
                        par.left = cur.right
                        par.left.parent = par
                    else:
                        par.right = cur.right
                        par.right.parent = par
                    self.size -= 1
                elif cur.right is None:  # left child only case
                    if par is None:
                        self.origin = cur.left
                    elif par.left == cur:
                        par.left = cur.left
                        par.left.parent = par
                    else:
                        par.right = cur.left
                        par.right.parent = par
                    self.size -= 1
                else:  # two child case
                    pred = cur.left
                    while pred.right:
                        pred = pred.right
                    temp_pred = pred.value
                    self.remove(root, pred.value)
                    cur.value = temp_pred
                cur = par
                while cur:
                    cur.height = 1 + max(self.height(cur.left), self.height(cur.right))
                    cur = cur.parent
                return root

            elif cur.value > val:
                par = cur
                cur = cur.left
            else:
                par = cur
                cur = cur.right

        return None

    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        Searches for a value in the given BST subtree
        :param root: root node of the subtree
        :param val: value to be searched for
        :return: node that contains the value, None if none found
        """
        par = None
        cur = root
        while cur:
            if cur.value == val:
                return cur
            elif cur.value > val:
                par = cur
                cur = cur.left
            else:
                par = cur
                cur = cur.right
        return par


class AVLTree:
    """
    Implementation of an AVL tree.
    Modify only below indicated line.
    """

    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty AVL tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree as a string.

        :return: string representation of the AVL tree
        """
        if self.origin is None:
            return "Empty AVL Tree"
        return super(AVLTree, self).__repr__()

    def __str__(self) -> str:
        """
        Represent the AVLTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Gives the height element of the provided node or -1 is NoneType
        :param root: The node that height is retrieved from
        :return: height value
        """
        return -1 if (root is None) else root.height

    def update_height(self, root: Node):
        """
        Updates the height of a node
        :param root: The node that height updated at
        """
        if root is None:
            return
        left_height = -1
        if root.left:
            left_height = self.height(root.left)
        right_height = -1
        if root.right:
            right_height = self.height(root.right)
        root.height = 1 + max(left_height, right_height)

    def set_child(self, parent: Node, which_child: str, child: Node):
        """
        Helper function to set either left or right child of a given node
        :param parent: the node that has a child set
        :param which_child: string of either left or right to direct which position
        :param child: the node to be set
        """
        if which_child == "left":
            parent.left = child
        else:
            parent.right = child
        if child:
            child.parent = parent
        self.update_height(parent)

    def replace_child(self, parent: Node, current_child: Node, new_child: Node):
        """
        Helper function to invoke set_child on either left or right child
        :param parent: the node pending a replacement child
        :param current_child: the current child residing under parent node
        :param new_child: the node that will replace the current child
        """
        if parent.left == current_child:
            self.set_child(parent, "left", new_child)
        elif parent.right == current_child:
            self.set_child(parent, "right", new_child)

    def left_rotate(self, root: Node) -> Optional[Node]:
        """
        Rotates the AVL tree left about the give node
        :param root: the given node to rotate about
        :return: the node that resides as the root of the post-rotated subtree
        """
        if root is None:
            return None

        right_left_child = root.right.left
        if root.parent:
            self.replace_child(root.parent, root, root.right)
        else:
            self.origin = root.right
            self.origin.parent = None
        self.set_child(root.right, "left", root)
        self.set_child(root, "right", right_left_child)
        self.update_height(root.parent)
        return root.parent


    def right_rotate(self, root: Node) -> Optional[Node]:
        """
        Rotates the AVL tree right about the give node
        :param root: the given node to rotate about
        :return: the node that resides as the root of the post-rotated subtree
        """
        if root is None:
            return None
        left_right_child = root.left.right
        if root.parent:
            self.replace_child(root.parent, root, root.left)
        else:
            self.origin = root.left
            self.origin.parent = None
        self.set_child(root.left, "right", root)
        self.set_child(root, "left", left_right_child)
        self.update_height(root.parent)
        return root.parent

    def balance_factor(self, root: Node) -> int:
        """
        Calculates the balance factor of a given node
        :param root: the given node to be tested
        :return: the balance factor value
        """
        if root is None:
            return 0
        if root.left is None and root.right is None:
            return 0
        if root.left is None:
            return -1 - root.right.height
        if root.right is None:
            return root.left.height + 1
        return root.left.height - root.right.height

    def rebalance(self, root: Node) -> Optional[Node]:
        """
        Balances the given node if needed
        :param root: the given node to be balanced
        :return: the node that is the root of the subtree
        """
        self.update_height(root)
        node = None
        b = self.balance_factor(root)
        if b == 0:
            return root
        if b >= 2:
            if self.balance_factor(root.left) == 1 or self.balance_factor(root.left) == 0:  # left-left case
                node = self.right_rotate(root)

            else:  # left-right case
                self.left_rotate(root.left)

                node = self.right_rotate(root)

        elif b <= -2:
            if self.balance_factor(root.right) == -1 or self.balance_factor(root.right) == 0:  # right-right case
                node = self.left_rotate(root)

            else:  # right-left case
                self.right_rotate(root.right)

                node = self.left_rotate(root)

        return node

    def insert(self, root: Node, val: T) -> Optional[Node]:
        """
        Inserts a node into the AVL subtree given with the value given
        :param root: root node for the subtree that the insertion occurs in
        :param val: the value that is assigned to the new node
        :return: returns the root node of the balanced subtree
        """
        if root is None:
            self.origin = Node(val, parent=None)
            self.size += 1
            self.origin.height = 0
            return self.origin
        else:
            if root.value == val:
                return root
            elif root.value < val:
                if root.right is None:
                    root.right = Node(val, parent=root)
                    self.size += 1
                else:
                    self.insert(root.right, val)
            else:
                if root.left is None:
                    root.left = Node(val, parent=root)
                    self.size += 1
                else:
                    self.insert(root.left, val)
            root.height = 1 + max(self.height(root.left), self.height(root.right))
            self.rebalance(root)
            return root
    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        Removes a node from the AVL subtree given if the value exists
        :param root: root of the given subtree to be removed from
        :param val: The value that is being searched for and then removed
        :return: The root node of the balanced subtree after removal
        """
        par = None
        cur = root
        while cur:
            if cur.value == val:
                if cur.left is None and cur.right is None:  # leaf node case
                    if par is None:
                        self.origin = None

                    elif par.left == cur:
                        par.left = None
                    else:
                        par.right = None
                    self.size -= 1
                elif cur.left is None:  # right child only case
                    if par is None:
                        self.origin = cur.right
                    elif par.left == cur:
                        par.left = cur.right
                        par.left.parent = par
                    else:
                        par.right = cur.right
                        par.right.parent = par
                    self.size -= 1
                elif cur.right is None:  # left child only case
                    if par is None:
                        self.origin = cur.left
                    elif par.left == cur:
                        par.left = cur.left
                        par.left.parent = par
                    else:
                        par.right = cur.left
                        par.right.parent = par
                    self.size -= 1
                else:  # two child case
                    pred = cur.left
                    while pred.right:
                        pred = pred.right
                    temp_pred = pred.value
                    self.remove(root, pred.value)
                    cur.value = temp_pred
                """cur = par
                while cur:
                    cur.height = 1 + max(self.height(cur.left), self.height(cur.right))
                    cur = cur.parent"""

                cur = par
                while cur:
                    self.rebalance(cur)
                    cur = cur.parent
                return root

            elif cur.value > val:
                par = cur
                cur = cur.left
            else:
                par = cur
                cur = cur.right

        return root

    def min(self, root: Node) -> Optional[Node]:
        """
        Calculates the minimum value within an AVL subtree
        :param root: root node of the subtree
        :return: minimum value node or None if empty AVL subtree
        """
        min_node = None
        while root:
            min_node = root
            root = root.left
        return min_node

    def max(self, root: Node) -> Optional[Node]:
        """
        Calculates the maximum value within an AVL subtree
        :param root: root node of the subtree
        :return: maximum value node or None if empty AVL subtree
        """
        max_node = None
        while root:
            max_node = root
            root = root.right
        return max_node

    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        Searches for a value in the given AVL subtree
        :param root: root node of the subtree
        :param val: value to be searched for
        :return: node that contains the value, None if none found
        """
        par = None
        cur = root
        while cur:
            if cur.value == val:
                return cur
            elif cur.value > val:
                par = cur
                cur = cur.left
            else:
                par = cur
                cur = cur.right
        return par

    def inorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Performs an inorder traversal of the given AVL subtree and generates the nodes
        :param root: root node of the given subtree
        :return: A generator yielding the nodes inorder
        """
        if root is None:
            return
        yield from self.inorder(root.left)
        yield root
        yield from self.inorder(root.right)

    def __iter__(self) -> Generator[Node, None, None]:
        """
        Method for making the AVL tree iterable
        :return: A generator yielding the nodes inorder
        """
        return self.inorder(self.origin)

    def preorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Performs a preorder traversal of the given AVL subtree and generates the nodes
        :param root: root node of the given subtree
        :return: A generator yielding the nodes preorder
        """
        if root is None:
            return
        yield root
        yield from self.preorder(root.left)
        yield from self.preorder(root.right)

    def postorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Performs a postorder traversal of the given AVL subtree and generates the nodes
        :param root: root node of the given subtree
        :return: A generator yielding the nodes postorder
        """
        if root is None:
            return
        yield from self.postorder(root.left)
        yield from self.postorder(root.right)
        yield root

    def levelorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Performs a breadth first traversal of the given AVL subtree and generates the nodes
        :param root: root node of the given subtree
        :return: A generator yielding the nodes breadth first
        """
        q = queue.SimpleQueue()
        q.put(root)
        while not q.empty():
            root = q.get()
            if root:
                yield root
                if root.left:
                    q.put(root.left)
                if root.right:
                    q.put(root.right)


####################################################################################################

class User:
    """
    Class representing a user of the stock marker.
    Note: A user can be both a buyer and seller.
    """

    def __init__(self, name, pe_ratio_threshold, div_yield_threshold):
        self.name = name
        self.pe_ratio_threshold = pe_ratio_threshold
        self.div_yield_threshold = div_yield_threshold


####################################################################################################

class Stock:
    __slots__ = ['ticker', 'name', 'price', 'pe', 'mkt_cap', 'div_yield']
    TOLERANCE = 0.001

    def __init__(self, ticker, name, price, pe, mkt_cap, div_yield):
        """
        Initialize a stock.

        :param name: Name of the stock.
        :param price: Selling price of stock.
        :param pe: Price to earnings ratio of the stock.
        :param mkt_cap: Market capacity.
        :param div_yield: Dividend yield for the stock.
        """
        self.ticker = ticker
        self.name = name
        self.price = price
        self.pe = pe
        self.mkt_cap = mkt_cap
        self.div_yield = div_yield

    def __repr__(self):
        """
        Return string representation of the stock.

        :return: String representation of the stock.
        """
        return f"{self.ticker}: PE: {self.pe}"

    def __str__(self):
        """
        Return string representation of the stock.

        :return: String representation of the stock.
        """
        return repr(self)

    def __lt__(self, other):
        """
        Check if the stock is less than the other stock.

        :param other: The other stock to compare to.
        :return: True if the stock is less than the other stock, False otherwise.
        """
        return self.pe < other.pe

    def __eq__(self, other):
        """
        Check if the stock is equal to the other stock.

        :param other: The other stock to compare to.
        :return: True if the stock is equal to the other stock, False otherwise.
        """
        return abs(self.pe - other.pe) < self.TOLERANCE


def make_stock_from_dictionary(stock_dictionary: dict[str: str]) -> Stock:
    """
    Builds an AVL tree with the given stock dictionary.

    :param stock_dictionary: Dictionary of stocks to be inserted into the AVL tree.
    :return: A stock in a Stock object.
    """
    stock = Stock(stock_dictionary['ticker'], stock_dictionary['name'], stock_dictionary['price'], \
                  stock_dictionary['pe_ratio'], stock_dictionary['market_cap'], stock_dictionary['div_yield'])
    return stock

def build_tree_with_stocks(stocks_list: List[dict[str: str]]) -> AVLTree:
    """
    Builds an AVL tree with the given list of stocks.

    :param stocks_list: List of stocks to be inserted into the AVL tree.
    :return: AVL tree with the given stocks.
    """
    avl = AVLTree()
    for stock in stocks_list:
        stock = make_stock_from_dictionary(stock)
        avl.insert(avl.origin, stock)
    return avl


####################################################################################################
# Implement functions below this line. #
####################################################################################################

def recommend_stock(stock_tree: AVLTree, user: User, action: str) -> Optional[Stock]:
    """
    Sifts through an AVL tree to find the optimal stock option for the user
    :param stock_tree: the AVL tree to be sifted
    :param user: the User class that contains the information of the user's preferences
    :param action: a string that indicates whether the user is buying or selling
    :return: the optimal stock, or None if no stock fits in the criteria of the user
    """
    node = stock_tree.origin
    optimal = None
    if action == "buy":
        while node:
            if (optimal is None or node.value.div_yield > optimal.value.div_yield) and node.value.div_yield > user.div_yield_threshold:
                optimal = node
            node = node.left
    else:
        while node:
            if (optimal is None or node.value.div_yield < optimal.value.div_yield) and node.value.div_yield < user.div_yield_threshold:
                optimal = node
            node = node.right
    return optimal.value if optimal else None


def prune(stock_tree: AVLTree, threshold: float = 0.05) -> None:
    """
    Prunes all subtrees in the given AVL tree that has a pe lower than the threshold
    :param stock_tree: the given AVL tree to be pruned
    :param threshold: the pe threshold value to be used
    """
    ### Unsure if this is O(n^2logn) or O(nlogn) time complexity
    generator = stock_tree.postorder(stock_tree.origin)
    for i in range(stock_tree.size):
        node = next(generator)
        if node.value.pe < threshold:
            stock_tree.remove(stock_tree.origin, node.value)
            generator = stock_tree.postorder(stock_tree.origin)

####################################################################################################
####################### EXTRA CREDIT ##############################################################
####################################################################################################

class Blackbox:
    def __init__(self):
        """
        Initialize a minheap.
        """
        self.heap = []

    def store(self, value: T):
        """
        Push a value into the heap while maintaining minheap property.

        :param value: The value to be added.
        """
        heapq.heappush(self.heap, value)

    def get_next(self) -> T:
        """
        Pop minimum from min heap.

        :return: Smallest value in heap.
        """
        return heapq.heappop(self.heap)

    def __len__(self):
        """
        Length of the heap.

        :return: The length of the heap
        """
        return len(self.heap)

    def __repr__(self) -> str:
        """
        The string representation of the heap.

        :return: The string representation of the heap.
        """
        return repr(self.heap)

    __str__ = __repr__


class HuffmanNode:
    __slots__ = ['character', 'frequency', 'left', 'right', 'parent']

    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency

        self.left = None
        self.right = None
        self.parent = None

    def __lt__(self, other):
        """
        Checks if node is less than other.

        :param other: The other node to compare to.
        """
        return self.frequency < other.frequency

    def __repr__(self):
        """
        Returns string representation.

        :return: The string representation.
        """
        return '<Char: {}, Freq: {}>'.format(self.character, self.frequency)

    __str__ = __repr__


class HuffmanTree:
    __slots__ = ['root', 'blackbox']

    def __init__(self):
        self.root = None
        self.blackbox = Blackbox()

    def __repr__(self):
        """
        Returns the string representation.

        :return: The string representation.
        """
        if self.root is None:
            return "Empty Tree"

        lines = pretty_print_binary_tree(self.root, 0, False, '-')[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    __str__ = __repr__

    def make_char_map(self) -> dict[str: str]:
        """
        Create a binary mapping from the huffman tree.

        :return: Dictionary mapping from characters to "binary" strings.
        """
        mapping = {}

        def traversal(root: HuffmanNode, current_str: str):
            if not root:
                return

            if not root.left and not root.right:
                mapping[root.character] = current_str
                return

            if root.left:
                traversal(root.left, current_str=current_str + '0')

            if root.right:
                traversal(root.right, current_str=current_str + '1')

        traversal(self.root, '')

        return mapping

    def compress(self, input: str) -> tuple[dict[str: str], List[str]]:
        """
        Compress the input data by creating a map via huffman tree.

        :param input: String to compress.
        :return: First value to return is the mapping from characters to binary strings.
        Second value is the compressed data.
        """
        self.build(input)

        mapping = self.make_char_map()

        compressed_data = []

        for char in input:
            compressed_data.append(mapping[char])

        return mapping, compressed_data

    def decompress(self, mapping: dict[str: str], compressed: List[str]) -> str:
        """
        Use the mapping from characters to binary strings to decompress the array of bits.

        :param mapping: Mapping of characters to binary strings.
        :param compressed: Array of binary strings that are encoded.
        """

        reverse_mapping = {v: k for k, v in mapping.items()}

        decompressed = ""

        for encoded in compressed:
            decompressed += reverse_mapping[encoded]

        return decompressed

    ########################################################################################
    # Implement functions below this line. #
    ########################################################################################

    def build(self, chars: str) -> None:
        """
        Creates a Huffman Tree with the characters in the given string
        :param chars: the string of characters
        """
        freq_table = {}
        for i in chars:
            if i in freq_table:
                freq_table[i] += 1
            else:
                freq_table[i] = 1
        for key, value in freq_table.items():
            self.blackbox.store(HuffmanNode(key, value))
        while len(self.blackbox) >= 2:
            first = self.blackbox.get_next()
            second = self.blackbox.get_next()
            parent = HuffmanNode(None, frequency=first.frequency + second.frequency)
            first.parent, second.parent = parent, parent
            parent.left, parent.right = first, second
            self.blackbox.store(parent)
        self.root = self.blackbox.get_next()


def pretty_print_binary_tree(root: Node, curr_index: int, include_index: bool = False,
                             delimiter: str = "-", ) -> \
        Tuple[List[str], int, int, int]:
    """
    Taken from: https://github.com/joowani/binarytree

    Recursively walk down the binary tree and build a pretty-print string.
    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root node value repr string
    (required for drawing branches) are sent up to the parent call. The parent
    call then combines its left and right sub-boxes to build a larger box etc.
    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :param curr_index: Level-order_ index of the current node (root node is 0).
    :type curr_index: int
    :param include_index: If set to True, include the level-order_ node indexes using
        the following format: ``{index}{delimiter}{value}`` (default: False).
    :type include_index: bool
    :param delimiter: Delimiter character between the node index and the node
        value (default: '-').
    :type delimiter:
    :return: Box of characters visually representing the current subtree, width
        of the box, and start-end positions of the repr string of the new root
        node value.
    :rtype: ([str], int, int, int)
    .. _Level-order:
        https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search
    """
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if include_index:
        node_repr = "{}{}{}".format(curr_index, delimiter, root.value)
    else:
        if type(root) == HuffmanNode:
            node_repr = repr(root)
        elif type(root.value) == AVLWrappedDictionary:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value.key) if root.parent else "None"}'
        else:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value) if root.parent else "None"}'

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = pretty_print_binary_tree(
        root.left, 2 * curr_index + 1, include_index, delimiter
    )
    r_box, r_box_width, r_root_start, r_root_end = pretty_print_binary_tree(
        root.right, 2 * curr_index + 2, include_index, delimiter
    )

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(" " * (l_root + 1))
        line1.append("_" * (l_box_width - l_root))
        line2.append(" " * l_root + "/")
        line2.append(" " * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(" " * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append("_" * r_root)
        line1.append(" " * (r_box_width - r_root + 1))
        line2.append(" " * r_root + "\\")
        line2.append(" " * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = " " * gap_size
    new_box = ["".join(line1), "".join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else " " * l_box_width
        r_line = r_box[i] if i < len(r_box) else " " * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


if __name__ == "__main__":
    pass

