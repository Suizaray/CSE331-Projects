"""
Project 2 - Hybrid Sorting - Tests
CSE 331 Spring 2024
Aman T., Daniel B., David R., Matt W.
"""

from collections.abc import MutableSequence
from collections import defaultdict
from random import seed, shuffle
import unittest

from solution import (selection_sort, bubble_sort, insertion_sort, hybrid_merge_sort, better_than_most, Score)

seed(331)


# Custom comparator used in all comprehensive testcases
def sum_digits(n: int):
    """Computes the sum of all digits in a number"""
    return sum(int(digit) for digit in str(n))


# Custom comparator used in all comprehensive testcases
def comp_sum_digits(x: int, y: int):
    """Compares two numbers by the sum of their digits"""
    return sum_digits(x) < sum_digits(y)


class Project2Tests(unittest.TestCase):

    def test_selection_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        selection_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(selection_sort(data))

    def test_selection_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        selection_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        selection_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_selection_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_selection_sort_comprehensive(self):
        # (1) sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1500))
        expected_data = sorted(data, key=sum_digits)
        selection_sort(data, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

    def test_bubble_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        bubble_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(bubble_sort(data))

    def test_bubble_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        bubble_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_bubble_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_bubble_sort_comprehensive(self):
        # (1) sort a lot of integers
        # Smaller than the other comprehensive tests; bubble sort is slow!
        data = list(range(500))
        shuffle(data)
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(500))
        expected_data = sorted(data, key=sum_digits)
        bubble_sort(data, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

    def test_insertion_sort_basic(self):
        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        insertion_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(insertion_sort(data))

    def test_insertion_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        insertion_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_insertion_sort_descending(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_insertion_sort_comprehensive(self):
        # (1) sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1500))
        expected_data = sorted(data, key=sum_digits)
        insertion_sort(data, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

    def test_hybrid_merge_sort_basic(self):
        # (1) test with basic list of integers - default comparator and threshold
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (2) test with basic set of strings - default comparator and threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator and threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # (4) test empty - default comparator and threshold
        data = []
        hybrid_merge_sort(data)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0))

    def test_hybrid_merge_sort_threshold(self):
        # first, all the tests from basic should work with higher thresholds

        # (1) test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (2) test with basic set of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # (4) now, for a longer test - a bunch of thresholds
        data = list(range(25))
        expected = sorted(data)
        for t in range(11):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comparator(self):
        # (1) sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        hybrid_merge_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # (2) sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        hybrid_merge_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_hybrid_merge_sort_descending(self):
        # (1) test with basic list of integers - default comparator, threshold of zero
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (2) test with basic list of strings - default comparator, threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (3) test with already sorted data - default comparator, threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # (4) test empty
        data = []
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual([], data)

        # (5) check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0, descending=True))

        # (6) now let's test with multiple thresholds
        data = list(range(50))
        expected = sorted(data, reverse=True)
        for t in range(20):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, descending=True)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comprehensive(self):
        # (1) sort a lot of integers, with a lot of thresholds
        data = list(range(500))
        for t in range(100):
            shuffle(data)
            expected = sorted(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

        # (2) sort a lot of integers with alternative comparator, threshold of 8
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1500))
        expected_data = sorted(data, key=sum_digits)
        hybrid_merge_sort(data, threshold=8, comparator=comp_sum_digits)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for expected, actual in zip(expected_data, data):
            expected_sum = sum_digits(expected)
            actual_sum = sum_digits(actual)
            self.assertEqual(expected_sum, actual_sum)

        # (3) sort a lot of integers with same comparator as above, thresholds in [1, ..., 49]
        # this comparator compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        data = list(range(1000))
        expected_data = sorted(data, key=sum_digits)
        for t in range(50):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, comparator=comp_sum_digits)
            for expected, actual in zip(expected_data, data):
                expected_sum = sum_digits(expected)
                actual_sum = sum_digits(actual)
                self.assertEqual(expected_sum, actual_sum)

    def test_hybrid_merge_sort_speed(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************
        # the point of this sort is to be fast, right?
        # this (probably) won't finish if you're not careful with time complexity,
        # but it isn't guaranteed
        data = list(range(300000))
        expected = data[:]
        shuffle(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

    def test_hybrid_merge_actually_hybrid(self):
        # *********************************************************
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # *********************************************************
        # this test is to make sure that the hybrid merge sort is actually
        # hybrid by calling insertion sort when appropriate

        calling_functions = defaultdict(set)

        class MyList(MutableSequence):
            # This class was taken from
            # https://stackoverflow.com/questions/6560354/how-would-i-create-a-custom-list-class-in-python
            def __init__(self, data=None):
                super(MyList, self).__init__()
                self._list = list(data)

            def __delitem__(self, ii):
                """Delete an item"""
                del self._list[ii]

            def __setitem__(self, ii, val):
                self._list[ii] = val

            def insert(self, ii, val):
                self._list.insert(ii, val)

            def __len__(self):
                """List length"""
                return len(self._list)

            def __getitem__(self, ii):
                import inspect
                calling_functions[inspect.stack()[1].function].add(len(self))
                if isinstance(ii, slice):
                    return self.__class__(self._list[ii])
                else:
                    return self._list[ii]

        data = MyList(range(50))
        hybrid_merge_sort(data, threshold=2)
        self.assertIn('insertion_sort', calling_functions)
        self.assertIn('hybrid_merge_sort', calling_functions)
        self.assertTrue(all(length <= 2 for length in calling_functions['insertion_sort']))
        self.assertAlmostEqual(len(calling_functions['hybrid_merge_sort']), 10, delta=2)

    def test_better_than_most(self):
        # Constants to represent the correct output
        MATH = 'Math'
        ENG = 'English'
        BOTH = 'Both'
        NONE = 'None'

        # (1) single score - student english median better than english median
        scores = [Score(600, 600)]
        expected = ENG
        actual = better_than_most(scores, Score(620, 580))
        self.assertEqual(expected, actual)

        # (2) three scores - student median better than both medians
        scores = [Score(600, 600), Score(700, 800), Score(650, 700)]
        expected = BOTH
        actual = better_than_most(scores, Score(680, 720))
        self.assertEqual(expected, actual)

        # (3) basic list of 5 scores - student math median better than math median
        scores = [Score(790, 200), Score(500, 500),
                  Score(610, 600), Score(800, 700), Score(700, 610)]
        expected = MATH
        actual = better_than_most(scores, Score(300, 620))
        self.assertEqual(expected, actual)

        # (4) basic list of 5 scores - student english median better than english median
        scores = [Score(600, 720), Score(300, 500),
                  Score(410, 600), Score(800, 800), Score(250, 500)]
        expected = ENG
        actual = better_than_most(scores, Score(420, 300))
        self.assertEqual(expected, actual)

        # (5) basic list of 5 scores - student median better than both medians
        scores = [Score(350, 720), Score(300, 500),
                  Score(410, 600), Score(800, 800), Score(250, 500)]
        expected = BOTH
        actual = better_than_most(scores, Score(420, 610))
        self.assertEqual(expected, actual)

        # (6) basic list of 5 scores - student median is not better than either median
        scores = [Score(350, 720), Score(300, 500),
                  Score(410, 600), Score(800, 800), Score(250, 500)]
        expected = NONE
        actual = better_than_most(scores, Score(200, 350))
        self.assertEqual(expected, actual)

        # Tests for EVEN length lists

        # (7)  empty list of scores
        scores = []
        expected = BOTH
        actual = better_than_most(scores, Score(600, 600))
        self.assertEqual(expected, actual)

        # (9) basic list of 6 scores - student math median better than math median
        scores = [Score(390, 100), Score(790, 200),
                  Score(500, 500), Score(610, 600),
                  Score(800, 700), Score(700, 610)]
        expected = MATH
        actual = better_than_most(scores, Score(300, 620))
        self.assertEqual(expected, actual)

        # (8) basic list of 6 scores - student english better than english median
        scores = [Score(150, 320), Score(600, 720),
                  Score(300, 500), Score(410, 600),
                  Score(800, 800), Score(250, 500)]
        expected = ENG
        actual = better_than_most(scores, Score(420, 300))
        self.assertEqual(expected, actual)

        # (9) basic list of 6 scores - student median better than both medians
        scores = [Score(350, 720), Score(300, 500),
                  Score(410, 600), Score(800, 800),
                  Score(250, 500), Score(300, 120)]
        expected = BOTH
        actual = better_than_most(scores, Score(420, 610))
        self.assertEqual(expected, actual)

        # (10) basic list of 6 scores - student is not better than either
        
        # English: Score(250, 500), Score(300, 500), Score(350, 720), Score(410, 600), Score(740, 620), Score(800, 800) 
        # Math: Score(300, 500), Score(250, 500), Score(410, 600), Score(740, 620), Score(350, 720), Score(800, 800)

        scores = [Score(740, 620), Score(350, 720),
                  Score(300, 500), Score(410, 600),
                  Score(800, 800), Score(250, 500)]
        expected = NONE
        actual = better_than_most(scores, Score(200, 350))
        self.assertEqual(expected, actual)

        # (11) longer list of scores - student english median is better than english median

        scores = [Score(800, 626), Score(621, 581),
                  Score(597, 421), Score(780, 674),
                  Score(481, 531), Score(623, 438),
                  Score(701, 786), Score(771, 571),
                  Score(745, 459), Score(549, 401),
                  Score(678, 576), Score(654, 796),
                  Score(664, 450), Score(426, 650),
                  Score(498, 501), Score(518, 565),
                  Score(552, 726), Score(615, 557),
                  Score(659, 475), Score(485, 699),
                  Score(505, 777), Score(575, 539),
                  Score(754, 780), Score(406, 621),
                  Score(422, 419), Score(604, 572),
                  Score(535, 792), Score(439, 520),
                  Score(548, 572), Score(674, 574)]
        expected = ENG
        actual = better_than_most(scores, Score(610, 570))
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
