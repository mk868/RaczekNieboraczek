import random
from . import ListIntConverter

class Chromosome:
    """
    genes:
    [x, x, x, y, y, x, x, x]
     1  2  3
    pocketSize = 3
    """

    def __init__(self, pocketSize):
        self.quality = 0 #init value
        self.pocketSize = pocketSize
        self.compSize = 2
        self.totalSize = pocketSize * 2 + self.compSize
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

    def cross(ch1, ch2):
        newCh1 = Chromosome(ch1.pocketSize)
        newCh1.setComp(0, ch1.getComp(0))
        newCh1.setPocket(0, ch1.getPocket(0))
        newCh1.setPocket(1, ch2.getPocket(1))

        newCh2 = Chromosome(ch1.pocketSize)
        newCh2.setComp(0, ch2.getComp(0))
        newCh2.setPocket(0, ch2.getPocket(0))
        newCh2.setPocket(1, ch1.getPocket(1))
        return (newCh1, newCh2)
    
    def getPocket(self, offset):
        realOffset = offset * (self.pocketSize + self.compSize)
        pocket = self.genes[realOffset: realOffset + self.pocketSize]
        num = ListIntConverter.List2Int(pocket)
        
        return num

    def setPocket(self, offset, num):
        realOffset = offset * (self.pocketSize + self.compSize)
        pocket = ListIntConverter.Int2List(num, self.pocketSize)

        for i in range(0, self.pocketSize):
            self.genes[realOffset + i] = pocket[i]
    
    def getComp(self, offset):
        realOffset = self.pocketSize + offset * (self.pocketSize + self.compSize)
        comp = self.genes[realOffset: realOffset + self.compSize]
        compNum = ListIntConverter.List2Int(comp)

        return self.comps[compNum % len(self.comps)]

    def setComp(self, offset, comp):
        realOffset = self.pocketSize + offset * (self.pocketSize + self.compSize)
        compNum = self.comps.index(comp)
        compList = ListIntConverter.Int2List(compNum, self.compSize)

        for i in range(0, self.compSize):
           self.genes[realOffset + i] = compList[i]
    
    def toReadableForm(self):
        result = []
        for i in range(0, 1):
            result.append(
            {
                'gene1': self.getPocket(0),
                'gene2': self.getPocket(1),
                'method': self.getComp(0)
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
    