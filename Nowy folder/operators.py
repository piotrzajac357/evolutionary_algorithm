#!/usr/bin/python
# -*- coding: utf-8 -*-
import xd
from random import randint, seed
from typing import List
from copy import copy


def crossover(parent1: List[int], parent2: List[int], number_of_carts: int = None, swath_length: int = 3) -> List[int]:
    # parent1 - wiodacy (child bedzie bardziej podobny do niego, niz do parent2)

    child1 = copy(parent1)
    child2 = copy(parent2)
    seed(1)
    if number_of_carts is None:
        number_of_carts = 0
        for elem in child1:
            if not elem:
                number_of_carts += 1

    zeros_p1 = []
    zeros_p2 = []

    # zapisanie pozycji zer poprzez ilosc stanowisk miedzy pierwszym i drugim, drugim i trzecim, itd.

    for index in range(0, len(child1)):
        if not child1[index]:
            zeros_p1.append(index)
        if not child2[index]:
            zeros_p2.append(index)

    # usuniecie wszystkich pozostalych zer z rodzicow
    for cart in range(number_of_carts):
        child1.remove(0)
        child2.remove(0)

    # wybranie losowo poczatku wycinanej sekwencji (jej dlugosc jest dana)

    swath_start_index = randint(0, len(child2) - swath_length)
    swath = []
    for i in range(0, swath_length):
        swath.append(child2[swath_start_index + i])

    # usuwanie z parent1 wartosci zawarty z wybranej z parent2 sekwencji

    for elem in swath:
        child1.remove(elem)

    for elem in swath[::-1]:
        child1.insert(swath_start_index, elem)

    for index in zeros_p1:
        child1.insert(index, 0)

    return child1


# Parent1 = [0, 2, 1, 3, 5, 0, 4, 8, 9, 10, 0, 7, 6, 12, 0, 16, 15, 14, 13, 11]
# Parent2 = [0, 8, 9, 10, 11, 4, 0, 3, 1, 2, 0, 5, 16, 15, 14, 13, 0, 12, 7, 6]
p1 = [0, 1, 2, 0, 3, 4, 5, 6]
p2 = [0, 6, 5, 4, 0, 3, 2, 1]
print(p1)
print(p2)

print(crossover(p1, p2))
print(crossover(p2, p1))
problem = xd.matrix_to_list(xd.generate_random_input(5, 10))
garage1 = xd.Garage(4, xd.generate_random_coefficients_vector(4), problem)
p3 = xd.generate_random_solutions(4, problem, 10)
for element in p3:
    print(element)
print('kurwa dziala xD')
print(crossover(p3[0], p3[1]))
print(crossover(p3[2], p3[3]))
print(crossover(p3[4], p3[5]))
print(crossover(p3[6], p3[7]))
print(crossover(p3[8], p3[9]))
