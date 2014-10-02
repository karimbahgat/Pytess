# algorithm for creating a TIN file from a set of points
# ie creating height triangles bw each three closest points
# for more resources check http://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation

import random, math, operator




# utilities

def random_n(low, high, n):
    return list(( random.randrange(low,high) for _ in xrange(n) ))

def neighbours(point, others, count):
    
    def dist(p1,p2):
        x1,y1,z1 = p1
        x2,y2,z2 = p2
        xdist = (x1 - x2) ** 2
        ydist = (y1 - y2) ** 2
        zdist = (z1 - z2) ** 2
        return sum((xdist,ydist,zdist))
        
    dists = ( (other,dist(point,other)) for other in others if other != point)
    sortdist = (_ for _ in sorted(dists, key=operator.itemgetter(1) ))
    return list(( next(sortdist)[0] for _ in xrange(count) ))

def midpoint(coords):
    xs,ys,zs = zip(*coords)
    xmid = sum(xs) / len(xs)
    ymid = sum(ys) / len(ys)
    zmid = sum(zs) / len(zs)
    return (xmid,ymid,zmid)




# triangulation algorithm

def triangulate_custom(points):
    # new approach
    # 1. create triangle polygons for all combinations of points
    # 2. for each poly
    # 2.1 drop if contains any other point
    # 3. return list of nonoverlapping triangles
    pass

def triangulate_onlyneighbours(points):
    # maybe not same as delauney triangles
    # of if make the algo from scratch, see http://www.geom.uiuc.edu/~samuelp/del_project.html
    # or try to port this weird language: http://rosettacode.org/wiki/Voronoi_diagram/J/Delaunay_triangulation
    for point in points:
        n1,n2 = neighbours(point, points, 2)
        triangle = (point, n1, n2)
        trimid = midpoint(triangle)
        yield triangle

def triangulate_seidel(points):
    # based on seidels port of poly2tri,see: https://code.google.com/p/poly2tri/source/browse/python/seidel.py?repo=archive&r=5ad6efedc1c120ea194bbce2a0d4ed849e6e6903
    # however, something wrong, triangles not correct
    import seidel
    points = [point[:2] for point in points]
    return seidel.Triangulator(points).triangles()
    
    



# test it

if __name__ == "__main__":

    # data samples

    test1 = [[10, 10],[10, 90],[90, 90],[90, 10]]
    test2 = [[5, 5],[5, -5],[-5, -5],[-3, 0],[-5, 5]]
    test_random = [random_n(0,500,2)+random_n(0,222,1) for _ in range(10)]
    test_dude = [[174.50415,494.59368],[215.21844,478.87939],[207.36129,458.87939],[203.07558,441.02225],[203.07558,418.1651],
        [210.93272,394.59367],[224.50415,373.1651],[241.64701,358.1651],[257.36129,354.59367],[275.93272,356.73653],
        [293.07558,359.59367],[309.50415,377.45082],[322.36129,398.1651],[331.64701,421.73653],[335.21844,437.45082],
        [356.64701,428.52225],[356.1113,428.34367],[356.1113,428.34367],[368.78987,419.59368],[349.50415,384.59367],
        [323.78987,359.59367],[290.93272,343.87939],[267.36129,341.02225],[264.50415,331.02225],[264.50415,321.02225],
        [268.78987,306.02225],[285.93272,286.02225],[295.21844,270.30796],[303.78987,254.59367],[306.64701,213.87939],
        [320,202.36218],[265,202.36218],[286.64701,217.45082],[293.78987,241.02225],[285,257.36218],[270.93272,271.73653],
        [254.50415,266.02225],[250.93272,248.1651],[256.64701,233.1651],[256.64701,221.02225],[245.93272,215.30796],
        [238.78987,216.73653],[233.78987,232.45082],[232.36129,249.59367],[243.07558,257.09367],[242.89701,270.30796],
        [235.93272,279.95082],[222.36129,293.1651],[205.21844,300.6651],[185,297.36218],[170,242.36218],[175,327.36218],
        [185,322.36218],[195,317.36218],[230.75415,301.02225],[235.39701,312.45082],[240.57558,323.52225],
        [243.61129,330.48653],[245.21844,335.12939],[245.03987,344.4151],[229.86129,349.4151],[209.14701,362.09367],
        [192.89701,377.80796],[177.18272,402.27225],[172.36129,413.87939],[169.14701,430.48653],[168.61129,458.52225],
        [168.61129,492.80796]]

    triangles = triangulate_onlyneighbours([p+[192.0] for p in test1])

    import sys
    sys.path.append("/Volumes/karim/Desktop/Python Programming/site_packages")
    import pydraw
    img = pydraw.Image(500,500)
    for triangle in triangles:
        triangle2d = [corner[:2] for corner in triangle]
        img.drawpolygon(triangle2d, fillcolor=(222,0,0),
                        outlinecolor=(0,222,0) )
        
    img.view()


