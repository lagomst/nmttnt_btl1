from board import Board
from pencilmark import PencilMark
from sudoku import Sudoku_GA
import numpy

def read_from_file(filename):
    """
    Read from file, return grid size as int and the board's values as an array
    """
    file = open(filename, "r")
    grid_size = int(file.readline())
    
    array = []
    
    lines = file.readlines()
    for line in lines:
        list_int = list(map(int,  line.split(' ')))
        array.extend(list_int)
    
    return grid_size, array

def main():
    filename="./sudoku/3x3.txt"
    grid_size, example_board = read_from_file(filename)
    # row_size = grid_size * grid_size
    # total_size = row_size * row_size
    #example_board = numpy.random.randint(0, grid_size * grid_size + 1, total_size)
    #example_board = [2, 1, 4, 0, 0, 0, 1, 2, 4, 0, 2, 1, 1, 2, 0, 0]
    
    board = Board()
    board.import_fixed_board(grid_size, example_board)
    
    population_size = 1000
    best_selection_rate = 0.05
    random_selection_rate = 0.025
    max_nb_generations = 100
    mutation_rate = 0.01
    presolving = 0
    restart_after_n_generations_without_improvment = 40
    
    sudoku = Sudoku_GA(population_size, best_selection_rate, random_selection_rate,
                      max_nb_generations, mutation_rate,
                      presolving, restart_after_n_generations_without_improvment, 
                      grid_size, board)
    
    sudoku.run()
    
    print("done")

if __name__ == '__main__':
    main()
    