import numpy
import random

class Board:

    grid_size = 0
    values = 0
    is_fixed = 0
    fit = None

    def __init__(self, grid_size=0):
        """
        :params grid_size: Length of a grid in
        :params values: An array containing values for every cell. 0 means cell is empty
        :params values: A bitmask determining if a cell is fixed from the beginning  
        """
        self.grid_size = grid_size
        self.values = numpy.zeros(self.row_size() * self.row_size(), dtype=int)
        self.is_fixed = 0
        pass
    
    def total_size(self):
        return self.row_size() * self.row_size()

    def row_size(self):
        return self.grid_size * self.grid_size

    def import_fixed_board(self, grid_size:int, fixed_board: list):
        self.grid_size = grid_size
        self.values = numpy.zeros(self.row_size() * self.row_size(), dtype=int)
        for i in range(self.total_size()):
            self.values[i] = fixed_board[i]
            if fixed_board[i] != 0:
                self.is_fixed |= (1 << i) # Set ith bit to 1
            i+=1


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

    def is_cell_fixed_at(self, cell):
        return (self.is_fixed & (1 << cell)) != 0
    
    def set_cell_to_fixed(self, cell):
        self.is_fixed |= (1 << cell)
    
    def set_values_nofixed(self, new_values): # Fill new value without changing is_fixed  
        self.values = new_values
    
    def write_to_cell_nofixed(self, cell, new_val):
        self.values[cell] = new_val

    def display_fixed(self):
        cell = 0
        row = ""
        for i in range(0, self.total_size(), 1):
            row += "X" if self.is_cell_fixed_at(i) else "O" # mark X if values is fixed, otherwise mark O
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
                row += " | "
            else:
                row += " " # next number
            
    def fill_random_grid_valid(self, grid_id=int):
        cells = self.retrieve_cells_in_grid(grid_id)
        available_digits = numpy.arange(1, self.grid_size * self.grid_size + 1, 1).tolist()
    # Remove values that has already been in grid
        for cell in cells:
            val = self.get_val_by_pos(cell)
            if val != 0:
                available_digits.remove(val)
        if len(available_digits) == 0:
            return
        # Shuffle the remaining values and fill each
        # of them from left to right, top to bottom
        random.shuffle(available_digits)
        for cell in cells:
            val = self.get_val_by_pos(cell)
            if val == 0:
                last_digits = len(available_digits) - 1
                self.write_to_cell_nofixed(cell, available_digits[last_digits])
                available_digits.pop()

    def fill_random_board(self):
        grid_cells = self.retrieve_all_grid_id()
        for cell in grid_cells:
            self.fill_random_grid_valid(cell)
        self.update_fit()
    
    def get_pos_by_coor(self, r, c):
        return r * self.row_size() + c
    
    def get_val_by_coor(self, r, c):
        """
        Return cell's value by row and column
        """
        return self.values[self.get_pos_by_coor(r, c)]
    
    def get_val_by_pos(self, pos):
        """
        Return cell's value by numbered position, from left to right, top to bottom.
        Start at 0.
        """
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

    def retrieve_all_grid_id(self):
        grids = []
        grid_row = 0
        grid_col = 0
        max_size = self.total_size()
        while grid_row < self.row_size():
            while grid_col < self.row_size():
                grid_cell = self.get_pos_by_coor(grid_row, grid_col)
                grids.append(grid_cell)
                grid_col += self.grid_size
            grid_col = 0
            grid_row += self.grid_size
        return grids
    
    def retrieve_cells_in_grid(self, grid_id):
        """
        Return all cells' pos in a grid.
        """
        cells = []
        offset = 0
        for i in range(self.grid_size * self.grid_size):
            cur_cell = grid_id + offset
            cells.append(cur_cell)
            offset += 1 
            if offset % self.grid_size == 0: # When offset goes out of grid, proceed to next row instead
                offset -= self.grid_size
                offset += self.row_size()
        return cells
    
    def update_fit(self):
        grid_size = self.grid_size
        row_size = self.row_size()
        r = 0
        c = 0
        duplicates = 0
        # Each cell is checked twice: one for column and one for row 
        for n in range(row_size):
            # Check column duplicate
            buckets = numpy.zeros(grid_size * grid_size + 1, dtype=int)
            for i in range(row_size):
                val = self.get_val_by_coor(i, c)
                buckets[val] += 1
            # Tally duplicates from buckets
            if buckets[0] > 0:
                raise Exception("This board isn't filled up before grading fitness score!")
            for digit in buckets:
                if digit > 1: 
                    duplicates += digit - 1 # A digit must appear no more than once per column/row           
            
            # Check row duplicate
            buckets = numpy.zeros(grid_size * grid_size + 1, dtype=int)
            for i in range(row_size):
                val = self.get_val_by_coor(r, i)
                buckets[val] += 1
            # Tally duplicates from buckets
            if buckets[0] > 0:
                raise Exception("This board isn't filled up before grading fitness score!")
            for digit in buckets:
                if digit > 1: 
                    duplicates += digit - 1 # A digit must appear no more than once per column/row
           
            # Increment to next row
            r += 1
            c += 1
        
        self.fit = duplicates
        return self.fit
    
    def get_fit(self):
        return self.fit
    
    def swap_two_values(self):
        """
        Swapping two values reside in a same grid
        """
        # Pick a random grid
        grids = self.retrieve_all_grid_id()
        random_index = random.randint(0, len(grids) - 1)
        picked_grid = grids[random_index]
        # Pick randomly two non-fixed cells in grid
        grid_cells = self.retrieve_cells_in_grid(picked_grid)
        non_fixed_cells = []
        for cell in grid_cells:
            if self.is_cell_fixed_at(cell):
                pass
            else:
                non_fixed_cells.append(cell)
        if int(len(non_fixed_cells)) < 2:
            return
        picked_cells = random.sample(non_fixed_cells, 2)
        # Swap values
        a = picked_cells[0]
        b = picked_cells[1]
        temp = self.values[a]
        self.values[a] = self.values[b]
        self.values[b] = temp
        
        self.update_fit()
        return