from typing import List, Tuple
from random import randint, shuffle


#   from copy import copy, deepcopy


class Garage:
    def __init__(self, number_of_carts: int, coefficients: List[float], matrix: List[List[int]],
                 first_population: List[List[int]]) -> None:

        self.number_of_carts = number_of_carts
        self.coefficients = coefficients
        self.stands = matrix_to_list(matrix)
        self.population = self.calculate_goal_for_all(first_population)
        self.population_size = len(self.population)

    def calculate_goal_for_all(self, population_without_costs: List[List[int]]) -> List[Tuple[List[int], float]]:
        # liczy f celu dla calej populacji - uzywana tylko wewnatrz instancji klasy Garage
        population = []
        for elem in population_without_costs:
            population.append((elem, self.goal_function(elem)))
        return population

    def get_size(self) -> int:
        return self.number_of_carts

    def get_coefficients(self) -> List[float]:
        return self.coefficients

    def get_stands(self) -> List[List[int]]:
        return self.stands

    def get_population_size(self) -> int:
        return self.population_size

    def get_one(self, which_one: int) -> Tuple[List[int], float]:
        return self.population[which_one]

    def set_one(self, which_one: int, gimme_new_one: Tuple[List[int], float]) -> None:
        self.population[which_one] = gimme_new_one

    def goal_function(self, solution: List[int]) -> float:
        # to liczy funkcje celu dla jednego rozwiazania
        goal = 0
        cart_number = -1
        last_elem = 0
        single_cart_time = 0
        for index, elem in enumerate(solution):
            if not elem:
                if single_cart_time > goal:
                    goal = single_cart_time
                cart_number += 1
                single_cart_time = 0
            else:
                single_cart_time += self.coefficients[cart_number] * self.stands[elem - 1][3]
                if not last_elem:
                    single_cart_time += (self.stands[elem - 1][1] + self.stands[elem - 1][2])
                else:
                    single_cart_time += (abs(self.stands[elem - 1][1] - self.stands[last_elem - 1][1]) +
                                         abs(self.stands[elem - 1][2] - self.stands[last_elem - 1][2]))
            last_elem = elem
        if single_cart_time > goal:
            goal = single_cart_time
        return round(goal, 4)

    def get_best_solution_as_tuple(self) -> Tuple[List[int], float]:
        goal_values = []
        for elem in self.population:
            goal_values.append(elem[1])
        min_value_index = goal_values.index(min(goal_values))
        return self.get_one(min_value_index)

    def get_best_solution_as_value(self) -> float:
        return self.get_best_solution_as_tuple()[1]

    def get_more_friendly_solution(self) -> List:
        #   zwraca rozwiazanie w postaci (0,x1,y1,x2,y2,0,x3,y4,...,xn,yn) - w postaci wspolrzednych
        solution = self.get_best_solution_as_tuple()
        more_friendly_solution = []
        zeros = 0
        for elem in solution[0]:
            if elem == 0:
                more_friendly_solution.append(0)
                zeros += 1
            else:
                more_friendly_solution.append((self.stands[elem - 1][2], self.stands[elem - 1][1]))
        return more_friendly_solution


def matrix_to_list(matrix: List[List[int]]) -> List[List[int]]:
    # funkcja przyjmuje liste list z kosztami
    # przeksztalca ja w liste elementow [numer_stanowiska, rzad, kolumna, koszt]
    # jak kon wyglada - kazdy widzi, potrzeba uzycia tej funkcji nie zajdzie
    converted = []
    index = 1
    for row in range(0, len(matrix)):
        for col in range(0, len(matrix)):
            if matrix[row][col]:
                converted.append([index, row, col, matrix[row][col]])
                index = index + 1
    return converted


def generate_random_input(dim: int = 1, costs_range: int = 1) -> List[List[int]]:
    # funkcja tworzy liste list z losowymi wartosciami naturalnymi od 0 do wartosci rownej drugiemu argumentowi
    matrix = []
    for i in range(0, dim):
        matrix.append([])
        for j in range(0, dim):
            matrix[i].append(randint(0, costs_range))
            #   matrix[i].append(randint(0, costs_range) if randint(0, costs_range) > costs_range/2 else 0)
            # wersja, w ktorej okolo polowa elementow to 0
    # zwrocona wartosc mozna wladowac do funkcji matrix_to_list
    return matrix


def generate_random_solution(number_of_carts: int = 1, problem: List[List[int]] = None) -> List[int]:
    if problem is None:
        problem = [[1]]
    solution = []
    for i in range(1, len(problem) + 1):
        solution.append(i)
    shuffle(solution)
    solution.insert(0, 0)
    if number_of_carts == 1:
        return solution
    for i in range(1, number_of_carts):
        solution.insert(randint(1, len(problem) + i), 0)
    return solution


def generate_random_solutions(number_of_carts: int = 1, problem: List[List[int]] = None,
                              number_of_solutions: int = 1) -> List[List[int]]:
    if problem is None:
        return [generate_random_solution(number_of_carts)]
    solutions = []
    for i in range(number_of_solutions):
        solutions.append(generate_random_solution(number_of_carts, problem))
    return solutions


def generate_random_coefficients_vector(number_of_carts: int = 1, lower_limit: float = 0.8, upper_limit: float = 1.2,
                                        step: float = 0.01) -> List[float]:
    coefficients_vector = []
    for i in range(0, number_of_carts):
        coefficients_vector.append(round((randint(0, int((upper_limit - lower_limit) / step)) * step + lower_limit), 2))
    return coefficients_vector


"""
seed(1)
abc = [[0, 0, 2], [3, 4, 0], [6, 0, 8]]
print("dzialanie matrix_to_list")
print(matrix_to_list(abc))  # sprawdzenie dzialania matrix_to_list
print("przykladowa macierz")
print("[0 7 3 0 0 0 0] \n [0 0 0 0 0 0 0] \n [2 0 0 0 0 0 0] \n [0 0 0 4 0 0 0] \n [0 0 0 0 5 0 0] \n [0 0 0 0 0 0 20]")
garage = Garage(3, [1, 2, 3], [[1, 0, 2, 2], [2, 2, 0, 3], [3, 3, 3, 4], [4, 4, 4, 5], [5, 5, 6, 20], [6, 0, 1, 7]])
print("policzona funkcja celu dla 3 wozkow i przypadkowego rozwiazania i wektora wspolczynnikow dla powyzszej macierzy")
print(garage.goal_function([0, 1, 2, 0, 3, 4, 0, 5, 6]))  # sprawdzenie dzialania goal_function (dziala)

# macierz losowych naturalnych wartosci 3x3
print("wygenerowana losowo macierz 5x5 z wartosciami max 10")
efg = generate_random_input(4, 20)
for p in efg:
    print(p)
print("wygenerowane losowo 5 rozwiazan do powyzszej macierzy i 4 wozkow")
abc = generate_random_solutions(4, matrix_to_list(efg), 5)
for xd in abc:
    print(xd)

print("losowo wygenerowany wektor 10 w  spolczynnikow z zakresu 0.5 - 1.5 z krokiem 0.01")
wsp = generate_random_coefficients_vector(4, 1, 3, 1)
print(wsp)

print("wyliczenie funkcji celu dla wygenerowanych wczesniej danych")
garage1 = Garage(4, wsp, matrix_to_list(efg))
for element in abc:
    print(round(garage1.goal_function(element), 3))
"""
