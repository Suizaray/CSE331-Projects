"""
Project 4: Circular Double-Ended Queue
CSE 331 SS24
David Rackerby
solution.py
"""

from typing import TypeVar, List, Optional

T = TypeVar('T')


class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: Optional[List[T]] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    # ============ Modify Functions Below ============#

    def __len__(self) -> int:
        """
        Gives the length of the deque
        :return: the size of the deque (length)
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Gives T/F depending on whether the deque is empty or not
        :return: boolean True if not empty, False otherwise
        """
        return True if self.size == 0 else False

    def front_element(self) -> Optional[T]:
        """
        Gives the first element of the deque
        :return: the first element, None if it doesn't exist
        """
        if self.is_empty():
            return None
        return self.queue[self.front]

    def back_element(self) -> Optional[T]:
        """
        Gives the back element of deque
        :return: the back element, None if it doesn't exist
        """
        if self.is_empty():
            return None
        return self.queue[self.back]

    def grow(self) -> None:
        """
        Grows the list by a factor of 2 and resets the front and back pointers to the new default state
        :return: None
        """
        new_cap = self.capacity * 2
        new_queue = [None] * new_cap

        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]
        self.queue = new_queue
        self.capacity = new_cap
        self.front = 0
        self.back = self.size - 1

    def shrink(self) -> None:
        """
        Shrinks the list by a factor of 2 and resets the front and back pointers to the new default state
        :return: None
        """
        new_cap = max(4, self.capacity // 2)
        new_queue = [None] * new_cap

        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]
        self.queue = new_queue
        self.capacity = new_cap
        self.front = 0
        self.back = self.size - 1

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Adds a value to the front or back depending on "front" boolean of the deque
        :value: value to be added
        :front: boolean that decides add in front or back, Defaulted to True (add to front)
        :return: None
        """

        if self.size == 0:
            self.queue[0] = value
            self.front = 0
            self.back = 0
            self.size += 1
            return
        if not front:
            back_spot = (self.back + 1) % self.capacity
            self.queue[back_spot] = value
            self.size += 1
            self.back = back_spot
        else:
            front_spot = (self.front - 1) % self.capacity
            self.queue[front_spot] = value
            self.size += 1
            self.front = front_spot

        if self.capacity == self.size:
            self.grow()

    def dequeue(self, front: bool = True) -> Optional[T]:
        """
        Deletes a value from the front or back depending on "front" boolean of the deque
        :value: value to be deleted
        :front: boolean that decides delete from front or back, Defaulted to True (delete from front)
        :return: None
        """
        if self.is_empty():
            return

        if front:
            del_value = self.queue[self.front]
            self.front = (self.front + 1) % self.capacity
        else:
            del_value = self.queue[self.back]
            self.back = (self.back - 1) % self.capacity

        self.size -= 1

        if self.size <= self.capacity // 4 and self.capacity // 2 >= 4:
            self.shrink()

        if self.size == 0:
            self.front = self.back = None

        return del_value


def maximize_profits(profits: List[int], k: int) -> int:
    """
    On working interval "k", retrieve the maximum profit that is possible within the period
    :profits: list of all the profits in the given days
    :k: working interval, must work (earn/loss profit) at least once within 'k' days
    :return: maximum profit sum
    """
    if len(profits) == 0:
        return 0
    if len(profits) == 1:
        return profits[0]

    dq = CircularDeque(capacity=k)
    for i in range(len(profits) - 1):
        if not dq.is_empty() and dq.size >= k:
            dq.enqueue(profits[i] + dq.front_element(), False)
            curr_element = profits[i] + dq.front_element()
            dq.dequeue()
            if dq.front_element() < curr_element:  # failed decreasing order check
                dq.front = dq.back
                dq.size = 1
        else:
            if dq.is_empty():  # first element
                dq.enqueue(profits[0], False)
            else:
                dq.enqueue(profits[i] + dq.front_element(), False)
                if dq.front_element() < profits[i] + dq.front_element():
                    dq.front = dq.back
                    dq.size = 1

    return dq.front_element() + profits[-1]

profits = [1,-3,-5,-10,-15,-1,1]
print(maximize_profits(profits, 3))