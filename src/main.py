import sys
import Configuration
from genetic.Population import Population

"""
if len(sys.argv) < 2:
    print("ERROR!")
    print("usage: " + sys.argv[0] + " config.xml")
    exit(1)
"""

POPULATION_SIZE = 10
SELECTION_SIZE = 5
POCKET_SIZE = 7 #TODO: floor(log2(TSPgenesCount)) + 1
MUTATION_PROBABILITY = 0.01

def checkQuality(data): #mock for TSP rule check
    """
    compare element data[0] with element data[2] using data[1] method
    data[0] = gene 1 row
    data[2] = gene 2 row
    data[1] = comparison method: '<', '<=', '>', '>=', '==', '!='

    ignore code below
    this example:
    10 < 100 = 100%
    """
    result = 0
    if data[0]['method'] == '<':
        result += 0.10
    
    dis1 = 0.45 - (abs(data[0]['gene1'] - 10)) / 50
    dis2 = 0.45 - (abs(data[0]['gene2'] - 100)) / 50

    if dis1 > 0:
        result += dis1

    if dis2 > 0:
        result += dis2

    if result > 1:
        result = 1

    return result # range: 0..1   (0-100%)


population = Population(POPULATION_SIZE, POCKET_SIZE)
population.setQualityChecker(checkQuality)
population.fillRandomly()

population.print()
for i in range(0, 1000):
    population.nextGeneration(SELECTION_SIZE, MUTATION_PROBABILITY)
    if population.isFound(1):
        break

population.print()


