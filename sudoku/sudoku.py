import random
from board import Board

class Sudoku_GA:
    
    candidates = {}
    
    def __init__(self, population_size, best_selection_rate, random_selection_rate, max_nb_generations,
                 mutation_rate, restart_after_n_generations_without_improvement, best_score_to_keep,
                 grid_size, init_board):
        """
        :params population_size: The population size for every generation
        :params best_selection_rate: Proportion of highest-score population that is chosen to create new generations
        :params random_selection_rate: Proportion of non-highest-score population that is chosen to ccreate new generations. 
        :params max_nb_generations: Max number of generations allowed to run
        :params mutation_rate: Chances for a child to mutate
        :params restart_after_n_generations_without_improvement: Max number of generations without score improvement run before restarting. 
        Will not be used if set at 0.
        :params best_score_to_keep: Minimum fitness score to keep before  
        """
        self.population_size = population_size
        self.best_selection_rate = best_selection_rate
        self.random_selection_rate = random_selection_rate
        self.max_nb_generations = max_nb_generations
        self.mutation_rate = mutation_rate
        self.restart_after_n_generations_without_improvement = restart_after_n_generations_without_improvement
        self.best_score_to_keep = best_score_to_keep
        
        self.grid_size = grid_size
        self.init_board = init_board

    def initialize_population(self, past_boards):
        """
        Initialize population by filling them randomly.  
        Add boards generated in past runs if available.
        """
        population = []
        population.extend(past_boards)
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

        # Keep a list of best and worst boards in past run
        past_boards = []
        found = False
        overall_nb_generations_done = 0
        restart_counter = 0

        # We will restart the 
        while overall_nb_generations_done < self.max_nb_generations and not found:
            new_population = self.initialize_population(past_boards)

            nb_generations_done = 0
            last_best = 0
            nb_generations_without_improvement = 0
            
            bonus_mutation = 0 # Extra bonus for mutation when best score does not change over time

            # Loop until max allowed generations is reached or a solution is found
            while overall_nb_generations_done < self.max_nb_generations and not found:
                # Rank the solutions
                ranked_population = sorted(new_population, key=lambda board: board.fit)
                best_solution = ranked_population[0]
                worst_solution = ranked_population[-1]
                best_score = best_solution.get_fit()
                worst_score = worst_solution.get_fit()

                # Manage best value and improvements among new generations over time
                if last_best == best_score:
                    nb_generations_without_improvement += 1
                    # Add a bonus to mutation rate when best score does not change
                    if self.restart_after_n_generations_without_improvement > 0:
                        bonus_mutation += (0.8 - self.mutation_rate) / self.restart_after_n_generations_without_improvement
                    else:
                        bonus_mutation += (0.8 - self.mutation_rate) / self.max_nb_generations
                    if bonus_mutation > (0.8 - self.mutation_rate): 
                        bonus_mutation = 0.8 - self.mutation_rate # Hard-cap on mutation bonus so it doesn't converge nowhere
                    
                else:
                    last_best = best_score
                if 0 < self.restart_after_n_generations_without_improvement < nb_generations_without_improvement:
                    print("No improvement since {} generations, restarting the program".
                          format(self.restart_after_n_generations_without_improvement))
                    restart_counter += 1
                    # When restart, keep the worst of current population
                    # Only keep the best when its fit score are good enough 
                    if best_score <= self.best_score_to_keep:
                        past_boards.append(best_solution)
                    past_boards.append(worst_solution)
                    break

                # Check if problem is solved and print best and worst results
                if best_score > 0:
                    print("Problem not solved on generation {} (restarted {} times). Best solution score is {} and "
                          "worst is {}".format(nb_generations_done, restart_counter, best_score, worst_score))
                    # Not solved => select a new generation among this ranked population
                    # Retain only the percentage specified by selection rate
                    next_breeders = self.selective_pick_from_population(ranked_population)

                    children = self.create_children_from_parents(next_breeders)
                    new_population = self.mutate_population(children, bonus_mutation)

                    nb_generations_done += 1
                    overall_nb_generations_done += 1
                else:
                    print("Problem solved after {} generations ({} overall generations)!!! Solution found is:".
                          format(nb_generations_done, overall_nb_generations_done))
                    best_solution.display_board()
                    found = True

            
            
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
        random_indexes = random.sample(range(number_of_best, len(sorted_population) - 1), k=number_of_random)
        for i in random_indexes:
            picked_individual.append(sorted_population[i]) 
        #random_picks = random.sample(sorted_population, k=number_of_random)
        #picked_individual.extend(random_picks)
        
        return picked_individual
    
    def create_child_from_parents(self, father=Board, mother=Board):
        """
        Create a child by crossovering gene from both parent
        """
        grids = father.retrieve_all_grid_id() # Retrieve from either parent is fine
        crossover_gene = []
        # Create an array of child's gene which 
        # would be inherited from either parent
        # 0 is father's gene, 1 is mother's
        for i in range(int(len(grids))):
            crossover_gene.append(random.randint(0, 1))
            
        child = Board(father.grid_size)
        i = 0
        for gene in crossover_gene:
            grid_cells = father.retrieve_cells_in_grid(grids[i]) # Retrieve from either parent is fine
            if gene == 0: # Get father gene and copy father's grid
                for cell in grid_cells:
                    child.values[cell] = father.values[cell]
                    # Mark cell if it's fixed
                    if father.is_cell_fixed_at(cell):
                        child.is_fixed |= (1 << cell) 
            else: # Get mother gene and copy father's grid
                for cell in grid_cells:
                    child.values[cell] = mother.values[cell]
                    # Mark cell if it's fixed
                    if mother.is_cell_fixed_at(cell):
                        child.is_fixed |= (1 << cell)
            i += 1
        
        child.update_fit()
        return child
    
    def mutate_population(self, population, bonus_mutation):
        for individual in population:
            # For each individual, roll a value from 0 to 1 
            # and apply mutation to individual if below the mutation rate  
            roll = random.uniform(0, 1)
            if roll - bonus_mutation < self.mutation_rate:
                individual.swap_two_values()
        return population
    
    def create_children_from_parents(self, breeders):
        new_population = []
        # Each pair of parents will create one child
        # To get n child, pick n pair of parents 
        for i in range(self.population_size):
            pair = random.sample(breeders, 2)
            father = pair[0]
            mother = pair[1]
            new_population.append(self.create_child_from_parents(father, mother))
        return new_population