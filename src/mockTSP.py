
class MockTSP:

    def __init__(self):
        self.count = 130

    def checkFitness(self, data): #mock for TSP rule check
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
        result = 0
        if data[0]['method'] == '<':
            result += 0.10
        
        dis1 = 0.45 - (abs(data[0]['gene1'] - 10)) / 50
        dis2 = 0.45 - (abs(data[0]['gene2'] - 100)) / 50

        if dis1 > 0:
            result += dis1

        if dis2 > 0:
            result += dis2

        if result > 1:
            result = 1

        return result # range: 0..1   (0-100%)

