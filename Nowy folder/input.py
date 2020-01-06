#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List


def save_input_to_file(matrix: List[List[int]], filename: str) -> None:

    file = open(filename, 'w')
    for row in matrix:
        for col in row:
            file.write(str(col)), file.write(' ')
        file.write('\n')
    file.close()


def load_input_from_file(filename: str) -> List[List[int]]:
    matrix = []
    file = open(filename, 'r')
    for line in file:
        matrix.append([int(a) for a in line.split()])
    file.close()
    return matrix


def save_coeff_vector_to_file(coeffs_vector: List[float], filename: str) -> None:
    file = open(filename, 'w')
    for coeff in coeffs_vector:
        file.write(str(coeff)), file.write(' ')
    file.close()


def load_coeff_vector_from_file(filename: str) -> List[float]:
    coeff_vector = []
    file = open(filename, 'r')
    for line in file:
        coeff_vector.append([float(a) for a in line.split()])
    file.close()
    return coeff_vector[0]


def save_solutions_to_file(solutions: List[List[int]], filename: str) -> None:
    file = open(filename, 'w')
    for solution in solutions:
        for elem in solution:
            file.write(str(elem)), file.write(' ')
        file.write('\n')
    file.close()


def load_solutions_from_file(filename: str) -> List[List[int]]:
    solutions = []
    file = open(filename, 'r')
    for line in file:
        solutions.append([int(a) for a in line.split()])
    file.close()
    return solutions
