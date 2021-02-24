# gdraw

gdraw.py defines two classes used to draw a discrete graph using matplolib.pyplot

```python
from gdraw import Graph, RadGraph, GraphDrawer

# First create a graph
G = Graph()

# Now add the vertices, the format for each
# vertex is:  k : [x,y] where
# k is the integer label of the vertex and
# [x,y] are the Cartesian coordinates of
# where the vertex will be placed:
    
G.vertices = {     
    1:[0,2],
    2:[1,3],
    3:[1,1],
    4:[2,2],
    5:[2,0],
    6:[3,1],
    7:[4,0],
    8:[5,2],
    9:[3,3],
    10:[3,4],
    11:[2,4]
}

# Now specify the edges
G.edges = [
     [1,2],[1,3],[2,4],[3,4],[4,6],
     [5,6],[5,7],[4,8],[4,9],[6,7],
     [6,8],[6,9],[7,9],[8,9],[9,10]
]

# Now specify where the vertex labels
# should be placed relative to the location
# of the vertex, you can define dx and dy
# as helper variables, but not necessary
dx, dy = 0.3, 0.3

# Each entry of G.label_positions is of the form
# k:[a,b] where k is the vertex and [a,b] is the 
# position of the label to vertex k relative to
# position [x,y] of vertex k (the position of k
# was set in G.vertices)

G.label_positions = {
    1:[-0.25,dy],
    2:[0,dy],
    3:[0,-dy],
    4:[0,2*dy],
    5:[0,-dy],
    6:[-2*dx,0],
    7:[0,-dy],
    8:[dx,dy],
    9:[2*dx,0.25*dy],
    10:[2*dx,0],
    11:[0,dy]
}

# Now specify the (width, height) of the figure
fig_size = (6,6)

# Now create the object that will
# actually do the drawing of the graph
gdrawer = GraphDrawer(fig_size)

# Now draw the graph
gdrawer.draw(G)

# And if needed save the drawing
file_name = 'sample-graph.pdf'
gdrawer.save(file_name)
```
