from tsp.models.class_attribute import ClassAttribute
from tsp.models.pair import Pair
import tsp.models.fildereader
import math
import random
import copy 

class TSP(object):
    classes = []

    def __init__(self, path, gamma, hasTest):
        self.instances = tsp.models.fildereader.load_data(path)
        self.gamma = gamma
        self.maxValueOfGene = self.instances.numAttributes()
        

        # temp = []
        # if(not hasTest):
        #     i = 0
        #     while(i < (len(self.instances.instances))/10):
        #         random.shuffle(self.instances.instances)
        #         temp.append(self.instances.instances[0])
        #         self.instances.instances.pop(0)
        #         i+=1
        
        # self.test = copy.deepcopy(self.instances)
        # self.test.instances = temp

        
        if(not hasTest):
            getClassDict = self.instances.getClasses()
            if getClassDict['count'] > 2:
                raise Exception('TSP works properly only with 2 classes')

            classDictionary = getClassDict['classes']
            rowsForClasses = self.instances.getNumberOfRowsForClass(classDictionary)
            rowsIndexesForClasses = self.instances.getRowsIndexesForClass(classDictionary)

            i = 0
            classes=[]
            for _class in classDictionary:
                classes.append(ClassAttribute(
                    i, _class, rowsForClasses[_class], rowsIndexesForClasses[_class]))
                i += 1

            temp = []
            i = 0
            while(i < (len(self.instances.instances))/10):
                random.shuffle(rowsIndexesForClasses[classes[i%2].name])
                v = rowsIndexesForClasses[classes[i%2].name][0]
                temp.append(self.instances.instances[v])
                self.instances.instances.pop(v)
                i+=1
        
            self.test = copy.deepcopy(self.instances)
            self.test.instances = temp
        

    def buildClassifier(self, instances):
        getClassDict = instances.getClasses()
        if getClassDict['count'] > 2:
            raise Exception('TSP works properly only with 2 classes')

        classDictionary = getClassDict['classes']
        self.rowsForClasses = instances.getNumberOfRowsForClass(
            classDictionary)
        self.rowsIndexesForClasses = instances.getRowsIndexesForClass(
            classDictionary)

        i = 0
        for _class in classDictionary:
            self.classes.append(ClassAttribute(
                i, _class, self.rowsForClasses[_class], self.rowsIndexesForClasses[_class]))
            i += 1

        # pair = self.computeSingleDelta(self.instances, 0, 56, '<')
        # print(pair.delta,';',pair.positivePropability,';',pair.negativePropability,';',pair.getX(),';',pair.getY())

    def indicator(self, firstValue, secondValue, method):
        if method == '>':
            return firstValue > secondValue
        if method == '<':
            return firstValue < secondValue
        if method == '<=':
            return firstValue <= secondValue
        if method == '>=':
            return firstValue >= secondValue
        if method == '==':
            return firstValue == secondValue
        if method == '!=':
            return firstValue != secondValue
        return False

    def computeSingleDelta(self, instances, gene1, gene2, method):
        positivePropability = self.computeFirstPropability(
            self.classes[0], instances, gene1, gene2, method)
        negativePropability = self.computeFirstPropability(
            self.classes[1], instances, gene1, gene2, method)
        return Pair(gene1, gene2, abs(positivePropability-negativePropability), positivePropability, negativePropability)

    def computeFirstPropability(self, classAttr, instances, gene1, gene2, method):
        sum = 0
        for val in classAttr.getRowsIndexes():
            instance = instances.instances[val]
            if self.indicator(instance.args[gene1], instance.args[gene2], method):
                sum = sum + 1
        return (1.0/classAttr.getNumberOfRows())*sum

    def checkFitness(self, data):
        alfaSum = 0
        for comparison in data:
            alfaSum += comparison['alpha']

        if alfaSum == 0:
            print('warning! alfaSum = 0')

        uniqueGenes = []

        # overflow, some gene value > instance count
        for comparison in data:
            gene1 = comparison['gene1']
            gene2 = comparison['gene2']
            if gene1 > len(self.instances.instances[0].args):
                gene1 = self.maxValueOfGene
            if gene1 not in uniqueGenes:
                uniqueGenes.append(gene1)
            if gene2 > len(self.instances.instances[0].args):
                gene2 = self.maxValueOfGene
            if gene2 not in uniqueGenes:
                uniqueGenes.append(gene2)

        class0Sum = 0
        rowsIndexesForClasses = self.instances.getRowsIndexesForClass(
            self.classes)
        # class0
        for index in self.rowsIndexesForClasses[self.classes[0].name]:
            personFitness = 0

            for dataElement in data:
                alfa = dataElement['alpha']
                beta = dataElement['beta']
                gene1Index = dataElement['gene1']
                gene2Index = dataElement['gene2']
                method = dataElement['method']

                gene1Value = beta + \
                    float(self.instances.instances[index].args[gene1Index])
                gene2Value = float(
                    self.instances.instances[index].args[gene2Index])
                if self.indicator(gene1Value, gene2Value, method):
                    personFitness += 1 * alfa
            # insted of if(personFitness == alfaSum)
            class0Sum += math.ceil(personFitness / alfaSum)
        resultClass0 = class0Sum / self.rowsForClasses[self.classes[0].name]

        class1Sum = 0
        # class1
        for index in self.rowsIndexesForClasses[self.classes[1].name]:
            personFitness = 0
            for dataElement in data:
                alfa = dataElement['alpha']
                beta = dataElement['beta']
                gene1Index = dataElement['gene1']
                gene2Index = dataElement['gene2']
                method = dataElement['method']

                gene1Value = beta + \
                    float(self.instances.instances[index].args[gene1Index])
                gene2Value = float(
                    self.instances.instances[index].args[gene2Index])
                if self.indicator(gene1Value, gene2Value, method):
                    personFitness += 1 * alfa
            class1Sum += math.ceil(personFitness / alfaSum)
        resultClass1 = class1Sum / self.rowsForClasses[self.classes[1].name]

        return abs(resultClass0 - resultClass1) - ((self.gamma * (len(uniqueGenes))) + self.gamma * 2)

        # result= 0

        # rowsIndexesForClasses = self.instances.getRowsIndexesForClass(self.classes)
        # for dataElement in data:
        #     alfa = dataElement['alpha']
        #     beta = dataElement['beta']
        #     gene1Index = dataElement['gene1']
        #     gene2Index = dataElement['gene2']
        #     method = dataElement['method']
        #     class0Sum = 0
        #     class1Sum = 0

        #     # class0
        #     for index in self.rowsIndexesForClasses[self.classes[0].name]:
        #         gene1Value = beta + float(self.instances.instances[index].args[gene1Index])
        #         gene2Value = float(self.instances.instances[index].args[gene2Index])
        #         if self.indicator(gene1Value, gene2Value, method):
        #             class0Sum += 1

        #     # class1
        #     for index in self.rowsIndexesForClasses[self.classes[1].name]:
        #         personFitness = 0
        #         gene1Value = beta + float(self.instances.instances[index].args[gene1Index])
        #         gene2Value = float(self.instances.instances[index].args[gene2Index])
        #         if self.indicator(gene1Value, gene2Value,method):
        #             class1Sum += 1

        #     result += (class0Sum  / self.rowsForClasses[self.classes[0].name] - class1Sum / self.rowsForClasses[self.classes[1].name]) * alfa

        # result = result / alfaSum

        # # range: 0..1   (0-100%)
        # return max(result - (self.gamma * (len(uniqueGenes))), 0) + self.gamma * 2
