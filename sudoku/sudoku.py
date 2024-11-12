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
    def __init__(self, grid_size=3):
        self.board = Board(grid_size)
        self.fit = None
        
    def update_fit(self):
        pass
    
class Board:

    grid_size = 0
    values = 0
    isFixed = 0

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.values = numpy.zeros(self.row_size() * self.row_size(), dtype=int) # Values store a 9x9 grid starting with 0, eg empty.
        self.isFixed = 0
        pass
    
    def total_size(self):
        return self.grid_size * self.grid_size * 9

    def row_size(self):
        return self.grid_size * 3

    def importFixedBoard(self, fixed_board: list):
        for i in range(self.total_size()):
            self.values[i] = fixed_board[i]
            if fixed_board[i] != 0:
                self.isFixed |= (1 << i) # Set ith bit to 1
            i+=1
            pass
        pass

    def display_board(self):
        cell = 0
        row = ""
        for val in self.values:
            row += str(val)
            cell+=1
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
            
        pass

    def isFixedAt(self, cell):
        return self.isFixed & (1 << cell) != 0

    def display_fixed(self):
        cell = 0
        row = ""
        for i in range(0, self.total_size(), 1):
            row += "X" if self.isFixedAt(i) else "O" # If flag bit at ith cell is 1, mark X, otherwise mark O
            cell+=1
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
            
        pass

    def get_cell_val_at(self, r, c):
        return self.board.values[r * self.grid_size + c]

    def retrieve_row_from_cell(self, cell):
        return int(cell / self.grid_size)
    
    def retrieve_col_from_cell(self, cell):
        return int(cell % self.grid_size)
    
    def retrieve_grid_from_cell(self, cell): 
        """
        Return top-left cell of a grid
        """
        c = self.retrieve_col_from_cell() 
        r = self.retrieve_row_from_cell()
        return int(c/3) + int(r/3)*self.row_size
    
class PencilMark:
    def __init__(self, board=Board):
        self.board = board
        pass
    
    def set_bit_to_one_at(bitmask=int, pos=int):
        return bitmask ^ (1 << pos)
    
    def set_bit_to_zero_at(bitmask=int, pos=int):
        return bitmask & ((1 << pos) ^ (1 << pos))
    
    def _run_one_iteration(self):
        """
        Pencil mark method: each cell has a bool array (all init to True). Each of the boolean represents the digit
        (from 1 to N = objects size). For each given fixed value we put other boolean (so representing other digits) to
        False in same row, column, grid
        :return: (dict) a pencil mark object. Key is the row/column position and value is a boolean array where True
        means that the value is fixed
        """
        sudoku_size = self.board.total_size()
        grid_size = self.board.grid_size

        # 1- Init a pencil mark with all set to True
        init_flag = (1 << (grid_size * grid_size)) - 1 # All bit set to 1
        
        pencil_mark = numpy.full(sudoku_size, init_flag, dtype=int)
        
        for cell in range(sudoku_size):
            if self.board.isFixedAt(cell):
                val = self.board.get_cell_val_at(cell)
                pencil_mark[cell] ^= 1 << val # Set flag bit to 1
                continue

            # Remove grid duplicates
            grid = self.board.retrieve_grid_from_cell(cell) # Get the position of the top left cell of a grid
            offset = 0 # How far away is cur_cell from cell
            for i in range(grid_size * grid_size):
                cur_cell = grid + offset
                val = self.board.get_cell_val_at(cur_cell)
                if val != 0 and cur_cell != cell:
                    pencil_mark[cell] &= (1 << val) ^ (1 << val) # Set flag bit to 0
                offset += 1
                if offset % grid_size == 0: # When currnet position goes out of grid,
                    offset += grid_size * 2 # proceed to next row from the current position
            
            r = self.board.retrieve_row_from_cell(cell)
            c = self.board.retrieve_col_from_cell(cell)
            
            # Remove column duplicates
            for i in range(grid_size * 3):
                if abs(i - r) <= 1: # Skip over the two adjacent cells and itself in the same row
                    continue
                val = self.board.get_cell_val_at(i, c)
                if val==0:
                    continue
                pencil_mark[cell] &= (1 << val) ^ (1 << val) # Set flag bit to 0
            
            # Remove row duplicates
            for i in range(grid_size * 3):
                if abs(i - c) <= 1: # Skip over the two adjacent cells and itself in the same column
                    continue
                val = self.board.get_cell_val_at(r, i)
                if val==0:
                    continue
                pencil_mark[cell] &= (1 << val) ^ (1 << val) # Set flag bit to 0
        return pencil_mark

    @staticmethod
    def generate_values_from_pencil(pencil_mark):
        """
        Given a pencil mark object, iterate over it and if at some position there is a single value found it means
        either it is a fixed one (i.e known at the beginning) or a predetermined one (i.e there is no option that this
        value). In this case we can add this new found value, otherwise we keep it as unknown with a '0' digit character
        :param pencil_mark: (dict) a pencil mark object. Key is the row/column position and value is a boolean array
        where True means that the value is fixed
        :return: (array) new values determined with such a pencil mark
        """
        new_values = []
        for flag in pencil_mark:
            if(flag.bit_count() == 1):
                new_values.append(flag.bit_length()) # Bit length return number of bits needed to represent a number
                                                     # When there's only one 1 bit, it returns where that bit is
            else:
                new_values.append(0)
        return new_values

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