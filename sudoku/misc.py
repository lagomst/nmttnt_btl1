# Note: no need to include this in final report
import numpy
import math

def find_optimal_rates(population_size):
    """
    Return best and random selection rate from a given population size
    """
    # We want to the total number of combination of breeders to be slightly larger than total population,
    # in order to avoid one pair giving birth to multiple children, raising the chance of creating clones
    # In short: Find rate x where "" (n * x) choose 2 > n "" with n is the total population size
    # Simplifying the inequation gives us n*x^2 - x - 2 > 0
    # And solving it give total rate we need  
    delta = 1 + 4 * population_size * 2
    total_rate =(1 + math.sqrt(delta)) / (2 * population_size) + 0.001 # Add extra 0.001 to ensure the inequation always true
    # Divide total rate into best and random rate
    best_rate = total_rate * 2/3
    random_rate = total_rate / 3
    return  best_rate, random_rate