"""
Project 4: Circular Double-Ended Queue
CSE 331 SS24
David Rackerby
tests.py
"""

import random
import unittest

from solution import CircularDeque, maximize_profits

random.seed(1342)

NAMES = ["Aaron", "Abhinay", "Aman", "Arhan", "Arnav", "Blake", "Daniel", "David", "Divya", "Ethan", "Gabriel", "Hank",
         "Hemanth", "Ilyas", "Jay", "Joel", "John", "Joseph", "Katelyn", "Lee", "Leo", "Maria", "Matt", "Nicole",
         "Scott"]


class CircularDequeTests(unittest.TestCase):
    def test_len(self):
        # Test 1 : length 0
        cd = CircularDeque()
        self.assertEqual(0, len(cd))

        # Test 2 : length 1
        cd = CircularDeque([1])
        self.assertEqual(1, len(cd))

        # Test 3 : length 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, len(cd))

        # Test 4 : length 50
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertEqual(50, len(cd))

    def test_is_empty(self):
        # Test 1 : Empty deque -> true
        cd = CircularDeque()
        self.assertTrue(cd.is_empty())

        # Test 2 : length 1 -> false
        cd = CircularDeque([1])
        self.assertFalse(cd.is_empty())

        # Test 3 : length 2 -> false
        cd = CircularDeque([1, 2])
        self.assertFalse(cd.is_empty())

        # Test 4 : length 50 -> false
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertFalse(cd.is_empty())

    def test_front_element(self):
        # Test 1: Empty deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.front_element())

        # Test 2: CD <1(F)> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.front_element())

        # Test 3: CD <2(F), 1(B)> -> 2
        cd = CircularDeque([2, 1])
        self.assertEqual(2, cd.front_element())

        # Test 4: CD <50(F), 49, ..., 1(B)> -> 50
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(50, cd.front_element())

        # Test 5: CD <10, 11, ..., 19(B), 0(F), 1, ... 9> -> 0
        # Start inserting from index 10
        cd = CircularDeque(list(range(20)), capacity=20, front=10)
        self.assertEqual(0, cd.front_element())

    def test_back_element(self):
        # Test 1: Empty Deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.back_element())

        # Test 2: CD <1(B)> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.back_element())

        # Test 3: CD <1(F), 2(B)> -> 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, cd.back_element())

        # Test 4: CD <50(F), 49, ..., 1(B)> -> 0
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(1, cd.back_element())

        # Test 5: CD <10, 11, ..., 19(B), 0(F), 1, ..., 9> -> 19
        # Start inserting from index 10
        cd = CircularDeque(list(range(20)), capacity=20, front=10)
        self.assertEqual(19, cd.back_element())

    def test_grow(self):
        """
        Tests grow functionality without use of enqueue
        Note that we call the grow function directly
        thus if you have a capacity check in your grow function this will fail
        """
        # Test (1) Empty Dequeue
        cd = CircularDeque()
        cd.grow()
        self.assertEqual(0, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual([None] * 8, cd.queue)

        # Test (2) Four element dequeue then grow
        cd = CircularDeque(NAMES[:4])
        cd.grow()
        self.assertEqual(4, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4] + [None] * 4, cd.queue)

    def test_grow_additional(self):
        """
        Additional test function for grow without use of enqueue
        Note that we call the grow function directly
        thus if you have a capacity check in your grow function this will fail
        """
        # Test (1) Reset front and back of wrap-around
        cd = CircularDeque(NAMES[:4])
        cd.front = 2
        cd.back = 1
        cd.grow()
        self.assertEqual(4, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(["Aman", "Arhan", "Aaron", "Abhinay"] + [None] * 4, cd.queue)

        # Test (2) Reset front and back of wrap-around
        cd = CircularDeque(NAMES[:8], capacity=8)
        cd.front = 1
        cd.back = 0
        cd.grow()
        self.assertEqual(8, cd.size)
        self.assertEqual(16, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(["Abhinay", "Aman", "Arhan", "Arnav", "Blake", "Daniel", "David", "Aaron"] + [None] * 8,
                         cd.queue)

        # Test (3) Reset front and back of wrap-around
        cd = CircularDeque(NAMES[5:8] + NAMES[:5], capacity=8)
        cd.front = 3
        cd.back = 2
        cd.grow()
        self.assertEqual(8, cd.size)
        self.assertEqual(16, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(NAMES[:8] + [None] * 8, cd.queue)

    def test_shrink(self):
        """
        Tests shrink without the use of dequeue
        NOTE: If you have a capacity/size check in your shrink this will fail since we call shrink directly
        """

        # Test 1, Capacity 8 -> 4
        cd = CircularDeque(NAMES[:4], capacity=8)
        cd.shrink()
        self.assertEqual(4, cd.capacity)
        self.assertEqual(4, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4], cd.queue)

        # Test 2, Capacity 16 -> 8
        cd = CircularDeque(NAMES[:8], capacity=16)
        cd.shrink()
        self.assertEqual(8, cd.capacity)
        self.assertEqual(8, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(NAMES[:8], cd.queue)

    def test_shrink_additional(self):
        """
        Test additional for shrink without using dequeue
        NOTE: If you have a capacity/size check in your shrink this will fail since we call shrink directly
        """
        # Test 1, Capacity 8 -> 4 with wrap-around index
        cd = CircularDeque(NAMES[2:4] + [None] * 4 + NAMES[:2], capacity=8)
        cd.front = 6
        cd.back = 1
        cd.size = 4
        cd.shrink()
        self.assertEqual(4, cd.capacity)
        self.assertEqual(4, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4], cd.queue)

        # Test 2, Capacity 16 -> 8 with wrap-around index
        cd = CircularDeque(NAMES[7:8] + [None] * 8 + NAMES[:7], capacity=16)
        cd.front = 9
        cd.back = 0
        cd.size = 8
        cd.shrink()
        self.assertEqual(8, cd.capacity)
        self.assertEqual(8, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(NAMES[:8], cd.queue)

    def test_front_enqueue_basic(self):
        """
        Tests front enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First')
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd.enqueue('Second')
        self.assertEqual(3, cd.front)  # Test 2
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['First', None, None, 'Second'], cd.queue)

        # Set deque capacity to 100, use name list which has length 14 thus we'll
        # never grow with unique insertion because math

        # Test 3: Front enqueue no wrap-around
        cd = CircularDeque(front=50, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual(49 - i, cd.front)
            self.assertEqual('Start', cd.back_element())  # back_element should never change
            self.assertEqual(50, cd.back)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 4: Front enqueue wrap-around
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual((100 - i) % 100, cd.front)
            self.assertEqual('Aaron', cd.back_element())  # back_element should never change
            self.assertEqual(0, cd.back)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_back_enqueue_basic(self):
        """
        Tests back enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First', front=False)
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd = CircularDeque(data=['First'], front=3)
        cd.enqueue('Second', front=False)
        self.assertEqual(3, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['Second', None, None, 'First'], cd.queue)

        # Test 3: Back enqueue normal (no wrap around) more elements
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual(i, cd.back)
            self.assertEqual('Aaron', cd.front_element())  # back_element should never change
            self.assertEqual(0, cd.front)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 4: Back enqueue wraparound (back < front) more elements
        cd = CircularDeque(front=99, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual((100 + i) % 100, cd.back)
            self.assertEqual('Start', cd.front_element())  # front_element should never change
            self.assertEqual(99, cd.front)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_front_enqueue(self):
        """
        Tests front_enqueue and grow functionality
        """
        # Test 1: Front_enqueue, multiple grows with 50 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element)
            # Test capacity of the dequeue while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the dequeue
        self.assertEqual(list(range(32, 0, -1)) + [None] * 14 + list(range(50, 32, -1)), cd.queue)
        self.assertEqual(50, cd.size)

        # Test 2: Front_enqueue, multiple grows with 64 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element)
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the cd
        self.assertEqual(list(range(64, 0, -1)) + [None] * 64, cd.queue)
        self.assertEqual(64, cd.size)
        self.assertEqual(128, cd.capacity)

    def test_back_enqueue(self):
        """
        Tests back_enqueue and grow functionality
        """
        # Test 1: 50 item, multiple grows
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 51)) + [None] * 14, cd.queue)
        self.assertEqual(64, cd.capacity)
        self.assertEqual(50, cd.size)

        # Test 2: 64 items, multiple grows
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 65)) + [None] * 64, cd.queue)
        self.assertEqual(128, cd.capacity)
        self.assertEqual(64, cd.size)

    def test_front_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue())

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue())
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([0, 1, 2])
        for i in range(3):
            self.assertEqual(i, cd.front)
            self.assertEqual(i, cd.dequeue())
            self.assertEqual(2 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [3, 0, 1, 2]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 3
        cd.back = 2
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.front)
            self.assertEqual(dequeue_result[i], cd.dequeue())
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue())

    def test_back_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue(False))

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue(False))
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([3, 2, 1, 0])
        for i in range(4):
            self.assertEqual(3 - i, cd.back)
            self.assertEqual(i, cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [0, 3, 2, 1]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 1
        cd.back = 0
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.back)
            self.assertEqual(dequeue_result[i], cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue(False))

    def test_back_dequeue(self):
        """
        Tests dequeue over shrinking conditions, does test size (length)
        Does not rely on enqueue functions
        """
        # Test 1: Begin with capacity 16, empty queue while checking all parameters
        cd = CircularDeque([i for i in range(15)], capacity=16)

        for item in range(15):
            self.assertEqual(14 - item, cd.dequeue(False))

            if item <= 9:  # shrunk 0 times
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:  # shrunk 1 time
                self.assertEqual(list(range(4)) + [None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:  # shrunk twice
                self.assertEqual([0, 1, None, None], cd.queue)
                self.assertEqual(4, cd.capacity)

            # ensure back is set correctly - note: pointers for an empty queue are up to implementation
            if cd.size != 0:
                self.assertEqual(13 - item, cd.back)

    def test_front_dequeue(self):
        """
        Tests dequeue along with shrinking
        Does not rely on enqueue functions
        """
        # Test 1: identical to above but removing from front rather than back
        cd = CircularDeque([i for i in range(15)], capacity=16)

        fronts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 1, 0, 1]

        for item in range(15):
            self.assertEqual(item, cd.dequeue())

            if item <= 9:
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:
                self.assertEqual([11, 12, 13, 14, None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:
                self.assertEqual([13, 14, None, None], cd.queue)

            if cd.size != 0:
                self.assertEqual(fronts[item], cd.front)

    def test_comprehensive(self):
        """
        A final (big) test for your dequeue
        This test is worth 0 points but is meant to help you debug your code
        """

        cd = CircularDeque()

        # (1) Grow a deque to a large size using enqueue
        for val in range(500):
            cd.enqueue(val, front=bool(val % 2))

        # (2) check that elements were successfully added
        for val in range(500):
            self.assertIn(val, cd.queue)

        # (2.5) intermediate size/cap check
        self.assertEqual(500, cd.size)
        self.assertEqual(512, cd.capacity)

        # (3) verify correct structure via dequeueing
        # (3.1) dequeue the first 499 elements and check
        for val in range(499, 0, -1):
            self.assertEqual(cd.dequeue(bool(val % 2)), val)
            self.assertNotIn(val, cd.queue[cd.front:cd.back+1] if cd.front <= cd.back else cd.queue[cd.front:]+cd.queue[:cd.back+1])
        # (3.2) dequeue the last element and check the empty deque
        self.assertEqual(cd.dequeue(bool(0 % 2)), 0)
        self.assertIsNone(cd.front)
        self.assertIsNone(cd.back)

        # (3.5) closing size/cap check
        self.assertEqual(0, cd.size)
        self.assertEqual(4, cd.capacity)

        # (4) dequeue from empty queue to check for crashes
        for val in range(10):
            self.assertIsNone(cd.dequeue(bool(val % 2)))

        # (4.5) final size/capacity check
        self.assertEqual(0, cd.size)
        self.assertEqual(4, cd.capacity)

    def test_maximize_profits(self):
        """
        Tests the application solution
        """
        # Test 1 small
        profits = [3, -8, 2]
        k = 2
        expected = 5
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 2 small
        profits = [1, -3, -2, 4, 0]
        k = 2
        expected = 3
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 2.5 small (increasing k) same input
        k = 3
        expected = 5
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 3 basic
        profits = [1, -1, -2, 4, -7, 3]
        k = 2
        expected = 7
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 4 basic
        profits = [10, -5, -2, 4, 0, 3]
        k = 3
        expected = 17
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 5 edge cases (start and end dates are the same)
        profits = [3]
        k = 1
        expected = 3
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 5.1 (large k) same input
        k = 10_000
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 5.2 (only two days)
        profits = [3, 2]
        k = 1
        expected = 5
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 5.3 (large k) same input
        k = 10_000
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 6 basic
        profits = [1, -5, -20, 4, -1, 3, -6, -3]
        k = 2
        expected = 0
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 7 basic
        profits = [100, -1, -100, -1, 100]
        k = 2
        expected = 198
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 8 basic
        profits = [100, -100, -300, -300, -300, -100, 100]
        k = 4
        expected = 0
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 9 large
        profits = [-5582, -5317, 6711, -639, 1001, 1845, 1728, -4575, -6066, -7770, 128, -3254, 7281, 3966, 6857, 5477,
                   8968, -1771, 9986, -6267, 9010, -764, 8413, -8154, 1087, -1107, 4183, 3033, 58, 659, 4625, 2825,
                   5031,
                   6811, 5657, 3229, 8597, -5772, 8869, 5723, 2960, 4040, 7222, 4841, -1014, 581, -2830, 3881, -3800,
                   577,
                   -7396, -611, -6944, 8461, 3294, 6297, 9713, -2246, -3441, 3831, -5754, 6716, 6040, -6715, 5763, 8611,
                   5412, -7630, 6216, 260, 2595, 6852, -8956, 2101, 6722, 1579, 3820, 7827, -3369, 7144, 1974, 7310,
                   -5369,
                   -6755, 3010, 5789, 1563, -3330, 5373, -2770, 4503, -4065, 8177, -3333, -4726, -2131, 2763, 9012,
                   -4755,
                   2382, 3642, -5284, -7174, -9815, 6392, 9729, -1943, -8749, 5343, 1036, 8508, 1484, 919, 4225, 3733,
                   8036, -6346, -2088, 475, 9378, 4271, -5906, 9327, 9399, -1582, 3845, 3499, -8912, -4671, -1143,
                   -5081,
                   -1621, -1287, 5995, 4963, 5071, 5118, -1966, -6249, 663, -2296, -8148, -4668, -6919, 334, -6609,
                   2888,
                   -4161, 118, -1867, 5629, 8588, -5325, -7853, -4868, -1487, -6544, -9697, -7038, 6422, -5545, 3376,
                   -8656, 8800, -7698, -2928, 2279, -9739, 4198, 6236, -9087, 9010, -9894, 2145, 7353, -92, 3205, 5431,
                   5913, 1619, -250, 4728, -7164, -5619, -4721, -9284, -9645, 146, 7131, -6501, 4261, 2016, 2880, 4944,
                   -8768, -6339, -3574, 539, 4633, 9188, 7227, -1549, 9271, 7110, 5706, 4968, -1275, 5545, -5844, -1985,
                   9560, 1560, 4630, 3169, 6076, -9433, 7007, 9927, -8385, -4557, -114, 9543, 2884, 8978, -6447, 3664,
                   -7499, -4643, -5993, -5321, 3250, -2945, 6216, -1606, 5569, 7326, -6027, 9723, -6997, -543, -8298,
                   -4647, 2563, 1493, 9574, 1087, -9433, -7749, -7159, -2682, 6626, 2787, -2845, -7907, -223, -8142,
                   -5403,
                   -3460, -2534, 5289, 999, 9404, -1958, 641, 4669, -2892, -2921, -7001, -1403, -2353, -7976, -5885,
                   4958,
                   -8117, 8785, -654, 5918, 5533, 8704, 5827, -7478, -3696, 2640, 1612, -500, 5694, -1973, 5308, 5272,
                   3358, 9190, 4648, -7836, 658, -3407, 6733, 1061, -2010, -2707, -1920, 1272, 3944, -6537, -6090,
                   -7429,
                   -640, 836, 1904, -4031, 814, -1886, 8040, -8312, -9407, -1395, -9944, -2074, -6814, 2672, 1360, 8990,
                   5465, -2131, 3838, 799, -3472, 1086, -583, 6302, 3032, 9138, -7778, 4538, -5337, 2087, 2870, -3005,
                   3401, 122, -819, -8074, 9630, -698, 5326, 2650, -9355, 6487, 3801, -3209, 8293, 662, -8318, -7863,
                   -3814, -2557, -5685, -7952, 6224, -7010, 2935, 5557, -1287, 9528, -9218, -5108, -2085, 17, 4870,
                   -8686,
                   -8854, -9657, 8848, -1883, -4535, 83, 9711, 4593, -3440, -6938, 3407, -6894, -6213, -883, 4552, -731,
                   1485, -7740, -3300, 3897, -7629, -4076, 7589, 3142, -1010, 2466, -592, -391, 3961, -7049, 7654, 5758,
                   6983, 6048, -4369, -5878, 3756, 2940, 9149, 8625, 8937, 5706, 6658, 9213, -5226, 284, -4524, -1577,
                   -5296, 6423, 9977, -1805, 5462, 7587, 476, -6424, 976, -3925, 8819, 1821, 3603, -842, -9618, -7130,
                   -6253, 2562, -7596, 3522, 6282, -3801, -3896, 6924, 441, 5944, 8535, 1253, -6154, 6872, -9548, -5358,
                   1604, 9593, -9256, -701, 1023, -1446, -1307, -6809, 9542, 3673, 1813, 8717, -6847, -5289, 5222,
                   -7266,
                   4231, 218, -9633, -4696, 5494, 9681, 1173, -4606, 2174, -1155, -8595, -3640, -6550, -7003, 4244,
                   -2543,
                   5241, 2831, 2690, 8950, -6609, -9724, 7562, -4096, 8878, 9962, 7179, -1170, 7826, -146, -2759, -5249,
                   253, 6206, 3205, -7708, 9448, 4622, 9260, -2853, 2486, 122, -8880, -769, -8922, 648, 7358, -6503,
                   -6382,
                   -4260, 3988, -5107, -6363, 2415, 8563, -9070, -5026, 2078, -2558, -2027, -7489, -4978, 5024, 4155,
                   -9737, -221, 9930, -9472, 1052, -268, 6221, 2726, -1310, -8708, 3482, -5488, -6506, 5389, -7048, 553,
                   -886, 2752, 85, -3938, 5940, -5112, 5855, -7295, 3735, 2657, 3269, 6231, 4771, 3229, -2009, -5748,
                   7256,
                   746, -4301, 752, -241, -6151, -2390, 9911, 825, -7679, -4960, -7224, -2739, -566, -5770, 6774, 6243,
                   3166, -783, -4303, -9016, 5555, -1866, -536, 8872, -3927, 4269, -3807, 1933, 9972, 981, 9256, 6857,
                   -208, 3645, -3725, 5961, 1105, 6320, -4702, -8419, -4904, -4935, 8378, -2994, 5831, 5296, 4730,
                   -9170,
                   -4229, -3911, -160, 8757, -5301, -3775, 1121, 9434, -9880, 2689, 2340, -7879, 3667, -5219, -6116,
                   -1670,
                   7595, 6900, 3990, 4444, 6385, -2924, 8968, -2673, -6182, 7503, 5209, 6030, 802, -3464, 1922, -8187,
                   1617, 4769, -4866, -3518, 5830, 3862, -7512, 5236, -5164, 6324, -5107, 6864, -7364, -1375, 5762,
                   -275,
                   4975, -7448, 5719, -3162, -1546, -2776, -9411, -1845, -4913, -3474, 2550, 5643, -5527, 2946, 7158,
                   1938,
                   5125, -8015, 2475, -1461, -4900, -5151, -4031, 9362, 8571, 9815, -8438, -6519, 1980, -8031, 9615,
                   7079,
                   -3573, -883, 4217, 1079, 5918, 1767, 8670, -5651, -6625, 1057, 7897, -7104, -4186, 851, -6333, -4108,
                   -3250, 7899, 9628, -6904, -3939, 4587, 1227, 3813, -7449, -7692, -8098, -9813, 8862, -2888, -1048,
                   -3564, 3074, 1437, -2291, 3974, 3164, 4921, -8958, 9007, -3938, 2042, 7454, -910, -998, -4450, -1103,
                   -237, 8182, -1391, -4255, -3482, -2918, 4053, 2280, -7403, 4319, -9457, 7157, -6315, -7533, 6309,
                   2211,
                   -9145, 443, 4255, -8847, -5557, -9089, 1752, -5784, -2399, -8296, -8400, 8170, 4628, -4583, 937,
                   -7067,
                   -3503, -549, -1194, 1576, 5004, -6963, -8837, 5567, 870, 3954, 5489, -8949, -7673, 8542, -9040,
                   -7689,
                   -4171, -889, 5552, -6836, -4393, 513, 3177, 6664, -5646, 2492, 9421, -342, 2570, 8816, 2869, -6820,
                   -3389, -1903, -3332, 138, 6618, 293, -9130, 3503, -2327, -9728, 7632, 5881, 540, 9678, -7629, 8804,
                   -2816, 7205, 7473, -5518, 7311, 3457, 9066, -1224, 2097, 7857, 6612, 186, 6759, -4516, -3491, -8268,
                   -8928, -7412, 7162, 6274, 5463, 2157, -4131, -7061, -8476, -5584, 7300, -4348, -5940, -8592, -302,
                   -5817, 3151, -4124, 1694, -5114, -3252, -2319, -2157, -293, 7724, -5673, 6105, 9535, 4333, 6353,
                   1290,
                   8710, -5035, 8995, -5865, 9746, 4708, -6387, -8937, 3096, -9716, -7124, 2531, -660, -4619, -8035,
                   3747,
                   -7821, 8793, -727, 8242, 4957, -7175, 4064, -9911, 4995, 9725, 1634, -4275, 788, -4920, 3831, -3525,
                   -4467, 2909, -1200, 5377, -4905, -3077, -1763, 4443, -3518, 3134, -5595, 5409, 5943, 6757, 3485,
                   2883,
                   -9261, -7221, 654, 2001, -926, 7840, -5568, 2715, -7053, -2082, -2005, 7607, -9511, 7545, 7564, 2380,
                   -7257, 1449, -3918, -3240, -1928, -6555, -4784, 1550, 2745, -5316]
        k = 56
        expected = 2354241
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 10 large
        profits = [122, -2920, 1798, 2421, -7678, -9915, 4320, -2000, -9548, 597, 8936, -9358, -6455, -7726, 2073,
                   -6663,
                   1692, -6049, 7086, 6556, -3851, 2229, 4559, 5206, -7787, -9155, -3245, 9256, 3611, -824, 4315, 7473,
                   3114, 5157, 7587, 1557, 4669, 7989, -218, 3401, -3125, -2048, 5370, 1400, -5237, -7032, -8641, 4352,
                   1629, 2465, -8563, -9017, -1026, -4173, 5364, -4536, -5932, -72, 9829, -1258, -2851, 6419, -2574,
                   -7016,
                   530, -1683, -6110, -1125, 1840, 1016, -1132, 1182, 4656, -7152, 5582, -8187, 1886, 3212, 4233, 4357,
                   -9575, 6296, -8957, 3862, -5852, -5324, 8833, 8524, 7539, -2600, 9462, -4339, 8798, -3992, -8367,
                   2108,
                   7453, -417, 3774, -9929, -7923, -4271, -2013, 2064, 6298, -8484, 1326, -5976, 3084, -2359, 8769,
                   4773,
                   8942, 6170, 5976, 2811, 5729, -6190, -8586, 1679, 5360, -288, -8812, 6095, -1925, -9241, -9614,
                   -5734,
                   -7241, 6009, -4365, 6289, 3118, -3706, -4178, -276, 8478, 2308, 530, 7092, -3753, 8659, 9214, -3315,
                   490, -5174, 5388, 5175, -9594, 3510, 3090, 8307, 2285, -141, -6180, -8067, 7132, -6010, -5869, -7063,
                   -8040, -6359, -1765, -7626, 310, 519, 180, -1969, -8832, 4021, -6416, 6907, 3997, -6163, 8854, 1643,
                   1948, -7314, 7365, 2801, -5467, 8881, 8946, -5075, -9173, 97, -8494, -1272, 8937, -9555, 4846, -8103,
                   9108, -4791, -1482, 5676, -9773, -8090, 5213, -1120, -5134, 3495, -8866, 2134, 8063, -980, -6785,
                   8527,
                   -2256, 1667, -4011, -1112, 4385, 823, -5881, 5120, 9221, 5020, 8779, -6911, -6773, -6492, -9569,
                   -5344,
                   7569, 2978, 764, -4126, -5557, 2125, -1516, 6111, 5163, -6171, -2255, -6969, 1314, -9761, 1809, 4941,
                   818, -7955, -9997, 4786, -1799, 325, -5192, 7103, 8185, 7932, -2441, 3971, -980, 8356, 8670, 1083,
                   -3384, -5976, -7204, -5421, 8214, 3339, 1166, 7744, 2934, 6059, -4570, -4115, -8947, -1087, -6579,
                   2345,
                   5423, 9177, -6461, 8056, 6595, 2085, 4103, 4020, 8250, 2887, 8409, 1104, -7105, 4617, -9401, -4199,
                   6050, 5978, -4432, 124, -8064, 3653, -3889, -2973, -4933, -8635, 3564, 2494, 5363, 1704, 5883, 4193,
                   8338, 1381, -3674, 7456, -2562, 8542, 9236, -1359, 7870, 9463, 9824, 7976, -1854, 6992, 4174, 9718,
                   -9535, 8085, -7278, 7543, 5108, -3992, -4699, -9787, -5361, 312, 3437, -9579, -8575, 2648, 4702,
                   1275,
                   6739, 3302, -6126, -3880, -6179, 2880, 1361, 7618, -7936, -5509, 4246, 610, -7184, -2450, 3701,
                   -7819,
                   4670, -4258, -6430, 7796, 7660, -4199, 3461, -6917, -2327, 2020, -4675, 9407, -7613, 3078, -6082,
                   1335,
                   6908, 4676, -6180, 2706, -6643, -714, -7122, -2017, -3377, 2413, 4275, 6847, -9655, -1448, -9924,
                   -7361,
                   -2400, -6232, 3949, 7406, 9737, 3761, -8771, 6060, 1845, 5717, -446, -5682, 6041, 461, -2502, 4019,
                   9256, 3326, 9201, 8623, -2373, 1057, 3575, 6198, 4142, -9247, -754, 1245, 3762]
        k = 743
        expected = 1082034
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)

        # Test 11 large
        profits = [-7622, 4131, 7439, -2974, -2663, -669, -4494, -9654, 8200, -1423, 1012, -5399, 7978, 5597, 4156,
                   1269, 5752, 6413, 7845, 6468, -2708, -2582, -2473, -1141, 2225, 4970, 1907, -4156, 1547, 515, -6515,
                   -7948, 4723, 7159, -208, -9331, 2182, 2163, 4143, -6634, -1341, 1365, -3940, 1654, -7759, 3755,
                   -8914, -2074, -2196, -6471, -1181, -4348, -3286, -8133, -9962, -8414, -2065, -6902, -6140, -4236,
                   2119, 9175, 6304, -2371, -1397, -6207, -2068, 245, 8186, -4801, -9801, 523, -8516, -8535, -8921,
                   986, -7736, 917, 3729, 5376, -7781, -8096, 112, -4801, -5053, -1975, -7434, 6048, -2763, -4995, 382,
                   -623, 3144, 9282, 9596, -1842, -4151, 5382, -9234, -8628, -3262, 7815, 1822, -1832, 7504, 1671,
                   9123, 3556, -8591, 852, -1532, 2187, -7890, -9172, 4549, 8099, 1991, -606, -3773, 7563, -211, 1231,
                   7057, -8568, 507, 3548, 4807, 917, -4038, -5476, 4656, 7961, -3677, 1615, -6729, 1817, 7709, 1546,
                   5243, 5591, 193, 2407, 3319, -3030, 2917, 2842, 2099, -9836, -5377, -6854, -2993, 8359, 9604, -8675,
                   9387, 4908, 8307, -7761, -1152, 129, 7618, 3838, 2014, 1934, -6755, 8865, 8777, -4127, 6342, 2476,
                   7002, -442, -7312, -7455, 1127, 9691, 5387, -904, 3385, -4165, -2821, 9663, 9008, -7629, 7807, 1162,
                   -9872, 1256, -15, -329, -6856, 4234,
                   -4821, -8776, -701, 7620, 4357, 2676, -6928, -2424, -2139, -1929, 5054, 3382, 6524, 749, 6176, 3439,
                   -1652, 2584, 5276, -5275, -1569, 8177, -3427, -1345, -2169, -3, 6504, -3242, -8556, 7536, 1434, 3233,
                   3053, 5896, -9001, 2737, -6662, 215, -3347, -1947, -7900, -8663, -833, 5085, -3647, -2711, 5841,
                   7269,
                   6194, -7867, 7909, 9877, 3742, -8832, 926, -360, -4137, -9435, 2956, -8219, -2530, -7418, 3501, 2796,
                   7044, -9552, -2184, -6011, 3288, -4472, -9205, -8032, 4208, -567, 1775, -2950, 3776, 8679, 8054,
                   -7973,
                   -5165, -158, -6207, -1279, -3379, -8371, -3334, -3694, 9768, 236, 3785, 8764, 6971, -1901, 2226,
                   -8868,
                   4795, 9763, -1264, 6291, -1777, 4207, 1636, -2133, 1922, 1159, 3944, 3925, -8555, -9445, 606, -6574,
                   -2042, 7775, 8769, 2326, 507, -1297, -3290, -3861, -1184, -4833, 2448, 6610, -3060, 5946, 9316,
                   -7709,
                   2120, -3767, 561, -7093, -6546, -1400, 581, 8453, -410, 6437, -7742, 5691, 5045, -3203, -1628, -7025,
                   -7812, 3870, 1714, 4988, 2669, -8119, 9178, -4510, -9805, 2817, 8677, -2374, -8097, -3934, 7536, 678,
                   2654, 9718, -5570, 4202, 2485, 8517, -7964, 8320, 9602, 1243, -4880, 3273, -3949, -2132, -2906,
                   -4817,
                   -3779, 1192, 6479, -6843, 8689, -9091, 2415, 9336, 6603, 7811, 5373, 2126, 6135, 1650, 8235, -3273,
                   2209, 2725, -5211, 5254, -6306, 2681, -8413, -4902, -5766, -3583, 7177, 2292, -9716, -4928, -8002,
                   9766,
                   7393, -1500, -9001, 4343, 9750, -2872, 4323, 7036, 6822, 6907, 1311, -197, -2493, -9135, -2842,
                   -5991,
                   -6384, 3828, 7727, -5035, 4234, -9708, -4310, -6079, -5965, 4366, 5877, 5122, -7984, 4728, 7359,
                   5274,
                   2689, 2809, 8316, 349, 3575, -6106, -5183, -8083, 650, 6596, 1388, -1468, -8118, 8700, 2356, -2605,
                   3825, -9160, -9769, -8180, -2831, 9219, -6564, -9246, 8422, -7080, 6669, -1054, -6123, -7619, 3901,
                   -2448, -9097, 1491, 9384, -5631, 4214, 6556, 4227, 4683, 5204, -2284, -6135, 7223, 7373, -3671, 2370,
                   -330, -5697, -5705, -6295, -7016, -860, -242, 3916, -9213, -5568, -7903, -2201, -2086, -2322, 2155,
                   2632, 3514, -6590, 5090, 4030, 3655, -3975, -3233, 5346, -9600, -5673, -1994, -5253, 9487, -6090,
                   1125,
                   360, 4840, 7555, -8382, -868, 6031, 1892, -1132, 7361, -2765, -3232, -5446, 8479, -6345, 8451, 4347,
                   -6726, -9611, -5408, -4226, 5767, -1359, 980, -5113, -3656, 1089, -8787, 751, -9950, -1233, 2591,
                   -9051,
                   2770, -9247, 2135, 1671, 4562, -9181, 760, 7333, 9463, 4615, -8531, -5105, -8997, -8917, -2119,
                   -1526,
                   4130, -8116, 428, -4960, -6746, 5245, 4239, -9682, 0, -5445, 6325, -2494, 3707, 1432, 3017, 9531,
                   5131,
                   -648, 2502, 9482, -2376, 1924, -4323, -6922, -1940, 4557, 4870, -8280, -8624, -1225, 9188, 457,
                   -4451,
                   -1879, 1024, 5554, 7911, 1952, -9987, 2431, -7259, -3090, 3186, -7979, -2869, -3588, -2984, 8502,
                   4346,
                   -9421, -3388, 8248, -3371, 3810, -3341, 7716, -1575, 94, -6752, 456, -9641, 7620, -745, -2204, 8773,
                   -1201, -678, 7773, -3927, 370, -4195, -4337, -916, 1171, 5888, 7362, 1832, 2413, 8683, -5835, -6350,
                   -2826, -1521, -6651, 814, -1456, -9420, -6943, 806, 259, 3916, 2341, 7456, -2144, 3793, -355, -892,
                   3428, -5367, -8549, -3033, 76, 3779, 8625, 7060, -9700, 178, -8565, 8894, -5115, 1948, 1805, -1157,
                   -5048, -7671, 7980, 3511, 8914, -1335, 5576, -6274, -6838, -9387, 8114, -4318, -5824, 6221, 5733,
                   2434,
                   6108, -3183, 3684, -5359, 394, 2567, 7276, -9106, -7819, -3018, 1582, 2240, -787, 3562, -3348, -6164,
                   306, -5418, 1610, 4351, 33, -4137, 3675, -2894, -9504, -1617, 2357, -228, -7390, -6662, 8349, -2545,
                   -3704, -7561, -7799, 820, -9509, 9179, 4376, -3967, -423, 8859, 6822, -638, -9344, -33, -2974, -3726,
                   9394, 279, 9057, -6554, 673, -6914, -5019, -557, -632, -4556, 6952, 8327, 7553, -4531, -3655, 8271,
                   9327, -938, 7449, 2112, -2435, 13, -3327, 7677, -8289, -6582, 9206, -7955, -6015, -7678, 4142, -9382,
                   431, 4325, -8026, -2229, 4453, -2046, 9986, -8213, 5182, 7148, -6869, -8932, -4907, -6791, 4722,
                   -7127,
                   -3651, 7287, 4839, -9833, -1779, -9332, -4581, -531, -5502, -6159, 9766, 2536, 224, 6060, 2436,
                   -3659,
                   -6798, 8364, -4348, -6894, 1324, -1198, 1299, 6779, -3810, -1042, -6795, -960, -1368, -5206, 9661,
                   -1318, 293, 9067, -5139, -1863, 8589, -7638, 9892, -7792, -5235, -3805, 7060, -9665, -7770, -5565,
                   5912,
                   4384, -6081]
        k = 690
        expected = 1892663
        actual = maximize_profits(profits, k)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
