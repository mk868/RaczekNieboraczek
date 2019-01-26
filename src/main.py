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
testFilePath = config.defaultTestFilePath

#read filepath from command prompt with no spaces
if len(sys.argv) > 2:
    filePath = sys.argv[1]
    testFilePath = sys.argv[2]

if not os.path.exists(filePath):
     raise Exception('File does not exists')

if(testFilePath == 'NONE'):
    TSP1 = TSP(filePath, config.gamma, False)
else:
    TSP1 = TSP(filePath, config.gamma, True)
TSP1.buildClassifier(TSP1.instances)

chromosomeConfig = ChromosomeConfig()
chromosomeConfig.alphaLength = config.alphaLength
chromosomeConfig.alphaInitValue = config.alphaInitValue
chromosomeConfig.betaLength = config.betaLength
chromosomeConfig.betaInitValue = config.betaInitValue
chromosomeConfig.geneLength = math.floor(math.log2(TSP1.maxValueOfGene)) #+ 1
chromosomeConfig.compLength = config.compLength

population = Population(config.selectionSize, config.selectionType)

population.setQualityChecker(TSP1.checkFitness)
population.fillRandomly(chromosomeConfig, config.comparisonsCount)
config.mutationProbability = (1 / chromosomeConfig.geneLength) + (config.mutationProbability * (1 / chromosomeConfig.geneLength))

start_time = time.time()
best = None
#population.print()
for i in range(0, config.evolutionLength):
    best = population.nextGeneration(config.crossingProbability, config.mutationProbability, best)
    if population.isFound(config.targetProbability):
        break
#population.print()
print('Generation: ' + str(population.generation))
best = population.printBest()
print('TIME: ' + str(round(time.time() - start_time, 2)))

if(testFilePath == 'NONE'):
    TSP1.buildClassifier(TSP1.test)
    print('Test score is: ' + str(TSP1.checkFitness(best.toReadableForm())) + '%') 
else:
    TSP2 = TSP(testFilePath, config.gamma)
    TSP2.buildClassifier(TSP2.instances)
    print('Test score is: ' + str(TSP2.checkFitness(best.toReadableForm())) + '%')
