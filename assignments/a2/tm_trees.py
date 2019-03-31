#  Copyright (c) 2019. Yuehao Huang huan1387 github@EroSkulled

"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: Optional[str]
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.
        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        if not subtrees:
            self.data_size = data_size
        else:
            self.data_size = 0
            for tree in subtrees:
                self.data_size += tree.data_size
        for tree in subtrees:
            if not tree.is_empty():
                tree._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.

        x, y, width, height = rect
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif width > height:
            self.rect = rect
            curr = x
            for i in range(len(self._subtrees)):
                if i != len(self._subtrees) - 1:
                    percent = self._subtrees[i].data_size / self.data_size
                    new_width = math.floor(percent * width)
                else:
                    new_width = width + x - curr
                self._subtrees[i].update_rectangles((
                    curr, y, new_width, height))
                curr += new_width
        else:
            self.rect = rect
            curr = y
            for i in range(len(self._subtrees)):
                if i != len(self._subtrees) - 1:
                    percent = self._subtrees[i].data_size / self.data_size
                    new_height = math.floor(percent * height)
                else:
                    new_height = height + y - curr
                self._subtrees[i].update_rectangles((
                    x, curr, width, new_height))
                curr += new_height

    def _find_last_non_zero_index(self) -> int:
        """
        return the last non zero index
        :return:
        """
        for item in reversed(self._subtrees):
            i = -1
            if item.data_size == 0:
                i -= 1
            else:
                return i
        return i

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.data_size == 0 or self.is_empty():
            return []
        elif not self._expanded:
            return [(self.rect, self._colour)]
        else:
            ans = []
            for tree in self._subtrees:
                ans.extend(tree.get_rectangles())
            return ans

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        x, y = pos
        left, up = self.rect[0], self.rect[1]
        right, down = left + self.rect[2], up + self.rect[3]
        if not (left <= x <= right and up <= y <= down):
            return None
        elif not self._expanded:
            return self
        elif self._subtrees:
            for tree in self._subtrees:
                if tree.get_tree_at_position(pos):
                    return tree.get_tree_at_position(pos)
        return self

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if not self._subtrees:
            return self.data_size
        else:
            size = 0
            for subtree in self._subtrees:
                size += subtree.update_data_sizes()
            self.data_size = size
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if not self._subtrees and destination._subtrees:
            destination._subtrees.append(self)
            self._parent_tree.data_size -= self.data_size
            self._parent_tree._subtrees.remove(self)
            self._parent_tree = destination

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self._subtrees:
            pass
        else:
            if factor > 0:
                self.data_size += math.ceil(self.data_size * factor)
            else:
                add = math.floor(self.data_size * factor)
                if self.data_size == 0:
                    pass
                elif self.data_size + add < 1:
                    self.data_size = 1
                else:
                    self.data_size += add

    def expand(self) -> None:
        """
        If the user selects a rectangle, and then presses e, the tree
        corresponding to that rectangle is expanded in the displayed-tree.
        If the tree is a leaf, nothing happens.
        :return:
        """
        if self._subtrees:
            self._expanded = True
        if self._parent_tree:
            self._parent_tree.expand()

    def expand_all(self) -> None:
        """
        If the user selects a rectangle, and then presses a, the tree
        corresponding to that rectangle, as well as all of its subtrees,
        are expanded in the displayed-tree. If the tree is a leaf,
        nothing happens.
        :return:
        """
        if not self._subtrees:
            pass
        else:
            self.expand()
            for tree in self._subtrees:
                tree.expand_all()

    def collapse(self) -> None:
        """
        If the user selects a rectangle, and then presses c, the parent
        of that tree is unexpanded (or “collapsed”) in the displayed-tree.
        (Note that since rectangles correspond to leaves in the displayed-tree,
        it is the parent that needs to be unexpanded.) If the parent is None
        because this is the root of the whole tree, nothing happens.
        :return:
        """

        if self._parent_tree:
            self._parent_tree._expanded = False
            for tree in self._parent_tree._subtrees:
                tree._collapse_helper()

    def _collapse_helper(self) -> None:
        """
        helper function for the collapse
        :return:
        """
        self._expanded = False
        for tree in self._subtrees:
            tree.collapse()


    def collapse_all(self) -> None:
        """
        If the user selects any rectangle, and then presses x, the
        entire displayed-tree is collapsed down to just a single tree
        node. If the displayed-tree is already a single node,
        nothing happens.
        :return:
        """
        self.collapse()
        if self._parent_tree:
            self._parent_tree.collapse_all()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        if os.path.isfile(path):
            TMTree.__init__(self, os.path.basename(path),
                            [], os.path.getsize(path))
        else:
            path_names = []
            for name in os.listdir(path):
                path_names.append(os.path.join(path, name))
            subtrees = []
            for paths in path_names:
                subtrees.append(FileSystemTree(paths))
            TMTree.__init__(self, os.path.basename(path), subtrees, 0)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
