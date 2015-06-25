import pypi
 
packpath = "pytess"
pypi.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="Pytess",
                   description="Pure Python tessellation of points into polygons, including Delauney/Thiessin, and Voronoi polygons.",
                   url="http://github.com/karimbahgat/Pytess",
                   keywords="GIS spatial tesselation voronoi delauney triangulation",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 4 - Beta",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop',
                                "Topic :: Scientific/Engineering :: GIS"],
                   changes=["First pypi release"]
                   )

pypi.generate_docs(packpath)
#pypi.upload_test(packpath)
#pypi.upload(packpath)

