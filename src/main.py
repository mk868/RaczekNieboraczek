import sys
import os
from Configuration import Configuration
from genetic.Population import Population
from genetic.ChromosomeConfig import ChromosomeConfig
import math
import time
from tsp.models.tsp import TSP

config = Configuration()
config.load('configuration.xml')

filePath = config.defaultFilePath
#read filepath from command prompt with no spaces
if len(sys.argv) > 1:
    filePath = sys.argv[1]

if not os.path.exists(filePath):
     raise Exception('File does not exists')
  
TSP = TSP(filePath, config.gamma)
TSP.buildClassifier(TSP.instances)

chromosomeConfig = ChromosomeConfig()
chromosomeConfig.alphaLength = config.alphaLength
chromosomeConfig.alphaInitValue = config.alphaInitValue
chromosomeConfig.betaLength = config.betaLength
chromosomeConfig.betaInitValue = config.betaInitValue
chromosomeConfig.geneLength = math.floor(math.log2(TSP.instances.numAttributes())) #+ 1
chromosomeConfig.compLength = config.compLength

population = Population(config.populationSize, config.selectionType)

population.setQualityChecker(TSP.checkFitness)
population.fillRandomly(chromosomeConfig, config.comparisonsCount)


start_time = time.time()
#population.print()
for i in range(0, config.evolutionLength):
    population.nextGeneration(config.selectionSize, config.crossingProbability, config.mutationProbability)
    if population.isFound(config.targetProbability):
        break
#population.print()
print('Generation: ' + str(population.generation))
population.printBest()
print('TIME: ' + str(round(time.time() - start_time, 2)))

