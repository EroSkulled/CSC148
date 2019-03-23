#  Copyright (c) 2019. Yuehao Huang huan1387 github@EroSkulled

"""Assignment 2: Modelling CS Education research paper data

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/

Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.


Recommended steps:
1. Start by reviewing the provided dataset in cs1_papers.csv. You can assume
   that any data used to generate this tree has this format,
   i.e., a csv file with the same columns (same column names, same order).
   The categories are all in one column, separated by colons (':').
   However, you should not make assumptions about what the categories are, how
   many categories there are, the maximum number of categories a paper can have,
   or the number of lines in the file.

2. Read through all the docstrings in this file once. There is a lot to take in,
   so don't feel like you need to understand it all the first time.
   Draw some pictures!
   We have provided the headers of the initializer as well as of some helper
   functions we suggest you implement. Note that we will not test any
   private top-level functions, so you can choose not to implement these
   functions, and you can add others if you want to for your solution.
   For this task, we will be testing that you are building the correct tree,
   not that you are doing it in a particular way. We will access your class
   in the same way as in the client code in the visualizer.

3. Plan out what you'll need to do to implement the PaperTree initializer.
   In particular, think about how to use the boolean parameters to do different
   things in setting up the tree. You may also find it helpful to review the
   Python documentation about the csv module, which you are permitted and
   encouraged to use. You should have a good plan, including what your subtasks
   are, before you begin writing any code.

4. Write the code for the PaperTree initializer and any helper functions you
   want to use in your design. You should not make any changes to the public
   interface of this module, or of the PaperTree class, but you can add private
   attributes and helpers as needed.

5. Tidy and test your code, and try it with the visualizer client code. Make
   sure you have documented any new private attributes, and that PyTA passes
   on your code.
"""
import csv
from typing import List, Dict
from tm_trees import TMTree


# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    _authors:
        The authors of this paper in list
    _doi:
        the doi of this paper
    _cat:
        the nested dict containing all the categories.
    These should store information about this paper's <authors> and <doi>.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """
    _authors: [str]
    _doi: str
    _cat: dict
    _by_year: bool
    # TODO: Add the type contracts for your new attributes here

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        self._doi = doi
        self._authors = authors
        self._cat = {}
        self._by_year = by_year
        if all_papers:
            if by_year:
                TMTree.__init__(self, name, subtrees, citations)
                tree = _build_tree_from_dict(_load_papers_to_dict(True))

            else:
                TMTree.__init__(self, name, subtrees, citations)
                tree = _build_tree_from_dict(_load_papers_to_dict(False))
        else:
            pass



        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        # TODO: Complete this initializer. Your implementation must not
        # TODO: duplicate anything done in the superclass initializer.

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        return ': '

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        if self._by_year:
            return ' (Year)'
        elif self._subtrees:
            return ' (Paper)'
        else:
            return ' (Category)'


def _get_data(num: int) -> str or int:
    """
    store all the data into self._data
    """
    with open(DATA_FILE) as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == num:
                return row


def _get_categories_and_num() -> dict:
    """
    get all the categories into a dict
    """
    tmp = []
    with open(DATA_FILE) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tmp.append(row[3].split(': ') + [reader.line_num])
    ans = {}
    for rows in tmp:
        curr = ans
        for cat in rows:
            if cat not in curr:
                curr[cat] = {}
            curr = curr[cat]
    return ans


def _get_categories_and_num_by_year() -> dict:
    """
    get all the categories into a dict
    """
    final = {}
    tmp = []
    with open(DATA_FILE) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tmp.append(row[2].split(': ') + [reader.line_num])
    ans = {}
    for rows in tmp:
        curr = ans
        for cat in rows:
            if cat not in curr:
                curr[cat] = {}
            curr = curr[cat]
    for key in ans:
        tmp = []
        for num in ans[key]:
            tmp.append(_get_data(num)[3].split(': ') + [num])
        anss = {}
        for rows in tmp:
            curr = anss
            for cat in rows:
                if cat not in curr:
                    curr[cat] = {}
                curr = curr[cat]
        final[key] = anss
    return final


def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    if by_year:
        return _get_categories_and_num_by_year()
    else:
        return _get_categories_and_num()


def _build_tree_from_dict(nested_dict: Dict) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    for x, y in nested_dict.items():
        if y == {}:
            spec = _get_data(x)
            return [PaperTree(spec[1], [], spec[0], spec[4][spec[4].find('10.'):], spec[-1], True, True)]
        else:
            return _build_tree_from_dict(y)
    # TODO: Implement this helper, or remove it if you do not plan to use it


if __name__ == '__main__':
    a = _build_tree_from_dict(_get_categories_and_num_by_year())
    print(a)
    import doctest
    doctest.testmod()
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
    #     'allowed-io': ['_load_papers_to_dict'],
    #     'max-args': 8
    # })
