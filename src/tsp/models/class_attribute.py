from tsp.models.treeset import TreeSet

class ClassAttribute(object):
    """description of class"""
    def __init__(self, index, name, numberOfRows, rowsIndexes):
        self.index = index
        self.name = name
        self.numberOfRows = numberOfRows
        self.rowsIndexes = rowsIndexes

    def addIndex(self, index):
        rowsIndexes.add(index)

    def plus(self):
        self.numberOfRows = self.numberOfRows + 1

    def getIndex(self):
        return self.index

    def getName(self):
        return self.name

    def getNumberOfRows(self):
        return self.numberOfRows

    def getRowsIndexes(self):   
        return self.rowsIndexes

    def setNumberOfRows(self, numberOfRows):
        self.numberOfRows = numberOfRows

    def toString(self):
        return "ClassAttribute [index=" + self.index + ", name=" + self.name + ", NumberOfRows=" + self.numberOfRows + ", rowsIndexes="+ self.rowsIndexes + "]"

