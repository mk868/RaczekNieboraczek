import xml.etree.ElementTree as ET

class Configuration:
    def __init__(self):
        self.populationSize = 0
        self.selectionSize = 0
        self.mutationProbability = 0.0
        self.crossingProbability = 0.0
        self.alphaInitValue = 0
        self.alphaLength = 0
        self.betaInitValue = 0
        self.betaLength = 0
        self.GAMMA = 0.0 #TODO
        self.comparisonsCount = 0
        self.targetProbability = 0.0
        self.evolutionLength = 0

    def load(self, file):    
        tree = ET.parse(file)
        root = tree.getroot()

        ''' genetic params '''
        self.populationSize = int(root.find('population').find('size').text)
        self.selectionSize = int(root.find('selection').find('size').text)
        #SELECTION_TYPE = root.find('selection').find('type').text #TODO
        
        self.mutationProbability = float(root.find('mutation').find('propability').text)
        self.crossingProbability = float(root.find('crossing').find('propability').text)

        ''' alpha '''
        self.alphaInitValue = int(root.find('alpha').find('initValue').text)
        self.alphaLength = int(root.find('alpha').find('length').text)
        
        ''' beta '''
        self.betaInitValue = int(root.find('beta').find('initValue').text)
        self.betaLength = int(root.find('beta').find('length').text)
        
        self.GAMMA = float(root.find('gamma').text) #TODO
        self.comparisonsCount = int(root.find('comparison').find('count').text)
        
        ''' end rules '''
        self.targetProbability = float(root.find('target').text)
        self.evolutionLength = int(root.find('evolution').find('length').text)
