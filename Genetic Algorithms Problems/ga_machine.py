import random
import string
import math
from statistics import mean
import matplotlib.pyplot as plt

# BINARY NUMBER PROBLEM
NUMBER_OF_GENES = 10
BINARY_NUMBER = "0001100100"


def fitness(indi):
    score = 0
    for i in range(0, NUMBER_OF_GENES):
        if str(indi[i]) == BINARY_NUMBER[i]:
            score += 1
    return score


def gene_factory():
    rand_value = random.randrange(0, 2)
    return rand_value


def individual_factory():
    return [gene_factory() for i in range(NUMBER_OF_GENES)]


# FINDING A WORD PROBLEM
NUMBER_OF_GENES2 = 10
WORD = "holaholaen"


def fitness2(indi):
    score = 0
    for i in range(0, NUMBER_OF_GENES2):
        if str(indi[i]) == WORD[i]:
            score += 1
    return score


def gene_factory2():
    rand_value = random.choice(string.ascii_letters.lower())
    return rand_value


def individual_factory2():
    return [gene_factory2() for i in range(NUMBER_OF_GENES2)]


# UNBOUND-KNAPSACK
NUMBER_OF_GENES3 = 15
OPT_FITNESS = 36
SOLUTION = [(4, 10), (4, 10), (4, 10), (1, 2), (1, 2), (1, 2), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]


def fitness3(indi):
    score = 0
    weight = 0
    for i in range(NUMBER_OF_GENES3):
        weight += indi[i][0]
        score += indi[i][1]
    penalty = weight - 15
    if penalty > 0:
        score = score - abs(penalty) * 5
    return score


def gene_factory3():
    weight, value = random.choice([(1, 1), (1, 2), (2, 2), (4, 10), (12, 4), (0, 0)])
    return weight, value


def individual_factory3():
    return [gene_factory3() for i in range(NUMBER_OF_GENES3)]


# 0-1-KNAPSACK
NUMBER_OF_GENES4 = 5
SOLUTION = [(4, 10), (1, 1), (1, 2), (2, 2), (0, 0)]

def fitness4(indi):
    score = 0
    weight = 0
    for i in range(NUMBER_OF_GENES4):
        weight += indi[i][0]
        if len(indi) != len(set(indi)):
            score = 0  # aquí debería ser muy muy negativo
            break
        score += indi[i][1]
    penalty = weight - 15
    if penalty > 0:
        penalty *= 100
    return score - penalty


def gene_factory4():
    weight = random.choice([1, 2, 4, 12])
    if weight == 1:
        value = random.choice([1, 2])
    elif weight == 2:
        value = 2
    elif weight == 4:
        value = 10
    else:
        value = 4
    return weight, value


def individual_factory4():
    return [gene_factory4() for i in range(NUMBER_OF_GENES4)]


class GA(object):
    def __init__(self, pop_size, mutation_rate, fit, gene_factory, indiv_factory, termination_condition,
                 number_of_genes, is_crossover):
        self.pop_size = pop_size
        print("Creating individuals...")
        self.mutation_rate = mutation_rate
        self.fitness = fit
        self.fits_list = []  # Results list of each individual
        self.individual_factory = indiv_factory
        self.gene_factory = gene_factory
        self.termination_condition = termination_condition
        self.genes_number = number_of_genes
        self.reproduce_crossover = is_crossover  # determines reproduction type
        self.best_fitness = []  # best fitness for each generation
        self.worst_fitness = []  # worst fitness for each generation
        self.average_fitness = []  # average fitness for each generation

        #  Initializes population generally randomly
        population = []
        for i in range(0, pop_size):
            population.append(self.individual_factory())
        self.population = population

    def evaluate(self):
        a_fits_list = []
        for individual in self.population:
            a_fits_list.append(self.fitness(individual))
        return a_fits_list

    def select(self):
        # Maximizes fitness function
        winner = None
        for i in range(0, 5):
            an_individual = random.choice(self.population)
            if winner is None or self.fitness(an_individual) > self.fitness(winner):
                winner = an_individual
        return winner

    def crossover(self, individual_1, individual_2):
        index = random.randrange(0, self.genes_number)
        new_individual = []
        for i in range(0, index):
            new_individual.append(individual_1[i])
        for i in range(index, self.genes_number):
            new_individual.append(individual_2[i])
        return new_individual

    def mutation(self, individual_1):
        new_individual = individual_1
        if random.random() <= self.mutation_rate:
            indexes_list = list(range(self.genes_number))
            mutation_number = int(self.genes_number * self.mutation_rate)
            chosen_indexes = random.sample(indexes_list, mutation_number)
            for index in chosen_indexes:
                new_gene = self.gene_factory()
                new_individual[index] = new_gene
        return new_individual

    def run(self):
        # for i in range(0, self.max_iter):
        i = 0
        while not self.termination_condition(self.best_fitness):
            new_population = []
            if self.reproduce_crossover:
                for j in range(0, self.pop_size):
                    parent_1 = self.select()
                    parent_2 = self.select()
                    child = self.crossover(parent_1, parent_2)
                    new_population.append(child)
                self.population = new_population
            else:
                for j in range(0, self.pop_size):
                    parent = self.select()
                    child = self.mutation(parent)
                    new_population.append(child)
                self.population = new_population
            self.fits_list = self.evaluate()

            # save best, worst and average fitness of each generation
            self.best_fitness.append(max(self.fits_list))
            self.worst_fitness.append(min(self.fits_list))
            self.average_fitness.append(mean(self.fits_list))
            print(self.best_fitness[-1])  # this is useful to determine whether the perfect score (fitness) was reached
            i += 1
        return self.population, self.fits_list

    def get_best_fitness(self):
        return self.best_fitness

    def get_worst_fitness(self):
        return self.worst_fitness

    def get_average_fitness(self):
        return self.average_fitness

    def generations(self):
        return len(self.best_fitness)

# BINARY NUMBER


#GA = GA(pop_size=20, mutation_rate=0, fit=fitness, gene_factory=gene_factory, indiv_factory=individual_factory,
#        termination_condition=0, max_iter=200, genes_number=NUMBER_OF_GENES, is_crossover=True)
#pop, list_fitness = GA.run()


# FINDING A WORD


#GA2 = GA(pop_size=150, mutation_rate=0, fit=fitness2, gene_factory=gene_factory2, indiv_factory=individual_factory2,
# termination_condition=0, max_iter=2500, genes_number=NUMBER_OF_GENES2, is_crossover=True)
#pop, list_fitness = GA2.run()
#for ind in pop:
#    print(ind)
#for fit in list_fitness:
#    print(fit)





# 0-1-KNAPSACK


