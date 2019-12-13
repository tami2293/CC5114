from arboles import *
from abstract_syntax_tree import *
from gp_machine import *
import matplotlib.pyplot as plt
import time
import numexpr
import sys

# FIND A FUNCTION (DIVISION INCLUDED)
FUNCTION = "x * x + x - 6"


def fitness_5(individual):
    dic = {}
    for terminalNum in range(-10, 11):
        dic.update({terminalNum: terminalNum})
    score = 0
    points_range = range(-100, 101)
    for i in points_range:
        x = i
        eq_result = numexpr.evaluate(FUNCTION).item()
        dic.update({'x': i})
        try:
            value = individual.eval(dic)
        except ZeroDivisionError:
            score = sys.maxsize
            return score
        score += (eq_result - value)**2
    # The total score will be the MSE plus a proportion attached to the size of the individual
    score = score/float(len(list(points_range))) + individual.get_size() / 10000.0
    return score


def individual_factory_5():
    terminalArr = []
    for terminalNum in range(-10, 11):
        terminalArr.append(terminalNum)
    for terminalVar in range(-10, 11):
        terminalArr.append('x')
    AST_generator = ABST([AddNode, SubNode, MultNode, DivNode], terminalArr)
    individual = AST_generator.__call__()
    return individual

GP_5 = GP(pop_size=500, mutation_rate=0, fit=fitness_5, indiv_factory=individual_factory_5, termination_condition=lambda i: i == 40, is_crossover=True)

# ini = time.time()
try:
    pop, list_fitness = GP_5.run()
except ZeroDivisionError:
    pass
# end = time.time()
# print("Time elapsed ")
# print(end - ini)

# Plot best, worst and average fitness per epoch
plt.figure()
epochs = list(range(1, GP_5.generations() + 1))
plt.plot(epochs, GP_5.get_best_fitness())
plt.title('Best Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('best_fitness_5.png')

plt.figure()
#plt.ylim(top=5*10**9)
plt.plot(epochs, GP_5.get_worst_fitness())
plt.title('Worst Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('worst_fitness_5.png')

plt.figure()
#plt.ylim(10**14)
plt.plot(epochs, GP_5.get_average_fitness())
plt.title('Average Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('average_fitness_5.png')

# No es necesario imprimir lo de abajo (sugerencia: eliminarlo)
for individual in pop:
    print(individual.__repr__())
print(" ")
for fit in list_fitness:
    print(fit)
print(" ")
for fitness_per_gener in GP_5.get_best_fitness():
    print(fitness_per_gener)

GP_5 = GP(pop_size=500, mutation_rate=0.5, fit=fitness_5, indiv_factory=individual_factory_5, termination_condition=lambda i: i == 40, is_crossover=False)

# ini = time.time()
try:
    pop, list_fitness = GP_5.run()
except ZeroDivisionError:
    pass
# end = time.time()
# print("Time elapsed ")
# print(end - ini)

# Plot best, worst and average fitness per epoch
plt.figure()
epochs = list(range(1, GP_5.generations() + 1))
plt.plot(epochs, GP_5.get_best_fitness())
plt.title('Best Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('best_fitness_5_mut.png')

plt.figure()
#plt.ylim(top=5*10**9)
plt.plot(epochs, GP_5.get_worst_fitness())
plt.title('Worst Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('worst_fitness_5_mut.png')

plt.figure()
#plt.ylim(10**14)
plt.plot(epochs, GP_5.get_average_fitness())
plt.title('Average Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('average_fitness_5_mut.png')

# No es necesario imprimir lo de abajo (sugerencia: eliminarlo)
for individual in pop:
    print(individual.__repr__())
print(" ")
for fit in list_fitness:
    print(fit)
print(" ")
for fitness_per_gener in GP_5.get_best_fitness():
    print(fitness_per_gener)