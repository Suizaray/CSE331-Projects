# Project 2: Sorting Algorithms

**Due Thursday, Feb 8th @ 9:00 PM ET**

*This is not a team project, do not copy someone else's work.*

*Make sure to read the entire project description, especially the grading policies.*

## Background Information

![](img/sorting_comparison.png)

A **sorting algorithm** is an algorithm that puts elements in
a [certain order](https://en.wikipedia.org/wiki/Total_order). Such algorithms are often used to organize an array or
list in numerical or lexicographical order. However, their use is not limited in scope to such simple orderings, a fact
that will be demonstrated in this project.

Throughout the 20th century, as the domain of problems to which computers were applied grew, so too did the size of data
sets that required sorting. This resulted in the rapid development of sorting algorithms. Simple *O(n^2)* algorithms,
such as selection and bubble sort, were supplemented by faster *O(n log(n))* algorithms, such as quick or merge sort.
Still, these *O(n^2)* algorithms have their place to this day because they are often faster for sorting small sets of
data. Optimized modern sorting methods use hybrid techniques, which leverage the recursive nature of quicksort or merge
sort by using these algorithms for large sets of data, but which use an algorithm such as insertion sort for the
smaller fragments of data that the input ends up being separated into.

This project will expose you to insertion sort, selection sort, bubble sort, merge sort, and quicksort. Additionally, it
will include a hybrid sort using merge and insertion sorts. Python's built in `list.sort` is actually based on
a ([somewhat more advanced](https://hg.python.org/cpython/file/tip/Objects/listsort.txt)) merge/insertion hybrid sort.

In addition to the overviews of each sort presented below, we encourage you to refer to the relevant sections in Zybooks. 

### Bubble Sort

![](img/bubble_sort.png)

Bubble sort is one of the simplest sorting algorithms, and it works by repeatedly traversing a list and swapping
adjacent elements whenever it finds two that are out of order. This traversal is then repeated until a complete
traversal is completed without having to do any swaps, which indicates that the list has been sorted.

Like selection and insertion sorts, it has *O(n^2)* worst/average case
time complexity, and can operate in-place for *O(1)* auxiliary space complexity. Bubble sort, however, tends to be the
slowest of the sorting algorithms mentioned here in practice.

### Insertion Sort

![](img/insertion_sort.png)

Insertion sort works by keeping track of sorted and unsorted portions of the list, and building up the sorted portion on
the lefthand side of the list. To start, the first element is considered sorted (a single-element list is always
sorted), and the remainder of the list is the unsorted portion. Next, the first element of the unsorted portion is
compared to each element of the sorted portion in reverse order until its proper place in the sorted portion is found.
Finally, the element from the unsorted portion is *inserted* into the list at the proper spot, which for arrays requires
a series of swaps. Each of these insertion steps increases the size of the sorted section by one, allowing the algorithm
to proceed with a new "first element of the unsorted section" until the entire list has been sorted.

Insertion sort has  *O(n^2)* worst/average case *O(n)* for the best case, and the same space complexity as bubble sort, but ittends to be a bit faster in practice. Insertion sort is especially well suited to sorting small lists.

### Selection Sort

![](img/selection_sort.png)

Selection sort works quite similarly to insertion sort, keeping a sorted and unsorted portion of the list, and building up the sorted portion one element at a time. The difference with selection sort is that instead of taking the first
element of the unsorted portion and inserting it at the proper spot, selection sort *selects* the smallest element of the unsorted portion on each pass, and puts it at the end of the sorted portion. This time, the entire list starts out
as the unsorted portion instead of the first element being sorted–the starting element of the sorted portion has to befound from the list like every other element since elements don't move after being put in the sorted portion.

To highlight the difference: insertion sort picks a spot for the next element by searching through the sorted portion,
selection sort picks an element for the next spot by searching through the unsorted portion.

Selection sort has identical time/space complexity for the worst case just like  bubble and insertion sorts, and like insertion sort is faster than
bubble sort. Still, insertion sort is usually preferred for small-data sorting.

### Merge Sort

![](img/merge_sort.png)

Merge sort is a more efficient algorithm than the three mentioned above. It works on the principle of [Divide and Conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm), repeatedly breaking down a list
into several sublists until each sublist consists of a single element, then repeatedly merging pairs of these sublists
in a manner that results in a sorted list.

Unlike bubble, insertion, and selection sorts, merge sort is worst case *O(n log(n))*, so it scales much better to large
lists. While there are ways to write an in-place merge sort, the typical space complexity is [*O(n)*](https://stackoverflow.com/a/28641693).

### Quicksort

Quicksort is an advanced sorting algorithm which works differently from the others we've seen so far. Like merge sort,
it is recursive, but for each step a "pivot" element from the list is selected, and elements to the left and right of the pivot are swapped as needed so that the list is partitioned into elements less than the pivot and elements greater
than or equal to the pivot. Quicksort is then applied recursively to these partitions until the list is fully sorted.

Like merge sort, quicksort is average case *O(n log(n))*, but its worst case performance is *O(n^2)*. 
The performance of quicksort depends heavily on the method used for pivot selection, with the 
[median-of-three pivot selection algorithm](https://stackoverflow.com/a/7560859)
helping to avoid pitfalls common in more naive (e.g., random, first, last) selection techniques. 

In practice, quicksort is still popular because it performs well on array-backed lists by exploiting optimizations for [locality of reference](https://en.wikipedia.org/wiki/Locality_of_reference). 
Merge sort may outperform it for very large data sets, and is usually preferred for linked lists. Both of these algorithms are significant improvements on the average case *O(n^2)* algorithms mentioned above.

### Hybrid Sorting

While merge sort has a better runtime complexity than insertion sort, it has some overhead from not being an in-place
sort, and insertion sort tends to be faster for sorting small amounts of data. This means that it is more efficient to
combine the two algorithms into a hybrid sorting routine, where the recursive list partitions that merge sort creates
are sorted by insertion sort instead of merge sort once they get small enough.


### **Auxiliary Space Complexity: An Overview**

Auxiliary space complexity refers to the amount of additional space, aside from the input, that an algorithm or a method requires to execute. This is especially important when evaluating the efficiency of algorithms. It's different from the space complexity in that it doesn't consider the space required by the inputs; instead, it looks only at the extra space (temporary space) taken up, typically for variables, temporary structures, etc.




## Project Details


### **"There's a term for people who don't read the project details: unemployed" - Dr. Owen**

### Overview

In this project, you will be implementing: the bubble, insertion, selection, and merge sort algorithms. We will provide the completed code for the quicksort algorithm for your reference. While you don't have any assignment relating to the quicksort code on this project, we recommend looking through it to familiarize yourself with that algorithm. Multiple questions regarding quick sort 
will appear on your exam, so it is in your best interest to take some time to understand it. The merge sort that you implement will be a hybrid merge sort which defers to insertion sort for handling small lists.

All the sorting algorithms should accept a custom `comparator` argument which substitutes for `<` when comparing
items to put in the list. If calling `comparator(a, b)` returns `True`, you should read that result as "`a` should come before `b` in a sorted list."

There is also an argument `descending` which defaults to `False`. If
the `descending` argument is `True`, you should sort the list in descending order. Since you can sort the list in
descending order by flipping the order of the inputs of the comparator and leaving the other logic the same, it might be
helpful for you to write a *helper function*, perhaps called `do_comparison`, which takes elements `a` and `b`, the `comparator`, and `descending` as arguments, and tells you whether or not to put `a` before `b` in the sorted list. This helper function should only be a few lines!
Implementing this function is **highly recommended** as it greatly simplifies the logic in your sorting functions.

It is important to note that ***the comparator means strictly `<` and not `<=`***, so for descending you should
consider `comparator(b, a)` instead of `not comparator(a, b)`, since the second one would give you `a >= b` instead of 
`a > b`. If you did it the second way, your bubble sort might never stop swapping!

You can call the argument `comparator` the same as any other function, and the underlying function that gets called will
be whatever function was passed in for this argument. This takes advantage of the fact that Python has what are
called [first-class functions](https://en.wikipedia.org/wiki/First-class_function), meaning functions can be stored and
passed around the same way as any other type of value. The type of `comparator` is explained by this diagram:

![](img/comparator_diagram.png)

Also note that some arguments will be specified after the pseudo-argument `*,`. 
The arguments following the asterisk `*` are ["keyword-only" arguments](https://www.python.org/dev/peps/pep-3102/).
Keyword-only arguments are designed to prevent accidental miscalls that can occur with positional parameters.

```python
# Note the "argument" *, which some of the other arugments come after
def some_func(a, b, *, c, d):
    pass

# Ok
some_func(1, 2, c=3, d=4)

# will raise TypeError: some_func() takes 2 positional arguments but 4 were given
some_func(1, 2, 3, 4)
```

### Tips, Tricks, and Notes

- There are different ways to implement merge sort, but make sure you are aiming for a solution that will fit the time
  complexity! If your recursive calls are some form of `hybrid_merge_sort(data[1:])`, this will not be *O(n log(n))*, as this does not divide the input list in half.
- A recursive implementation of merge sort will be the easiest to write. As you split the arrays, you should switch to
  insertion sort as soon as the split arrays get smaller than threshold. This means each of the recursive calls should
  be using the same threshold, such that the threshold is considered at each recursive call.
- Make sure to pass `comparator` and `descending` properly for all recursive calls as well.
- Using a helper function to do your comparisons that takes `descending` into account will make your code much easier
  to write. Look at the `do_comparison` stub that's provided in the starter code.
- Try these web applications to visualize sorting algorithms:
  - <https://visualgo.net/bn/sorting>
  - <https://opendsa-server.cs.vt.edu/embed/mergesortAV> (good merge sort visualization)
  - <https://www.cs.usfca.edu/~galles/visualization/ComparisonSort.html>

### Assignment Specs

You will be given one file to edit, `solution.py`. You must complete and implement the following functions. Take note of
the specified return values and input parameters. 

***DO NOT USE BUILT-IN SORT FUNCTIONS LIKE `list.sort()` or `sorted()` FOR THIS PROJECT IN ANY FUNCTION! ANY FUNCTION THAT USES A BUILT-IN SORT WILL LOSE ALL AUTO AND MANUAL GRADE FOR THAT FUNCTION.***

***Do not change the function signatures, including default values.***

***If you implement a function that passes the tests but does not use the specified sorting algorithm for that function*,
*you will not get **any** points for that function.***

Make sure to consult the lectures, Zybooks, and other resources available if
you are not sure how a given sorting algorithm works. To earn manual points, you must also meet the required time and
space complexity. Using the right algorithm will help!

**solution.py:**
- **selection_sort(data: List[T], \*, comparator: Callable[[T,T], bool], descending: bool = False)**
  - Given a list of values, sort that list in-place using the selection sort algorithm and the provided comparator,
    and perform the sort in descending order if `descending` is `True`.
  - **param data**: List of items to be sorted
  - **param comparator**: A function which takes two arguments of type `T` and returns `True` when the first argument
    should be treated as less than the second argument.
  - **param descending**: Perform the sort in descending order when this is `True`. Defaults to `False`.
  - Time Complexity: *O(n^2)*
  - Aux.Space Complexity: *O(1)*


- **bubble_sort(data: List[T], \*, comparator: Callable[[T,T], bool], descending: bool = False)**
  - Given a list of values, sort that list in-place using the bubble sort algorithm and the provided comparator,
    and perform the sort in descending order if `descending` is `True`.
  - **param data**: List of items to be sorted
  - **param comparator**: A function which takes two arguments of type `T` and returns `True` when the first argument
    should be treated as less than the second argument.
  - **param descending**: Perform the sort in descending order when this is `True`. Defaults to `False`.
  - Time Complexity: *O(n^2)*
  - Aux.Space Complexity: *O(1)*
  

- **insertion_sort(data: List[T], \*, comparator: Callable[[T,T], bool], descending: bool = False)**
  - Given a list of values, sort that list in-place using the insertion sort algorithm and the provided comparator,
    and perform the sort in descending order if `descending` is `True`.
  - **param data**: List of items to be sorted
  - **param comparator**: A function which takes two arguments of type `T` and returns `True` when the first argument
    should be treated as less than the second argument.
  - **param descending**: Perform the sort in descending order when this is `True`. Defaults to `False`.
  - Time Complexity: *O(n^2)*
  - Aux.Space Complexity: *O(1)*


- **hybrid_merge_sort(data: List[T], \*, threshold: int = 12, comparator: Callable[[T,T], bool], descending: bool = False)**
  - Given a list of values, sort that list using a hybrid sort with the merge sort and insertion sort
    algorithms and the provided comparator, and perform the sort in descending order if `descending` is `True`.
    The function should use `insertion_sort` to sort lists once their size is less than or equal to `threshold`, and
    otherwise perform a merge sort. DO NOT hardcode the threshold check such as `if threshold == {any value}`. Hint: Think about what should happen for lists with only one item.
  - **IMPORTANT**: Every semester there are students that don't actually implement a hybrid sort. These students generally make one of these mistakes:
    1. Check the threshold only once in hybrid_sort, and not for _every_ recursive call of merge_sort (if implemented separately).
    2. Call insertion_sort in each recursive call of merge sort, regardless of threshold
    3. Call merge_sort regardless of threshold
    4. Forget to pass threshold to each call of merge_sort
  - **param data**: List of items to be sorted
  - **param threshold**: Maximum size at which insertion sort will be used instead of merge sort. **Students frequently make mistakes with this, so be careful!**
  - **param comparator**: A function which takes two arguments of type `T` and returns `True` when the first argument
    should be treated as less than the second argument.
  - **param descending**: Perform the sort in descending order when this is `True`. Defaults to `False`.
  - Time Complexity: *O(n log(n))*
  - Aux. Space Complexity: *O(n)*
    

## Application Problem: SAT Score Analyzer

![SAT score logo](img/sat_logo.jpg)
<a href="https://www.google.com/url?sa=i&url=https%3A%2F%2Fhighered.collegeboard.org%2Fassessments&psig=AOvVaw27mXvKUdnttaCe6UBT-NPa&ust=1705501891255000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCOiUlOaP4oMDFQAAAAAdAAAAABAD"> Image Source</a>

### Background:

In order to gauge a high school student's readiness for college, it is common practice for them to undergo standardized testing. One of the most popular standardized tests is the "Scholastic Assesment Test", also known as, the "SAT". These tests are based on a score out of 1600 and comprise of two major sections: **English** and **Math**.

Most colleges and universities in the United States encourage students to submit scores to this test as part of the application process, including Michigan State University. MSU only wants the best and brightest students to become Spartans (like you!), therefore the admissions office must work day and night reviewing applications, test scores, and essays. 

To make their lives easier, they've asked the CSE 331 team to assist in labeling prospective MSU students SAT scores based on the median of SAT scores from the pool of applicants. This is where you come in!

### Challenge:

Your job is to determine if a selected student's SAT score (or part of it) is greater than the median of current MSU student's SAT scores.

*Remember that the median is the middle value of dataset, or if there are an even number of items, the average of the middle 2 elements.* 

**Note**: Refrain from using built-in sort functions or the provided quicksort function (although the ones discussed previously are permissible).

You are given the class described below. **DO NOT** modify this class - any modification will result in zero for this portion of the project.
<hr>

**class Score:**

*DO NOT MODIFY the following attributes/functions*

- **Attributes:**  
  -  **english**: **int**: English portion of total score
  -  **math**: **int**:  Math portion of total score


- **\_\_init\_\_(self, english: int, math: int) -> None**
  - Constructs a **Score** object
  - **param english**: value to assign as english score
  - **param math**: value to assign as math score
  - **return: None**


- **\_\_repr\_\_(self) -> str**
  - Returns the Score as a string representation (for debugging)
  - **return: string**


- **\_\_str\_\_(self) -> str**
   - Returns the Score as a string representation
   - **return: string**



***MODIFY BELOW***:

<hr>

*NOTE: For general information regarding the behavior of a comparator in this project refer to the [project overview](#overview).*

```python
def better_than_most(scores: List[Score], student_score: Score) -> str:
```
- **Input**:
  - **scores: List[Score]**: A list of Score objects representing the SAT score of every student.
  - **student_score: Score** A Score object representing a student's SAT score broken into two values: English and Math. 
  
- **Output**: A string which is one of:
    - `'Both'` if the student's English and Math scores are above the median.
    - `'Math'` if only their Math score is above the median. 
    - `'English'` if only their English score is above the median. 
    - `'None'` if neither score is above the median. 

- **Complexity**:
    - Time: *O(nlogn)*
    - Space: *O(n)*

### Sample Scenarios:

#### Scenario 1
```python
scores = [Score(600, 600)]
output = better_than_most(scores, Score(620, 580))
# Expected: 'English'
```
**Explanation**: Since there is only one item, the median of English and Math are both 600. Since only the English score of the student is above the median, 'English' is returned.

#### Scenario 2
```python
scores = [Score(600, 600), Score(700, 800), Score(650, 700)]
output = better_than_most(scores, Score(680, 720))
# Expected: 'Both'
```
**Explanation**: The median of all the English scores is 650, and the median of all Math scores is 700. The student's English score (680) is greater than the median of 650, and the student's Math score (720) is greater than the median of 700, therefore 'Both' is returned. 

#### Scenario 3
```python
scores = []
output = better_than_most(scores, Score(600, 600))
# Expected: 'Both'
```
**Explanation**: Since there is no median, the function returns 'Both'.

#### Scenario 4
```python
scores = [Score(390, 100), Score(790, 200),
                  Score(500, 500), Score(610, 600),
                  Score(800, 700), Score(700, 610)]
output = better_than_most(scores, Score(300, 620))
# Expected: 'Math'
```
**Explanation**: The median of the English scores is 655 and the median of the Math scores is 550. Therefore, the student's SAT score is better than the median of math scores and the function returns 'Math'.

**Application Problem Notes:**
-----
- Keep in mind that objects of the Score class are custom objects with multiple attributes. In order to sort custom objects in Python (within the scope of this project), you **MUST** pass a custom comparator to the desired sorting method.

- There are various approaches to creating a custom comparator that can be used by the sorting methods implemented in this project; You could use <a href="https://www.w3schools.com/python/python_lambda.asp">Python Lambda functions</a>, helper functions, or even inner functions. 

- Refer to the default parameters of the various sorting functions implemented in this project (except quicksort) to see a basic example of a comparator.

**Application Problem Authors**: *David Rackerby, Matt Wright, Aman Dhruva Thamminana, Daniel Berezovsky*




## **Submission Guidelines**

### **Deliverables:**

For each project, a `solution.py` file will be provided. Ensure to write your Python code within this file. For best results:
- 📥 **Download** both `solution.py` and `tests.py` to your local machine.
- 🛠️ Use **PyCharm** for a smoother coding and debugging experience.

### **How to Work on a Project Locally:**

Choose one of the two methods below:

---

#### **APPROACH 1: Using D2L for Starter Package**
1. 🖥️ Ensure PyCharm is installed.
2. 📦 **Download** the starter package from the *Projects* tab on D2L. *(See the tutorial video on D2L if needed)*.
3. 📝 Write your code and, once ready, 📤 **upload** your `solution.py` to Codio. *(Refer to the D2L tutorial video for help)*.

---

#### **APPROACH 2: Directly from Codio**
1. 📁 On your PC, create a local folder like `Project01`.
2. 📥 **Download** `solution.py` from Codio.
3. 📥 **Download** `tests.py` from Codio for testing purposes.
4. 🛠️ Use PyCharm for coding.
5. 📤 **Upload** the `solution.py` back to Codio after ensuring the existing file is renamed or deleted.
6. 🔚 Scroll to the end in Codio's Guide editor and click the **Submit** button.

---

### **Important:**
- Always **upload** your solution and **click** the 'Submit' button as directed.
- All project submissions are due on Codio. **Any submission after its deadline is subject to late penalties** .
  
**Tip:** While Codio can be used, we recommend working locally for a superior debugging experience in PyCharm. Aim to finalize your project locally before submitting on Codio.



### Grading

The following 100-point rubric will be used to determine your grade on Project 2:

- Policies
  - ***Making all of these policies bold or italic would get too visually fatiguing but read them all because they're
    important!***
  - Using a different sorting algorithm than the one specified for some function will result in the loss of all
    automated and manual points for that function.
  - Not making the merge sort ***hybrid*** will result in the loss of half of all automated and manual points for that
    function.
  - You will not receive any points for that function if you use Python's built-in sorting functions or sorting functions
    imported from any library.
  - You will not receive any points on the project if you use any list-reversing function such as `reversed`,
    `list.reverse`, or a homemade alternative to these. You must sort the lists in ascending or descending order
    directly.



**Important Note about Using Sorts on the Application Problem:**

- You **must** use a sort that you have implemented yourself.
- Using the provided full implementation of QuickSort will result in **zero points**.
- If you opt to use QuickSort, all points (both manual and auto-graded) will be **deducted**.


    

- Tests (70)
- Sorts: __/50
    - Selection: __/11
      - test_selecton_sort_basic: __/3
      - test_selection_sort_comparator: __/3
      - test_selection_sort_descending: __/3
      - test_selection_sort_comprehensive: __/2
    - Bubble: __/11
      - test_bubble_sort_basic: __/3
      - test_bubble_sort_comparator: __/3
      - test_bubble_sort_descending: __/3
      - test_bubble_sort_comprehensive: __/2
    - Insertion: __/11
      - test_insertion_sort_basic: __/3
      - test_insertion_sort_comparator: __/3
      - test_insertion_sort_descending: __/3
      - test_insertion_sort_comprehensive: __/2
    - Hybrid Merge: __/17
      - test_hybrid_merge_sort_basic: __/3
      - test_hybrid_merge_sort_threshold: __/4
      - test_hybrid_merge_sort_comparator: __/4
      - test_hybrid_merge_sort_descending: __/4
      - test_hybrid_merge_sort_comprehensive: __/2
      - test_hybrid_merge_sort_speed: __/0
        - This test helps checking if your hybrid merge sort is implemented properly to make sure your code time complexity is correct
      - test_hybrid_merge_actually_hybrid: __/0
        - This test is similar to test_hybrid_merge_sort_speed, but it checks if your hybrid merge sort function is a true hybrid merge sort or not.
        - NOTE: one way to fail this test is if `hybrid_merge_sort` doesn't call itself recursively (e.g. if you have a separate `merge_sort` helper function). In this case, you must take extra care and ensure that your overall algorithm **is actually hybrid** to avoid losing manual points.
  - Application: __/20
    - test_better_than_most: __/20

**Note on Comprehensive Tests:**

If your solution fails to pass a comprehensive test for a specific function during our assessment, **half of the manual points allocated for that function will be deducted**. This is to emphasize the importance of not only meeting basic requirements but also ensuring robustness and correctness in your code. Consider these comprehensive tests as tools for ensuring quality and resilience in your solutions.

**Additional Note on Scenario Generation:**

While we make every effort to generate test cases that encompass every possible scenario, there might be times when some edge cases are inadvertently overlooked. Nevertheless, should we identify any scenario where your submitted logic doesn't hold, even if it's not part of our provided test cases, we reserve the right to deduct from the manual points. This highlights the significance of crafting logic that doesn't merely pass the given tests, but is genuinely resilient and correctly addresses the problem's entirety. Always strive to think beyond the provided cases, ensuring that your solutions are comprehensive and robust.

* **Manual (30 points)**
  * Time and Space complexity points are **divided equally** for each function. If you fail to meet time **or** space complexity in a given function, you receive half of the manual points for that function.
  * Loss of 1 point per missing docstring (max 5 point loss)
  * Loss of 2 points per changed function signature (max 20 point loss)
  * **Loss of complexity and loss of testcase points for the required functions in this project. You may not use any additional data structures such as dictionaries, and sets!”**
  * M1 - selection sort: \_\_/4
  * M2 - bubble sort: \_\_/4
  * M3 - insertion sort: \_\_/4
  * M4 - hybrid sort: \_\_/8
  * M6 - better_than_most: \_\_/10

- We probably don't have to tell you this if you made it this far but make sure to read the specs including all grading 
  requirements!

    * **DOCSTRING** is not provided for this project. Please use Project 1 as a template for your DOCSTRING. 
    To learn more on what is a DOCSTRING visit the following website: [What is Docstring?](https://peps.python.org/pep-0257/)
      * One point per function that misses DOCSTRING.
      * Up to 5 points of deductions

<input type="checkbox"> <b>STEP 1 :Rename the old solution file by clicking Rename button below. This button renames your file to **solution_old.py** </b>
{Rename}(mv solution.py solution_old.py)
<input type="checkbox"> <b>STEP 2 : Refresh your file tree by clicking on the refresh button under project name or refresh your browser. </b>

<input type="checkbox"> <b>STEP 3 : Upload your **solution.py** from your computer to Codio File Tree on the left. Refresh your file tree or browser to see if it actually updated the solution.py </b>


<input type="checkbox"> <b>STEP 4:Submit your code, by clicking the Submit button, you can submit as many times as you like, no limit on submission. 


Submit button is tied to tests.py in our secure folder, and it always gets the updated version of the tests.py. In case of any tests.py update, students will always get the latest version to test their code through the submit button. 
{SUBMIT!|assessment}(test-3379255259)
Please note that there will be manual grading after you submit your work. Clicking Submit only runs the Auto-grader for the test cases. Manual Grading is 30 points in this project.


<input type="checkbox"> <b>STEP 5: Please make sure to **scroll all the way down on Guide Editor page**, Guide is the specs document, it is the document you are reading right now, scroll all the way down, and **click at the Mark as Completed button**, see below for the image of the button so you know what it looks like. Please scroll down and actually push the button. If you do not mark complete yourself, Codio will mark it at the end of the last penalty day, which will give 0 to your project. </b>
![](img/markcomplete.png)

{Check It!|assessment}(grade-book-3266829715)
{Submit Answer!|assessment}(free-text-3024451938)
