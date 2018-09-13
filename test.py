import pytess
import itertools

# Define data

import random
def random_n(low, high, n, onlyints=False):
    if onlyints: randfunc = random.randrange
    else: randfunc = random.uniform
    return list(( randfunc(low,high) for _ in range(n) ))

test_random = [random_n(10,490,2)+random_n(0,222,1,onlyints=True)
               for _ in range(100)]

def midpoint(coords):
    xs,ys,zs = zip(*coords)
    xmid = sum(xs) / len(xs)
    ymid = sum(ys) / len(ys)
    zmid = sum(zs) / len(zs)
    return (xmid,ymid,zmid)

points = test_random

def test_triangulate(points):
    
    # Run test
    triangles = pytess.triangulate(points)
    print(len(triangles))

    # Visualize

    import sys
    sys.path.append("/Volumes/karim/Desktop/Python Programming/site_packages")
    import pydraw
    img = pydraw.Image(500,500)

    for triangle in triangles:
        if len(triangle) != 3: print("warning: returned non-triangle")
        triangle_xy = [map(int,point[:2]) for point in triangle]
        xmid,ymid,zmid = midpoint(triangle)
        img.drawpolygon(triangle_xy, fillcolor=(0,zmid,zmid),
                        outlinecolor=None )

    #for point in points:
    #    img.drawsquare(*point[:2], fillsize=2, fillcolor=(0,222,0))

    img.save("test.png")
    img.view()

def test_voronoi(points):
    
    # Run test
    
    polygons = pytess.voronoi(points)
    print(len(polygons))

    # Visualize

    import sys
    sys.path.append("/Volumes/karim/Desktop/Python Programming/site_packages")
    import pydraw
    crs = pydraw.CoordinateSystem([0,0,500,500])
    img = pydraw.Image(500,500)

    for i,(center,poly) in enumerate(polygons):
        #print i, poly
        
##        def pairwise(iterable):
##            a, b = itertools.tee(iterable)
##            next(b, None)
##            return itertools.izip(a, b)
##        
##        for line in pairwise(poly):
##            (x1,y1),(x2,y2) = line
##            img.drawline( x1,y1,x2,y2, fillcolor=(i/1.3,111,111),
##                            outlinecolor=None )
            ## img.view()

        img.drawpolygon( poly, fillcolor=(i/1.3,111,111),
                        outlinecolor=(0,0,0) )
##        
##        img.view()

        if center:
            img.drawsquare(*center[:2], fillsize=2, fillcolor=(0,222,0))

##    for point in points:
##        img.drawsquare(*point[:2], fillsize=2, fillcolor=(0,222,0))

    img.save("test.png")
    img.view()

# Run test
test_triangulate(points)
test_voronoi(points)



