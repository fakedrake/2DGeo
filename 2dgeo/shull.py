from itertools import izip

import networkx as nx

from fdgeo.visual import *
from fdgeo.vector import *
from fdgeo.plane import Plane


class SHull(object):
    """ An shull that structures itself.
    """

    def __init__(self, plane):
        """ 3 points to start with.
	"""
        self.plane = plane
        points = plane.points

        p1 = points[0]
        points.remove(p1)
        p2 = min(points, key=lambda p: abs(p-p1))
        points.remove(p2)
        p3 = min(points, key=lambda p: circumcircle(p1, p2, p)[1])
        points.remove(p3)

        self.hull_edge(p1,p2)
        self.hull_edge(p2,p3)
        self.hull_edge(p1,p3)
        c = circumcircle(p1, p2, p3)

        self.pool = sorted(points, key=lambda p: abs(p-c[0]))

    def hull_edge(self, p1, p2):
        self.plane.add_edge(p1, p2, 'shull')

    def triangle_edge(self, p1, p2):
        self.plane.add_edge(p1, p2, 'triangulation')

    @property
    def points(self):
        """ Get the points.
        """
        return self.pool + self.points_graph.nodes()

    def triangulate(self):
        """Populate the graph."""
        while self.pool:
            p = self.pool.pop(0)
            added = False

            for tangent, i in self._visible_points(p):
                if tangent:
                    if t1 is None:
                        t1 = i
                    else:
                        t2 = i
                else:
                    self.hull.remove_node(i)

                self.points_graph.add_edge(p, i)

            self.hull.add_edge(n, p)

    def convex_hull(self, slow=False):
        """Return the convex hull."""
        if self.pool:
            self.triangulate()

        return self.hull

    def _visible_points(self, p):
        """Get the visible points of the  hull from p."""
        for a, b, c in izip(self.hull, self.hull[1:]+self.hull[:1], self.hull[2:]+self.hull[:2]):
            if not self._inside_angle((a, b, c), p):
                yield self._tangent((a,b,c), p), b

    def _tangent(self, (a,b,c), p):
        """True if line b-p is tangent to the convex hull."""
        return ccw2d((a,b), p) == RIGHT or ccw2d((c,b), p) == LEFT

    def _inside_angle(self, (a,b,c), p):
        """Check if a point is inside an angle."""
        return ccw2d((b,a),c) == ccw2d((b,a),p) and ccw2d((b,c),a) == ccw2d((b,c),p)


def show_shull(sh):
    sh.triangulate()
    v = VisualizePlane(sh)
    pi = v.triangles_image().show()


if __name__ == "__main__":
    POINT_NUM = 7

    POINTS = [(100,0), (0,100), (100,100), (50,50), (0,0)]

    sh = SHull(points=[Point(p) for p in POINTS])
    show_shull(sh)
