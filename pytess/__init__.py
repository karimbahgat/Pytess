"""
# Pytess

Pure Python tessellation of points into polygons, including
Delauney/Thiessin, and Voronoi polygons. Built as a
convenient user interface for Bill Simons/Carson Farmer python port of
Steven Fortune C++ version of a Delauney triangulator.


## Platforms

Tested on Python version 2.x and 3.x. 


## Dependencies

Pure Python, no dependencies. 


## Installing it

Pytess is installed with pip from the commandline:

    pip install pytess


## Usage

To triangulate a set of points, simply do:

    import pytess
    points = [(1,1), (5,5), (3,5), (8,1)]
    triangles = pytess.triangulate(points)

And for voronoi diagrams:

    import pytess
    points = [(1,1), (5,5), (3,5), (8,1)]
    voronoipolys = pytess.voronoi(points)
    

## More Information:

- [Home Page](http://github.com/karimbahgat/Pytess)
- [API Documentation](http://pythonhosted.org/Pytess)


## License:

This code is free to share, use, reuse,
and modify according to the MIT license, see license.txt


## Credits:

I just made it more convenient to use for end-users and uploaded it to PyPi.
The real credit goes to Bill Simons/Carson Farmer and Steven Fortune for
implementing the algorithm in the first place.

- Karim Bahgat
- Michael Currie

"""


__version__ = "1.0.0"


from .main import *


