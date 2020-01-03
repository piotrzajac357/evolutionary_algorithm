#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List


def save_to_file(matrix: List[List], filename: str = 'matrix.txt') -> None:

    f = open(filename, 'w')
    for index, i in enumerate(matrix):
        for index1, j in enumerate(i):
            f.write(str(j))
            if index1 != len(i) - 1:
                f.write(' ')
        if index != len(matrix) - 1:
            f.write('\n')
    f.close()
