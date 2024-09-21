# Project 1: Doubly Linked Lists
**Due: Thursday, January 25th at 9:00 PM ET**

# Assignment Overview

Doubly linked lists (DLLs) are a fundamental data structure used to store sequential information. DLLs consist of a chain of *nodes* linked to one another by *forward* and *backward* references, such that one may traverse the chain from the *head* to the *tail*, or vice-versa. Each node stores a *value*, which may be a number, string, or more complex object.

![](img/basic_DLL.png)

Traditional *arrays* provide a simpler means for storing sequential information, but come with a major drawback which DLLs avoid: arrays require contiguous blocks of memory, while DLLs may utilize memory wherever it is available. In settings where data is updated, manipulated or deleted frequently, DLLs outperform traditional arrays by avoiding the need for memory reallocation. [This article](https://www.geeksforgeeks.org/linked-list-vs-array/) gives a nice overview of the distinction between DLLs and arrays.

For more information on Doubly Linked Lists, please visit [Zybooks Chapter 20](https://learn.zybooks.com/zybook/MSUCSE331Spring2024/chapter/20/section/5).

# Assignment Notes
1. Time **and** space complexity account for 30% of the points on Project 2. Be sure to review the rubric and adhere to complexity requirements!
2. Docstrings (the multi-line comments beneath each function header) are NOT provided in Project 2 and will need to be completed for full credit.
3. Testcases are your friend: before asking about the form of input/output or what happens in a particular edge case, check to see if the test cases answer your question for you. By showing the expected output in response to each input, they supplement the specs provided here.
4. Don't be afraid to go to D2L Course Tools for tutorial videos on how to debug,  it will help you figure out where you're going wrong far more quickly than ad-hoc print statements!
5. Throughout the specs, we mention Python double-underscore "magic" methods. These are central to the structure of object-oriented programming in Python, and will continue to appear in future projects in CSE 331 and beyond. [This page](https://rszalski.github.io/magicmethods/) is a great reference if you'd like to learn more about how they work!
6. There are two functions which may seem a little odd to you *_find_nodes* and *_remove_node*. These functions are intended as helper functions to help you reuse code and allow you to practice writing modular code.
7. We **strongly** encourage you to avoid calling `remove` in `remove_all`. Why? It's far less efficient to repeatedly call `remove`, as each call to remove begins searching at the beginning of the list. In the worst case, this will lead our function to operate with O(n^2) time complexity, **violating the required time complexity.**
8. We **strongly** encourage you to implement reverse in-place, without creating any new Node objects and instead rearranging prev and next pointers. Why? It's far less efficient to rebuild the DLL than it is to simply adjust references, as it's far more work to construct a brand new Node object than it is to simply adjust an existing one's references.
9. In the testcases for this project, you will notice the use of assertEqual and assertIs. What's the difference? It ties back to the difference between == and is in Python. The double-equal sign compares *values* in Python, while the is operator compares *memory addresses* in Python. Put simply, the is keyword is stronger than ==: if two objects are at the same memory address, they must contain the same value. However, it is possible for two objects *not* at the same memory address to have the same value. In other words, if a is b then we know a == b as well, but if a == b we cannot conclude a is b. A great read on the subject is [available here](https://realpython.com/courses/python-is-identity-vs-equality/).

### **Auxiliary Space Complexity: An Overview**

Auxiliary space complexity refers to the amount of additional space, aside from the input, that an algorithm or a method requires to execute. This is especially important when evaluating the efficiency of algorithms. It's different from the space complexity in that it doesn't consider the space required by the inputs; instead, it looks only at the extra space (temporary space) taken up, typically for variables, temporary structures, etc.

In order to add more clarity to this new term, auxiliary space usage is explained in first few methods to help you. 

# Assignment Specifications

**class Node:**

A class that implements the nodes to be created for a DLL.

*DO NOT MODIFY the following attributes/functions*

- **Attributes**
  - **value: T:** Value held by the Node. Note that this may be any type, such as a str, int, float, dict, or a more complex object.
  - **next: Node:** Reference to the next Node in the linked list (may be None).
  - **prev: Node:** Reference to the previous Node in the linked list (may be None).
  - **child: Node:** Reference to the child Node of this Node. Note: this will only be used for the application problem, you should not be using the **child** member in any of your functions aside from the application problem.
- **\_\_init\_\_(self, value: T, next: Node = None, prev: Node = None) -> None**
  - Constructs a doubly linked list node.
  - **value: T:** Value held by the Node.
  - **next: Node:** Reference to the next Node in the linked list (may be None).
  - **prev: Node:** Reference to the previous Node in the linked list (may be None).
  - **Returns:** None.
- **\_\_str\_\_(self) -> str** and **\_\_repr\_\_(self) -> str**
  - Represents the Node as a string.
  - Note that Python will automatically invoke this function when using printing a Node to the console, and PyCharm will automatically invoke this function when displaying a Node in the debugger.
  - As with all double-underscore "magic" methods in Python (see note 5), this function may be called with str(node) or repr(node). It is not necessary (and stylistically improper) to use node.\_\_str\_\_() or node.\_\_repr\_\_(), just as it is preferable to call len(some\_list) instead of some\_list.\_\_len\_\_().
  - **Returns:** str.

**class DLL:**

A class that implements the doubly linked list with previous and forward references.

*DO NOT MODIFY the following attributes/functions*

- **Attributes**
  - **head: Node:** Head (first node) of the doubly linked list (may be None).
  - **tail: Node:** Tail (last node) of the doubly linked list (may be None).
  - **size: int:** Number of nodes in the doubly linked list.
  - Note that the implementation in this project does not use a [sentinel node](https://en.wikipedia.org/wiki/Sentinel_node). As such, an empty DLL will have head and tail attributes which are None.
- **\_\_init\_\_(self) -> None**
  - Construct an empty DLL. Initialize the head and tail to None, and set the size to zero.
  - **Returns:** None.
- **\_\_str\_\_(self) -> str** and **\_\_repr\_\_(self) -> str**
  - Represents the DLL as a string of the form "value <-> value <-> ... <-> value."
  - Note that Python will automatically invoke this function when printing a DLL to the console, and PyCharm will automatically invoke this function when displaying a DLL in the debugger.
  - As with all double-underscore "magic" methods in Python (see note 5), this function may be called with str(dll) or repr(dll). It is not necessary (and stylistically improper) to use dll.\_\_str\_\_() or dll.\_\_repr\_\_(), just as it is preferable to call len(some\_list) instead of some\_list.\_\_len\_\_().
  - **Returns:** str.

*IMPLEMENT the following functions*

- **empty(self) -> bool**
  - Returns a boolean indicating whether the DLL is empty.
  - *Required time complexity:* O(1).
  - *Auxiliary space complexity:* O(1).
  - **Returns:** True if DLL is empty, else False.
  - Since this method is simply checking if the doubly linked list (DLL) is empty (likely by verifying if the head of the list is `None` or if the size of the list is 0), it doesn't need to allocate any additional space. Thus, its auxiliary space complexity is `O(1)`, meaning it requires constant additional space. 
- **push(self, val: T, back: bool = True) -> None**
  - Adds a Node containing val to the back (or front) of the DLL and updates size accordingly.
  - *Required time complexity:* O(1).
  - *Auxiliary space complexity:* O(1).
  - **val: T:** Value to be added to the DLL.
  - **back: bool:** If True, add val to the back of the DLL. If False, add to the front. Note that the default value is True.
  - **Returns:** None.
  - The act of pushing a value onto a DLL involves creating a new node and adjusting a couple of pointers (previous and next). It doesn't matter how long the DLL is; the process of adding a node requires a fixed amount of space. Hence, its auxiliary space complexity remains `O(1)`. 
- **pop(self, back: bool = True) -> None**
  - Removes a Node from the back (or front) of the DLL and updates size accordingly.
  - In the case that the DLL is empty, pop does nothing.
  - *Required time complexity:* O(1).
  - *Auxiliary space complexity:* O(1).
  - **back: bool:** If True, remove from the back of the DLL. If False, remove from the front. Note that the default value is True.
  - **Returns:** None.
  - Popping a value from the DLL involves adjusting pointers and, in some implementations, deallocating the node's memory. Like the push method, the space it requires doesn't depend on the size of the DLL. Therefore, its auxiliary space complexity is `O(1)`. 
- **list\_to\_dll(self, source: list[T]) -> None**
  - Creates a DLL from a standard Python list. If there are already nodes in the DLL, the DLL should be cleared and replaced by **source**.
  - Hint: clearing the DLL can be very simple. Think about what an empty DLL looks like (what are the values of head and tail?).
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(n).
  - **source: list[T]:** Standard Python list from which to construct DLL.
  - **Returns:** None.
  - When transforming a standard Python list into a DLL, the method will likely iterate over each item in the source list and create a new node in the DLL. The number of nodes created will be proportional to the size of the source list. Thus, in the worst-case scenario, if the source list contains 'n' elements, the method will require space for 'n' nodes. Hence, its auxiliary space complexity is `O(n)`, meaning it requires linear additional space relative to the size of the input list. 
- **dll\_to\_list(self) -> list[T]**
  - Creates a standard Python list from a DLL.
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(n).
  - **Returns:** list[T] containing the values of the nodes in the DLL.
- **def \_find\_nodes(self, val: T, find\_first: bool =False) -> List[Node]:**
  - Construct list of Node with value val in the DLL and returns the associated Node object list
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(n).
  - MUST BE CALLED FROM find AND find\_all
    - If find and find\_all do not call \_find\_nodes, **all testcase and manual points** for find and find\_all will be forfeited.
  - Will not be tested explicitly
    - Tests for find and find\_all will ensure functionality
  - **val: T:** Value to be found in the DLL.
  - **find\_first: bool:**  if True find only the first element in the DLL, it false find all instances of the elements in the DLL.
  - **Returns:** list of Node objects in the DLL whose value is val. If val does not exist in the DLL, returns empty list.
- **find(self, val: T) -> Node**
  - Finds first Node with value val in the DLL and returns the associated Node object.
  - *Requires call to* \_find\_nodes
    - Failure to call \_find\_nodes will result in **all testcase and manual points** being forfeited for find.
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(1).
  - **val: T:** Value to be found in the DLL.
  - **Returns:** first Node object in the DLL whose value is val. If val does not exist in the DLL, return None.
- **find\_all(self, val: T) -> list[Node]**
  - Finds all Node objects with value val in the DLL and returns a standard Python list of the associated Node objects.
  - *Requires call to* `_find_nodes`
    - Failure to call `_find_nodes` will result in **all testcase and manual points** being forfeited for find\_all.
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(n).
  - **val: T:** Value to be found in the DLL.
  - **Returns:** standard Python list of all Node objects in the DLL whose value is val. If val does not exist in the DLL, returns an empty list.
- **\_remove\_node(self, to\_remove: Node) -> None**
  - Given a reference to a node in the linked list, remove it
  - MUST BE CALLED FROM `remove`  AND `remove_all`
  - Will not be tested explicitly
    - Tests for remove and remove\_all will ensure functionality
  - *Required time complexity:* O(1).
  - *Auxiliary space complexity:* O(1).
  - **to\_remove: Node:** Node to be removed from the DLL.
  - **Returns:** None.
- **remove(self, val: T) -> bool**
  - removes first Node with value val in the DLL.
  - MUST CALL `remove_node`
    - Failure to call `remove_node` will result in **all testcase and manual points** being forfeited for remove.
  - Hint
    - Use of `find` allows this to be implemented in less than 10 lines.
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(1).
  - **val: T:** Value to be removed from the DLL.
  - **Returns:** True if a Node with value val was found and removed from the DLL, else False.
- **remove\_all(self, val: T) -> int**
  - removes all Node objects with value val in the DLL. See note 7.
  - MUST CALL `remove_node`
    - Failure to call `remove_node` will result in **all testcase and manual points** being forfeited for remove\_all.
  - Hint
    - Use of `find_all` allows this to be implemented in less than 10 lines.
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(n).
  - **val: T:** Value to be removed from the DLL.
  - **Returns:** number of Node objects with value val removed from the DLL. If no node containing val exists in the DLL, returns 0.
- **reverse(self) -> None**
  - Reverses the DLL in-place by modifying all next and prev references of Node objects in DLL. Updates self.head and self.tail accordingly. See note 8.
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(1).
  - **Returns:** None.

# Application Problem: Dream Escaper
![inception](./img/inception-deeper.gif)

You have made millions of dollars as a highly-skilled "extractor"- someone who specializes in stealing juicy corporate secrets straight from the dreams of their targets.


However, the jig is up; some of your would-be victims have started to prepare for your attacks. They try to trap you in their subconscious forever by creating dreams within dreams or **dreamceptions**.
After a few narrow escapes from these newly bolstered defenses, you decide to deploy your 331 skills to take matters into your own hands. You realize that you can represent these dreamceptions with a **multilevel DLL**.

Thus, you decide to build an algorithm called `dream_escaper`. This algorithm will transform a multilevel DLL full of malicious dreamceptions into a single-level DLL that is much easier to escape from!


## Multilevel DLL Description
Each node in the multilevel DLL has an extra data member named child. Everything in the child’s DLL should occur after the current `node` but before current `node.next`. 

A small aside:
Though a multi-level structure seems odd, there are actually applications of this structure in the popular Pandas data science library. The Pandas library supports a multi-index structure that is structured in this way. If you would like to learn more, check out the links [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html) and [here](https://datascientyst.com/flatten-multiindex-in-pandas/).

**Multi-level Input**

![](img/Multilevel_DLL.png)


**Single-level Output**

![](img/Single_level_DLL.png)

**Explanation**
- A is the first node in multi so it will also be first in single level
- A has no children so B is A's next
- B has children so those are brought up to be B's next
- J has no children so it's next would be B's next, C
- C has a child so E becomes C's next
- E has no child so E's next stays the same, F
- F has a child so it's next becomes F's Next
- H has no next and no child so H's next is F's next
- G's has no next and no child so it's next is D
- Compiling this gives you the single level DLL above

## Function Description
Let's summarize:

- **dream\_escaper (dll: DLL) -> DLL**
  - Turns a multilevel dll into a single level dll
  - Child nodes are placed after the `parent` node but before the `parent.next` node in the final DLL.
  - *Required time complexity:* O(n).
  - *Auxiliary space complexity:* O(n).
  - **dll: DLL:** A DLL where each Node holds a value of str where the string is the task. The Node may also hold a child in `.child` and store the child DLL to the current node.
  - **Returns:** a DLL holding str representing the names of all of the tasks
  - Notes:
    - **IMPORTANT:** if your solution contains any hard-coding of the number of levels in the DLL, you will automatically lose all points for this section.  
    - If the DLL is empty, return an empty DLL.
    - When `node.child` is `None` it means there is no child DLL
    - All child values should be `None` in the DLL that is returned
    

**Example 1**

```
Input
A - B - C - D
    |   |
    E   F
    

Output
A - B - E - C - F - D
```

- **Explanation:**
  - A is the first node in the input  so it is the first in the output
  - A has no children so it is followed by its next, B.
  - B has a child DLL so nodes from that are inserted next, E.
  - All of B’s child’s are finished so it goes to B’s next, C
  - C has a child DLL so nodes from that are inserted next, F.
  - All of C’s child’s are finished so it goes to C’s next, D
  - Compiling the nodes into a DLL gives us the desired result.

**Example 2**
```
Input
A - B - C
|       | 
E - F   G
        |
        H
Output
A - E - F - B - C - G - H
```

- **Explanation:**
  - A is the first node in the input so it is the first in the output
  - A has 2 children so they will be placed before B
  - E is first in A’s child DLL so it is placed first
  - E has no children so its next is placed into the output, F
  - F is the last element in the child DLL and has no children so A’s Next is placed in the output, B
  - B has no child DLL so it's next is C
  - C has child DLL with start of G so G is placed in output
  - G has child DLL beginning with H so H is placed in output
  - Compiling the nodes into a DLL gives us the desired result.

**Example 3**
```
Input
A - B - C
    |
    D - F
    |   |
    E   H
    |
    G

Output 
A - B - D - E - G - F - H - C
```

- **Explanation:**
  - A is the first node in the input  so it is the first in the output
  - A has no children so it is followed by its next, B.
  - B has a child DLL so nodes from that are inserted next, D.
  - D has a child DLL so that is inserted next, E
  - E has child DLL so that is inserted next, G
  - G has no children and no next so the next element inserted is F
  - F has child DLL so that is inserted next, H
  - H has no child DLL and no next so F’s next is inserted, C
  - C has no DLL and no next so we are finished
  - Compiling the nodes into a DLL gives us the desired result.




**Here is some music for you to listen while working on this project:**
[Chillstep Music for Programming](https://youtu.be/M5QY2_8704o)

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
- All project submissions are due on Codio. **Any submission after its deadline ( Thursday, January 25th, 2024 at 9:00 PM ET) is subject to late penalties** .
  
**Tip:** While Codio can be used, we recommend working locally for a superior debugging experience in PyCharm. Aim to finalize your project locally before submitting on Codio.

---

**Grading**

The application problem test cases, include test_get_current_url, test_visit, test_backward, test_forward, test_malicious_sites. The first four get the basic browser history functionality working and then the last malicious sites test case gets the special skipover working.

* **Auto Graded Tests (70 points)** see below for the point distribution for the auto graded tests:
    * 01 - test\_empty: \_\_/5
    * 02 - test\_push: \_\_/5
    * 03 - test\_pop: \_\_/5
    * 04 - test\_list\_to\_dll: \_\_/5
    * 05 - test\_dll\_to\_list: \_\_/5
    * 06 - test\_find: \_\_/7
    * 07 - test\_find\_all: \_\_/7
    * 08 - test\_remove: \_\_/7
    * 09 - test\_remove\_all: \_\_/7
    * 10 - test\_reverse: \_\_/7 
    * 11 - test\_dream\_escaper: \_\_/10 

* **Manual (30 points)**
  * Time and Space complexity points are **divided equally** for each function. If you fail to meet time **or** space complexity in a given function, you receive half of the manual points for that function.
  * Loss of 1 point per missing docstring (max 5 point loss)
  * Loss of 2 points per changed function signature (max 20 point loss)
  * Loss of complexity and loss of testcase points for the required functions in this project. You may not use any additional data structures such as dictionaries, and sets!”
  
  * M1 - test\_empty: \_\_/1
  * M2 - test\_push: \_\_/2
  * M3 - test\_pop: \_\_/2
  * M4 - test\_list\_to\_dll: \_\_/2
  * M5 - test\_dll\_to\_list: \_\_/2
  * M6 - test\_find\_nodes: \_\_/2
    - If find and find\_all do not call \_find\_nodes, **all testcase and manual points** for find and find\_all  will be forfeited.
    - If \_find\_nodes violates time and/or space complexity and is called by find and find\_all  (as it must be), **all manual points** will be forfeited for the three functions
  * M7 - test\_find: \_\_/2
  * M8 - test\_find\_all: \_\_/2
  * M9 - test\_remove\_node: \_\_/2
    - If remove  and remove\_all do not call \_remove\_node, **all testcase and manual points** for remove  and remove\_all will be forfeited.
    - If \_remove\_node violates time and/or space complexity and is called by remove  and remove\_all (as it must be), **all manual points** will be forfeited for the three functions.
  * M10 - test\_remove: \_\_/2
  * M11 - test\_remove\_all: \_\_/2
  * M12 - test\_reverse: \_\_/2
  * M13 - test\_dream\_escaper: \_\_/6
  * M14 - test\_feedback and citation: \_\_/1
* **Important reminder**
Note students can not use Chegg or similar sites, see syllabus for details, use of outside resources for the application problem is strictly forbidden, use of outside resources is limited to max of 2 functions in a project.


    * **DOCSTRING** is not provided for this project. Please use Project 1 as a template for your DOCSTRING . 
    To learn more on what is a DOCSTRING visit the following website: [What is Docstring?](https://peps.python.org/pep-0257/)
      * One point per function that misses DOCSTRING.
      * Up to 5 points of deductions

---
Authors of DLL : Andrew McDonald, Alex Woodring, Andrew Haas, Matt Kight, Lukas Richters, Anna De Biasi, Tanawan Premsri, Hank Murdock, & Sai Ramesh

---

## **Upload Checklist**

- <input type="checkbox"> <b> **STEP 1:** Rename the old solution file by clicking the 'Rename' button below. This action will change your file's name to **solution_old.py**.  
  {Rename}(mv solution.py solution_old.py)

- <input type="checkbox"> **STEP 2:** Refresh your file tree either by using the refresh button located under the project name or simply refresh your browser.

- <input type="checkbox"> **STEP 3:** Upload your **solution.py** from your local machine to the Codio File Tree on the left. Once uploaded, refresh your file tree or browser to confirm the update.

- <input type="checkbox"> **STEP 4:** Click on the **Submit** button to upload your code. When finished, **Mark** your work as complete. Feel free to submit multiple times; there's no submission limit.

- <input type="checkbox"> **STEP 5:** Ensure you scroll to the very bottom of the **Guide Editor** page (you're currently reading this Guide, which is our specs document). At the end of the document, click on the **Mark as Completed button**. Below, you'll find an image of the button for reference. If you neglect to mark it as complete, Codio will auto-mark it at the conclusion of the final penalty day, resulting in a score of **0** for your project.
![](img/markcomplete.png)

---

## 📝 **Submission Instructions**

The `Submit` button fetches the `tests.py` file from our secure directory, ensuring it always uses the most recent version. Should there be any updates to `tests.py`, rest assured that students will always have access to the latest version when pressing the submit button.

{SUBMIT!|assessment}(test-3379255259)

> 🚨 **Important Note:** After clicking `Submit`, automated grading will run based on the test cases. However, manual grading follows this step. **30 points** of this project are allocated to manual grading:
> - **28 points** for assessing the runtime and space complexity of your solution.
> - **+2 points** for filling out feedback and citing sources in the appropriate text box.


{Check It!|assessment}(grade-book-3266829715)
{Submit Answer!|assessment}(free-text-3024451938)
