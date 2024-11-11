import numpy
import random

digit_num = 9 # Number of digits

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
        if(x.fitness < y.fitness)
            return 1
        if(x.fitness == y.fitness)
            return 0
        return -1

class Candidate:
    def __init__(self):
        self.values = numpy.zeros((digit_num, digit_num), dtype=int) # Values store a 9x9 grid starting with 0, eg empty.
        self.fit = None
        
    def update_fit(self):
        pass
    
    def display_all(self):
        cell = 1
        for i in self.values:
            print(i)
            if(cell%9==0):
                print('\n')
            elif(cell%3==0):
                print(" || ")
            else:
                print(" ")
            cell+=1
        pass

class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self):
        self.given = None
        return
    
    def load(self, path):
        # Load a configuration to solve.
        with open(path, "r") as f:
            values = numpy.loadtxt(f).reshape((Nd, Nd)).astype(int)
            self.given = Given(values)
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(Nd*Nd), fmt='%d')
        return