import os
from setuptools import setup, find_packages

setup(
    name = "geode",
    version = "0.0.1",
    author = "Renat R. Dusaev",
    author_email = "crank@qcrypt.org",
    description = ("Geometry management for HEP."),
    license = "MIT",
    keywords = "physics geometry gdml",
    url = "https://github.com/CrankOne/geode",
    packages=[ 'geode'
             , 'geode.GDMLParser'
             , 'geode.GDMLParser.v3_1_6'
             ],
    package_data={ 'geode.GDMLParser.v3_1_6' : ['GDML_3_1_6/schema/*.xsd'] },
    classifiers=[
        "Development Status :: 1 - Planning",
    ]
)
