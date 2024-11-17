from board import Board
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

def load_params_from_config(filename):
    """
    Load parameters for the Genetic Algorithm from a config file
    """
    config = configparser.ConfigParser()
    config.read(filename)
    
    # Read parameters from the GeneticAlgorithm section
    params = config['GeneticAlgorithm']
    return {
        "population_size": int(params['population_size']),
        "best_selection_rate": float(params['best_selection_rate']),
        "random_selection_rate": float(params['random_selection_rate']),
        "max_nb_generations": int(params['max_nb_generations']),
        "mutation_rate": float(params['mutation_rate']),
        "restart_after_n_generations_without_improvement": int(params['restart_after_n_generations_without_improvement']),
        "best_score_to_keep": int(params['best_score_to_keep'])
    }

def main():
    board_filename = "./sudoku/3x3_49.txt"
    params_filename = "./sudoku/params.ini"

    grid_size, example_board = read_board_from_file(board_filename)

    # Load the Genetic Algorithm parameters from the config file
    params = load_params_from_config(params_filename)

    board = Board()
    board.import_fixed_board(grid_size, example_board)

    # Pass the parameters to the Sudoku_GA class
    sudoku = Sudoku_GA(
        params['population_size'],
        params['best_selection_rate'],
        params['random_selection_rate'],
        params['max_nb_generations'],
        params['mutation_rate'],
        params['restart_after_n_generations_without_improvement'],
        params['best_score_to_keep'],
        grid_size,
        board
    )
    
    sudoku.run()
    print("done")
    
if __name__ == '__main__':
    main()