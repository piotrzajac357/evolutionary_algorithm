#!/usr/bin/python
# -*- coding: utf-8 -*-

from xd import *
from input import *
from operators import *
import math
from random import seed, shuffle, random

seed(1)
#   tworzenie warunkow zadania

matrix_size = 5
matrix_values_range = 10
number_of_carts = 3
size_of_population = 1000
tournament_size = 3
number_of_iterations = 500
chance_of_mutation = 0.1
chance_of_crossover = 1

save_input_to_file(generate_random_input(matrix_size, matrix_values_range), 'set1/input.txt')

save_solutions_to_file(
    generate_random_solutions(number_of_carts, matrix_to_list(load_input_from_file('set1/input.txt')),
                              size_of_population), 'set1/solutions.txt')

save_coeff_vector_to_file(generate_random_coefficients_vector(number_of_carts), 'set1/coefficients.txt')

garage = Garage(len(load_coeff_vector_from_file('set1/coefficients.txt')),
                load_coeff_vector_from_file('set1/coefficients.txt'),
                load_input_from_file('set1/input.txt'),
                load_solutions_from_file('set1/solutions.txt'))

for iteracja in range(number_of_iterations):
    for i in range(math.ceil(garage.get_population_size() / tournament_size) if
                   garage.get_population_size() % tournament_size > 2 else
                   math.floor(garage.get_population_size() / tournament_size)):
        if random() <= chance_of_crossover:
            tournament_group = []
            tournament_group_goals = []
            for j in range(tournament_size):
                # if random.rand(1) <= prawdopodobienstwo_krzyzowania:
                # else: zrob nic
                if tournament_size * i + j < garage.get_population_size():
                    tournament_group.append(garage.get_one(tournament_size * i + j)[0])
                    tournament_group_goals.append(garage.get_one(tournament_size * i + j)[1])
            loser_index = tournament_group_goals.index(max(tournament_group_goals))
            parent_1_index = tournament_group_goals.index(min(tournament_group_goals))
            parent_1 = tournament_group[parent_1_index]
            tournament_group_goals[parent_1_index] += tournament_group_goals[loser_index]
            parent_2_index = tournament_group_goals.index(min(tournament_group_goals))
            parent_2 = tournament_group[parent_2_index]
            child_1_sol = crossover(parent_1, parent_2)
            child_1 = (child_1_sol, garage.goal_function(child_1_sol))
            child_2_sol = crossover(parent_2, parent_1)
            child_2 = (child_2_sol, garage.goal_function(child_2_sol))
            if child_1[1] <= child_2[1]:
                better_child = child_1
            else:
                better_child = child_2

            if better_child[1] <= tournament_group_goals[loser_index]:
                garage.set_one(tournament_size * i + loser_index, better_child)

    for index, elem in enumerate(garage.population):
        if random() <= chance_of_mutation:
            child = change_carts(elem[0])
            child_goal_function = garage.goal_function(child)
            #if child_goal_function <= elem[1]:
            garage.set_one(index, (child, child_goal_function))
        if random() <= chance_of_mutation:
            child2 = move_cart_marker(elem[0])
            child2_goal_function = garage.goal_function(child2)
            #if child_goal_function <= elem[1]:
            garage.set_one(index, (child2, child2_goal_function))
        if random() <= chance_of_mutation:
            child3 = permutate_cart_queue(elem[0])
            child3_goal_function = garage.goal_function(child3)
            if child3_goal_function <= elem[1]:
                garage.set_one(index, (child3, child3_goal_function))

    shuffle(garage.population)
    print(garage.get_best_solution_as_value())

print(garage.get_best_solution_as_tuple())
