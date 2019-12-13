import numpy
import matplotlib.pyplot as plt
import numexpr
from abstract_syntax_tree import *
from gp_machine import *

# SYMBOLIC REGRESSION
FUNCTION = "x * x + x - 6"


def fitness_4(individual):
    dic = {}
    for terminalNum in range(-10, 11):
        dic.update({terminalNum: terminalNum})
    score = 0
    points_range = range(-100, 101)
    for i in points_range:
        x = i
        eq_result = numexpr.evaluate(FUNCTION).item()
        dic.update({'x': i})
        value = individual.eval(dic)
        #score += abs(eq_result - value)
        score += (eq_result - value)**2
    # The total score will be the sum of the differences at each point plus a proportion attached to the size of
    # the individual
    #score += individual.get_size() / 10000.0
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


population = numpy.arange(50, 1000, 50)
mut_rate = numpy.arange(0, 1, .1)
iterations = numpy.empty([population.size, mut_rate.size])
for ind_pop in range(population.size):
    for ind_rate in range(mut_rate.size):
        print(population[ind_pop])
        GP4 = GP(pop_size=population[ind_pop], mutation_rate=mut_rate[ind_rate], fit=fitness_4,
                 indiv_factory=individual_factory_4,
                 termination_condition=lambda l: False if (not l or (l[-1] >= 1 and len(l) < 30)) else True, is_crossover=False)
        individuals, fits = GP4.run()
        iterate = GP4.generations()
        iterations[ind_pop, ind_rate] = iterate

fig, ax = plt.subplots()
im = ax.imshow(iterations)

ax.set_xticklabels(population)
ax.set_yticklabels(mut_rate)
ax.set_xlabel('Population')
ax.set_ylabel('Mutation Rate')

cbar = fig.colorbar(im)

ax.set_title("Number of iterations to find a solution")
fig.tight_layout()
plt.savefig('hotmap.png')