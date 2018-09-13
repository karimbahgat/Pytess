"""
Where all the end-user functionality is defined. 
"""


import operator

from . import tesselator

class _Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __getitem__(self, get):
        if get == 0:
            return self.x
        elif get == 1:
            return self.y

def triangulate(points):  
    """
    Connects an input list of xy tuples with lines forming a set of 
    smallest possible Delauney triangles between them.

    Arguments:

    - **points**: A list of xy or xyz point tuples to triangulate. 

    Returns:

    - A list of triangle polygons. If the input coordinate points contained
        a third z value then the output triangles will also have these z values. 

    """
    # Remove duplicate xy points bc that would make delauney fail, and must remember z (if any) for retrieving originals from index results
    seen = set() 
    uniqpoints = [ p for p in points if str( p[:2] ) not in seen and not seen.add( str( p[:2] ) )]
    classpoints = [_Point(*point[:2]) for point in uniqpoints]

    # Compute Delauney
    triangle_ids = tesselator.computeDelaunayTriangulation(classpoints)

    # Get vertices from result indexes
    triangles = [[uniqpoints[i] for i in triangle] for triangle in triangle_ids]
    
    return triangles

def voronoi(points, buffer_percent=100):
    """
    Surrounds each point in an input list of xy tuples with a
    unique Voronoi polygon.

    Arguments:
    
    - **points**: A list of xy or xyz point tuples to triangulate. 
    - **buffer_percent** (optional): Controls how much bigger than
        the original bbox of the input points to set the bbox of fake points,
        used to account for lacking values around the edges (default is 100 percent).

    Returns:
    
    - Returns a list of 2-tuples, with the first item in each tuple being the
        original input point (or None for each corner of the bounding box buffer),
        and the second item being the point's corressponding Voronoi polygon. 

    """
    # Remove duplicate xy points bc that would make delauney fail, and must remember z (if any) for retrieving originals from index results
    seen = set() 
    uniqpoints = [ p for p in points if str( p[:2] ) not in seen and not seen.add( str( p[:2] ) )]
    classpoints = [_Point(*point[:2]) for point in uniqpoints]

    # Create fake sitepoints around the point extent to correct for infinite polygons
    # For a similar approach and problem see: http://gis.stackexchange.com/questions/11866/voronoi-polygons-that-run-out-to-infinity
    xs,ys = list(zip(*uniqpoints))[:2]
    pointswidth = max(xs) - min(xs)
    pointsheight = max(ys) - min(ys)
    xbuff,ybuff = ( pointswidth / 100.0 * buffer_percent , pointsheight / 100.0 * buffer_percent )
    midx,midy = ( sum(xs) / float(len(xs)) , sum(ys) / float(len(ys)) )
    #bufferbox = [(midx-xbuff,midy-ybuff),(midx+xbuff,midy-ybuff),(midx+xbuff,midy+ybuff),(midx-xbuff,midy+ybuff)] # corner buffer
    bufferbox = [(midx-xbuff,midy),(midx+xbuff,midy),(midx,midy+ybuff),(midx,midy-ybuff)] # mid sides buffer
    classpoints.extend([_Point(*corner) for corner in bufferbox])

    # Compute Voronoi
    vertices,edges,poly_dict = tesselator.computeVoronoiDiagram(classpoints)

    # Turn unordered result edges into ordered polygons
    polygons = list()
    for sitepoint,polyedges in list(poly_dict.items()):
        polyedges = [edge[1:] for edge in polyedges]
        poly = list()
        firststart,firstend = polyedges.pop(0)
        poly.append(firstend)
        while polyedges:
            curend = poly[-1]
            for i,other in enumerate(polyedges):
                otherstart,otherend = other
                if otherstart == curend:
                    poly.append(otherend)
                    ##print otherstart,otherend
                    polyedges.pop(i)
                    break
                elif otherend == curend:
                    ##print otherend,otherstart
                    poly.append(otherstart)
                    polyedges.pop(i)
                    break
        # Get vertices from indexes
        try: sitepoint = uniqpoints[sitepoint]
        except IndexError:
            sitepoint = None # fake bbox sitepoints shouldnt be in the results
        poly = [vertices[vi] for vi in poly if vi != -1]
        polygons.append((sitepoint, poly))

    # Maybe clip parts of polygons that stick outside screen?
    # ...

    return polygons


