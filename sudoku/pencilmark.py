from board import Board
import bitmanip as bit_manip
import numpy

class PencilMark:
    def __init__(self, board=Board):
        self.board = board
        pass
    
    def _run_one_iteration(self):
        sudoku_size = self.board.total_size()
        grid_size = self.board.grid_size
        row_size = self.board.row_size()

        # 1- Init a pencil mark with all set to True
        init_flag = (1 << (grid_size * grid_size)) - 1 # All bit set to 1
        
        pencil_mark = numpy.full(sudoku_size, init_flag, dtype=int)
        
        for cell in range(sudoku_size):
            init_val = self.board.get_val_by_pos(cell)
            if init_val != 0:
                pencil_mark[cell] = bit_manip.set_bit_to_one_at(0, init_val - 1) # Set flag bit to 1
                continue

            # Remove grid duplicates
            grid = self.board.retrieve_grid_from_cell(cell)
            offset = 0
            for i in range(grid_size * grid_size):
                cur_cell = grid + offset
                val = self.board.get_val_by_pos(cur_cell)
                if val != 0 and cur_cell != cell:
                    pencil_mark[cell] = bit_manip.set_bit_to_zero_at(pencil_mark[cell], val - 1) # Set flag bit to 0
                offset += 1
                if offset % grid_size == 0:
                    offset = offset - grid_size + row_size
            
            r = self.board.retrieve_row_from_cell(cell)
            c = self.board.retrieve_col_from_cell(cell)
            
            # Remove column duplicates
            for i in range(row_size):
                if i == r: 
                    continue
                val = self.board.get_val_by_coor(i, c)
                if val==0:
                    continue
                pencil_mark[cell] = bit_manip.set_bit_to_zero_at(pencil_mark[cell], val - 1) # Set flag bit to 0
            
            # Remove row duplicates
            for i in range(row_size):
                if i == c:
                    continue
                val = self.board.get_val_by_coor(r, i)
                if val==0:
                    continue
                pencil_mark[cell] &= bit_manip.set_bit_to_zero_at(pencil_mark[cell], val - 1) # Set flag bit to 0
        return pencil_mark
    
    def run(self):
        """
        Start the pencil mark algorithm by giving it the initial values (unknown values are represented by a '0' digit).
        The strategy is to loop until we cannot deduce new values to place in the given objects. For very basic puzzles,
        this algorithm might fill it up.

        The puzzle this pencil mark is running on has its values changed if new one are found
        """
        found_new = True

        while found_new:
            pencil_mark = self._run_one_iteration()
            new_values = self.generate_values_from_pencil(pencil_mark)
            if (numpy.array_equal(new_values, self.board.values)):
                found_new = False
            self.board.set_values_nofixed(new_values)
    
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
            if(bit_manip.get_bit_count(flag) == 1):
                new_values.append(bit_manip.get_bit_length(flag)) 
                # Bit length return number of bits needed to represent a number
                # When there's only one 1 bit, it returns where that bit is
            else:
                new_values.append(0)
        return new_values
    
