from board import Board
from pencilmark import PencilMark
from sudoku import Sudoku_GA
import configparser

def read_board_from_file(filename):
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
    board_filename="./sudoku/3x3_hard2.txt"
    params_filename="./sudoku/params.txt"
    grid_size, example_board = read_board_from_file(board_filename)
   
    board = Board()
    board.import_fixed_board(grid_size, example_board)

    # TODO: make .ini file and use config to set these values
    # BTW, I find these values should be set as default for 3x3 grid
    population_size=2500 # Total population size in each generations
    best_selection_rate=0.015 # Percentage of population that has highest fit score to become parents of next generation
    random_selection_rate=0.01 # Percentage of population that is randomly picked to become parents
    max_nb_generations=400 # Max total ammount of generations allowed to run
    mutation_rate=0.04 # Chance of an individual mutating
    
    # Number of consecutive generation that do not improve before restarting
    restart_after_n_generations_without_improvement= 100  
    
    sudoku = Sudoku_GA(population_size, best_selection_rate, random_selection_rate,
                      max_nb_generations, mutation_rate,
                      restart_after_n_generations_without_improvement, 
                      grid_size, board)
    
    sudoku.run()
    
    print("done")

if __name__ == '__main__':
    main()
    