try: from setuptools import setup
except: from distutils.core import setup

setup(	long_description=open("README.rst").read(), 
	name="""Pytess""",
	license="""MIT""",
	author="""Karim Bahgat""",
	author_email="""karim.bahgat.norway@gmail.com""",
	url="""http://github.com/karimbahgat/Pytess""",
	package_data={'pytess': ['.\\.DS_Store']},
	version="""0.1.1""",
	keywords="""GIS spatial tesselation voronoi delauney triangulation""",
	packages=['pytess'],
	classifiers=['License :: OSI Approved', 'Programming Language :: Python', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Intended Audience :: End Users/Desktop', 'Topic :: Scientific/Engineering :: GIS'],
	description="""Pure Python tessellation of points into polygons, including Delauney/Thiessin, and Voronoi polygons.""",
	)
