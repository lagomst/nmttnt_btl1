from board import Board
from pencilmark import PencilMark
import numpy

def main():
    grid_size = 2
    row_size = grid_size * grid_size
    total_size = row_size * row_size
    #example_board = numpy.random.randint(0, grid_size * grid_size + 1, total_size)
    example_board = [2, 1, 4, 0, 0, 0, 1, 2, 4, 0, 2, 1, 1, 2, 0, 0]
    board = Board(grid_size)
    board.importFixedBoard(example_board)
    board.display_board()
    pencil_board = PencilMark(board)
    pencil_board.run()
    print("Display pencil:")
    pencil_board.board.display_board()
    print("done")

if __name__ == '__main__':
    main()
    