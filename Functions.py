from numpy.core.fromnumeric import size
import config, math
import numpy as np
from random import random, randint
from Classes import Node, Grid, Network


def setSharedEdgeWeights():
    newEdges = []
    while config.edges:
        temp = config.edges.pop()
        removedBoth = False
        for edge in config.edges:
            if temp.n1.x == edge.n1.x and temp.n1.y == edge.n1.y and temp.n2.x == edge.n2.x and temp.n2.y == edge.n2.y:
                if temp.cost == 3 and edge.cost == 3:
                    config.edges.remove(edge)   #remove both edges as cannot traverse between two playgrounds
                    removedBoth = True
                    break
                newval = (temp.cost + edge.cost)/2
                temp.cost = newval
                config.edges.remove(edge)
                break
        if not removedBoth:
            newEdges = [temp] + newEdges
    config.edges = newEdges

def buildAdjList():
    adjList = {}
    for edge in config.edges:
        adjList[edge.n1] = adjList.get(edge.n1, []) + [(edge.n2, edge.cost, calcDistanceToGoal(edge.n2, config.finish))]
        adjList[edge.n2] = adjList.get(edge.n2, []) + [(edge.n1, edge.cost, calcDistanceToGoal(edge.n1, config.finish))]
    return adjList

def calcDistanceToGoal(node: Node, finish: Grid):
    tldist = math.sqrt((((finish.tl.x-node.x)**2)+((finish.tl.y-node.y)**2)))
    trdist = math.sqrt((((finish.tr.x-node.x)**2)+((finish.tr.y-node.y)**2)))
    bldist = math.sqrt((((finish.bl.x-node.x)**2)+((finish.bl.y-node.y)**2)))
    brdist = math.sqrt((((finish.br.x-node.x)**2)+((finish.br.y-node.y)**2)))
    node.heuristic = min(tldist, trdist, bldist, brdist)*10
    return round(min(tldist, trdist, bldist, brdist),3)*10

def getUserInput_Network():
    # Set col and row size  (user input)
    print("\nWelcome to fastest path finder\n")
    while True:
        try:
            config.cols = int(input("Please enter # of columns: "))
            config.rows = int(input("Please enter # of rows: "))
            break
        except ValueError:
            print("Invalid input for rows and cols - try again")
        
    # Set type of each grid in network  (user input)
    print("Okay now to choose the types of the grids")
    #config.gridTypes = [randint(1,4) for x in range(config.cols*config.rows)]
    config.gridTypes = np.random.randint(1,5, size=(config.cols*config.rows))
    
    # for i in range(config.cols*config.rows):
    #     config.gridTypes.append(randint(1,4))
        # while True:
        #     try:
        #         choice = int(input(f"Grid {i+1} - Enter choice (1 = quarantine, 2 = vaccine, 3 = playground, 4 = empty): "))
        #         if choice > 4 or choice < 1:
        #             raise ValueError
        #         config.gridTypes.append(choice)
        #         break
        #     except ValueError:
        #         print("Invalid input - try again")

def getUserInput_FinishLocation():
     # Filter finishing grid options
    gridIndexes = []    # allowed finishing grids
    for i, entry in enumerate(config.gridTypes):
        if entry == 1:  # quarantine type
            gridIndexes.append(i+1)     
    
    # Finishing grid selection
    while True:
        try:
            finish = int(input(f"Please choose a finishing grid from ({gridIndexes}): "))
            if finish not in gridIndexes:
                raise ValueError
            finish = finish - 1
            break
        except ValueError:
            print("Invalid choice - please choose one number from the list")
    return config.grids[finish]

def buildNetwork():
    n = Network()
    setSharedEdgeWeights()

def getStartingNode(x, y):
        
     #calculate which grid starting point is in - if between two grids will go to closest top right corner
    tempx = x
    tempy = y
    gridLoc = 0
    while tempx > 0.2:
        tempx -= 0.2
        gridLoc += 1
    while tempy > 0.1:
        tempy -= 0.1
        gridLoc += config.cols
    start = config.grids[gridLoc].tr     #starting node - agent's position
    return start

def getUserInput_Start():

    # Set start pos x & y pos  (user input)
    while True:
        try:
            x = input("Would you like to enter custom start coordinates? (y/n): ")
            x = x.upper()
            if x != 'Y' and x != 'N':
                raise ValueError
            break
        except ValueError:
            print("Invalid input - please choose from y or n")
    if x == 'Y':
        while True:
            try:
                x = float(input("Please enter x pos: "))
                y = float(input("Please enter y pos: "))
                break
            except ValueError:
                print("Invalid input for x and y - try again")
        start = getStartingNode(x,y)
    else:
        start = getStartingNode(round((random()*100)%(config.cols*0.2),2), round((random()*100)%(config.rows*0.1),2))
    return start

def printAdjList():
    for k, vals in config.adjList.items():
        print("Key node: ",k)
        for v in vals:
            print("\t",v[0], v[1], v[2])
        print()