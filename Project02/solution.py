"""
Project 2 - Hybrid Sorting
CSE 331 Spring 2024
Aman T., Daniel B., David R., Matt W.
"""

from typing import TypeVar, List, Callable


T = TypeVar("T")  # represents generic type


# This is an optional helper function but HIGHLY recommended,  especially for the application problem!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    Compares first and second variable in either descending or ascending with comparator lambda
    :param: first: first element to compare
    :param: second: second element to compare
    :param: comparator:lambda comparison that takes two variables of Type T and returns True
        when the first argument should be treated as less than the second argument.
    :param: descending: True if comparing in descending order, False if ascending. Defaulted to False
    :return: result of comparator lambda
    """
    if descending:
        return comparator(second, first)
    else:
        return comparator(first, second)


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in place through selection sorting, sorts ascending by default (False) and descending when descending
        variable is True
    :param: data: The list that is to be sorted
    :param: comparator: lambda comparison that takes two variables of Type T and returns True
        when the first argument should be treated as less than the second argument.
    :param: descending: True if comparing in descending order, False if ascending. Defaulted to False
    """
    for i in range(len(data)):
        # finding min element
        min_index = i
        for j in range(i + 1, len(data)):
            if do_comparison(data[j], data[min_index], comparator, descending):
                min_index = j
        # Perform swap
        data[i], data[min_index] = data[min_index], data[i]

def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Sorts the given list through bubble sort, given descending is True, sort in descending order.
    :param: comparator: lambda comparison that takes two variables of Type T and returns True
        when the first argument should be treated as less than the second argument.
    :param: descending: True if comparing in descending order, False if ascending. Defaulted to False
    """
    length = len(data)
    for i in range(length):
        for j in range(length - i - 1):
            if do_comparison(data[j+1], data[j], comparator, descending):
                data[j], data[j+1] = data[j+1], data[j]


def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sort the given list using insertion sorting method and perform the sort in descending order if descending is True.
    :param: data: List of items to be sorted
    :param: comparator: lambda comparison that takes two variables of Type T and returns True
        when the first argument should be treated as less than the second argument.
    :param: descending: True if comparing in descending order, False if ascending. Defaulted to False
    """
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and do_comparison(key, data[j], comparator, descending):
            data[j+1] = data[j]
            j -= 1
        data[j+1] = key

def merge(data: List[T], S1: List[T], S2: List[T], comparator: Callable[[T, T], bool], descending: bool):
    """
    Helper merge function for merge sort that performs the merging of the sub lists
    :param: data: list being merged into
    :param: S1: first half of the mergee
    :param: S2: second half of the mergee
    :param: comparator: lambda comparison that takes two variables of Type T and returns True
        when the first argument should be treated as less than the second argument.
    :param: descending: True if comparing in descending order, False if ascending. Defaulted to False
    """
    i = j = 0
    while i + j < len(data):
        if j == len(S2) or (i < len(S1) and do_comparison(S1[i], S2[j], comparator, descending)):
            data[i+j] = S1[i]
            i += 1
        else:
            data[i+j] = S2[j]
            j += 1
def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Sorts a list with merge sort when above threshold and insertion sort when at or below threshold value.
    :param: data: list to be sorted
    :param: threshold: value that decides when to switch to insertion sort
    :param: comparator: lambda comparison that takes two variables of Type T and returns True
        when the first argument should be treated as less than the second argument.
    :param: descending: True if comparing in descending order, False if ascending. Defaulted to False
    """
    comp = comparator
    des = descending
    length = len(data)
    if length <= threshold: #calls insertion sort when length below or equal to threshold
        insertion_sort(data, comparator = comp, descending = des)
    else:
        if length < 2:
            return
        thres = threshold
        mid = length // 2
        S1 = data[0:mid]
        S2 = data[mid:length]
        hybrid_merge_sort(S1, threshold = thres, comparator = comp, descending = des)
        hybrid_merge_sort(S2, threshold = thres, comparator = comp, descending = des)
        merge(data, S1, S2, comp, des)



def quicksort(data: List[T]) -> None:
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first: int, last: int) -> None:
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)


###########################################################
# DO NOT MODIFY
###########################################################

class Score:
    """
    Class that represents SAT scores
    NOTE: While it is possible to implement Python "magic methods" to prevent the need of a key function,
    this is not allowed for this application problems so students can learn how to create comparators of custom objects.
    Additionally, an individual section score can be outside the range [400, 800] and may not be a multiple of 10
    """

    __slots__ = ['english', 'math']

    def __init__(self, english: int, math: int) -> None:
        """
        Constructor for the Score class
        :param english: Score for the english portion of the exam
        :param math: Score for the math portion of the exam
        :return: None
        """
        self.english = english
        self.math = math

    def __repr__(self) -> str:
        """
        Represent the Score as a string
        :return: representation of the score
        """
        return str(self)

    def __str__(self) -> str:
        """
        Convert the Score to a string
        :return: string representation of the score
        """
        return f'<English: {self.english}, Math: {self.math}>'


###########################################################
# MODIFY BELOW
###########################################################

def better_than_most(scores: List[Score], student_score: Score) -> str:
    """
    Determines if a student's score is greater than the median SAT score in a list in math, english, both, or neither.
    :param: scores: list of SAT scores that will used to compare to the student score
    :param: student_score: score of the student in question
    :return: 'Math' if only math, 'English' if only english, 'Both' if both, and 'None' if neither is better
    """
    if len(scores) == 0:
        return 'Both'
    if len(scores) % 2 == 0: # if list is even, median would be the average of middle 2 in the list
        mid1 = len(scores) // 2
        mid2 = mid1 - 1
        # sort for math
        hybrid_merge_sort(scores, threshold= 2, comparator = lambda x, y : x.math < y.math)
        math_median_avg = (scores[mid1].math + scores[mid2].math) / 2
        # sort for eng
        hybrid_merge_sort(scores, threshold= 2, comparator = lambda x, y : x.english < y.english)
        eng_median_avg = (scores[mid1].english + scores[mid2].english) / 2
        if student_score.english > eng_median_avg:
            if student_score.math > math_median_avg:
                return 'Both'
            return 'English'
        elif student_score.math > math_median_avg:
            return 'Math'
        return 'None'

    mid = (len(scores) // 2)
    # sort for math
    hybrid_merge_sort(scores, threshold= 2, comparator = lambda x, y : x.math < y.math)
    math_median = scores[mid].math
    # sort for eng
    hybrid_merge_sort(scores, threshold= 2, comparator = lambda x, y : x.english < y.english)
    eng_median = scores[mid].english
    if student_score.english > eng_median:
        if student_score.math > math_median:
            return 'Both'
        return 'English'
    elif student_score.math > math_median:
        return 'Math'
    return 'None'


list = [1, 4, 3, 2, 8]
x = len(list)
selection_sort(list)