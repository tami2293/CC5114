import random
import string
from statistics import mean
from arboles import *
from abstract_syntax_tree import *
import sys
import inspect


class GP(object):
    def __init__(self, pop_size, mutation_rate, fit, indiv_factory, termination_condition, is_crossover):
        self.pop_size = pop_size
        print("Creating individuals...")
        self.mutation_rate = mutation_rate
        self.fitness = fit
        self.fits_list = []  # Results list of each individual
        self.individual_factory = indiv_factory
        self.termination_condition = termination_condition
        self.reproduce_crossover = is_crossover  # determines reproduction type
        self.best_fitness = []  # best fitness for each generation
        self.worst_fitness = []  # worst fitness for each generation
        self.average_fitness = []  # average fitness for each generation

        self.max_size = []

        print(self.reproduce_crossover)

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

    def select_max(self):
        # Maximizes fitness function: takes random individuals and chooses the one with the max. value
        winner = None
        for i in range(5):
            an_individual = random.choice(self.population)
            if winner is None or self.fitness(an_individual) > self.fitness(winner):
                winner = an_individual
        return winner

    def select_min(self):
        # Minimizes fitness function: takes random individuals and chooses the one with the min. value
        winner = None
        for i in range(5):
            an_individual = random.choice(self.population)
            if winner is None or self.fitness(an_individual) < self.fitness(winner):
                winner = an_individual
        return winner

    def crossover(self, individual_1, individual_2):
        a_size = individual_1.get_size()
        self.max_size.append(a_size)
        new_individual = individual_1.copy()  # First parent copy

        # Pick random first parent node
        child_list_1 = new_individual.serialize()
        random_index_1 = random.randrange(0, len(child_list_1))
        to_replace = child_list_1[random_index_1]

        # Pick random second parent node
        child_list_2 = individual_2.serialize()
        random_index_2 = random.randrange(0, len(child_list_2))
        replacement = child_list_2[random_index_2].copy()

        # Replace first parent child picked by second parent child picked
        to_replace.replace(replacement)

        return new_individual

    def mutation(self, individual_1):
        if random.random() <= self.mutation_rate:
            new_individual = individual_1.copy()

            # Pick random first parent node
            child_list_1 = new_individual.serialize()
            random_index_1 = random.randrange(0, len(child_list_1))
            to_replace = child_list_1[random_index_1]

            # Create random individual
            random_node = self.individual_factory()

            # Replace first individual node picked by random generated node
            to_replace.replace(random_node)

            return new_individual

        return individual_1

    def run(self):
        i = 0
        while not self.termination_condition(i):  # must change parameters if it's necessary (self.best_fitness)
            new_population = []
            if self.reproduce_crossover:
                for j in range(0, self.pop_size):
                    parent_1 = self.select_min()
                    parent_2 = self.select_min()
                    child = self.crossover(parent_1, parent_2)
                    new_population.append(child)
                self.population = new_population
            else:
                for j in range(0, self.pop_size):
                    parent = self.select_min()
                    child = self.mutation(parent)
                    new_population.append(child)
                self.population = new_population
            self.fits_list = self.evaluate()

            # save best, worst and average fitness of each generation
            self.best_fitness.append(min(self.fits_list))
            self.worst_fitness.append(max(self.fits_list))
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


