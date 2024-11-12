import numpy
import random
import bitmanip as bit_manip

class Population:
    def __init__(self):
        self.candidate = []
        return
    
    def seed(self):
        pass
    
    def sort(self):
        self.candidate.sort(self.sort_fit)
        return
    
    def sort_fit(self, x, y):
        if(x.fitness < y.fitness):
            return 1
        if(x.fitness == y.fitness):
            return 0
        return -1

class Candidate:
    def __init__(self, grid_size=3):
        self.board = Board(grid_size)
        self.fit = None
        
    def update_fit(self):
        pass

class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.given = None
        return
    
    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            values = numpy.loadtxt(f).reshape((self.row_size, self.row_size)).astype(int)
            self.given = Given(values)
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(self.row_size * self.row_size), fmt='%d')
        return