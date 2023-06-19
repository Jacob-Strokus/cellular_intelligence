#! pip3 install deap
from deap import algorithms, base, creator, tools
import random


# class to create cooperative coevolution objects to simulate ditributed evolutionary algorithms in python3
# This process facilitates our main goal of observing cellular intelligence in computing
class coevolution:

    toolbox = None

    # initialization function
    def __init__(self, individual_size):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("individual", tools.initRepeat, creator.Individual, self.random_init, n=individual_size)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mate", self.crossover_operator)  # Define the crossover operator
        toolbox.register("mutate", self.mutate_crossover)  # Define the mutation operator
        toolbox.register("select", self.selection_operator)  # Define the selection operator
        

    #  select individual length from uniform random distribution 
    def random_init(length):
        return [random.randint(0, 1) for _ in range(length)]


    # setup evalutation function
    def evaluate(individual):
        # Implement your evaluation function here
        # Compute the fitness of the individual
        return fitness_values,  # Return the fitness as a tuple (comma at the end is important)


    # single-point crossover operator
    def crossover_operator(ind1, ind2):
        # Select a crossover point
        crossover_point = random.randint(1, len(ind1) - 1)

        # Create offspring by exchanging genetic material
        offspring1 = ind1[:crossover_point] + ind2[crossover_point:]
        offspring2 = ind2[:crossover_point] + ind1[crossover_point:]

        return offspring1, offspring2


    # single-point mutation crossover from uniform random point distribution
    def mutate_crossover(individuals, cxpb, mutpb):
        offspring = []

        for ind in individuals:
            # Apply crossover with probability cxpb
            if random.random() < cxpb:
                # Select a random individual from the population as a mate
                mate = random.choice(individuals)
                # Create two offspring using the crossover operator
                offspring1, offspring2 = crossover_operator(ind, mate)
                # Add the offspring to the new generation
                offspring.extend([offspring1, offspring2])
            else:
                # No crossover, add the individual to the new generation
                offspring.append(ind)

        for ind in offspring:
            # Apply mutation with probability mutpb
            if random.random() < mutpb:
                # Apply mutation operator to the individual
                mutated_ind = mutation_operator(ind)
                # Replace the original individual with the mutated one
                offspring[offspring.index(ind)] = mutated_ind

        return offspring


    # 2/3 of individuals in population are selected in tournament-style competition for reproduction
    def selection_operator(individuals, k):
        return tools.selTournament(individuals, k, tournsize=67)
                                                                 


    @staticmethod
    def main():

        NUM_GENERATIONS = 10
        subpop1_size = 100
        subpop2_size = 100
    
        # setup_toolbox()
    
        # Initialize the subpopulations
        subpop1 = toolbox.population(n=subpop1_size)
        subpop2 = toolbox.population(n=subpop2_size)

        # Run the cooperative coevolution algorithm
        algorithms.eaCooperativeCoevolution(subpop1, subpop2, toolbox, cxpb=crossover_prob, mutpb=mutation_prob,
                                            ngen=NUM_GENERATIONS, stats=None, halloffame=None)


if __name__ == "__main__":
    coevolution.main()