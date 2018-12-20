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

    def nextGeneration(self, selectionSize, crossProbability, mutationProbability):
        self.generation += 1

        # selection
        if(self.selectionType == "ranking"):
            while len(self.chromosomes) > selectionSize:
                self.chromosomes.pop()
        else:  # roulete
            steps = 0
            roulete = []
            chromosomeCount = len(self.chromosomes)

            for i in range(1, chromosomeCount - 1):  # roulete generation
                steps += chromosomeCount - i
                for j in range(steps - (chromosomeCount - i), steps):
                    roulete.append(i)
            random.shuffle(roulete)

            # best subject is automaticly taken to selection
            newChromosomes = [self.chromosomes[0]]
            alreadyTakenChromosomes = []

            for sel in range(1, selectionSize):  # roulete selection
                lottery = roulete[random.randint(1, len(roulete) - 2)]
                while lottery in alreadyTakenChromosomes:
                    lottery = roulete[random.randint(0, len(roulete) - 1)]
                    
                alreadyTakenChromosomes.append(lottery)
                newChromosomes.append(self.chromosomes[lottery])

            self.chromosomes = newChromosomes

        # mutation
        for chromosome in self.chromosomes:
            chromosome.mutate(mutationProbability)

        # cross v1
        # chromosomesSize = len(self.chromosomes)
        # for i in range(0, chromosomesSize, 2):
        #     ch1 = self.chromosomes[i]
        #     ch2 = self.chromosomes[i + 1]

        #     if(random.random() >= crossProbability):
        #         continue

        #     children = ch1.cross(ch2)

        #     self.chromosomes.append(children[0])
        #     self.chromosomes.append(children[1])

        # cross v2
        chromosomesSize = len(self.chromosomes)
        alreadyCrossed = []
        for i in range(0, chromosomesSize, 1):
            if(i in alreadyCrossed):
                continue

            alreadyCrossed.append(i)
            partner = random.randint(i + 1, chromosomesSize - 1)
            while partner in alreadyCrossed:
                partner = random.randint(i + 1, chromosomesSize - 1)
            alreadyCrossed.append(partner)

            ch1 = self.chromosomes[i]
            ch2 = self.chromosomes[partner]

            if(random.random() >= crossProbability):
                continue

            children = ch1.cross(ch2)

            self.chromosomes.append(children[0])
            self.chromosomes.append(children[1])

        self.checkQuality()
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
