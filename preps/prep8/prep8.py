#  Copyright (c) 2019. Yuehao Huang huan1387 github@EroSkulled

"""Prep 8 Synthesize

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
Your task in this prep is to implement each of the unimplemented Tree methods
in this file.
The starter code has a recursive template that treats both the "empty tree"
and the "size-one" tree as base cases.  You may not need both of these base
cases -- it depends on the method you are writing.  If you can, collapse down
to just one base case.
"""
from __future__ import annotations
from typing import Any, List, Optional


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[Any]
    # The list of all subtrees of this tree.
    _subtrees: List[Tree]

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty Tree.
    #
    #   Note: self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    def __init__(self, root: Any, subtrees: List[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return True if this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also do len(subtree) here
            return size

    def num_positives(self) -> int:
        """Return the number of positive integers in this tree.

        Precondition: all items in this tree are integers.

        Remember, 0 is *not* positive.

        >>> t1 = Tree(17, [])
        >>> t1.num_positives()
        1
        >>> t2 = Tree(-10, [])
        >>> t2.num_positives()
        0
        >>> t3 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(30, [])])
        >>> t3.num_positives()
        3
         >>> t3 = Tree(1, [Tree(-2, [Tree(1, [Tree(-2, []), Tree(0, []), Tree(-30, [])])]), Tree(10, []), Tree(-30, [])])
        >>> t3.num_positives()
        3
        """
        if self.is_empty():
            return 0
        else:
            total = 0
            if self._root > 0:
                total += 1
            for subtree in self._subtrees:
                total += subtree.num_positives()
            return total

    def maximum(self: Tree) -> int:
        """Return the maximum item stored in this tree.

        Return 0 if this tree is empty.

        Precondition: all values in this tree are positive integers.

        >>> t1 = Tree(17, [])
        >>> t1.maximum()
        17
        >>> t3 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t3.maximum()
        10
        >>> t3 = Tree(1, [Tree(-2, [Tree(1, [Tree(-2, []), Tree(10, []), Tree(30, [])])]), Tree(10, []), Tree(30, [])])
        >>> t3.maximum()
        30
        """

        if self.is_empty():
            return 0
        else:
            maximum = self._root
            for subtree in self._subtrees:
               if subtree.maximum() > maximum:
                   maximum = subtree.maximum()
            return maximum

    def height(self: Tree) -> int:
        """Return the height of this tree.

        Please refer to the prep readings for the definition of tree height.

        >>> t1 = Tree(17, [])
        >>> t1.height()
        1
        >>> t2 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t2.height()
        2
        >>> t3 = Tree(1, [Tree(-2, [Tree(1, [Tree(-2, []), Tree(10, []), Tree(30, []), Tree(30, [])])]), Tree(10, []), Tree(30, [])])
        >>> t3.height()
        4
        >>> t4 = Tree(1, [Tree(-2, [Tree(1, [Tree(-2, []), Tree(10, []), Tree(30, []), Tree(30, []), Tree(30, [Tree(30, [])])])]), Tree(10, []), Tree(30, [])])
        >>> t4.height()
        5
        """

        if self.is_empty():
            return 0
        else:
            height = 1
            heights = [0]
            for subtree in self._subtrees:
                heights.append(subtree.height())
            height += max(heights)
            return height

    def __contains__(self, item: Any) -> bool:
        """Return whether this tree contains <item>.

        >>> t = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t.__contains__(-30)  # Could also write -30 in t.
        True
        >>> t.__contains__(148)
        False
        >>> t = Tree(1, [Tree(-2, [Tree(1, [Tree(-2, []), Tree(10, [Tree(0, [Tree(10, [])])]), Tree(30, []), Tree(90, [Tree(910, [])])])]), Tree(110, []), Tree(30, [])])
        >>> t.__contains__(148)
        False
        >>> t.__contains__(110)
        True
        >>> t.__contains__(90)
        True
        >>> t.__contains__(910)
        True
        >>> t.__contains__(10)
        True
        >>> t.__contains__(0)
        True
        """
        if self.is_empty():
            return False
        else:
            if self._root == item:
                return True
            for subtree in self._subtrees:
                if item in subtree:
                    return True
            return False

    def leaves(self) -> list:
        """
        >>> t = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [Tree(None, [])])])
        >>> t.leaves()
        [-2, 10]
        """
        if self.is_empty():
            return []
        elif self._subtrees == []:
            return [self._root]
        else:
            ans = []
            for subtree in self._subtrees:
                ans.extend(subtree.leaves())
            return ans

    def average(self) -> float:
        """
        >>> t1 = Tree(2, [Tree(2, []), Tree(2, [])])
        >>> t1.average()
        2.0
        >>> t = Tree(2, [Tree(2, [Tree(2, [])]), Tree(2, []), Tree(-2, [])])
        >>> t.average()
        1.2
        >>> t2 = Tree(2, [])
        >>> t2.average()
        2.0
        """
        if self.is_empty():
            return 0.0
        else:
            total, count = self._avghelper()
            return total / count

    def _avghelper(self) -> Tuple[int, int]:
        """Return the total values in this tree and the number of values in this tree
        >>> t = Tree(2, [Tree(2, [Tree(2, [])]), Tree(2, []), Tree(-2, [])])
        >>> t._avghelper()
        (6, 5)
        """
        if self.is_empty():
            return 0, 0
        elif self._subtrees == []:
            return self._root, 1
        else:
            total = self._root
            count = 1
            for subtree in self._subtrees:
                t, c = subtree._avghelper()
                total += t
                count += c
            return total, count



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
