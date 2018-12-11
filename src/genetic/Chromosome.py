import random
from . import ListIntConverter

class Chromosome:
    """
    genes:
    [x, x, x, y, y, x, x, x]
     1  2  3
    pocketSize = 3
    """

    def __init__(self, pocketSize, comparisonsCount):
        self.quality = 0 #init value
        self.pocketSize = pocketSize
        self.compSize = 2
        self.comparisonsCount = comparisonsCount
        self.totalSize = (pocketSize * 2 + self.compSize) * self.comparisonsCount
        self.genes = [0] * self.totalSize
        self.comps = ['>', '<', '>=', '==', '<=', '!='] # used elements count: 2 ^ self.compSize
    
    def fillRandomly(self):
        for i in range(0, self.totalSize):
            if random.random() >= 0.5:
                self.genes[i] = 1
            else:
                self.genes[i] = 0

    def mutate(self, probability):
        for i in range(0, self.totalSize):
            if random.random() < probability:
                self.genes[i] = 1 - self.genes[i]

    def cross(self, ch2):
        ch1 = self
        newCh1 = Chromosome(ch1.pocketSize, self.comparisonsCount)
        newCh2 = Chromosome(ch1.pocketSize, self.comparisonsCount)
        for i in range(0, self.comparisonsCount):
            pocket1Position = 0 + i * 2
            pocket2Position = 1 + i * 2
            compPosition = i

            newCh1.setComp(compPosition, ch1.getComp(compPosition))
            newCh1.setPocket(pocket1Position, ch1.getPocket(pocket1Position))
            newCh1.setPocket(pocket2Position, ch2.getPocket(pocket2Position))

            newCh2.setComp(compPosition, ch2.getComp(compPosition))
            newCh2.setPocket(pocket1Position, ch2.getPocket(pocket1Position))
            #newCh2.setPocket(pocket2Position, ch1.getPocket(pocket2Position))
        
        return (newCh1, newCh2)
    
    def getPocket(self, offset):
        comparisonNum = offset // 2
        realOffset = comparisonNum * (self.pocketSize * 2 + self.compSize) + offset % 2
        pocket = self.genes[realOffset: realOffset + self.pocketSize]
        num = ListIntConverter.List2Int(pocket)
        
        return num

    def setPocket(self, offset, num):
        comparisonNum = offset // 2
        realOffset = comparisonNum * (self.pocketSize * 2 + self.compSize) + offset % 2
        pocket = ListIntConverter.Int2List(num, self.pocketSize)

        for i in range(0, self.pocketSize):
            self.genes[realOffset + i] = pocket[i]
    
    def getComp(self, offset):
        realOffset = self.pocketSize + offset * (self.pocketSize * 2 + self.compSize)
        comp = self.genes[realOffset: realOffset + self.compSize]
        compNum = ListIntConverter.List2Int(comp)

        return self.comps[compNum % len(self.comps)]

    def setComp(self, offset, comp):
        realOffset = self.pocketSize + offset * (self.pocketSize * 2 + self.compSize)
        compNum = self.comps.index(comp)
        compList = ListIntConverter.Int2List(compNum, self.compSize)

        for i in range(0, self.compSize):
           self.genes[realOffset + i] = compList[i]
    
    def toReadableForm(self):
        result = []
        for i in range(0, self.comparisonsCount):
            result.append(
            {
                'gene1': self.getPocket(0 + i * 2),
                'gene2': self.getPocket(1 + i * 2),
                'method': self.getComp(i)
            })
        return result
        

    def __str__(self):
        return str(self.genes)


if __name__ == '__main__': # test
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
    