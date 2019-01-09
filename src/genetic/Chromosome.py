import random
from . import ListIntConverter
from . import ChromosomeConfig


class Chromosome:
    """
    gene pattern:
    aaaaabbbbb111111cc222222
    a-alpha
    b-beta
    1 - gene1
    c - comparison type
    2 - gene2

    """

    def __init__(self, chromosomeConfig, comparisonsCount):
        self.config = chromosomeConfig
        self.comparisonsCount = comparisonsCount

        self.quality = 0  # init value
        self.compLength = self.config.compLength
        self.comparisonLength = self.config.geneLength * 2 + \
            self.config.alphaLength + self.config.betaLength + self.config.compLength
        self.totalSize = self.comparisonLength * self.comparisonsCount
        # used elements count: 2 ^ self.compSize
        self.comps = ['>', '<=', '<', '>=', '==', '!=']
        self.genes = [0] * self.totalSize

    def fillRandomly(self):
        ''' random '''
        for i in range(0, self.totalSize):
            if random.random() >= 0.5:
                self.genes[i] = True
            else:
                self.genes[i] = False
        ''' init default alpha & beta '''
        for i in range(0, self.comparisonsCount):
            self.setAlpha(i, self.config.alphaInitValue)
            self.setBeta(i, self.config.betaInitValue)

    def mutate(self, probability):
        clone = Chromosome(self.config, self.comparisonsCount)
        for i in range(0, self.comparisonsCount):
            clone.setPair(i, self.getPair(i))
            clone.setAlpha(i, self.config.alphaInitValue)
            clone.setBeta(i, self.config.betaInitValue)

        for i in range(0, clone.totalSize):
            if random.random() < probability:
                clone.genes[i] = not(clone.genes[i])

        # TODO mutacja alfy i bety do całkowitej zmiany
        ''' init default alpha & beta '''   # póki nie poprawimy bet i alf to zostawiamy je domyślne !!!!!
        for i in range(0, clone.comparisonsCount):
            clone.setAlpha(i, clone.config.alphaInitValue)
            clone.setBeta(i, clone.config.betaInitValue)
            
        return clone

    # cross v1
    # def cross(self, ch2):
    #     ch1 = self
    #     newCh1 = Chromosome(self.config, self.comparisonsCount)
    #     newCh2 = Chromosome(self.config, self.comparisonsCount)
    #     for i in range(0, self.comparisonsCount):
    #         newCh1.setAlpha(i, ch1.getAlpha(i))
    #         newCh1.setBeta(i, ch2.getBeta(i))
    #         newCh1.setGene1(i, ch1.getGene1(i))
    #         newCh1.setComp(i, ch1.getComp(i))
    #         newCh1.setGene2(i, ch2.getGene2(i))

    #         newCh2.setAlpha(i, ch2.getAlpha(i))
    #         newCh2.setBeta(i, ch1.getBeta(i))
    #         newCh2.setGene1(i, ch2.getGene1(i))
    #         newCh2.setComp(i, ch2.getComp(i))
    #         newCh2.setGene2(i, ch1.getGene2(i))

    #     return (newCh1, newCh2)

    # cross v3
    def cross(self, ch2):
        ch1 = self
        ch1Cut = random.randint(1, ch1.comparisonsCount)
        ch2Cut = random.randint(1, ch2.comparisonsCount)
        ch1NewLength = (ch1.comparisonsCount - ch1Cut) + \
            (ch2.comparisonsCount - ch2Cut)
        ch2NewLength = ch1Cut + ch2Cut

        gn = 0
        newCh2 = Chromosome(self.config, ch2NewLength)
        for i in range(0, ch2Cut):
            newCh2.setPair(gn, ch2.getPair(i))
            newCh2.setAlpha(gn, newCh2.config.alphaInitValue)
            newCh2.setBeta(gn, newCh2.config.betaInitValue)
            gn += 1
        for i in range(0, ch1Cut):
            newCh2.setPair(gn, ch1.getPair(i))
            newCh2.setAlpha(gn, newCh2.config.alphaInitValue)
            newCh2.setBeta(gn, newCh2.config.betaInitValue)
            gn += 1

        if(ch1NewLength == 0):
            return (ch1, newCh2)

        gn = 0
        newCh1 = Chromosome(self.config, ch1NewLength)
        for i in range(ch2Cut, ch2.comparisonsCount):
            newCh1.setPair(gn, ch2.getPair(i))
            newCh1.setAlpha(gn, newCh1.config.alphaInitValue)
            newCh1.setBeta(gn, newCh1.config.betaInitValue)
            gn += 1
        for i in range(ch1Cut, ch1.comparisonsCount):
            newCh1.setPair(gn, ch1.getPair(i))
            newCh1.setAlpha(gn, newCh1.config.alphaInitValue)
            newCh1.setBeta(gn, newCh1.config.betaInitValue)
            gn += 1

        return (newCh1, newCh2)

    ''' getters '''

    def getAlpha(self, comparisonNum):
        offset = self.comparisonLength * comparisonNum
        alpha = self.genes[offset: offset + self.config.alphaLength]
        return ListIntConverter.List2Int(alpha)

    def getBeta(self, comparisonNum):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength
        beta = self.genes[offset: offset + self.config.betaLength]
        return ListIntConverter.List2Int(beta)

    def getGene1(self, comparisonNum):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength + self.config.betaLength
        gene = self.genes[offset: offset + self.config.geneLength]
        return ListIntConverter.List2Int(gene)

    def getGene2(self, comparisonNum):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength + self.config.betaLength + \
            self.config.geneLength + self.config.compLength
        gene = self.genes[offset: offset + self.config.geneLength]
        return ListIntConverter.List2Int(gene)

    def getComp(self, comparisonNum):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength + \
            self.config.betaLength + self.config.geneLength
        comp = self.genes[offset: offset + self.config.compLength]
        compNum = ListIntConverter.List2Int(comp)
        return self.comps[compNum % len(self.comps)]

    def getPair(self, comparisonNum):
        offset = self.comparisonLength * comparisonNum
        gene = self.genes[offset: offset + self.comparisonLength]
        return ListIntConverter.List2Int(gene)

    ''' setters '''

    def setAlpha(self, comparisonNum, value):
        offset = self.comparisonLength * comparisonNum
        binValue = ListIntConverter.Int2List(value, self.config.alphaLength)
        for i in range(0, len(binValue)):
            self.genes[offset + i] = binValue[i]

    def setBeta(self, comparisonNum, value):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength
        binValue = ListIntConverter.Int2List(value, self.config.betaLength)
        for i in range(0, len(binValue)):
            self.genes[offset + i] = binValue[i]

    def setGene1(self, comparisonNum, value):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength + self.config.betaLength
        binValue = ListIntConverter.Int2List(value, self.config.geneLength)
        for i in range(0, len(binValue)):
            self.genes[offset + i] = binValue[i]

    def setGene2(self, comparisonNum, value):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength + self.config.betaLength + \
            self.config.geneLength + self.config.compLength
        binValue = ListIntConverter.Int2List(value, self.config.geneLength)
        for i in range(0, len(binValue)):
            self.genes[offset + i] = binValue[i]

    def setComp(self, comparisonNum, value):
        offset = self.comparisonLength * comparisonNum
        offset += self.config.alphaLength + \
            self.config.betaLength + self.config.geneLength
        binValue = ListIntConverter.Int2List(
            self.comps.index(value), self.config.compLength)
        for i in range(0, len(binValue)):
            self.genes[offset + i] = binValue[i]

    def setPair(self, comparisonNum, value):
        offset = self.comparisonLength * comparisonNum
        binValue = ListIntConverter.Int2List(value, self.comparisonLength)
        for i in range(0, len(binValue)):
            self.genes[offset + i] = binValue[i]

    ''' helpers '''

    def toReadableForm(self):
        result = []
        for i in range(0, self.comparisonsCount):
            result.append(
                {
                    'alpha': self.getAlpha(i),
                    'beta': self.getBeta(i),
                    'gene1': self.getGene1(i),
                    'method': self.getComp(i),
                    'gene2': self.getGene2(i),
                })
        return result

    def __str__(self):
        return str(self.genes)


if __name__ == '__main__':  # test
    ch = Chromosome(4)
    ch.fillRandomly()
    print('ch1:')
    print(ch)
    print(ch.toReadableForm())

    ch2 = Chromosome(4)
    ch2.fillRandomly()
    print('ch2:')
    print(ch2)
    print(ch2.toReadableForm())

    chNew = ch.cross(ch2)
    print('chNew[0]:')
    print(chNew[0])
    print(chNew[0].toReadableForm())
    print('chNew[1]:')
    print(chNew[1])
    print(chNew[1].toReadableForm())
