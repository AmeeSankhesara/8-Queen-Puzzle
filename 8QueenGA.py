#Amee Sankhesara 


import random

maxFitness = 28
population_size = 1000
mutation_probability = 0.05
generation = 5

#Generate initial population randomly
def generateinitialpopulation():
    population = []
    for i in range (1,population_size):
        population1 = [random.randint(1, 8) for _ in range(8)]
        population.append(population1)
    return population

#Fitness function will calculate horizontal_collisions and diagonal_collisions. It is used to 
# find solution of 8-queen problem. It will return 28(maxfitness) if there is no horizontal or diagonal collision.
# We can found solution when fitness = 28.      
def fitness(individual):
    horizontal_collisions = sum([individual.count(queen)-1 for queen in individual])/2
    diagonal_collisions = 0   

    n = len(individual)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + individual[i] - 1] += 1
        right_diagonal[len(individual) - i + individual[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
        
    return int(maxFitness - (horizontal_collisions + diagonal_collisions))

#Below function will calculate probability 
def probability(individual, fitness):
    return fitness(individual) / maxFitness

#Below function will choose the best two mates based on random probability
def pickRandomByProbability(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

#Random crossover of two parents to produce 2 offsprings   
def crossover(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

#changes a single queen position in each state randomly with probability Mutation_probability
def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

#Below genetic queen function will do random selection,crossover, random mutation for given input of initial population
def genetic_queen(population, fitness):
    fitnessCalc = []
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = pickRandomByProbability(population, probabilities)
        y = pickRandomByProbability(population, probabilities)
        child = crossover(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        fitnessCalc.append(fitness(child))
        new_population.append(child)
        if fitness(child) == 28: break
    return new_population, fitnessCalc

#Print function to print solution 
def print_individual(x):
    print("Solution = {},  fitness = {}, probability = {:.6f}"
        .format(str(x), fitness(x), probability(x, fitness)))

if __name__ == "__main__":
    population = generateinitialpopulation() 
    
    averageFitenss = []

    while not 28 in [fitness(x) for x in population]:
        #Print generation number
        print("=== Generation {} ===".format(generation))
        population, fitnessCalc = genetic_queen(population, fitness)
        #Print maximum fitness of specific generation
        print("Maximum fitness = {}".format(max([fitness(n) for n in population])))
        #Calculate average fitness of specific generation
        avg = sum(fitnessCalc)/len(fitnessCalc)
        #Print average fitness of specific generation
        print("Average fitness = ",avg)
        averageFitenss.append(avg) 
        generation += 1
        

    print("Solved in Generation {}!".format(generation-1))
    for x in population:
        if fitness(x) == 28:
            print_individual(x)
            #Create board for 8 queen solution             
            board = [['_','_','_','_','_','_','_','_'],
                     ['_','_','_','_','_','_','_','_'],
                     ['_','_','_','_','_','_','_','_'],
                     ['_','_','_','_','_','_','_','_'],
                     ['_','_','_','_','_','_','_','_'],
                     ['_','_','_','_','_','_','_','_'],
                     ['_','_','_','_','_','_','_','_'],
                     ['_','_','_','_','_','_','_','_']]
            Generation = x
            for i in range(8):
               for j in range(8):
                   value = Generation[i]-1
                   if j == value: 
                       board[j][i] = 'Q'
                   
            
            for i in board:
               print(i) 
            #calculate average fitness of all generation   
            averageAverageFitenss = sum(averageFitenss)/generation
            print("Average fitness of all generation = ",averageAverageFitenss)
            