import random
import string
from statistics import mean

# BINARY NUMBER PROBLEM
BIN_NUMBER_OF_GENES = 10
BINARY_NUMBER = "0001100100"


def bin_fitness(indi):
    score = 0
    for i in range(BIN_NUMBER_OF_GENES):
        if str(indi[i]) == BINARY_NUMBER[i]:
            score += 1
    return score


def bin_gene_factory():
    rand_value = random.randrange(0, 2)
    return rand_value


def bin_individual_factory():
    return [bin_gene_factory() for i in range(BIN_NUMBER_OF_GENES)]


# FINDING A WORD PROBLEM
WORD_NUMBER_OF_GENES = 10
WORD = "holaholaen"


def word_fitness(indi):
    score = 0
    for i in range(WORD_NUMBER_OF_GENES):
        if str(indi[i]) == WORD[i]:
            score += 1
    return score


def word_gene_factory():
    return random.choice(string.ascii_letters.lower())


def word_individual_factory():
    return [word_gene_factory() for i in range(WORD_NUMBER_OF_GENES)]


# UNBOUND-KNAPSACK
KNAP_NUMBER_OF_GENES = 15
OPT_FITNESS = 36
SOLUTION = [(4, 10), (4, 10), (4, 10), (1, 2), (1, 2), (1, 2), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]


def knap_fitness(indi):
    score = 0
    weight = 0
    for i in range(KNAP_NUMBER_OF_GENES):
        weight += indi[i][0]
        score += indi[i][1]
    penalty = weight - 15
    if penalty > 0:
        score = score - abs(penalty) * 5
    return score


def knap_gene_factory():
    weight, value = random.choice([(1, 1), (1, 2), (2, 2), (4, 10), (12, 4), (0, 0)])
    return weight, value


def knap_individual_factory():
    return [knap_gene_factory() for i in range(KNAP_NUMBER_OF_GENES)]


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
        for i in range(5):
            an_individual = random.choice(self.population)
            if winner is None or self.fitness(an_individual) > self.fitness(winner):
                winner = an_individual
        return winner

    def crossover(self, individual_1, individual_2):
        index = random.randrange(0, self.genes_number)
        new_individual = individual_1[0:index] + individual_2[index::]
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
        i = 0
        while not self.termination_condition(self.best_fitness):  # must change parameters if it's necessary
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


#GA = GA(pop_size=20, mutation_rate=0, fit=bin_fitness, gene_factory=bin_gene_factory, indiv_factory=bin_individual_factory,
#        termination_condition=lambda i: i == 20, number_of_genes=BIN_NUMBER_OF_GENES, is_crossover=True)
#pop, list_fitness = GA.run()


# FINDING A WORD


#GA2 = GA(pop_size=300, mutation_rate=0, fit=word_fitness, gene_factory=word_gene_factory, indiv_factory=word_individual_factory,
#               termination_condition=lambda i: i == 50, number_of_genes=WORD_NUMBER_OF_GENES, is_crossover=True)
#pop, list_fitness = GA2.run()

# PRINT RESULTS

#for ind in pop:
#    print(ind)
#for fit in list_fitness:
#    print(fit)


