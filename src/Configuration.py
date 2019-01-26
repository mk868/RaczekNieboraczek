import xml.etree.ElementTree as ET

class Configuration:
    def __init__(self):
        self.selectionSize = 0
        self.selectionType = "ranking"
        self.mutationProbability = 0.0
        self.crossingProbability = 0.0
        self.alphaInitValue = 0
        self.alphaLength = 0
        self.betaInitValue = 0
        self.betaLength = 0
        self.gamma = 0.0 #TODO
        self.comparisonsCount = 0
        self.targetProbability = 0.0
        self.evolutionLength = 0
        self.defaultFilePath = 'Init'
        self.defaultTestFilePath = 'Init'
        self.compLength = 1
        
    def load(self, file):    
        tree = ET.parse(file)
        root = tree.getroot()

        ''' genetic params '''
        self.selectionSize = int(root.find('selection').find('size').text)
        self.selectionType = root.find('selection').find('type').text
        
        self.mutationProbability = float(root.find('mutation').find('propability').text)
        self.crossingProbability = float(root.find('crossing').find('propability').text)

        ''' alpha '''
        self.alphaInitValue = int(root.find('alpha').find('initValue').text)
        self.alphaLength = int(root.find('alpha').find('length').text)
        
        ''' beta '''
        self.betaInitValue = int(root.find('beta').find('initValue').text)
        self.betaLength = int(root.find('beta').find('length').text)
        
        self.gamma = float(root.find('gamma').text) #TODO
        self.comparisonsCount = int(root.find('comparison').find('count').text)
        self.compLength = int(root.find('comparison').find('length').text)
        
        ''' end rules '''
        self.targetProbability = float(root.find('target').text)
        self.evolutionLength = int(root.find('evolution').find('length').text)
        
        ''' data file '''
        self.defaultFilePath = root.find('defaultFilePath').find('path').text
        self.defaultTestFilePath = root.find('defaultTestFilePath').find('path').text

        if(self.selectionSize < 10):
            raise ValueError('Selection size is inncorrect.')
        if (self.selectionType != "rulete" and self.selectionType != "ranking"):
            raise ValueError('Selection type is incorrect.')
        if(self.mutationProbability < 0.1 or self.mutationProbability > 1):
            raise ValueError('Mutation probability is incorrect')
        if(self.crossingProbability < 0.2 or self.crossingProbability > 1):
            raise ValueError('Crossing probability is incorrect')
        if(self.compLength < 1 or self.compLength > 3):
            raise ValueError('Comparsion length is incorrect')
        if(self.evolutionLength < 1):
            raise ValueError('Evolution length is incorrect')
        if(self.targetProbability < 0):
            raise ValueError('Target probability is incorrect')
        if(self.comparisonsCount < 1):
            raise ValueError('Comparsions count is incorrect')
        if(self.alphaInitValue < 1 or self.alphaInitValue > 2):
            raise ValueError('Alfa init value is incorrect')
        if(self.betaInitValue < 0 or self.betaInitValue > 1):
            raise ValueError('Beta init value is incorrect')