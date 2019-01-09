import random
from .Chromosome import Chromosome


class Population:

    def __init__(self, size, selectionType):
        self.generation = 0
        self.size = size
        self.chromosomes = [None] * self.size
        self.qualityChecker = None
        self.selectionType = selectionType

    def fillRandomly(self, chromosomeConfig, comparisonsCount):
        for i in range(0, self.size):
            ch = Chromosome(chromosomeConfig,
                            random.randint(1, comparisonsCount))
            ch.fillRandomly()
            self.chromosomes[i] = ch
        self.checkQuality()
        self.sort()

    def setQualityChecker(self, qualityChecker):
        self.qualityChecker = qualityChecker

    def sort(self):
        self.chromosomes.sort(key=lambda x: x.quality, reverse=True)

    def nextGeneration(self, crossProbability, mutationProbability):
        self.generation += 1

        # mutation
        for chromosome in self.chromosomes:
            chromosome.mutate(mutationProbability)

        # cross v2
        chromosomesSize = len(self.chromosomes)
        chromosomeAvaliable = []
        for chromosomeNumber in range(chromosomesSize):
            chromosomeAvaliable.append(chromosomeNumber)
        for i in range(0, chromosomesSize, 1):
            if(i not in chromosomeAvaliable):
                continue

            chromosomeAvaliable.remove(i)
            random.shuffle(chromosomeAvaliable)
            partner = chromosomeAvaliable[0]
            chromosomeAvaliable.pop(0)

            ch1 = self.chromosomes[i]
            ch2 = self.chromosomes[partner]

            if(random.random() >= crossProbability):
                continue

            children = ch1.cross(ch2)

            self.chromosomes[i] = children[0]
            self.chromosomes[partner] = children[1]

        self.checkQuality()
        self.sort()

        # selection
        if(self.selectionType == "ranking"):
            while len(self.chromosomes) > self.size:
                self.chromosomes.pop()
        else:  # roulete # TODO ruletka do innej klasy wywalić unikalność
            steps = 0
            roulete = []
            chromosomeCount = len(self.chromosomes)

            for i in range(0, chromosomeCount - 1):  # roulete generation
                steps += chromosomeCount - i
                for j in range(steps - (chromosomeCount - i), steps):
                    roulete.append(i)
            random.shuffle(roulete)

            # best subject is automaticly taken to selection
            newChromosomes = [self.chromosomes[0]]

            for sel in range(1, self.size):  # roulete selection
                lottery = roulete[random.randint(0, len(roulete) - 1)]
                newChromosomes.append(self.chromosomes[lottery])

            self.chromosomes = newChromosomes
        
        self.sort()

    def mutate(self, probability):
        for chromosome in self.chromosomes:
            chromosome.mutate(probability)

    def checkQuality(self):
        if not self.qualityChecker:
            return

        for chromosome in self.chromosomes:
            chromosome.quality = self.qualityChecker(
                chromosome.toReadableForm())

    def isFound(self, minProbability):
        return self.chromosomes[0].quality >= minProbability

    def print(self):
        i = 0
        print('Generation: ' + str(self.generation))
        for chromosome in self.chromosomes:
            print(' Chromosome #' + str(i) + ' ' + str(chromosome.toReadableForm()
                                                       ) + ' Quality: ' + str(chromosome.quality))
            i += 1

    def printBest(self):
        bestChromosome = self.chromosomes[0]
        print(' Best Chromosome ' + str(bestChromosome.toReadableForm()
                                        ) + ' Quality: ' + str(bestChromosome.quality))
