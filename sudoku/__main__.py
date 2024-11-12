from sudoku import Board
import numpy

def main():
    grid_size = 2
    row_size = grid_size * 3
    total_size = row_size * row_size
    example_board = numpy.random.randint(0, 9, total_size)
    board = Board(grid_size)
    board.importFixedBoard(example_board)
    board.display_board()
    board.display_fixed()
    print("done")

if __name__ == '__main__':
    main()
    