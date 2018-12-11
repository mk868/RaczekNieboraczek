class Pair(object):
    """description of class"""
    def __init__(self, x, y, delta, xPropability, yPropability,secondDelta):
        self.x = x
        self.y = y
        self.delta = delta
        self.positivePropability = xPropability
        self.negativePropability = yPropability
        self.secondDelta = secondDelta

    def __init__(self, x, y, delta, xPropability, yPropability):
        self.x = x
        self.y = y
        self.delta = delta
        self.positivePropability = xPropability
        self.negativePropability = yPropability


    def __init__(self, x, y, delta):
        self.x = x 
        self.y = y
        self.delta = delta
        

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getDelta(self):
        return self.delta

    def getPositivePropability(self):
        return self.positivePropability

    def getNegativePropability(self):
        return self.negativePropability

    def getSecondDelta(self):
        return self.secondDelta

    def setSecondDelta(self,secondDelta):
        self.secondDelta = secondDelta

    def toString(self):
        return 'Pair [x=' + self.x + ', y=' + self.y + ', delta=' + self.delta + ', positivePropability=' + self.positivePropability + ", secondDelta=" + self.secondDelta + "]"