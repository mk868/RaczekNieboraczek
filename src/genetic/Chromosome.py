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
        for i in range(0, self.totalSize):
            if random.random() < probability:
                self.genes[i] = not(self.genes[i])

        ''' init default alpha & beta '''   # póki nie poprawimy bet i alf to zostawiamy je domyślne !!!!!
        for i in range(0, self.comparisonsCount):
            self.setAlpha(i, self.config.alphaInitValue)
            self.setBeta(i, self.config.betaInitValue)

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

    # cross v2
    def cross(self, ch2):
        ch1 = self

        newCh1 = Chromosome(self.config, random.randint(1, ch1.comparisonsCount + ch2.comparisonsCount))
        ch2genAvaliable = []

        for ch2number in range(ch2.comparisonsCount):
            ch2genAvaliable.append(ch2number)

        for i in range(0, newCh1.comparisonsCount):
            if(i in range(min(ch1.comparisonsCount, ch2.comparisonsCount))):
                random.shuffle(ch2genAvaliable)
                ch2gene = ch2genAvaliable[0]
                ch2genAvaliable.pop(0)

                # ALFY I BETY DO ZMIANY JAK JE OGARNIEMY !!!!
                newCh1.setAlpha(i, ch1.getAlpha(i))
                newCh1.setBeta(i, ch1.getBeta(i))
                # POKI CO BEZ ZNACZENIA BO TO STALE !!!!

                # set genes
                genNum1 = random.randint(0, 1)
                genNum2 = random.randint(0, 1)
                newCh1.setGene1(i, ch1.mixGene(i, genNum1, ch2, ch2gene, genNum2))
                newCh1.setGene2(i, ch1.mixGene(i, (genNum1 + 1) % 2, ch2, ch2gene, (genNum2 + 1) % 2))

                # set comp
                if(i % 2 == 1):
                    newCh1.setComp(i, ch1.getComp(i))
                else:
                    newCh1.setComp(i, ch2.getComp(ch2gene))

            else:  # when child have more genes than single parent then take rest of its genes from closest parent
                ch1i = i % ch1.comparisonsCount # tu można ew losować

                # ALFY I BETY DO ZMIANY JAK JE OGARNIEMY !!!!
                newCh1.setAlpha(i, ch1.getAlpha(ch1i))
                newCh1.setBeta(i, ch1.getBeta(ch1i))
                # POKI CO BEZ ZNACZENIA BO TO STALE !!!!

                # set genes
                newCh1.setGene1(i, ch1.getGene1(ch1i))
                newCh1.setGene2(i, ch1.getGene2(ch1i))

                # set comp
                newCh1.setComp(i, ch1.getComp(ch1i))

        newCh2 = Chromosome(self.config, random.randint(1, ch1.comparisonsCount + ch2.comparisonsCount))
        ch1genAvaliable = []

        for ch1number in range(ch1.comparisonsCount):
            ch1genAvaliable.append(ch1number)

        for i in range(0, newCh2.comparisonsCount):
            if(i in range(min(ch1.comparisonsCount, ch2.comparisonsCount))):
                random.shuffle(ch1genAvaliable)
                ch1gene = ch1genAvaliable[0]
                ch1genAvaliable.pop(0)

                # ALFY I BETY DO ZMIANY JAK JE OGARNIEMY !!!!
                newCh2.setAlpha(i, ch2.getAlpha(i))
                newCh2.setBeta(i, ch1.getBeta(i))
                # POKI CO BEZ ZNACZENIA BO TO STALE !!!!

                # set genes
                genNum1 = random.randint(0, 1)
                genNum2 = random.randint(0, 1)
                newCh2.setGene1(i, ch2.mixGene(i, genNum1, ch1, ch1gene, genNum2))
                newCh2.setGene2(i, ch2.mixGene(i, (genNum1 + 1) % 2, ch1, ch1gene, (genNum2 + 1) % 2))

                # set comp
                if(i % 2 == 0):
                    newCh2.setComp(i, ch2.getComp(i))
                else:
                    newCh2.setComp(i, ch1.getComp(ch1gene))

            else:  # when child have more genes than single parent then take rest of its genes from closest parent
                ch2i = i % ch2.comparisonsCount # tu można ew losować

                # ALFY I BETY DO ZMIANY JAK JE OGARNIEMY !!!!
                newCh2.setAlpha(i, ch2.getAlpha(ch2i))
                newCh2.setBeta(i, ch2.getBeta(ch2i))
                # POKI CO BEZ ZNACZENIA BO TO STALE !!!!

                # set genes
                newCh2.setGene1(i, ch2.getGene1(ch2i))
                newCh2.setGene2(i, ch2.getGene2(ch2i))

                # set comp
                newCh2.setComp(i, ch2.getComp(ch2i))

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
    
    def mixGene(self, comparisonNum1, genNum1, ch2, comparisonNum2, genNum2):
        offset1 = self.comparisonLength * comparisonNum1
        offset1 += self.config.alphaLength + self.config.betaLength
        
        if(genNum1 == 1):
            offset1 += self.config.geneLength + self.config.compLength

        gene1 = self.genes[offset1: offset1 + self.config.geneLength]

        offset2 = ch2.comparisonLength * comparisonNum2
        offset2 += ch2.config.alphaLength + ch2.config.betaLength
        
        if(genNum2 == 1):
            offset2 += ch2.config.geneLength + ch2.config.compLength

        gene2 = ch2.genes[offset2: offset2 + ch2.config.geneLength]

        cut = random.randint(int(self.config.geneLength * 0.25), self.config.geneLength - 1)
        newGene = []
        for i in range(0, cut):
            newGene.append(gene1[i])
        for i in range(cut + 1, self.config.geneLength):
            newGene.append(gene2[i])

        return ListIntConverter.List2Int(newGene)

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
