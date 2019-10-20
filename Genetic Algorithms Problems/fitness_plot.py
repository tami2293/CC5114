from ga_machine import *

# UNBOUND KNAPSACK


GA3 = GA(pop_size=500, mutation_rate=0.1, fit=fitness3, gene_factory=gene_factory3, indiv_factory=individual_factory3,
         termination_condition=lambda i: i == 10, number_of_genes=NUMBER_OF_GENES3, is_crossover=True)
pop, list_fitness = GA3.run()

# Plot best, worst and average fitness per epoch
plt.figure()
epochs = list(range(1, GA3.generations() + 1))
plt.plot(epochs, GA3.get_best_fitness())
plt.plot(epochs, GA3.get_worst_fitness())
plt.plot(epochs, GA3.get_average_fitness())
plt.title('Fitness per epoch')
plt.xlabel('Epoch number')
plt.ylabel('Fitness')
plt.legend(('Best Fitness', 'Worst Fitness', 'Average Fitness'))
plt.savefig('fitness.png')