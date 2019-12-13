from arboles import *
from abstract_syntax_tree import *
from gp_machine import *
import matplotlib.pyplot as plt
import time
import numexpr

# FIND A FUNCTION
FUNCTION = "x * x + x - 6"


def fitness_4(individual):
    dic = {}
    # Add numbers to the dictionary
    for terminalNum in range(-10, 11):
        dic.update({terminalNum: terminalNum})
    score = 0
    points_range = range(-100, 101)
    # Evaluate for each point
    for i in points_range:
        x = i
        eq_result = numexpr.evaluate(FUNCTION).item()
        dic.update({'x': i})
        value = individual.eval(dic)
        score += (eq_result - value)**2  # Total score will be MSE
    # The total score will be the sum of the differences at each point plus a proportion attached to the size of
    # the individual
    score = score/float(len(list(points_range))) + individual.get_size() / 10000.0
    return score


def individual_factory_4():
    terminalArr = []
    for terminalNum in range(-10, 11):
        terminalArr.append(terminalNum)
    for terminalVar in range(-10, 11):
        terminalArr.append('x')
    AST_generator = ABST([AddNode, SubNode, MultNode], terminalArr)
    individual = AST_generator.__call__()
    return individual


GP_4 = GP(pop_size=500, mutation_rate=0, fit=fitness_4, indiv_factory=individual_factory_4, termination_condition=lambda i: i == 40, is_crossover=True)

# ini = time.time()
pop, list_fitness = GP_4.run()
# end = time.time()
# print("Time elapsed ")
# print(end - ini)

# Plot best, worst and average fitness per epoch
plt.figure()
epochs = list(range(1, GP_4.generations() + 1))
plt.plot(epochs, GP_4.get_best_fitness())
plt.title('Best Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('best_fitness_4.png')

plt.figure()
#plt.ylim(top=5*10**9)
plt.plot(epochs, GP_4.get_worst_fitness())
plt.title('Worst Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('worst_fitness_4.png')

plt.figure()
#plt.ylim(10**14)
plt.plot(epochs, GP_4.get_average_fitness())
plt.title('Average Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('average_fitness_4.png')

# No es necesario imprimir lo de abajo (sugerencia: eliminarlo)
for individual in pop:
    print(individual.__repr__())
print(" ")
for fit in list_fitness:
    print(fit)
print(" ")
for fitness_per_gener in GP_4.get_best_fitness():
    print(fitness_per_gener)

GP_4 = GP(pop_size=500, mutation_rate=0.5, fit=fitness_4, indiv_factory=individual_factory_4, termination_condition=lambda i: i == 40, is_crossover=False)

# ini = time.time()
pop, list_fitness = GP_4.run()
# end = time.time()
# print("Time elapsed ")
# print(end - ini)

# Plot best, worst and average fitness per epoch
plt.figure()
epochs = list(range(1, GP_4.generations() + 1))
plt.plot(epochs, GP_4.get_best_fitness())
plt.title('Best Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('best_fitness_4_mut.png')

plt.figure()
#plt.ylim(top=5*10**9)
plt.plot(epochs, GP_4.get_worst_fitness())
plt.title('Worst Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('worst_fitness_4_mut.png')

plt.figure()
#plt.ylim(10**14)
plt.plot(epochs, GP_4.get_average_fitness())
plt.title('Average Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('average_fitness_4_mut.png')

# No es necesario imprimir lo de abajo (sugerencia: eliminarlo)
for individual in pop:
    print(individual.__repr__())
print(" ")
for fit in list_fitness:
    print(fit)
print(" ")
for fitness_per_gener in GP_4.get_best_fitness():
    print(fitness_per_gener)