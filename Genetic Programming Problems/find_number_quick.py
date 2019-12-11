from arboles import *
from abstract_syntax_tree import *
from gp_machine import *
import matplotlib.pyplot as plt
import time

# FIND A NUMBER WITH REPETITIONS (MODIFIED FITNESS FUNCTION TO RUN THE PROGRAM QUICKER)
NUMBER = 65346


def fitness_2(individual):
    # Must evaluate the tree (individual) and check its value
    value = individual.eval({25: 25, 100: 100, 4: 4, 8: 8, 7: 7, 2: 2})
    # The fitness value will be the same as before with an error related to the expression size
    # score = abs(NUMBER - value) * (1 + individual.get_size() / 50000.0)
    score = abs(NUMBER - value) + individual.get_size() / 10000.0
    return score


def individual_factory_2():
    AST_generator = ABST([AddNode, SubNode, MultNode], [25, 100, 4, 8, 7, 2])
    individual = AST_generator.__call__()
    return individual

GP_2 = GP(pop_size=500, mutation_rate=0, fit=fitness_2, gene_factory=0, indiv_factory=individual_factory_2, termination_condition=lambda i: i == 50, number_of_genes=0, is_crossover=True)

ini = time.time()
pop, list_fitness = GP_2.run()
end = time.time()
print("Time elapsed ")
print(end - ini)

# Plot best, worst and average fitness per epoch
plt.figure()
epochs = list(range(1, GP_2.generations() + 1))
plt.plot(epochs, GP_2.get_best_fitness())
plt.title('Best Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('best_fitness_2.png')

plt.figure()
#plt.ylim(top=5*10**9)
plt.plot(epochs, GP_2.get_worst_fitness())
plt.title('Worst Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('worst_fitness_2.png')

plt.figure()
#plt.ylim(10**14)
plt.plot(epochs, GP_2.get_average_fitness())
plt.title('Average Fitness per Epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.savefig('average_fitness_2.png')

# No es necesario imprimir lo de abajo (sugerencia: eliminarlo)
for individual in pop:
    print(individual.__repr__())
print(" ")
for fit in list_fitness:
    print(fit)
print(" ")
for fitness_per_gener in GP_2.get_best_fitness():
    print(fitness_per_gener)

"Para castigar a los que aumentan el tamaño, hay que calcular el tamaño máximo primero antes de que se caiga el programa" \
"Sea S el tamaño máximo, s el tamaño actual del árbol y P el puntaje de la minimización de error, la formula final será P(1 + s/S)" \
"S puede ser un valor que nunca se alcanzará, la idea es que sea lo suficientemente alto como para que el error no sea demasiado grande" \
"Probar con S = 10000" \
"Sin la modificación de la función de fitness se hace con 50 iteraciones aprox."