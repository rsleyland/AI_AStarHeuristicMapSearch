import matplotlib.image as mpimg

nodes = []
edges = []
grids = []
adjList = {}    # can access adjList by passing a node - will return list of tuples - each tuple with (node, edge-cost, heuristic)
gridTypes = []     # GRID TYPES: 1 = quarantine, 2 = vaccine, 3 = playground, 4 = empty
gridCosts = { 1: 0, 2: 2, 3: 3, 4: 1}   # GRID COSTS: quarantine = 0, vaccine = 2, playground = 3, empty = 1
gridNames = { 1: "Quarantine", 2: "Vaccine", 3: "School", 4: "Empty"}
cols = 0
rows = 0
gridIcons = { 1: mpimg.imread('icons/quarantine.png'), 2: mpimg.imread('icons/vaccine.png'), 3: mpimg.imread('icons/school.png'), 4: mpimg.imread('icons/empty.png')}