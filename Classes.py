import config

class Network:
    def __init__(self) -> None:
        self.createNetwork()

    def createNetwork(self):
        totalGrids = config.rows * config.cols
        for i in range(totalGrids):
            Grid(i, config.gridCosts[config.gridTypes[i]])

class Grid:
    def __init__(self, num, cost):
        self.num = num
        self.cost = cost
        self.nodez = []
        self.createNodes()
        self.createEdges()
        config.grids.append(self) 

    def createNodes(self):
        self.tl = Node(int(self.num%config.cols)*0.2,int(self.num//config.cols)*0.1)
        self.tr = Node(int(self.num%config.cols)*0.2+0.2,int(self.num//config.cols)*0.1)
        self.bl = Node(int(self.num%config.cols)*0.2,int(self.num//config.cols)*0.1+0.1)
        self.br = Node(int(self.num%config.cols)*0.2+0.2,int(self.num//config.cols)*0.1+0.1)

        if self.tl in config.nodes:
            self.tl = config.nodes[config.nodes.index(self.tl)]    # already in list of nodes so point to existing node
        else:
            config.nodes.append(self.tl)    #append unique node to list of nodes
        if self.tr in config.nodes:
            self.tr = config.nodes[config.nodes.index(self.tr)]    
        else:
            config.nodes.append(self.tr)    #append unique node to list of nodes
        if self.bl in config.nodes:
            self.bl = config.nodes[config.nodes.index(self.bl)]    
        else:
            config.nodes.append(self.bl)    #append unique node to list of nodes
        if self.br in config.nodes:
            self.br = config.nodes[config.nodes.index(self.br)]    
        else:
            config.nodes.append(self.br)    #append unique node to list of nodes
        self.nodez.append(self.tl)
        self.nodez.append(self.tr)
        self.nodez.append(self.bl)
        self.nodez.append(self.br)  # storing nodes belonging to this grid in object, easier to check for finishing position of winning grid

        
    def createEdges(self): # top to bottom and left to right - for ease of edge comparison
        self.te = Edge(self.tl, self.tr, self.cost)
        self.re = Edge(self.tr, self.br, self.cost)
        self.be = Edge(self.bl, self.br, self.cost)
        self.le = Edge(self.tl, self.bl, self.cost)
        config.edges.append(self.te)
        config.edges.append(self.re)
        config.edges.append(self.be)
        config.edges.append(self.le) 

    def __str__(self) -> str:
        return (f"{self.tl}, {self.tr}, {self.bl}, {self.br}")

class Node:
    def __init__(self, x, y) -> None:
        self.x = round(x,1)
        self.y = round(y,1)
        self.heuristic = 0

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __str__(self) -> str:
        return (f"({self.x}, {self.y})")

    def __hash__(self):
      return hash((self.x, self.y))

class Edge:
    def __init__(self, n1, n2, cost) -> None:
        self.n1 = n1
        self.n2 = n2
        self.cost = cost

    def __str__(self) -> str:
        return (f"{self.n1} --> {self.n2}, Cost: {self.cost}")
