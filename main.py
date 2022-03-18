import config
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
from Functions import getUserInput_Network, buildNetwork, getUserInput_FinishLocation, buildAdjList, getUserInput_Start, printAdjList
from random import random
from PriorityQueue import PQ

if __name__ == "__main__":
    
    # Get user input (rows, cols, gridtypes, start_location, finish_grid), build network (generate nodes, edges and grids), initialize PQ and append start node
    getUserInput_Network()
    Network = buildNetwork()
    start = getUserInput_Start()    # Type: Node
    config.finish = getUserInput_FinishLocation()    # Type = grid
    config.adjList = buildAdjList() # build adjaceny list which will be used to traverse the network (dict(node:[(n, edgecost, h(n)),...]))
    print("START: ", start)
    print("GOALS: ", config.finish)
    pq = PQ()
    pq.addToPQ(start)
    visited = []    # will store visited nodes that have been popped off the PQ
    winningroute = None 

    #set default figure size (window size)
    plt.figure(figsize=(14,7))

    # Set / create grid grid icons
    gridlabels2 = []
    for i in range(len(config.gridTypes)):
        pos = (int(i%config.cols)*0.2+0.1,int(i//config.cols)*0.1+0.05)
        type = config.gridTypes[i]
        name = config.gridNames[type]
        cost = config.gridCosts[type]
        imgplot = plt.imshow(config.gridIcons[type][::10,::10], extent=(pos[0]-0.05,pos[0]+0.05, -pos[1]-0.03, -pos[1]+0.03))
        #gridlabels2.append(plt.text(pos[0], -pos[1], f"{name}\nCost: {cost}", color='blue', weight='bold', ha='center', va='center'))

   
    current = start
    plt.text((config.cols*0.2)/2+0.2, 0.1, f"Start Node: {start}", ha='center', va='center',weight='bold',size='large')
    currentNodeText = plt.text((config.cols*0.2)/2+0.2, 0.06, f"Current Node: {current}", ha='center', va='center',weight='bold',size='large')

    # BUILD GRAPH WITH EDGES FROM ADJLIST
    npAdjList = np.array(list(config.adjList.items()), dtype=object)    # adjList converted to np array
    G = nx.Graph()
    for item in npAdjList:
        for node in item[1]:
            G.add_edge(item[0], node[0], weight=float(round(node[1],1)))    #adding edges also adds nodes involved
    # set node position variables for plotting
    for node in G.nodes:
        G.nodes.get(node)['pos'] = (node.x, -node.y)
    pos=nx.get_node_attributes(G,'pos')
    edgelabels = nx.get_edge_attributes(G, 'weight')
    poscopy = pos.copy()
    labelpos = {}
    for k, v in pos.items():
        labelpos[k] = (v[0],v[1]-0.02)      # shifting node label positions so not directly on top of node
        poscopy[k] = (poscopy[k][0],-poscopy[k][1])
    nx.draw_networkx_labels(G, labelpos, labels=poscopy)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edgelabels)


    # plt legend
    red_patch = mpatches.Patch(color='red', label='Visited Node')
    green_patch = mpatches.Patch(color='green', label='Goal Node')
    orange_patch = mpatches.Patch(color='orange', label='Current Path')
    plt.legend(loc='upper left', bbox_to_anchor=(0.05, 1.1), ncol=3, borderaxespad=0.3, handles=[orange_patch,green_patch,red_patch])
    


    # A* SEARCH ALGORITHM + PYPLOT GUI - will run until PQ is empty (no more moves)
    while pq.isNotEmpty():
        current = pq.popTop()   #get highest priority node from PQ ( min(f(n) = g(n) + h(n)) )

        currentNodeText.set_text(f"Current Node: {current[0]} - f(n)={round(current[2],3)}")

        nodeColours = []        # Colours of nodes to display in pyplot
        for node in G.nodes:
            if node in current[3]:
                nodeColours.append('orange')
            elif node in config.finish.nodez:
                nodeColours.append('green')
            elif node in visited:
                nodeColours.append('red')
            else:
                nodeColours.append('black')

        for edge in G.edges():      # Colours of edges to display in pyplot
            if edge[0] in current[3] and edge[1] in current[3]:
                G.edges.get(edge)['color'] = 'orange'
            elif 'color' in G.edges.get(edge) and G.edges.get(edge)['color'] == 'orange':
                G.edges.get(edge)['color'] = 'red'
            else:
                G.edges.get(edge)['color'] = 'black'
        edgecolors = [G[u][v]['color'] for u,v in G.edges()]

        # SUCCESS CASE - reached goal grid
        if current[0] in config.finish.nodez: # reached winning position
            print('SUCCESS') 
            winningroute = current[3]
            costOfTravel = current[2]
            text = f"SUCCESS - Goal reached\nCost of Travel: {costOfTravel}\nRoute: "
            for i, node in enumerate(winningroute):
                if i%config.cols==0 and i !=0:
                        text = text + "\n"
                if i == len(winningroute)-1:
                    text = text + str(node)
                    break
                text = text + str(node)+ "->"
            t = plt.text((config.cols*0.2)/2, -((config.rows*0.1)+0.04), text, color='red', weight='bold', ha='center', va='top',size='large')
            nx.draw(G, pos, with_labels=False, node_color=nodeColours, edge_color=edgecolors, node_size=150)
            plt.tight_layout()
            plt.ion()
            plt.show()
            input("Press [enter] to continue.")     # wait for user to enter to continue
            break

        # Add all available moves from x to PQ
        for move in config.adjList[current[0]]:
            if move[0] not in visited:
                pq.addToPQ(move[0], move[1], current[1], current[3])
        visited.append(current[0])

        # FAILURE CASE - cannot reach goal grid
        if pq.isEmpty():
            t = plt.text((config.cols*0.2)/2, -((config.rows*0.1)+0.06), "FAILURE - Cannot reach goal", color='red', weight='bold', ha='center', va='center',size='large')
            nx.draw(G, pos, with_labels=False, node_color=nodeColours, edge_color=edgecolors, node_size=150)
            plt.tight_layout()
            plt.ion()
            plt.show()
            input("Press [enter] to continue.") # wait for user to enter to continue
            break

        # Draw / redraw network with networkx and display using pyplot
        nx.draw(G, pos, with_labels=False, node_color=nodeColours, edge_color=edgecolors, node_size=150)
        plt.tight_layout()
        plt.ion()
        plt.show()
        plt.pause(0.1)
        # input("Press [enter] to continue.") 
 

    #Display result in terminal - if success -> show route and cost
    if winningroute:
        print("Route:", end=" ")
        for route in winningroute:
            print(route, end=', ')
        print("\nCost of travel:",costOfTravel)
    else:
        print('FAILURE - no path found')
