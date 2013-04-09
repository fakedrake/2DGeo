from random import randint

import networkx as nx
import Image

IMAGE_PADDING = (20, 20)

LOWER_LEFT = (0,0)
UPPER_RIGHT = (500, 500)

class Plane(object):
    """A plane of objects connected into a graph. A plane accomodeates a
    dict of graphs that hold points.
    """

    def __init__(self, points=None, random_points=0, min_p=LOWER_LEFT, max_p=UPPER_RIGHT):
        """ Get points or random points.
	"""
        self.min_p = min_p
        self.max_p = max_p

        if points is None:
            points = [Point(randint(min_p[0], max_p[0]),randint(min_p[1], max_p[1])) for i in range(random_points)]

        self.points = points
        self.graphs = {}


    def add_edge(self, p1, p2, graph=None):
        """Add an associataion between two points inside a graph. If graph is
        not provided assume the first found.

        """
        if graph is None:
            graph = self.graphs.keys()[0]
        elif graph not in self.graphs:
            self.graphs[graph] = nx.Graph(id=graph)

        self.graphs[graph].add_edge(p1, p2)

    def geometry(self, padding=IMAGE_PADDING):
        """Get the default geometry of the image at hand."""
        ur_corner = Point(max(self.plane.points, key=lambda (x,y): x)[0], max(self.plane.points, key=lambda (x,y): y)[1])

        ll_corner =  Point(min(self.plane.points, key=lambda (x,y): x)[0], min(self.plane.points, key=lambda (x,y): y)[1])


        return ur_corner + ll_corner + Point(padding)


    def show(self, graphs=None):
        """Show points and the provided graphs. If no graphs are provided
        show all of them.
        """

        if graphs is None:
            graphs = self.graphs.values()
        else:
            graphs = [self.graphs[g] for g in graphs]

        image = Image.new("RGB", self.geometry())

        draw = ImageDraw.Draw(image)

        n = len(graphs)
        colors = ["hsl(%d, 100%, 50%)" % i for i in range(0,360,360/n)]

        draw.point(self.points, fill=colors[0])
        for c,g in zip(colors, graphs):
            for l in g.edges():
                draw.line(l, fill=c)

        return image
