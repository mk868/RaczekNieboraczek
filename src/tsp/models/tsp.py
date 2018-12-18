from tsp.models.class_attribute import ClassAttribute
from tsp.models.pair import Pair
import tsp.models.fildereader
import math

class TSP(object):
    classes = []
    def __init__(self,path):
         self.instances = tsp.models.fildereader.load_data(path)
        


    def buildClassifier(self, instances):
        getClassDict = instances.getClasses()
        if getClassDict['count'] > 2 :
            raise Exception('TSP works properly only with 2 classes')

        classDictionary = getClassDict['classes']
        self.rowsForClasses = instances.getNumberOfRowsForClass(classDictionary)
        self.rowsIndexesForClasses = instances.getRowsIndexesForClass(classDictionary)

        i = 0
        for _class in classDictionary:
            self.classes.append(ClassAttribute(i,_class,self.rowsForClasses[_class],self.rowsIndexesForClasses[_class]))
            i += 1      
        
        #pair = self.computeSingleDelta(self.instances, 0, 56, '<')
        #print(pair.delta,';',pair.positivePropability,';',pair.negativePropability,';',pair.getX(),';',pair.getY())
        

    def indicator(self,firstValue,secondValue, method):
        if method == '>':
           if firstValue<secondValue:
                 return True
           else:
                return False
        if method == '<':
            if firstValue<secondValue:
                return True
            else:
                return False
        if method == '<=':
            if firstValue <= secondValue:
                return True    
            else:
                return False
        if method == '>=':
            if firstValue >= secondValue:
                return True
            else:
                return False
        if method == '==':
            if firstValue == secondValue:
                return True
            else:
                return False
        if method == '!=':
            if firstValue == secondValue:
                return True
            else:
                return False

    def computeSingleDelta(self, instances, gene1, gene2,method):
         positivePropability = self.computeFirstPropability(self.classes[0], instances, gene1, gene2, method)
         negativePropability = self.computeFirstPropability(self.classes[1], instances, gene1, gene2, method)
         return Pair(gene1, gene2, abs(positivePropability-negativePropability), positivePropability, negativePropability)

    def computeFirstPropability(self, classAttr, instances, gene1, gene2, method):
        sum = 0
        for val in classAttr.getRowsIndexes():
            instance = instances.instances[val]
            if self.indicator(instance.args[gene1], instance.args[gene2], method):
                sum = sum +1
        return (1.0/classAttr.getNumberOfRows())*sum


    def checkFitness(self, data): 
            result = 0
            alfaSum = 0
            gene1Value = 0
            gene2Value = 0
            
            resultClass0 = 0
            resultClass1 = 0
            tempNumerator = 0
            rowsIndexesForClasses = self.instances.getRowsIndexesForClass(self.classes)
            for index in self.rowsIndexesForClasses[self.classes[0].name]:
                    for dataElement in data: 
                        if len(self.instances.instances[0].args) < int(dataElement['gene1']) or len(self.instances.instances[0].args) < int(dataElement['gene2']):
                            return result
                        
                        alfa = dataElement['alpha']
                        alfaSum += alfa 
                        beta = dataElement['beta']
                        gene1Index = dataElement['gene1']
                        gene2Index = dataElement['gene2']
                        method = dataElement['method']
                        
                        dlugosc = len(self.instances.instances[index].args)
                        gene1Value = alfa * (beta + float(self.instances.instances[index].args[gene1Index])) 
                        gene2Value = float(self.instances.instances[index].args[gene2Index])
                        #print(self.instances.instances[index].args[gene1Index],'=',gene1Value,';',self.instances.instances[index].args[gene2Index],'=',gene2Value)
                        if self.indicator(gene1Value, gene2Value,method):
                            temp = 1
                        else: temp = 0
                        tempNumerator += alfa * temp
                        if alfa != 0:
                            resultClass0 = tempNumerator/alfaSum
                            resultClass0 = resultClass0/self.rowsForClasses[self.classes[0].name]
                        
            for index in self.rowsIndexesForClasses[self.classes[1].name]:
                    for dataElement in data: 
                        alfa = dataElement['alpha']
                        alfaSum += alfa 
                        beta = dataElement['beta']
                        gene1Index = dataElement['gene1']
                        gene2Index = dataElement['gene2']
                        method = dataElement['method']

                        gene1Value = alfa * (beta + float(self.instances.instances[index].args[gene1Index])) 
                        gene2Value = float(self.instances.instances[index].args[gene2Index])
                        #print(self.instances.instances[index].args[gene1Index],'=',gene1Value,';',self.instances.instances[index].args[gene2Index],'=',gene2Value)
                        if self.indicator(gene1Value, gene2Value,method):
                            temp = 1
                        else: temp = 0
                        tempNumerator += alfa * temp
                        if alfa != 0:
                            resultClass1 = tempNumerator/alfaSum
                            resultClass1 = resultClass1/self.rowsForClasses[self.classes[1].name]

            result = abs(resultClass0 - resultClass1)
        
            return result # range: 0..1   (0-100%)
                    
  