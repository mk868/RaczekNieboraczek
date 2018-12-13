import random
from .Chromosome import Chromosome

class Population:

    def __init__(self, size):
        self.generation = 0
        self.size = size
        self.chromosomes = [None] * self.size
        self.qualityChecker = None

    def fillRandomly(self, chromosomeConfig, comparisonsCount):
        for i in range(0, self.size):
            ch = Chromosome(chromosomeConfig, comparisonsCount)
            ch.fillRandomly()
            self.chromosomes[i] = ch
        self.checkQuality()
        self.sort()
    
    def setQualityChecker(self, qualityChecker):
        self.qualityChecker = qualityChecker

    def sort(self):
        self.chromosomes.sort(key = lambda x: x.quality, reverse = True)

    def nextGeneration(self, selectionSize, crossProbability, mutationProbability):
        self.generation += 1

        #selection
        while len(self.chromosomes) > selectionSize:            
            self.chromosomes.pop()

        #mutation
        for chromosome in self.chromosomes:
            chromosome.mutate(mutationProbability)
        
        #cross
        chromosomesSize = len(self.chromosomes)
        for i in range(0, chromosomesSize, 2):
            ch1 = self.chromosomes[i]
            ch2 = self.chromosomes[i + 1]

            if(random.random() >= crossProbability):
                continue

            children = ch1.cross(ch2)

            self.chromosomes.append(children[0])
            self.chromosomes.append(children[1])

        self.checkQuality()
        self.sort()

        while len(self.chromosomes) > self.size:            
            self.chromosomes.pop()


    def mutate(self, probability):
        for chromosome in self.chromosomes:
            chromosome.mutate(probability)

    def checkQuality(self):
        if not self.qualityChecker:
            return
        
        for chromosome in self.chromosomes:
            chromosome.quality = self.qualityChecker(chromosome.toReadableForm())

    def isFound(self, minProbability):
        return self.chromosomes[0].quality >= minProbability

    def print(self):
        i = 0
        print('Generation: ' + str(self.generation))
        for chromosome in self.chromosomes:
            print(' Chromosome #' + str(i) + ' ' + str(chromosome.toReadableForm()) + ' Quality: ' + str(chromosome.quality))
            i += 1

    def printBest(self):
        bestChromosome = self.chromosomes[0]
        print(' Best Chromosome ' + str(bestChromosome.toReadableForm()) + ' Quality: ' + str(bestChromosome.quality))
        
