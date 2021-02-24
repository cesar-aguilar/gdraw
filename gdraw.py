# gdraw.py
"""
Copyright 2021 Cesar O. Aguilar

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the 
Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall 
be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

import matplotlib.pyplot as plt
from math import cos, sin, pi
import copy

#%% Graph class
class Graph:
    """
    A simple graph class.

    Attributes
    ----------
    vertices : dictionary
      the keys are the vertices and the values are 
      the positions where each vertex is to be drawn, 
      each position is a two-element list of 
      (x, y) coordinates of the vertex position, the 
      keys can be strings, integers, or anything that 
      has a string representation

    edges : list or dictionary
      the edges of the graph, if edges is a list then edges 
      is a list of 2-element lists representing an edge in
      the graph, if edges is a dictionary then each
      key is a vertex and the corresponding value is
      a list of the neighbors of the vertex, in other 
      words an adjacency list

    label_positions : dictionary
      the keys are the vertices and the values are 
      2-element lists which is the offset (dx, dy)
      of where the vertex label should be placed
      relative to the position (x, y) of the vertex

    graph_label : dictionary
      the keys are strings representing a label that
      is to be placed at an (xx, yy) position determined
      by the corresponding value, these are used to 
      place a label like 'G' or 'C_4' somewhere in
      the graph, or any other desired text

    label_style : string
      determines the format of the vertex labels, 
      the default is 'v_i' which causes the _i to be
      replaced by the number used to name a vertex, if
      'raw' then the exact objects used as the vertices
      will be used, so long as the objects have a string
      representation

    node_colors : dictionary
      a key is a vertex and a value is a valid Python
      color to use for coloring the vertex

    """
    
    def __init__(self, vertices=None, edges=None):
        """
        Parameters
        ----------
        vertices : dictionary
        the keys are the vertices and the values are 
        the positions where each vertex is to be drawn, 
        each position is a two-element list of the 
        (x,y) coordinates of the vertex position, the 
        keys can be strings, integers, or anything that 
        has a string representation.

        edges : list or dictionary
        the edges of the graph, if E is a list then E 
        is a list of edges where each edge is a 
        2-element list, if E is a dictionary then each
        key is a vertex and the corresponding value is
        a list of the neighbors of the vertex, in other 
        words an adjacency list

        """

        self.vertices = vertices
        self.edges = edges
        self.label_positions = None
        self.graph_label = None
        self.label_style = 'v_i'
        self.node_colors = None


    def _set_vertex_xpts(self):
        """Creates list of x-coordinates of vertex positions."""
        
        self.x_pts = []
        for x_val, _ in self.vertices.values():
            self.x_pts.append(x_val)


    def _set_vertex_ypts(self):
        """Creates list of y-coordinates of vertex positions."""
        self.y_pts = []
        for _, y_val in self.vertices.values():
            self.y_pts.append(y_val)


    def shift_vertices(self, dx, dy):
        """
        Shift all vertices horizontally by dx and vertically by dy.
        
        Parameters
        ----------
        dx : float
            all vertices will by shifted by dx
        dy : float
            all vertices will be shifted by dy
        """
    
        for vertex in self.vertices:
            
            self.vertices[vertex][0] += dx 
            self.vertices[vertex][1] += dy


    def add_edge(self, u, v):

        """
        Add edge {u, v}.
        
        Parameters
        ----------
        u : int, str
        v : int, str
        """
        
        if u in self.vertices and v in self.vertices:
        
            if isinstance(self.edges, list):
                
                self.edges.append([u, v])
                
            else:  # then neighbors_list
                                                                                    
                if u in self.edges:
                    
                    self.edges[u].append(v)                                
                    
                else:
                    
                    self.edges[u] = [v]

            return None

        raise TypeError("Both u = {u} and v = {v} must already be vertices.")
                                        
        
                                                 

    def add_edges(self, edges):
        """
        Add multiple edges to graph.
        
        Paramters
        ---------
        edges : list
          a list of lists where each sublist is a 
          2-element list forming an edge
        
        """
        
        if isinstance(edges, list):
            
            for e in edges:
                
                self.add_edge(e)

            return None

        raise TypeError("Argument must be a list of lists.")

                                
    def add_vertex(self, v, pos, w=None):
        """
        Adds vertex v at position pos.
        
        If w is the label for an existing vertex
        then the location where v is added is 
        relative to w.

        Parameters
        ----------
        v : mixed, usually str or int
          a vertex in the graph
        pos : list
          a 2D-point of the position of the new vertex
        w : mixed, usually str or int
          an existing vertex of the graph

        """

        if v in self.vertices:
            raise Exception(f"Vertex v = {v} is already in the graph.")

        w_x = w_y = 0 
        
        if w is not None:
            if w not in self.vertices:            
                raise Exception(f"Vertex w = {w} is not in the graph.")

            w_x, w_y = self.vertices[w]
                            
        self.vertices[v] = [pos[0] + w_x, pos[1] + w_y]
        
            
    def radd_vertex(self, v, R, theta, w):

        """
        Adds vertex v at distance R and angle theta 
        relative to existing vertex w.
        
        The parameters R and theta are polar coordinates.  
        If w has position (x, y) then v is added at 
        Euclidean position 
            (x+R*cos(theta), y+R*sin(theta)).  
        The angle theta should be given in degrees not 
        radians.

        Paramters
        ---------
        v : mixed, usually str or int
          the new vertex to be added
        R : float
          distance from vertex
        theta : float
          angle measured CCW from horizontal line through w
        w : mixed, usually str or int
          existing vertex in graph

        """
        
        if v in self.vertices:
            
            raise Exception(f"Vertex v = {v} is already in the graph.")
        
        if w not in self.vertices:

            raise Exception(f"Vertex w = {w} is not in the graph.")

            
        w_x, w_y = self.vertices[w]
                            
        angle = theta*pi/180

        self.vertices[v] = [R*cos(angle) + w_x, R*sin(angle) + w_y]

        
    def copy(self):
        """
        Returns a deep copy of the graph.
        """

        G_new = Graph()

        G_new.vertices = copy.deepcopy( self.vertices )
        G_new.edges = copy.deepcopy( self.edges )
        G_new.label_positions = copy.deepcopy( self.label_positions )
        G_new.graph_label = copy.deepcopy( self.graph_label )

        return G_new


#%% RadGraph
class RadGraph(Graph):
    
    """A graph whose vertices are placed on a circle."""
    
    def __init__(self, n, R, phi=None, dr=0.5, vertex_labels=True):
        """                
        Parameters
        ----------
        n : int
            number of vertices
        R : float
            radius of circle
        phi : float, optional
            degrees to shift all vertices. The default is None.
        dr : float, optional
            distance from vertex to place label. The default is 0.5.
        vertex_labels : boolean, optional
            if True then labels are created automatically. The default is True.

        Returns
        -------
        None.

        """
        
        dt = (360/n)*(pi/180)
        
        t0 = 0.5*dt if phi is None else phi*pi/180
                
        super().__init__()
        
        self.vertices = {}
        self.label_positions = {}
        for v in range(n):
            a, b = cos(t0+v*dt), sin(t0+v*dt)
            x, y = R*a, R*b
            self.add_vertex(v+1, [x, y] )
            if vertex_labels:
                self.label_positions[v+1] = [dr*a, dr*b]
            
                            
#%% GraphDrawer class
class GraphDrawer:
    """
    A Graph drawer.
    """
        
    def __init__(self, fig_size, font_size=25, marker_size=20):
        """        
            
        Paramters
        ---------
        fig_size : tuple
          width and height of the figure in inches
        font_size : int
          font size used in vertex labels
        marker_size : int
          the marker size used for the vertices
        """
          
        self.fig_size = fig_size
        self.font_size = font_size
        self.marker_size = marker_size
        self.graphs = []
        self.fig = None
        self.ax = None
    
        
    def _load(self, graphs):
        """        
        Parameters
        ----------
        graphs : list
            list of Graph objects

        Returns
        -------
        None.

        """

        for g in graphs:
            if isinstance(g, Graph):
                self.graphs.append(g)
                    
        return None
    

    def draw(self, *args):
    
        """Draw graphs."""
    
        self._load(args)
    
        self.fig = plt.figure(figsize=self.fig_size)
    
        self.ax = self.fig.gca()
                
        for g in self.graphs:
            
            self.plot_graph(g)
    
        
        self._center_axis()
        
        return self

    
    def save(self, file_name, dpi=150):
        """
        Saves figure to the file file_name.
        
        When file_name contains an extension, for example, 'mygraph.png'
        then a .png file is generated.  If no extension is included then
        two files are generated with .eps and .png extensions using
        file_name as the base name of the file.
        
        Parameters
        ----------
        file_name : str
            Name of file when saving with extension.  
        dpi : int, optional
            Dots per square inch. The default is 100.

        Returns
        -------
        None.

        """
                                    
        if '.' in file_name:        
            self.fig.savefig(file_name, dpi=dpi, bbox_inches='tight',pad_inches=0,transparent=True)
        else:
            self.fig.savefig(f"{file_name}.eps",dpi=dpi, bbox_inches='tight',pad_inches=0,transparent=True)
            self.fig.savefig(f"{file_name}.png",dpi=dpi, bbox_inches='tight',pad_inches=0,transparent=True)
            
        return None
    
    
    
    def plot_graph(self, G):
    
        if G.vertices:
            G._set_vertex_xpts()
            G._set_vertex_ypts()
        else:
            raise TypeError("The graph has no vertices.")
        
        if G.edges:
            self.make_edges(G)
        else:
            print("Warning: No graph structure defined.")
    
        # First plot vertices, use specified colors if any
        if G.node_colors:
                
            for v, color in G.node_colors.items():
                if v in G.vertices:            
                    x , y = G.vertices[v]            
                    self.ax.plot(x, y, '.',color=color, markersize=self.marker_size)                
                else:                
                    raise Exception(f"Vertex {v} is not a vertex in the graph.")
                                                    
        else:                
            
            self.ax.plot(G.x_pts, G.y_pts,'.k', markersize=self.marker_size)        
                
                                   
        if G.label_positions:                 
            self.add_vertex_labels(G)
        else:
            print('Note: No label positions defined.')
            
        if G.graph_label:
            for label, position in G.graph_label.items():
                x, y  = position
                s = r'${}$'.format(label)
                self.ax.text(x, y, s, fontsize=self.font_size, horizontalalignment='center')
    
        return None
    
    
    def make_edges(self, G):

        """Create edges connecting adjacent vertices."""
    
        if isinstance(G.edges, list):
        
            for e in G.edges:
                
                x = [ G.vertices[e[0]][0] , G.vertices[e[1]][0] ]
                y = [ G.vertices[e[0]][1] , G.vertices[e[1]][1] ]
                
                self.ax.plot(x, y, '.-k', ms=self.marker_size)
                                    
        elif isinstance(G.edges, dict):  # using adjacency lists
            
            for v, Nv in G.edges.items():        
                for u in Nv:
                    
                    x = [G.vertices[v][0], G.vertices[u][0]]
                    y = [G.vertices[v][1], G.vertices[u][1]]
                    
                    self.ax.plot(x, y, '-k', ms=self.marker_size)
                                
        else:  # invalid type
            
            raise TypeError("The edge structure must be a list or a dictionary.")
    
        return None
    
    
    def add_vertex_labels(self, G):

        """Add labels to the vertices."""
    
        for v, pos in G.label_positions.items():
            
            x = G.vertices[v][0] + pos[0]
            y = G.vertices[v][1] + pos[1]
            
            # Use latex to render label
            if G.label_style == 'raw':
                
                s = r'${}$'.format(v)            
                
            else:
                
                s = r'${}$'.format('v_{' + str(v) + '}')
    
            
            self.ax.text(x, y, s, fontsize=self.font_size, 
                         horizontalalignment='center', 
                         verticalalignment='center')
    
        return None    
    

    def _center_axis(self):
        """
        Makes the axis of a plot with center of axis at (0,0)
        instead of the default box-style axis in matplotlib    
    
    
        Returns
        -------
        None.
    
        """
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
    
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.spines['bottom'].set_position(('data',0)) # set position of x spine to x=0
        self.ax.yaxis.set_ticks_position('left')
        self.ax.spines['left'].set_position(('data',0))   # set position of y spine to y=0
    
        for t in self.ax.xaxis.get_major_ticks(): 
            t.label.set_fontsize(self.font_size)
            t.label.set_color('black')
        for t in self.ax.yaxis.get_major_ticks(): 
            t.label.set_fontsize(self.font_size)
            t.label.set_color('black')
    
        self.ax.axis('equal')
        
        self.ax.axis('off')
        
        return None
            
                    