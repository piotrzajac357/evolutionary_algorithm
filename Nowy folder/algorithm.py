#!/usr/bin/python
# -*- coding: utf-8 -*-

from garage import *
from input import *
from operators import *
import math
from random import seed, shuffle, random


matrix_size = 8
matrix_values_range = 5
number_of_carts = 6
size_of_population = 2000
tournament_size = 5
number_of_iterations = 100
chance_of_mutation_1 = 0.25
chance_of_crossover = 1
rapid_mutation = 4 * chance_of_mutation_1
mutation_1_participation = 0.1
mutation_2_participation = 0.1
mutation_3_participation = 0.8
indiversity = 0

#   tworzenie warunkow zadania
seed(1)
save_input_to_file(generate_random_input(matrix_size, matrix_values_range), 'set1/input.txt')

save_coeff_vector_to_file(generate_random_coefficients_vector(number_of_carts), 'set1/coefficients.txt')

save_solutions_to_file(
    generate_random_solutions(number_of_carts, matrix_to_list(load_input_from_file('set1/input.txt')),
                              size_of_population), 'set1/solutions.txt')

garage = Garage(len(load_coeff_vector_from_file('set1/coefficients.txt')),
                load_coeff_vector_from_file('set1/coefficients.txt'),
                load_input_from_file('set1/input.txt'),
                load_solutions_from_file('set1/solutions.txt'))
file = open('set1/export.txt', 'w')


for a in range(1):
    garage = Garage(len(load_coeff_vector_from_file('set1/coefficients.txt')),
                    load_coeff_vector_from_file('set1/coefficients.txt'),
                    load_input_from_file('set1/input.txt'),
                    load_solutions_from_file('set1/solutions.txt'))
    seed(a)
    for iteracja in range(number_of_iterations):
        #  nagly wzrost prawdopodobienstwa mutacji
        chance_of_mutation = chance_of_mutation_1 + 1 * chance_of_mutation_1 * iteracja / number_of_iterations
        last_iteration_best_value = garage.get_best_solution_as_value
        #  powolny wzrost prawdopodobienstwa mutacji
        if garage.get_best_solution_as_value == last_iteration_best_value:
            indiversity += 1
        else:
            indiversity = 0
        if indiversity >= number_of_iterations / 50:
            chance_of_mutation = rapid_mutation

        #  tworzenie grup turniejowych i wybieranie rodzicow
        for i in range(math.ceil(garage.get_population_size() / tournament_size) if
                       garage.get_population_size() % tournament_size > 2 else
                       math.floor(garage.get_population_size() / tournament_size)):
            if random() <= chance_of_crossover:
                tournament_group = []
                tournament_group_goals = []
                for j in range(tournament_size):
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
                    worse_child = child_2
                else:
                    better_child = child_2
                    worse_child = child_1

                #  zastapienie najgorszego osobnika turnieju lepszym dzieckiem, jesli jest lepsze od niego
                if better_child[1] <= tournament_group_goals[loser_index]:
                    garage.set_one(tournament_size * i + loser_index, better_child)

                    #  przeprowadzenie z zadanym prawdopodobienstwem mutacji na dziecku
                    case = random()
                    if case <= chance_of_mutation:        #  zamiana wozkow
                        if case <= mutation_1_participation:
                            child = change_carts(better_child[0])
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= better_child[1]:
                                garage.set_one(tournament_size * i + loser_index, (child, child_goal_function))

                        elif case <= mutation_1_participation + mutation_2_participation:   #  permutacja kolejki wozka
                            child = permutate_cart_queue(better_child[0])
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= better_child[1]:
                                garage.set_one(tournament_size * i + loser_index, (child, child_goal_function))

                        else:
                            child = move_cart_marker(better_child[0])       #  przesuniecie znacznika wozka o 1 miejsce
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= better_child[1]:
                                garage.set_one(tournament_size * i + loser_index, (child, child_goal_function))

                    """if worse_child[1] <= tournament_group_goals[parent_2_index]:
                        garage.set_one(tournament_size * i + parent_2_index, worse_child)
                        if random() <= chance_of_mutation:
                            child = change_carts(worse_child[0])
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= worse_child[1]:
                                garage.set_one(tournament_size * i + parent_2_index, (child, child_goal_function))
    
                        if random() <= chance_of_mutation:
                            child = permutate_cart_queue(better_child[0])
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= better_child[1]:
                                garage.set_one(tournament_size * i + parent_2_index, (child, child_goal_function))
    
                        if random() <= chance_of_mutation:
                            child = move_cart_marker(better_child[0])
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= better_child[1]:
                                garage.set_one(tournament_size * i + parent_2_index, (child, child_goal_function))
                      """  # zastepowanie gorszego rodzica gorszym dzieckiem

        shuffle(garage.population)
        file.write(str(garage.get_best_solution_as_value())), file.write(" ")
        print(garage.get_best_solution_as_value())

print(garage.get_best_solution_as_tuple())
