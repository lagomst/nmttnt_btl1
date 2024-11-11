import numpy
import random

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
    def __init__(self):
        self.board = Board()
        self.fit = None
        
    def update_fit(self):
        pass
    


class Board:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.values = numpy.zeros(self.row_size() * self.row_size(), dtype=int) # Values store a 9x9 grid starting with 0, eg empty.
        self.isFixed = 1 << (self.row_size() * self.row_size()) - 1
        pass
    
    def total_size(self):
        return self.grid_size * self.grid_size * 9

    def row_size(self):
        return self.grid_size * 3

    def importFixedBoard(self, fixed_board: list):
        for i in range(0, self.total_size() - 1, 1):
            self.values[i] = fixed_board[i]
            if fixed_board[i] != 0:
                self.isFixed |= (1 << i) # Set ith bit to 1, (bit ith is now fixed)
            i+=1
            pass
        pass

    def display_board(self):
        cell = 1
        row = ""
        for val in self.values:
            row += str(val)
            if(cell%(self.row_size())==0): # next row
                print(row)
                if(cell % (self.grid_size * self.row_size()) == 0):
                    line = ""
                    for i in range(1, len(row), 1):
                        line += '-'
                    print(line)
                row = "" # Reset row's value
            elif(cell%(self.grid_size)==0): # next grid
                row += " || "
            else:
                row += " " # next number
            cell+=1
        pass

    def display_fixed(self):
        cell = 1
        row = ""
        for i in range(0, self.total_size() - 1, 1):
            row += "X" if self.isFixed & (1 << i) != 0 else "O" # If flag bit at ith cell is 1, mark X, otherwise mark O
            if(cell%(self.row_size())==0): # next row
                print(row)
                if(cell % (self.grid_size * self.row_size()) == 0):
                    line = ""
                    for i in range(1, len(row), 1):
                        line += '-'
                    print(line)
                row = "" # Reset row's value
            elif(cell%(self.grid_size)==0): # next grid
                row += " || "
            else:
                row += " " # next number
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
            values = numpy.loadtxt(f).reshape((self.row_size, self.row_size)).astype(int)
            self.given = Given(values)
        return

    def save(self, path, solution):
        # Save a configuration to a file.
        with open(path, "w") as f:
            numpy.savetxt(f, solution.values.reshape(self.row_size * self.row_size), fmt='%d')
        return