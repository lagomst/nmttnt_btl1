import numpy
import random
from board import Board
import rand_fill as rf
import bitmanip as bit_manip

class Sudoku_GA:
    
    candidates = {}
    
    def __init__(self, population_size, best_selection_rate, random_selection_rate, max_nb_generations,
                 mutation_rate, presolving, restart_after_n_generations_without_improvement,
                 grid_size, init_board):
        """
        
        """
        
        self.population_size = population_size
        self.best_selection_rate = best_selection_rate
        self.random_selection_rate = random_selection_rate
        self.max_nb_generations = max_nb_generations
        self.mutation_rate = mutation_rate
        self.presolving = presolving
        self.restart_after_n_generations_without_improvement = restart_after_n_generations_without_improvement
        
        self.grid_size = grid_size
        self.init_board = init_board

    def initialize_population(self):
        population = []
        for n in range(self.population_size):
            new_candidate = Board()
            new_candidate.import_fixed_board(self.grid_size, self.init_board.values)
            new_candidate.fill_random_board()
            population.append(new_candidate)
        return population
            
    def run(self):
        """
        Start the GA to solve the objects
        """
        #values_to_set = self._load().get_initial_values()

        best_data = []
        worst_data = []
        found = False
        overall_nb_generations_done = 0
        restart_counter = 0

        while overall_nb_generations_done < self.max_nb_generations and not found:
            new_population = self.initialize_population()

            nb_generations_done = 0
            last_best = 0
            nb_generations_without_improvement = 0

            # Loop until max allowed generations is reached or a solution is found
            while nb_generations_done < self.max_nb_generations and not found:
                # Rank the solutions
                ranked_population = sorted(new_population, key=lambda board: board.fit)
                best_solution = ranked_population[0]
                best_score = best_solution.get_fit()
                worst_score = ranked_population[-1].get_fit()
                best_data.append(best_score)
                worst_data.append(worst_score)

                # Manage best value and improvements among new generations over time
                if last_best == best_score:
                    nb_generations_without_improvement += 1
                else:
                    last_best = best_score
                if 0 < self.restart_after_n_generations_without_improvement < nb_generations_without_improvement:
                    print("No improvement since {} generations, restarting the program".
                          format(self.restart_after_n_generations_without_improvement))
                    restart_counter += 1
                    break

                # Check if problem is solved and print best and worst results
                if best_score > 0:
                    print("Problem not solved on generation {} (restarted {} times). Best solution score is {} and "
                          "worst is {}".format(nb_generations_done, restart_counter, best_score, worst_score))
                    # Not solved => select a new generation among this ranked population
                    # Retain only the percentage specified by selection rate
                    next_breeders = self.selective_pick_from_population(ranked_population)

                    children = self.create_children_from_parents(next_breeders)
                    new_population = self.mutate_population(children)

                    nb_generations_done += 1
                    overall_nb_generations_done += 1
                else:
                    print("Problem solved after {} generations ({} overall generations)!!! Solution found is:".
                          format(nb_generations_done, overall_nb_generations_done))
                    best_solution.display_board()
                    found = True
                    #print("It took {} to solve it".format(tools.get_human_readable_time(self._start_time, time())))

        if not found:
            print("Problem not solved after {} generations. Printing best and worst results below".
                  format(overall_nb_generations_done))
            ranked_population = sorted(new_population, key=lambda board: board.fit)
            best_solution = ranked_population[0]
            worst_solution = ranked_population[-1]
            print("Best is:")
            best_solution.display_board()
            print("Worst is:")
            worst_solution.display_board()

        #graphics.draw_best_worst_fitness_scores(best_data, worst_data)
    
    def selective_pick_from_population(self, sorted_population: list):
        """
        Selectively picking individuals in population to become parents of the new one
        """
        
        picked_individual = []
        
        number_of_best = int(len(sorted_population) * self.best_selection_rate)
        number_of_random = int(len(sorted_population) * self.random_selection_rate)
        
        # Pick a number of best individual and a number of random individual
        for i in range(number_of_best):
            picked_individual.append(sorted_population[i])
        
        # Random individual might be a duplicate of one of the best
        random_picks = random.sample(sorted_population, k=number_of_random)
        picked_individual.extend(random_picks)
        
        return picked_individual
    
    def create_child_from_parents(self, father=Board, mother=Board):
        grids = father.retrieve_all_grid_id() # Retrieve from either parent is fine
        crossover_gene = []
        for i in range(int(len(grids))):
            crossover_gene.append(random.randint(0, 1))
            
        child = Board(father.grid_size)
        i = 0
        for gene in crossover_gene:
            grid_cells = father.retrieve_cells_in_grid(grids[i]) # Retrieve from either parent is fine
            if gene == 0: # Get father gene
                for cell in grid_cells:
                    child.values[cell] = father.values[cell]
                    if father.is_cell_fixed_at(cell):
                        child.is_fixed |= (1 << cell) 
            else: # Get mother gene
                for cell in grid_cells:
                    child.values[cell] = mother.values[cell]
                    if mother.is_cell_fixed_at(cell):
                        child.is_fixed |= (1 << cell)
            i += 1
        
        child.update_fit()
        return child
    
    def mutate_population(self, population):
        for individual in population:
            # For each individual, roll a value from 0 to 1 
            # and apply mutation to individual if below the mutation rate  
            roll = random.uniform(0, 1)
            if roll < self.mutation_rate:
                individual.swap_two_values()
        return population
    
    def create_children_from_parents(self, breeders):
        new_population = []
        # Each pair of parents will create one child
        # To get n child, pick n pair of parents 
        for i in range(self.population_size):
            father = random.choice(breeders)
            mother = random.choice(breeders)
            new_population.append(self.create_child_from_parents(father, mother))
        return new_population