# AI_AStarHeuristicMapSearch

Python project for Artificial Intelligence class at Concordia University (Montreal).

The program is a covid-19 map simulation. A grid area map is implemented using networkx, matplotlib and numpy. THe grid will have four grid types which will occupy the grids of the map. The simulation will start at the user entered coordinates. It will use the A* algorithm with a heuristic that calculates the shortest path to a quarantine grid. The program will update the GUI on every node traversal, displaying the cumulative heuristic function values at each node. The program will pause when the path animation has finished and will close when the user presses return in the CLI.

- Python
- Matplotlib
- numpy
- networkx
- Custom Priority Queue Implementation

### Setup
- `git clone git@github.com:rsleyland/AI_AStarHeuristicMapSearch.git`
- `cd AI_AStarHeuristicMapSearch`
- create virtual env of your choice ex. `virtualenv -p python3 myenv`
- start virtual env ex. `source myenv/bin/activate`
- install dependencies from requirements.txt `pip install -r requirements.txt`
- Start server `python main.py`
- Follow CLI prompts, matplotlib GUI will open displaying animating map traversal

User Inputs:
- rows and columns of map
- Grid types (can be auto generated)
- Number of quarantine grids to include if auto generated
- Start location x and y
