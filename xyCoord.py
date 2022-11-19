class XyCoord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.x
    
    def __lt__(self, other):
        return self.x < other.x