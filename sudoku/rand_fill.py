from board import Board
import numpy
from random import shuffle

def fill_random_grid_valid(board=Board, grid_id=int):
    cells = board.retrieve_cells_in_grid(grid_id)
    available_digits = numpy.arange(1, board.grid_size * board.grid_size + 1, 1).tolist()
    # Remove values that has already been in grid
    for cell in cells:
        val = board.get_val_by_pos(cell)
        if val != 0:
            available_digits.remove(val)
    if len(available_digits) == 0:
        return
    # Shuffle the remaining values and fill each
    # of them from left to right, top to bottom
    shuffle(available_digits)
    for cell in cells:
        val = board.get_val_by_pos(cell)
        if val == 0:
            last_digits = len(available_digits) - 1
            board.write_to_cell_nofixed(cell, available_digits[last_digits])
            available_digits.pop()

def fill_random_board(board=Board):
    grid_cells = board.retrieve_all_grid_id()
    for cell in grid_cells:
        fill_random_grid_valid(board, cell)