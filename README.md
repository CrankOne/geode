# Geode

_Geode_ is a text processing engine providing access to detector geometry in
various computational applications of High-Energy Physics (HEP). It heavily
relies on GDML and exploits RESTful API for maintenance tasks.

## Features

* Combining multiple items (adsorbers, detectors, assemblies) into setups with
exhaustive parameterisation level: positions, rotations, replica numbers,
materials, etc may be changed by user's config defining setup.
* Support for custom GDML XSD schema extensions (e.g. sensitive detector class
bindings, tracking volumes, etc)
* Conversion of the GDML geometry into ROOT TGeo format, optionally preserving
any additional information (constants, variables, quatnities and various
extension attributes)
* Versatile setup configuration management routines via RESTful API

# Principles

Generally, the geometry library may be organized as a filesystem subtree with
set of GDML files corresponding to various detectors and _assemblies_. One may
find benefits of maintaing the library with one of popular VCS. By default,
specific _assembly_ is supposed to be a standalone GDML that Geant4 can read
directly -- that may simplify maintenance and development.

Access to the library is provided by interface implementation (see reference to
default `GeoLibrary` class), available for overriding. This way one may use
their own DB/artifact storages/whatsoever by implementing custom access
protocols.

_Geode_ provides a higher-level API to deal with _setups_. A _setup_ may be
assembled from multiple _assemblies_. Combining _assemblies_ into setup is done
automatically by the _Geode_, managing definition collisions.

## Configuration levels

Three levels of normalized config data are available:

1. `common` level is defined with `setting.yaml`
2. `setup` level is defined by particular setup
3. `client` level is submitted by client

The latter parameter overrides the former.

# Troubleshooting

## Segmentation Foults in LXML Python Module

The `lxml` package that we are using to parse and validate XML is one of the
most mature packages in Python ecosystem. However, it is known to have multiple
issues with memory management that is hard to trace and debug. In case you've
faced one, it most probably relates to some advanced features.

Typical traces of the lxml memory issues may appear themselves as following
abruption messages:

    double free or corruption (out)
    Aborted (core dumped)

We are working on collecting the problematic cases and hope to help the LXML
with patches. You may help us by providing minified XML fragments.

Unfortunately, currently there are not general recommendation to avoid this
kind of issues rather than circumvent some advanced XML constructions (e.g.
file `!ENTITY` may be replaced with direct emplacement of XML content). Also,
if you are working in virtual environment, consider using
`--system-site-packages` -- these bugs are known to be resolved this way at
least at some cases.

