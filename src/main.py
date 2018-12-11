import sys
import Configuration
import xml.etree.ElementTree as ET
from genetic.Population import Population

tree = ET.parse('configuration.xml')
root = tree.getroot()

"""
if len(sys.argv) < 2:
    print("ERROR!")
    print("usage: " + sys.argv[0] + " config.xml")
    exit(1)
"""

POPULATION_SIZE = int(root.find('population').find('size').text)
SELECTION_SIZE = int(root.find('selection').find('size').text)
POCKET_SIZE = 7 #TODO: floor(log2(TSPgenesCount)) + 1
MUTATION_PROBABILITY = float(root.find('mutation').find('propability').text)
CROSSING_PROBABILITY = float(root.find('crossing').find('propability').text)
TARGET = float(root.find('target').text)
ALFA = float(root.find('alfa').text)
BETA = float(root.find('beta').text)

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
    if data[1] == '<':
        result += 0.10
    
    dis1 = 0.45 - (abs(data[0] - 10)) / 50
    dis2 = 0.45 - (abs(data[2] - 100)) / 50

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


