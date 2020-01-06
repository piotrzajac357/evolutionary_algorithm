#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint, sample, random, shuffle
from typing import List
from copy import copy


def crossover(parent1: List[int], parent2: List[int], number_of_carts: int = None, swath_length: int = None) -> List[int]:
    # parent1 - wiodacy (child bedzie bardziej podobny do niego, niz do parent2)

    child1 = copy(parent1)
    child2 = copy(parent2)
    zeros_p1 = []
    zeros_p2 = []

    if number_of_carts is None:
        number_of_carts = 0
        for elem in child1:
            if not elem:
                number_of_carts += 1

    if swath_length is None:
        swath_length = randint(2, len(parent1) - number_of_carts - 1)

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


def change_carts(parent1: List[int]) -> List[int]:
    child = copy(parent1)
    number_of_carts = 0
    for elem in child:
        if not elem:
            number_of_carts += 1
    if number_of_carts == 1:
        return child
    carts_to_swap = sample([i for i in range(1, number_of_carts + 1)], 2)
    first_cart = min(carts_to_swap)
    second_cart = max(carts_to_swap)
    first_cart_stands = []
    second_cart_stands = []
    cart_number = 0
    for index, i in enumerate(child):
        if i == 0:
            cart_number += 1
        else:
            if cart_number == first_cart:
                first_cart_stands.append(i)
            if cart_number == second_cart:
                second_cart_stands.append(i)
    for i in range(len(first_cart_stands)):
        child.remove(first_cart_stands[i])
    for i in range(len(second_cart_stands)):
        child.remove(second_cart_stands[i])
    cart_number = 0
    for index, elem in enumerate(child):
        if elem == 0:
            cart_number += 1
            if cart_number == first_cart:
                for i in second_cart_stands[::-1]:
                    child.insert(index + 1, i)
            if cart_number == second_cart:
                for i in first_cart_stands[::-1]:
                    child.insert(index + 1, i)
    return child


def move_cart_marker(parent1: List[int]) -> List[int]:
    child = copy(parent1)
    number_of_carts = child.count(0)
    cart_number = randint(2, number_of_carts)
    if cart_number == number_of_carts and child[-1] == 0:
        child[-1] = child[-2]
        child[-2] = 0
    else:
        cart_counter = 0
        for index, elem in enumerate(child):
            if elem == 0:
                cart_counter += 1
                if cart_counter == cart_number:
                    if random() <= 0.5:
                        child[index] = child[index - 1]
                        child[index - 1] = 0
                    else:
                        child[index] = child[index + 1]
                        child[index + 1] = 0
    return child


def permutate_cart_queue(parent1: List[int]) -> List[int]:
    child = copy(parent1)
    number_of_carts = child.count(0)
    cart_number = randint(1, number_of_carts)
    cart_counter = 0
    cart_queue = []
    cart_index = 0
    for index, i in enumerate(child):
        if i == 0:
            cart_counter += 1
        else:
            if cart_number == cart_counter:
                cart_queue.append(i)
                cart_index = index - len(cart_queue)
    shuffle(cart_queue)
    for index, elem in enumerate(cart_queue):
        child[cart_index + index + 1] = elem
    return child


parent = [0, 1, 2, 0, 3, 4, 6, 5, 7, 0]

"""
print(parent)
for j in range(0,10):
    print(permutate_cart_queue(parent))


parent = [0, 1, 2, 0, 3, 0, 4, 0, 5, 6, 7, 0]
print(parent)
for i in range(10):
    print(parent)
    print(move_cart_marker(parent))


parent = [0, 2, 4, 3, 10, 11, 12, 13, 0, 1, 7, 0, 6, 8, 9]
print(parent)
print(change_carts(parent))

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
"""
