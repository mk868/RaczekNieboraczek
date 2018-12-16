from class_attribute import ClassAttribute
from pair import Pair
from fildereader import Instance, Instances
import fildereader
import math

class tsp(object):
    classes = []
    def __init__(self,path):
         self.instances = fildereader.load_data('A:/Studia/MAGISTERKA/Zaawansowana inżynieria oprogramowania/Prosty algorytm TSP/TSP/dane/format2/baza_01_train.csv')
        


    def buildClassifier(self, instances):
        getClassDict = instances.getClasses()
        if getClassDict['count'] > 2 :
            raise Exception('TSP works properly only with 2 classes')

        classDictionary = getClassDict['classes']
        rowsForClasses = instances.getNumberOfRowsForClass(classDictionary)
        rowsIndexesForClasses = instances.getRowsIndexesForClass(classDictionary)

        i = 0
        for _class in classDictionary:
            self.classes.append(ClassAttribute(i,_class,rowsForClasses[_class],rowsIndexesForClasses[_class]))
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

    #Ta metoda wymaga rozpatrzenia i poprawnej implementacji. Narazie to raczej gówno
    def checkFitness(self, data): 
            """
            compare element data[x]['gene1'] with element data[x]['gene2'] using data[x]['method'] method
            data[x]['alpha'] = alpha
            data[x]['gene1'] = gene 1 row
            data[x]['method'] = comparison method: '<', '<=', '>', '>=', '==', '!='
            data[x]['gene2'] = gene 2 row
            data[x]['beta'] = beta

            ignore code below
            this example:
            10 < 100 = 100%
            """
            alfa = 0.1
            beta = 0.2
            method = '<'
            gene1 = 0
            gene2 = 1
            result = 0
            
            if len(self.instances.instances[0].args) < gene1 or len(self.instances.instances[0].args) < gene2:
                    return result

            goodRule = 0
            rulesNum = 0
            instancesNum = 0

            for rule in data:
                rulesNum += 1
                for instance in self.instances.instances:
                   
                    pair = self.computeSingleDelta(self.instances, gene1, gene2,method)
                    gene1Value = alfa * (beta + float(instance.args[gene1])) 
                    gene2Value = float(instance.args[gene2])
                    if gene1Value < gene2Value:
                        goodRule += 1
             
            print(pair.delta ,' - TSP')   
            result = (goodRule / rulesNum)/100
            return result # range: 0..1   (0-100%)
                    
                   
                       
tsp = tsp('xd')
tsp.buildClassifier(tsp.instances)
print(tsp.checkFitness('x'),' - Wzor')

        