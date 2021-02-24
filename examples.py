# examples.py

from gdraw import Graph, RadGraph, GraphDrawer

#%% 
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


#%% Another example

g = Graph()

# Add only one vertex
g.vertices = {6:[3,0]}


# Now add more vertices one at a time
# The command g.add_vertex(v_i, [x, y], v_j)
# means to add vertex v_i at the Coordinates
# [x, y] relative to the existing vertex v_j
# For example, the following:
g.add_vertex(7, [-1,1.75], 6)

# means to add vertex v_i = 7 at the position
# [-1, 1.75] relative to the existing vertex v_j = 6
# This is useful when building the graph one vertex
# at a time.  Do the same for the rest of the vertices:


g.add_vertex(8, [-2,0], 7)
g.add_vertex(11, [-0.25,2.5], 8)
g.add_vertex(5, [1,1], 7)
g.add_vertex(4, [1.75,-0.5], 5)
g.add_vertex(9, [-0.75,1.75], 5)
g.add_vertex(10, [1,1], 11)
g.add_vertex(12, [-0.5,1.5], 10)
g.add_vertex(1, [2.5,0.25], 12)
g.add_vertex(2, [1,-2], 1)
g.add_vertex(3, [2,-0.5], 2)

# Now create the positions of the vertex labels
# The label positions are always relative to
# the vertex position
g.label_positions = {}
    
dx = 0.4    
g.label_positions[12] = [-dx,dx]    
g.label_positions[11] = [-1.5*dx,0]
g.label_positions[8] = [-1.5*dx,0]
g.label_positions[10] = [dx,dx]
g.label_positions[9] = [-dx,-dx]
g.label_positions[7] = [-dx/2,dx]
g.label_positions[5] = [dx,dx]
g.label_positions[6] = [1.5*dx,0]
g.label_positions[4] = [1.5*dx,0]
g.label_positions[3] = [dx,0]
g.label_positions[2] = [dx,-dx]
g.label_positions[1] = [dx,dx/2]

# Add edges, this time we are using neighboring lists
g.edges = {
    1:[2,3,12],
    2:[3,9],
    3:[4],
    4:[5,6],
    5:[7,9],
    6:[7,8],
    7:[8],
    8:[11],
    9:[10],
    10:[11,12],
    11:[12]
}

# Now draw
fig_size = (10, 7)

gdrawer = GraphDrawer(fig_size)

gdrawer.draw(g)
gdrawer.save('sample-graph-2.pdf')


#%% Another example
# A graph whose vertices are along a circle

import math

fig_size = (7,7)
n = 12
G = RadGraph(n=n, R=3)

G.edges = []

# {u,v} is an edge iff gcd(u,v) >= 2
for u in range(1, n+1):
    for v in range(u+1,n+1):
        if math.gcd(u,v) >= 2:
            G.edges.append([u,v])

gdrawer = GraphDrawer(fig_size)
gdrawer.draw(G)

#%% Another example

fig_size = (4,4)
n = 8
G = RadGraph(n=8, R=2)
G.edges = [
    [1, 7],
    [2, 3],
    [4, 1],
    [7, 2],
    [5, 8],
    [6, 2],
    [5, 2],
    [4, 7],
    [1, 6]
    ]

gd = GraphDrawer(fig_size)
gd.draw(G)





