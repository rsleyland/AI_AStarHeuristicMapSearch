from Classes import Node
class PQ:
    def __init__(self):
        self.q = []
    
    def addToPQ(self, node: Node, edgecost=0, sumedges=0, route=[]):
        sumedges = sumedges + edgecost
        f = sumedges + node.heuristic
        route = route + [node]
        for i, entry in enumerate(self.q):
            if node.x == entry[0].x and node.y == entry[0].y:   # if already in queue, replace value if higher priority
                if f <= entry[2]:
                    entry[1] = sumedges
                    entry[2] = f
                    entry[3] = route
                return
        self.q.append([node, sumedges, f, route])
    
    def popTop(self):   #highest priority - lowest value
        highest = 1000
        for i, el in enumerate(self.q):
            if el[2] < highest:
                index = i
                highest = el[2]
        return self.q.pop(index)

    def isEmpty(self):
        return len(self.q) == 0

    def isNotEmpty(self):
        return len(self.q) > 0