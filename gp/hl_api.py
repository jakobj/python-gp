import numpy as np


def evolve(pop, objective, max_generations, min_fitness, record_history=False, *, label=None):
    """
    Evolves a population and returns the history of fitness of parents.
    """

    # generate initial parent population of size N
    pop.generate_random_parent_population()

    # generate initial offspring population of size N
    pop.generate_random_offspring_population()

    # data structure for recording evolution history
    history = {}
    if record_history:
        history['fitness'] = np.empty((max_generations, pop._n_parents))

    # perform evolution
    for generation in range(max_generations):

        # combine parent and offspring populations
        pop.create_combined_population()

        #  compute fitness for all objectives for all individuals
        pop.compute_fitness(objective, label=label)

        # sort population according to fitness & crowding distance
        pop.sort()

        # fill new parent population according to sorting
        pop.create_new_parent_population()

        # generate new offspring population from parent population
        pop.create_new_offspring_population()

        if record_history:
            history['fitness'][generation] = pop.fitness_parents()

        if pop.champion.fitness + 1e-10 >= min_fitness:
            if record_history:
                history['fitness'] = history['fitness'][:generation]
            break

    return history