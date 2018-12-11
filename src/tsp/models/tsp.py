from class_attribute import ClassAttribute
from pair import Pair
import math

class tsp(object):
    """description of class"""
    def __init__(self,classes, genNumber, classIndex, pair):
        self.serialVersionUID = 1
        self.classes = classes
        self.genNumber = genNumber
        self.classIndex = classIndex
        self.pair = pair

    def buildClassifier(self, instances):
        if instances.numClasses() > 2 :
            raise Exception('TSP works properly only with 2 classes')
        
        i = 0
        for val in instances.classAttribute().enumarateValues():
            classes[i] = ClassAttribute(i,val.nextElement())
            i = i + 1

        genNumber = instances.numAttributes();
        
        computeNumberOfClassAndIndexes(instance)
        classIndex = instances.classIndex()
        computePaires(instances)

    def computeNumberOfClassAndIndexes(self, instances):
        classValue = 0 
        index = 0 
        for val in instances:
            classValue = val.classValue()
            self.classes[classValue].plus()
            self.classes[classValue].addIndex(index)
            index = index + 1

    def indicator(self,firstValue,secondValue):
        if firstValue<secondValue:
            return true
        else:
            return false

    def computeSingleDelta(self,instances, i, j):
         positivePropability = self.computeFirstPropability(classes[0],instances,i,j)
         negativePropability = computeFirstPropability(classes[1],instances,i,j)
         return Pair(i,j,abs(positivePropability-negativePropability),positivePropability,negativePropability)

    def computeFirstPropability(self,classAttr, instances, i ,j):
        sum = 0
        for val in classAttr.getRowsIndexes():
            instance = instances.instance(val)
            if indicator(instance.value(i), instance.value(j)):
                sum = sum +1
        return (1.0/classAttr.getNumberOfRows())*sum

    def computePaires(self, instances):
        maxDelta = 0
        result = Pair()
        paires = []

        for i in range(self.genNumber):
            if i == self.classIndex:
                None
            else:
                j = i + 1
                while j < self.genNumber:
                    j = j + 1
                    if j == self.classIndex:
                        None
                    result = computeSingleDelta(instances,i,j)
                    if maxDelta < result.getDelta():
                        maxDelta = result.getDelta()
                        paires.clear()
                        paires.append(result)
                    if maxDelta == result.getDelta():
                        paires.append(result)
        

                    
                   
                       


        