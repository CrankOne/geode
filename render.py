# -*- coding: utf-8 -*-
"""
A Geode's geometry preprocessor util. Expects input to be in form of a YAML
document describing various geometrical entities from the library. Input will
be parsed with geometry entities applied and output GDML or ROOT::TGeo will
be written w.r.t. output arguments.
"""

import os
import logging
import logging.config

logging.config.fileConfig( fname='logging.ini'
                         #, disable_existing_loggers=False
                         )

import sys
import yaml, json
import argparse
import importlib
from geode.library import Library as GDMLLibrary
from geode.export import build_root_GDML
from geode.export import export as geode_export
from geode.defs import DefinitionsIndex as GDMLDefinitions
import geode.nist_mats_export

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True  # suppress default ROOT option parser

def main(args):
    L = logging.getLogger(__name__)
    # Read the YAML definitions
    detectors = yaml.load(args.inputConfig, Loader=yaml.FullLoader)
    # Print the parsed geometry definitions, if need
    if args.dump_placements_json:
        sys.stdout.write(json.dumps(detectors, indent=2))
    # Read the geometry library
    lib = GDMLLibrary()
    lib.import_fs_subtree(args.geomlib)

    if args.list_lib_items:
        sys.stdout.write( 'Items read from library "%s":\n'%args.geomlib )
        for k in lib.items.keys():
            sys.stdout.write('  * %s\n'%('/'.join(k)))
    oFormat = args.output_format
    if oFormat is None:
        if args.output.name.endswith('.gdml'):
            oFormat = 'gdml'
        elif args.output.name.endswith('.root'):
            oFormat = 'TGeo'
        else:
            raise RuntimeError('No output file format specified.')
    # Resolve files relatively to the output file
    file_resolver = None
    if args.output is not sys.stdout:  # TODO or any other stream
        oDir = args.base_dir if args.base_dir else os.path.dirname(args.output.name)
        file_resolver = lambda item, geoPath, entryName, cfgParameters: os.path.relpath( item['file'], oDir )
    # Make the new GDML document
    gdmlRoot = build_root_GDML( detectors['assemblies'].items()
                              , lib
                              , worldVol={ 'x': 1, 'y':1, 'z':2, 'lunit':'m' }  # TODO: world size?
                              , file_resolver=file_resolver
                              )
    if 'gdml' == oFormat:
        # The GDML output format can be accomplished directly from LXML ETREE,
        # only the common XML header must be typed beforehead
        args.output.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE gdml>\n')
        gdmlRoot.export( args.output, 0, name_='gdml' )
    else:
        # Instantiate definitions index
        defs = GDMLDefinitions()
        # If Geant4 NIST materials enabled, lookup for the `G4_*' material
        # references within a parsed data
        if not args.disable_G4NIST_materials:
            mats = geode.nist_mats_export.find_refs(gdmlRoot, lib)
            geode.nist_mats_export.inject(gdmlRoot, mats)
        # Export
        geode_export( gdmlRoot
                    , defs
                    , exportFormat=oFormat )

if "__main__" == __name__:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument( 'inputConfig', help='Input YAML file describing the'
            ' items and their placements. Use "-" for `stdin\'.'
            , type=argparse.FileType('r')
            )
    p.add_argument( '-g', '--geomlib', help='Root dir of the geometry library to'
            ' use.'
            , default='specs/geomlib' )
    p.add_argument( '--dump-placements-json', help='When given, the parsed'
            ' input will be printed to `stdout\' as JSON. Useful for assurance'
            ' tests in some sophisticated cases with complex alias/anchor YAML'
            ' syntax.'
            , action='store_true' )
    p.add_argument( '-b', '--base-dir', help="Directory considered as a current"
            " for \"name\" attricbute for GDML <file/> tag (used with GDML"
            " output). If not specified, paths will be relative to the output"
            " file location.")
    p.add_argument( '-l', '--list-lib-items', help='When given, the list of'
            ' items discovered in library will be printed to stdout.'
            , action='store_true' )
    p.add_argument( '-o', '--output', help='File for the output. Set to "-" to'
            ' use `stdout\'.'
            , type=argparse.FileType('w')
            , default='-' )
    p.add_argument( '-f', '--output-format', help='Format of the output'
            ' geometry. Currently, only "gdml" and "TGeo" are available for'
            ' GDML and ROOT::TGeo formats. If not specified explicitly, format'
            ' will be assumed by output file\'s suffix, if possible.'
            , choices=['gdml', 'TGeo']  # NOTE: must correspond to one of the *Export in geode/ dir
            )
    p.add_argument( '--disable-G4NIST-materials', help='If provided, none'
            ' of the NIST materials will be converted to explicit definitions'
            ' within the output.'
            , action='store_true' )
    args = p.parse_args()
    main(args)
