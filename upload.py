import pipy
 
packpath = "pytess"
pipy.define_upload(packpath,
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
                   changes=["Bump to stable version",
                            "Python 3.x compatibility"]
                   )

pipy.generate_docs(packpath)
#pipy.upload_test(packpath)
#pipy.upload(packpath)

