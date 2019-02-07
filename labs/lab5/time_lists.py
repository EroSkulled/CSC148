#  Copyright (c) 2019. Yuehao Huang huan1387 github@EroSkulled

"""CSC148 Lab 5: Linked Lists

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===

This module runs timing experiments to determine how the time taken
to call `len` on a Python list vs. a LinkedList grows as the list size grows.
"""
from timeit import timeit
from linked_list import LinkedListV1

NUM_TRIALS = 3000                        # The number of trials to run.
SIZES = [1000, 2000, 4000, 8000, 16000]  # The list sizes to try.


def profile_len(list_class: type, size: int) -> float:
    """Return the time taken to call len on a list of the given class and size.

    Precondition: list_class is either list or LinkedList.
    """

    lst = []
    my_list = []
    for size in SIZES:
        for i in range(size):
            lst.append(0)
            i += 1
        my_list.append(LinkedListV1(lst))
    time = 0
    for lists in my_list:
        time += timeit('len(lists)', number=NUM_TRIALS, globals=locals())
    # Look at the Lab 4 starter code if you don't remember how to use timeit:
    # https://www.teach.cs.toronto.edu/~csc148h/fall/labs/w4_ADTs/starter-code/timequeue.py
    return time


if __name__ == '__main__':
    for list_class in [LinkedListV1]:
        # Try each list size
        for s in SIZES:
            time = profile_len(list_class, s)
            print(f'[{list_class.__name__}] Size {s:>6}: {time}')
