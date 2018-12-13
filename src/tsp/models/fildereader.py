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
    
    def numClasses(self):
        classes = []
        sum = 0
        for instance in self.instances:
            if len(classes) <= 0:
                 classes.append(instance.className)
                 sum += 1
            if  not instance.className in classes and instance.className != 'init':
                classes.append(instance.className)
                sum += 1
        print(classes)
        return sum

    def numAttributes(self):
        return len(self.instances[0].args) #w wece pokazuje +1

FUNDING = 'A:/Studia/MAGISTERKA/Zaawansowana inżynieria oprogramowania/Prosty algorytm TSP/TSP/dane/format2/baza_01_train.csv'

def read_funding_data(path):
    with open(path, 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row

if __name__ == "__main__":
    instances = []
    for idx, row in enumerate(read_funding_data(FUNDING)):
        instance = Instance(idx)
        #if idx < 1: #print(row) #tutaj możemy sobie ograniczyć liczbę wczytywanych wierszy no i dodać jakąś serializacje np. uzupełnić kolekcje instances o instancje z klasą i atrybutami
        #row to tak naprawdę nasza instancja jednego pacjenta atrybuty w row to geny a ostatni nazwany class to klasa decyzyjna
        for genes in row:  
            if genes == 'class':
                instance.className = row[genes]
            else: 
                instance.args.append(row[genes])
                instance.args_names.append(genes)
       
        instances.append(instance)
        instancesObject = Instances(instances)

    print(instances[0].className)
    print(instances[0].args[0])
    print(instances[0].args_names[24480])
    print(instancesObject.numClasses())
    print(instancesObject.numAttributes())


