class Coordinate:
    def __init__(self, pos_i, pos_j):
        self.pos_i = pos_i
        self.pos_j = pos_j

    def clone(self):
        return Coordinate(self.pos_i, self.pos_j)

    def getPos_i(self) -> int:
        return self.pos_i

    def getPos_j(self) -> int:
        return self.pos_j
    
    def equals(self, c) -> bool:
        return self.pos_i == c.pos_i and self.pos_j == c.pos_j