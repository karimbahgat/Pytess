"""
Convenient user interface for Bill Simons/Carson Farmer python port of
Steven Fortune C++ version of a Delauney triangulator.
Located in tesselator.py.

Karim Bahgat, 2014
"""

import operator

from . import tesselator

class Point:
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
    Returns a list of triangle polygons. If the input coordinates contained
    a third z value then the output triangles will also have these z values. 

    """
    # Remove duplicate xy points bc that would make delauney fail, and must remember z (if any) for retrieving originals from index results
    seen = set() 
    uniqpoints = [ p for p in points if str( p[:2] ) not in seen and not seen.add( str( p[:2] ) )]
    classpoints = [Point(*point[:2]) for point in uniqpoints]
    print "data prepped"

    # Compute Delauney
    triangle_ids = tesselator.computeDelaunayTriangulation(classpoints)

    # Get vertices from result indexes
    triangles = [[uniqpoints[i] for i in triangle] for triangle in triangle_ids]
    print "triangulated!"
    
    return triangles

##def _unorderedlines2polygons(lines):
##    closedpolys = []
##    openpolys = []
##    for line in lines:
##        print len(openpolys)
##        start,end = line
##        for i,openpoly in enumerate(openpolys):
##            #openstarts,openends = zip(*openpoly)
##            flattened = [s_or_e for openline in openpoly for s_or_e in openline]
##            startexists = start in flattened
##            endexists = end in flattened
##            if startexists and endexists:
##                # polygon complete, save and remove it
##                ###print "remove poly"
##                openpoly.append(line)
##                closedpolys.append(openpoly)
##                openpolys.pop(i)
##                break
##            if startexists or endexists:
##                # same start or endpoint, connect line to the open polygon
##                ###print "add to open",len(openpoly)
##                openpoly.append(line)
##        # completely new line, create new open polygon
##        openpolys.append([line])
##
##    for l in openpolys:
##        pass #print "unfinished", l
##
##    return closedpolys

def voronoi(points, buffer_percent=100):
    """

    Surrounds each point in an input list of xy tuples with a
    unique Voronoi polygon.
    An optional buffer_percent argument controls how much bigger than
    the original bbox of the input points to set the bbox of fake points,
    used to account for lacking values around the edges (default is 100 percent). 
    Returns a list of 2-tuples of the original points (or None for fake buffer points)
    along with their corressponding Voronoi polygon. 

    """
    # Remove duplicate xy points bc that would make delauney fail, and must remember z (if any) for retrieving originals from index results
    seen = set() 
    uniqpoints = [ p for p in points if str( p[:2] ) not in seen and not seen.add( str( p[:2] ) )]
    classpoints = [Point(*point[:2]) for point in uniqpoints]

    # Create fake sitepoints around the point extent to correct for infinite polygons
    # For a similar approach and problem see: http://gis.stackexchange.com/questions/11866/voronoi-polygons-that-run-out-to-infinity
    xs,ys = zip(*uniqpoints)[:2]
    pointswidth = max(xs) - min(xs)
    pointsheight = max(ys) - min(ys)
    xbuff,ybuff = ( pointswidth / 100.0 * buffer_percent , pointsheight / 100.0 * buffer_percent )
    midx,midy = ( sum(xs) / float(len(xs)) , sum(ys) / float(len(ys)) )
    #bufferbox = [(midx-xbuff,midy-ybuff),(midx+xbuff,midy-ybuff),(midx+xbuff,midy+ybuff),(midx-xbuff,midy+ybuff)] # corner buffer
    bufferbox = [(midx-xbuff,midy),(midx+xbuff,midy),(midx,midy+ybuff),(midx,midy-ybuff)] # mid sides buffer
    classpoints.extend([Point(*corner) for corner in bufferbox])
    print "data prepped"

    # Compute Voronoi
    vertices,edges,poly_dict = tesselator.computeVoronoiDiagram(classpoints)
    print "voronoied!"

    # Turn unordered result edges into ordered polygons
    polygons = list()
    for sitepoint,polyedges in poly_dict.items():
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


##    edge_ids,v1s,v2s = zip(*edges)
##    edge_lines = zip(v1s,v2s)
##    edges_dict = dict(zip(edge_ids,edge_lines))
        
##    for _poly,edges in poly_dict.items():
##        poly = list()
##        for edge in edges:
##            _,i1,i2 = edge
##            if i1 == -1 or i2 == -1: continue # infinite lines have -1 as their index so ignore for now, but this drops of the edges so must deal with later
##            poly.append((vertices[i1],vertices[i2]))
##        polygons.append(poly)
    
##    polyedges = [vertices[i] 
##                 for edgeids in polygon_edgeids.values()
##                 for edgeindex in poly_ids]
##    for m in polygon_ids.values(): print m
##    polygons = [vertices[i] for poly_ids in polygon_ids.values()
##                for i in poly_ids]

##    vertices,edges,poly_dict = tesselator.computeVoronoiDiagram(classpoints)
##    lines = []
##    for edge in edges:
##        _,i1,i2 = edge
##        if i1 == -1 or i2 == -1: continue # infinite lines have -1 as their index so ignore for now, but this drops of the edges so must deal with later
##        lines.append((vertices[i1],vertices[i2]))
##    print "voronoied!"
##
##    polygons = _unorderedlines2polygons(lines)



    # Maybe clip parts of polygons that stick outside screen?
    # ...


    return polygons


