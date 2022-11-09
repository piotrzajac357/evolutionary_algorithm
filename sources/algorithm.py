from garage import *
from input import *
from operators import *
import math
from random import seed, shuffle, random
import matplotlib.pyplot as plt

matrix_size = 12         # rozmiar fabryki n x n
matrix_values_range = 5         # wartosci w macierzy
number_of_carts = 5         # liczba wozkow
size_of_population = 100         # rozmiar populacji (nie zmienia sie w czasie dzialania algorytmu)
number_of_iterations = 1000
replace_worse_parent_with_worse_kid = 1     # zastepowanie gorszego rodzica gorszym dzieckiem (jesli lepsze od niego) 1 - wlaczone, 0 - wylaczone

tournament_size = 3         # rozmiar turnieju (metody selekcji rodzicow)
swath_length = 0        # dlugosc wycinka genu branego do krzyzowania - 0 daje losowa
chance_of_crossover = 1     # prawdopodobienstwo wystapienia krzyzowania
chance_of_mutation_1 = 0.5      # prawdopodobienstwo wystapienia mutacji (ogolnie)
mutation_1_participation = 0.33     # udzial pierwszej mutacji we wszystkich - change carts
mutation_2_participation = 0.33     # udzial drugiej mutacji - permutate cart queue
mutation_3_participation = 0.34     # udzial trzeciej - move cart marker
max_slow_mutation_chance_growth = 2     # powolny wzrost prawd. mutacji z biegiem iteracji (ustawic 0 zeby wylaczyc)
rapid_mutation = 2 * chance_of_mutation_1       # zwiekszenie prawd. mutacji jak populacja sie nie zmienia (1*chance_of_mutation_1 nic nie zmienia)

b = 5           # liczba powtorzen algorytmu dla tej samej instancji testowej i roznych ziaren
suma = 0            # do usrednienia wyniku z wielu powtorzen
y = []
x = []
seed(1)
# tworzenie warunkow zadania
save_input_to_file(generate_random_input(matrix_size, matrix_values_range), '100x100/input.txt')
save_coeff_vector_to_file(generate_random_coefficients_vector(number_of_carts), '100x100/coefficients.txt')
save_solutions_to_file(
    generate_random_solutions(number_of_carts, matrix_to_list(load_input_from_file('100x100/input.txt')),
                              size_of_population), '100x100/solutions.txt')

#book = xlrd.open_workbook("testy.xlsx")
#sheet = book.sheet_by_name("100x100")
#file = open("100x100/wyniki.txt", 'w')
"""
for row in range(0, 16):
    tournament_size = int(sheet.row_values(row)[0])
    swath_length = int(sheet.row_values(row)[1])
    chance_of_crossover = float(sheet.row_values(row)[2])
    chance_of_mutation_1 = float(sheet.row_values(row)[3])
    mutation_1_participation = float(sheet.row_values(row)[4])
    mutation_2_participation = float(sheet.row_values(row)[5])
    mutation_3_participation = float(sheet.row_values(row)[6])
    max_slow_mutation_chance_growth = int(sheet.row_values(row)[7])
    rapid_mutation = chance_of_mutation_1 * int(sheet.row_values(row)[8])
    suma = 0
    print(mutation_1_participation)
    print(mutation_2_participation)
    print(mutation_3_participation)
    for a in range(b):
        seed(a)
"""
        # tworzenie zadania z macierzy wejscia, wspolczynnikow i populacji poczatkowej
garage = Garage(len(load_coeff_vector_from_file('100x100/coefficients.txt')),
                load_coeff_vector_from_file('100x100/coefficients.txt'),
                load_input_from_file('100x100/input.txt'),
                load_solutions_from_file('100x100/solutions.txt'))

indiversity = 0
for iteracja in range(number_of_iterations):
    #  powolny wzrost prawdopodobienstwa mutacji
    chance_of_mutation = chance_of_mutation_1 + max_slow_mutation_chance_growth * chance_of_mutation_1 * iteracja / number_of_iterations
    last_iteration_best_value = garage.get_best_solution_as_value
    #  nagly wzrost prawdopodobienstwa mutacji
    if garage.get_best_solution_as_value == last_iteration_best_value:
        indiversity += 1
    else:
        indiversity = 0
    if indiversity >= number_of_iterations / 10:
        chance_of_mutation = rapid_mutation * chance_of_mutation
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
            child_1_sol = crossover(parent_1, parent_2, swath_length=swath_length)
            child_1 = (child_1_sol, garage.goal_function(child_1_sol))
            child_2_sol = crossover(parent_2, parent_1, swath_length=swath_length)
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
                if case <= chance_of_mutation:  # zamiana wozkow
                    if case <= mutation_1_participation:
                        child = change_carts(better_child[0])
                        child_goal_function = garage.goal_function(child)
                        if child_goal_function <= better_child[1]:
                            garage.set_one(tournament_size * i + loser_index, (child, child_goal_function))

                    elif case <= mutation_1_participation + mutation_2_participation:  # permutacja kolejki wozka
                        child = permutate_cart_queue(better_child[0])
                        child_goal_function = garage.goal_function(child)
                        if child_goal_function <= better_child[1]:
                            garage.set_one(tournament_size * i + loser_index, (child, child_goal_function))

                    else:
                        child = move_cart_marker(better_child[0])  # przesuniecie znacznika wozka o 1 miejsce
                        child_goal_function = garage.goal_function(child)
                        if child_goal_function <= better_child[1]:
                            garage.set_one(tournament_size * i + loser_index, (child, child_goal_function))

                # zastepowanie gorszego rodzica gorszym utworzonym dzieckiem
                if replace_worse_parent_with_worse_kid == 1 and tournament_size > 2:
                    if worse_child[1] <= tournament_group_goals[parent_2_index]:
                        garage.set_one(tournament_size * i + parent_2_index, (worse_child[0], worse_child[1]))
                        case = random()
                        if case <= mutation_1_participation:
                            child = change_carts(worse_child[0])
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= worse_child[1]:
                                garage.set_one(tournament_size * i + parent_2_index, (child, child_goal_function))

                        elif case <= mutation_1_participation + mutation_2_participation:  # permutacja kolejki wozka
                            child = permutate_cart_queue(worse_child[0])
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= worse_child[1]:
                                garage.set_one(tournament_size * i + parent_2_index, (child, child_goal_function))

                        else:
                            child = move_cart_marker(worse_child[0])  # przesuniecie znacznika wozka o 1 miejsce
                            child_goal_function = garage.goal_function(child)
                            if child_goal_function <= worse_child[1]:
                                garage.set_one(tournament_size * i + parent_2_index, (child, child_goal_function))
    shuffle(garage.population)
    print(garage.get_best_solution_as_value())
            #   print(garage.get_best_solution_as_value())  # wyswietlenie najlepszego rozw. w iteracji (zakomentowac jak nie ma potrzeby)
        #suma += garage.get_best_solution_as_value()     # do usrednienia wyniku z wielu przejsc algorytmu

        #   print(garage.get_more_friendly_solution())      # wyswietla rozwiazanie i f celu po przejsciu algorytmu

    #file.write(str(round(suma/b, 3))), file.write('\n')
    y.append(garage.get_best_solution_as_value())
    x.append(iteracja)
print(garage.get_best_solution_as_tuple())
print(garage.get_more_friendly_solution())
print(garage.get_best_solution_as_value())
#file.close()
plt.plot(x, y)
plt.xlabel('numer iteracji')
plt.ylabel('f celu najlepszego znalezionego rozwiazania')
plt.show()
