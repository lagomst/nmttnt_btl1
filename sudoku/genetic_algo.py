from board import Board
from sudoku import Population


def rank_population(population):
    """
    Evaluate each individual of the population and give a ranking note whether it solves a lot or a little the problem
    (based on fitness method)
    :param population: (array) array of individuals to rank
    :return: (list) a sorted (asc) population. Individuals are sorted based on their fitness score
    """
    fit_scores = {}
    for individual in population:
        fit_scores[individual] = individual.get_fit()
    return sorted(fit_scores, key=fit_scores.get)