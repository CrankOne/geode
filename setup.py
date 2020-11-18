import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "geode",
    version = "0.0.1",
    author = "Renat R. Dusaev",
    author_email = "crank@qcrypt.org",
    description = ("Geometry management for HEP."),
    license = "MIT",
    keywords = "physics geometry gdml",
    url = "https://github.com/CrankOne/geode",
    packages=['geode', 'geode.GDMLParser', 'geode.GDMLParser.v3_1_6'],
    #package_dir={ 'geode': 'geode' },
    package_data={ 'geode.GDMLParser.v3_1_6' : ['GDML_3_1_6/schema/*.xsd'] },
    #long_description=read('README'),
    #classifiers=[
    #    "Development Status :: 3 - Alpha",
    #    "Topic :: Utilities",
    #    "License :: OSI Approved :: MIT License",
    #],
    classifiers=[
        "Development Status :: 1 - Planning",
    ]
)
