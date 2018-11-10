import numpy as np


class Individual():
    fitness = None
    genome = None

    def __init__(self, fitness, genome):
        self.fitness = fitness
        self.genome = genome

    def __repr__(self):
        return 'Individual(fitness={}, genome={})'.format(self.fitness, self.genome)


class AbstractPopulation():

    def __init__(self, n_individuals, n_breeding, tournament_size, n_mutations):

        self._n_individuals = n_individuals  # number of individuals in parent population
        self._n_breeding = n_breeding  # size of breeding population
        self._tournament_size = tournament_size  # size of tournament for selection breeding population
        self._n_mutations = n_mutations  # number of mutations in genome per individual

        self._parents = None  # list of parent individuals
        self._offsprings = None  # list of offspring individuals
        self._combined = None  # list of all individuals

    def generate_random_parent_population(self):
        self._parents = self._generate_random_individuals()

    def generate_random_offspring_population(self):
        self._offsprings = self._generate_random_individuals()

    def compute_fitness(self, objective):
        self._combined = []

        for ind in self._parents:
            fitness = objective(ind.genome)
            ind.fitness = fitness
            self._combined.append(Individual(fitness, ind.genome))

        for ind in self._offsprings:
            fitness = objective(ind.genome)
            ind.fitness = fitness
            self._combined.append(Individual(fitness, ind.genome))

    def sort(self):
        self._combined = sorted(self._combined, key=lambda x: -x.fitness)

    def create_new_parent_population(self):
        self._parents = []
        for i in range(self._n_individuals):
            self._parents.append(self._combined[i])

    def create_new_offspring_population(self):
        # fill breeding pool via tournament selection
        breeding_pool = []
        while len(breeding_pool) < self._n_breeding:
            sample = sorted(np.random.permutation(self._combined)[:self._tournament_size], key=lambda x: -x.fitness)
            breeding_pool.append(sample[0])

        offsprings = self._crossover(breeding_pool)
        offsprings = self._mutate(offsprings)

        self._offsprings = offsprings

    def _generate_random_individuals(self):
        raise NotImplementedError()

    def _crossover(self, breeding_pool):
        raise NotImplementedError()

    def _mutate(self, offsprings):
        raise NotImplementedError()

    def local_search(self, objective):
        raise NotImplementedError()

    @property
    def parents(self):
        return self._parents

    @property
    def fitness(self):
        return [ind.fitness for ind in self._parents]