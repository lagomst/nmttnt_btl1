import numpy

class Board:

    grid_size = 0
    values = 0
    is_fixed = 0

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.values = numpy.zeros(self.row_size() * self.row_size(), dtype=int) # Values store a 9x9 grid starting with 0, eg empty.
        self.is_fixed = 0
        pass
    
    def total_size(self):
        return self.row_size() * self.row_size()

    def row_size(self):
        return self.grid_size * self.grid_size

    def importFixedBoard(self, fixed_board: list):
        for i in range(self.total_size()):
            self.values[i] = fixed_board[i]
            if fixed_board[i] != 0:
                self.is_fixed |= (1 << i) # Set ith bit to 1
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

    def is_fixed_at(self, cell):
        return self.is_fixed & (1 << cell) != 0
    
    def set_values_nofixed(self, new_values): # Fill new value without changing is_fixed  
        self.values = new_values

    def display_fixed(self):
        cell = 0
        row = ""
        for i in range(0, self.total_size(), 1):
            row += "X" if self.is_fixed_at(i) else "O" # If flag bit at ith cell is 1, mark X, otherwise mark O
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
    
    def get_val_by_coor(self, r, c):
        return self.values[r * self.row_size() + c]
    
    def get_val_by_pos(self, pos):
        return self.values[pos]

    def retrieve_row_from_cell(self, cell):
        return int(cell // self.row_size())
    
    def retrieve_col_from_cell(self, cell):
        return int(cell % self.row_size())
    
    def retrieve_grid_from_cell(self, cell): 
        """
        Return top-left cell of a grid
        """
        c = self.retrieve_col_from_cell(cell) 
        r = self.retrieve_row_from_cell(cell)
        grid = int(c//self.grid_size) * self.grid_size + int(r//self.grid_size) * self.row_size()
        return grid

