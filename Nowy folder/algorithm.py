#!/usr/bin/python
# -*- coding: utf-8 -*-

from xd import *
from input import *
from random import seed

"""seed(1)
#   tworzenie warunkow zadania
save_input_to_file(generate_random_input(10, 99), 'set1/input.txt')
save_solutions_to_file(generate_random_solutions(5, matrix_to_list(load_input_from_file('set1/input.txt')), 1000),
                       'set1/solutions.txt')
"""

garage = Garage(len(load_coeff_vector_from_file('set1/coefficients.txt')),
                load_coeff_vector_from_file('set1/coefficients.txt'),
                matrix_to_list(load_input_from_file('set1/input.txt')))
