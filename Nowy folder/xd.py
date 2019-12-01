#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
#   from copy import copy, deepcopy


class Garage:
    def __init__(self, number_of_carts: int, coefficients: List[float], stands: List[List[int]]) -> None:

        # liczba wozkow przeznaczona do pracy
        # lista wspolczynnikow tempa prayc kazdego wozka

        self.number_of_carts = number_of_carts
        self.coefficients = coefficients
        self.stands = stands

    def get_size(self) -> int:
        return self.number_of_carts

    def get_coefficients(self) -> List[float]:
        return self.coefficients

    def goal_function(self, solution: List[int]) -> float:
        goal = 0
        cart_number = -1
        last_elem = 0
        for elem in solution:
            if not elem:
                cart_number += 1
            else:
                goal += self.coefficients[cart_number] * self.stands[elem - 1][3]
                if not last_elem:
                    goal += (self.stands[elem - 1][1] + self.stands[elem - 1][2])
                else:
                    goal += (abs(self.stands[elem - 1][1] - self.stands[last_elem - 1][1]) +
                             abs(self.stands[elem - 1][2] - self.stands[last_elem - 1][2]))
            last_elem = elem
        return goal


class Solution(Garage):

    def __init__(self, solution: List[int], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.solution = solution

    def get_solution_as_list(self) -> List[int]:
        return self.solution


def matrix_to_list(matrix: List[List[int]]) -> List[List[int]]:
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


abc = [[0, 0, 2], [3, 4, 0], [6, 0, 8]]
print(matrix_to_list(abc))
# sprawdzenie dzialania matrix_to_list

print("[0 7 3 0 0 0 0 \n 0 0 0 0 0 0 0 \n 2 0 0 0 0 0 0 \n 0 0 0 4 0 0 0 \n 0 0 0 0 5 0 0 \n 0 0 0 0 0 0 20]")
garage = Garage(3, [1, 2, 3], [[1, 0, 2, 2], [2, 2, 0, 3], [3, 3, 3, 4], [4, 4, 4, 5], [5, 5, 6, 20], [6, 0, 1, 7]])
print(garage.goal_function([0, 1, 2, 0, 3, 4, 0, 5, 6]))
# sprawdzenie dzialania goal_function (dziala)
