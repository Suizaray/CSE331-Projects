"""
Project 1
CSE 331 SS24 (Onsay)
Authors of DLL: Andrew McDonald, Alex Woodring, Andrew Haas, Matt Kight, Lukas Richters, 
                Anna De Biasi, Tanawan Premsri, Hank Murdock, & Sai Ramesh
solution.py
"""

from typing import TypeVar, List

# for more information on type hinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
Node = TypeVar("Node")  # represents a Node object (forward-declare to use in Node __init__)
DLL = TypeVar("DLL")


# pro tip: PyCharm auto-renders docstrings (the multiline strings under each function definition)
# in its "Documentation" view when written in the format we use here. Open the "Documentation"
# view to quickly see what a function does by placing your cursor on it and using CTRL + Q.
# https://www.jetbrains.com/help/pycharm/documentation-tool-window.html


class Node:
    """
    Implementation of a doubly linked list node.
    DO NOT MODIFY
    """
    __slots__ = ["value", "next", "prev", "child"]

    def __init__(self, value: T, next: Node = None, prev: Node = None, child: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        DO NOT MODIFY
        """
        self.next = next
        self.prev = prev
        self.value = value

        # The child attribute is only used for the application problem
        self.child = child

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        DO NOT MODIFY
        """
        return f"Node({str(self.value)})"

    __str__ = __repr__


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        DO NOT MODIFY
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        DO NOT MODIFY
        """
        result = []
        node = self.head
        while node is not None:
            result.append(str(node))
            node = node.next
            if node is self.head:
                break
        return " <-> ".join(result)

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        return repr(self)

    def __eq__(self, other: DLL) -> bool:
        """
        :param other: compares equality with this List
        :return: True if equal otherwise False
        DO NOT MODIFY
        """
        cur_node = self.head
        other_node = other.head
        while True:
            if cur_node != other_node:
                return False
            if cur_node is None and other_node is None:
                return True
            if cur_node is None or other_node is None:
                return False
            cur_node = cur_node.next
            other_node = other_node.next
            if cur_node is self.head and other_node is other.head:
                return True
            if cur_node is self.head or other_node is other.head:
                return False

    # MODIFY BELOW #
    # Refer to the classes provided to understand the problems better#

    def empty(self) -> bool:
        """
        Returns a boolean indicating whether the DLL is empty.
        :Returns: True if DLL is empty, else False.
        """
        if self.head is None:
            return True
        return False

    def push(self, val: T, back: bool = True) -> None:
        """
        Adds a Node containing val to the back (or front) of the DLL and updates size accordingly.
        :val: T: Value to be added to the DLL.
        :back: bool: If True, add val to the back of the DLL. If False, add to the front.
        :Returns: None
        """
        # checks if self is empty
        if self.head is None:
            self.head = Node(val)
            self.tail = self.head
        # adds new node into the back
        elif back is True:
            self.tail.next = Node(val)
            self.tail.next.prev = self.tail
            self.tail = self.tail.next
        # adds new node into the front
        else:
            self.head.prev = Node(val)
            self.head.prev.next = self.head
            self.head = self.head.prev
        self.size += 1

    def pop(self, back: bool = True) -> None:
        """
        Removes a Node from the back (or front) of the DLL and updates size accordingly.
        :back: bool: If True, remove from the back of the DLL. If False, remove from the front.
        :Returns: None.
        """
        if self.empty() is False:
            # check if self is only 1 node
            if self.head == self.tail:
                self.head = None
                self.tail = None
            # check for pop from back or front
            elif back is False:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
            self.size -= 1

    def list_to_dll(self, source: List[T]) -> None:
        """
        Creates a DLL from a standard Python list. Replaces Nodes if the DLL already had any.
        :source: list[T]: Standard Python list from which to construct DLL.
        :Returns: None.
        """
        # check for empty self
        if self.empty() is False:
            self.head = None
            self.tail = None
            self.size = 0
        # loop the list and push each element into self
        for i in source:
            self.push(i)

    def dll_to_list(self) -> List[T]:
        """
        Creates a standard Python list from a DLL.
        :Returns: list[T] containing the values of the nodes in the DLL.
        """
        if self.head is None:
            return []
        curr = self.head
        dll_list = []
        while curr:
            dll_list.append(curr.value)
            curr = curr.next
        return dll_list

    def _find_nodes(self, val: T, find_first: bool = False) -> List[Node]:
        """
        Construct list of Node with value val in the DLL
        Is not directly called
        :Returns: list[Node] containing the node/s found
        """
        if self.head is None:
            return []

        curr = self.head
        if find_first:
            while curr:
                if curr.value == val:
                    return [curr]
                curr = curr.next
        else:
            find_list = []
            while curr:
                if curr.value == val:
                    find_list.append(curr)
                curr = curr.next
            return find_list
        return []

    def find(self, val: T) -> Node:
        """
        Finds first Node with value val in the DLL
        :val: T: Value to be found in the DLL.
        :Returns: first Node object in the DLL whose value is val. If val does not exist in the DLL, return None.
        """
        single_find_list = self._find_nodes(val, True)
        if not single_find_list:
            return None
        return single_find_list[0]

    def find_all(self, val: T) -> List[Node]:
        """
        Finds all Node objects with value val in the DLL
        :val: T: Value to be found in the DLL.
        :Returns: standard Python list of all Node objects in the DLL whose value is val.
            If val does not exist in the DLL, returns an empty list.
        """
        all_find_list = self._find_nodes(val)
        return all_find_list

    def _remove_node(self, to_remove: Node) -> None:
        """
        Removes the specified node from the doubly linked list.

        This method is intended for internal use and should not be called directly.

        :to_remove: The node to be removed from the doubly linked list.

        :Returns: None
        """
        if to_remove == self.head and self.head == self.tail:
            self.head = None
            self.tail = None
        elif to_remove == self.head:
            self.head = to_remove.next
            self.head.prev = None
        elif to_remove == self.tail:
            self.tail = to_remove.prev
            self.tail.next = None
        else:
            pred = to_remove.prev
            succ = to_remove.next
            pred.next = succ
            succ.prev = pred
        self.size -= 1

    def remove(self, val: T) -> bool:
        """
        removes first Node with value val in the DLL.
        :val: T: Value to be removed from the DLL.
        :Returns: True if a Node with value val was found and removed from the DLL, else False.
        """
        if self.empty():
            return False
        curr = self.head
        while curr:
            if curr.value == val:
                self._remove_node(curr)
                return True
            curr = curr.next
        return False

    def remove_all(self, val: T) -> int:
        """
        removes all Node objects with value val in the DLL.
        :val: T: Value to be removed from the DLL.
        :Returns: number of Node objects with value val removed from the DLL. If no node containing val exists in the DLL, returns 0.
        """
        if self.empty():
            return 0
        curr = self.head
        count = 0
        while curr:
            if curr.value == val:
                self._remove_node(curr)
                count += 1
            curr = curr.next
        return count

    def reverse(self) -> None:
        """
        Reverses the DLL in-place
        :Returns: None.
        """
        curr = self.head
        temp_tail = self.tail
        self.head = temp_tail
        self.tail = curr
        while curr:
            pred = curr.prev
            succ = curr.next

            curr.prev = curr.next
            curr.next = pred

            curr = succ

def dream_escaper(dll: DLL) -> DLL:
    """
    Turns a multilevel dll into a single level dll
    Child nodes are placed after the parent node but before the parent.next node in the final DLL.

    :dll: DLL: A DLL where each Node holds a value of str where the string is the task. The Node may also hold a child in .child and store the child DLL to the current node.
    :Returns: a DLL holding str representing the names of all of the tasks
    """
    if dll.empty():
        return dll
    curr = dll.head
    flat_dll = DLL()
    #list to store where the entry point of a new level was
    parent_list = []
    while curr:
        #push when curr has no child
        if not curr.child:
            flat_dll.push(curr.value)
            #go next
            curr = curr.next
        #check to make sure curr isn't None (so it doesn't break on curr.child check
        if curr:
            #check is there is a child
            if curr.child:
                flat_dll.push(curr.value)
                #check if the parent level has more to go
                if curr.next:
                    parent_list.append(curr)
                curr = curr.child
        #checks to see if at the end of a level and if there is an old level that still has more to go
        if curr is None and len(parent_list) != 0:
            curr = parent_list[-1]
            parent_list.pop()
            curr = curr.next

    return flat_dll

