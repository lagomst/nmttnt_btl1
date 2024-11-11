from sudoku import Board

def main():
    pattern = [5, 0, 3, 1, 0, 6, 4, 8, 0, 7, 9]
    example_board = []
    for i in range(1, 9, 1):
        example_board.extend(pattern)
    board = Board(3)
    board.importFixedBoard(example_board)
    board.display_board()
    board.display_fixed()
    print("done")

if __name__ == '__main__':
    main()
    