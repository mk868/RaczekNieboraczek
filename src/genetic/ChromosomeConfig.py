
class ChromosomeConfig:
    def __init__(self):
        self.geneLength = 0
        self.alphaLength = 0
        self.alphaInitValue = 0
        self.betaLength = 0
        self.betaInitValue = 0
        self.compLength = 2

    def __str__(self):
        return ('geneLength: ' + str(geneLength) +
        'alphaLength: ' + str(alphaLength) +
        'alphaInitValue: ' + str(alphaInitValue) +
        'betaLength: ' + str(betaLength) +
        'betaInitValue: ' + str(betaInitValue) +
        'compLength: ' + str(compLength))
