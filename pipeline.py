"""Example to demonstrate how to build data pipelines 
using Python generators.
"""

import os
import sys

def find(root): 
    """Finds all the files in the given 
    directory tree.
    """
    for path, dirnames, filenames in os.walk(root):
        for f in filenames:
            yield os.path.join(path, f)

def readlines(paths):
    """Returns a generator over lines in
    all the files specified.
    """
    for path in paths:
        yield from open(path)

def grep(pattern, lines):
    """Returns only the lines that 
    contain given pattern.
    """
    return (line for line in lines 
                 if pattern in line)

def main(): 
    root_dir = sys.argv[1]

    # find all files in the project
    filenames = find(root_dir)  

    # pick only python files
    filenames = grep('.py', filenames)

    # read all the lines
    lines = readlines(filenames)

    # pick only function definitions
    lines = grep('def ', lines)

    # count the total number of functions in your project
    print(count(lines))

if __name__ == "__main__":
    main()
