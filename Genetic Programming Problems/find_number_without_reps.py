from arboles import *
from abstract_syntax_tree import *
from gp_machine import *
import matplotlib.pyplot as plt
import time

# FIND A NUMBER WITHOUT REPETITIONS
NUMBER = 65346


def fitness_3(individual):
    # Must evaluate the tree (individual) and check its value
    value = individual.eval()

    # Count number of repetitions for terminal nodes
    serialized = individual.serialize()
    terminal_nodes = []
    dup_error = 0
    for elem in serialized:
        if isinstance(elem, TerminalNode):
            terminal_nodes.append(elem)
            dup_count = {i: terminal_nodes.count(i) for i in terminal_nodes}
            dup_error = (sum(dup_count.values()) - len(dup_count)) / len(terminal_nodes)
    # The fitness value will be the same as before with an error related to the expression size and number repetitions
    # score = abs(NUMBER - value) * (1 + individual.get_size() / 50000.0)
    score = abs(NUMBER - value) + individual.get_size() / 10000.0 + dup_error
    return score


def individual_factory_3():
    AST_generator = ABST([AddNode, SubNode, MultNode], [25, 100, 4, 8, 7, 2])
    individual = AST_generator.__call__()
    return individual

GP_3 = GP(pop_size=500, mutation_rate=0, fit=fitness_3, gene_factory=0, indiv_factory=individual_factory_3, termination_condition=lambda i: i == 50, number_of_genes=0, is_crossover=True)

ini = time.time()
pop, list_fitness = GP_3.run()
end = time.time()
print("Time elapsed ")
print(end - ini)

# Plot best, worst and average fitness per epoch
plt.figure()
epochs = list(range(1, GP_3.generations() + 1))
plt.plot(epochs, GP_3.get_best_fitness())
plt.title('Best Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('best_fitness_3.png')

plt.figure()
#plt.ylim(top=5*10**9)
plt.plot(epochs, GP_3.get_worst_fitness())
plt.title('Worst Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('worst_fitness_3.png')

plt.figure()
#plt.ylim(10**14)
plt.plot(epochs, GP_3.get_average_fitness())
plt.title('Average Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('average_fitness_3.png')

# No es necesario imprimir lo de abajo (sugerencia: eliminarlo)
for individual in pop:
    print(individual.__repr__())
    print(individual.eval())
print(" ")
for fit in list_fitness:
    print(fit)
print(" ")
for fitness_per_gener in GP_3.get_best_fitness():
    print(fitness_per_gener)