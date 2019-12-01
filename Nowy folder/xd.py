#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
#   from copy import copy, deepcopy


class Solution:
    def __init__(self, solution: List[int]) -> None:
        self.solution = solution

    def get_solution_as_list(self) -> List[int]:
        return self.solution

    def goal_function(self) -> float:
        goal = 0

        for elem in self.solution:
            i


class Garage:
    def __init__(self, number_of_wozki: int, coefficients: List[float]) -> None:

        # liczba wozkow przeznaczona do pracy
        # lista wspolczynnikow tempa prayc kazdego wozka

        self.number_of_wozki = number_of_wozki
        self.coefficients =  coefficients

    def get_size(self) -> int:
        return self.number_of_wozki

    def get_coefficients(self) -> List[float]:
        return self.coefficients


def matrix_to_list(matrix: List[List[int]]) -> List[List]:
    # funkcja przyjmuje liste list z kosztami
    # przeksztalca ja w liste elementow [numer_stanowiska, rzad, kolumna, koszt]
    converted = []
    index = 1
    for row in range(0, len(matrix)):
        for col in range(0, len(matrix)):
            if matrix[row][col]:
                converted.append([index, row, col, matrix[row][col]])
                index = index + 1
    return converted

#   abc = [[0, 0, 2], [3, 4, 0], [6, 0, 8]]
#   print(matrix_to_list(abc))
