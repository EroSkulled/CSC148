#  Copyright (c) 2019. Yuehao Huang huan1387 github@EroSkulled

"""Assignment 2: Demonstration of using the os module

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith
"""

import os


def print_items(d: str, indentation: str) -> None:
    """A sample program showing how to recurse on directories using os.

    Print the list of files and directories in directory <d>, recursively,
    prefixing each with the given <indentation>.
    """
    print(indentation + d + ':')
    for filename in os.listdir(d):
        print(indentation + filename)
        subitem = os.path.join(d, filename)
        if os.path.isdir(subitem):
            print_items(subitem, indentation + '    ')


if __name__ == '__main__':
    # Put in a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/walterhuang/Documents/courses/csc148/assignments' (OSX)
    # to print the contents of that folder.
    print_items('/Users/walterhuang/Documents/csc148/assignments/a2', '')
