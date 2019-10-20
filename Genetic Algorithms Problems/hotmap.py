from ga_machine import *
import numpy
import matplotlib.pyplot as plt
import os

# UNBOUND KNAPSACK


population = numpy.arange(50, 1000, 50)
mut_rate = numpy.arange(0, 1, .1)
iterations = numpy.empty([population.size, mut_rate.size])
for ind_pop in range(population.size):
    for ind_rate in range(mut_rate.size):
        GA3 = GA(pop_size=population[ind_pop], mutation_rate=mut_rate[ind_rate], fit=knap_fitness,
                 gene_factory=knap_gene_factory,indiv_factory=knap_individual_factory,
                 termination_condition=lambda l: False if (not l or (l[-1] < OPT_FITNESS and len(l) < 100)) else True,
                 number_of_genes=KNAP_NUMBER_OF_GENES, is_crossover=True)
        individuals, fits = GA3.run()
        iterate = GA3.generations()
        iterations[ind_pop, ind_rate] = iterate

fig, ax = plt.subplots()
im = ax.imshow(iterations)

# We want to show all ticks...
#ax.set_xticks(numpy.arange(len(population)))
#ax.set_yticks(numpy.arange(len(mut_rate)))
# ... and label them with the respective list entries
ax.set_xticklabels(population)
ax.set_yticklabels(mut_rate)
ax.set_xlabel('Population')
ax.set_ylabel('Mutation Rate')

cbar = fig.colorbar(im)
# Rotate the tick labels and set their alignment.
#plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
#for i in range(len(population)):
#    for j in range(len(mut_rate)):
#        text = ax.text(i, j, iterations[i, j],
#                       ha="center", va="center", color="b")

ax.set_title("Number of iterations to find a solution")
fig.tight_layout()
plt.show()
plt.savefig('Genetic Algorithms Problems/hotmap.png')