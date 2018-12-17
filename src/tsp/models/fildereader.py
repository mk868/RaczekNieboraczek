import csv

class Instance(object):
    index = 0
    className = 'init'
    args = []
    args_names = []

    def __init__(self, index, className, args):
        self.index = index  
        self.className = className
        self.args = args
    
    def __init__(self, index):  
        self.index = index
        self.args = []
        self.args_names = []

class Instances(object):
    instances = []

    def __init__(self,instances):
        self.instances = instances
    
    def getClasses(self):
        classes = []
        sum = 0
        for instance in self.instances:
            if len(classes) <= 0:
                 classes.append(instance.className)
                 sum += 1
            if  not instance.className in classes and instance.className != 'init':
                classes.append(instance.className)
                sum += 1
        return {'count':sum,'classes':classes}

    def numAttributes(self):
        return len(self.instances[0].args) 

    def getNumberOfRowsForClass(self, classes):
        class1Rows = 0
        class2Rows = 0
        for instance in self.instances:
            if instance.className == classes[0]:
                class1Rows += 1
            if instance.className == classes[1]:
                class2Rows += 1
        rowsForClasses = {classes[0]:class1Rows,classes[1]:class2Rows}
        return rowsForClasses 

    def getRowsIndexesForClass(self,classes):
        class1Indexes = []
        class2Indexes = []
        i = 0
        for instance in self.instances:
            if instance.className == classes[0]:
                class1Indexes.append(i)
            if instance.className == classes[1]:
                class2Indexes.append(i)
            i += 1
        return {classes[0]:class1Indexes, classes[1]:class2Indexes}

def read_funding_data(path):
    with open(path, 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row

def load_data(path):
    instances = []
    for idx, row in enumerate(read_funding_data(path)):
        instance = Instance(idx)
        for genes in row:  
            if genes == 'class':
                instance.className = row[genes]
            else: 
                instance.args.append(row[genes])
                instance.args_names.append(genes)
       
        instances.append(instance)
        instancesObject = Instances(instances)
    return instancesObject
