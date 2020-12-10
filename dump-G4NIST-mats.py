# -*- coding: utf8 -*-

# TODO: make the script more versatile, move the list of materials to import
# to configuration file or retrieve this list from somewhere whithin Geant4
# installation

from __future__ import print_function

import sys
from io import StringIO

if "__main__" == __name__:
    if len(sys.argv) != 2:
        sys.stderr.write( "Usage: %s <outfile>\n"%sys.argv[0] )
        exit()

# NOTE: we used to have the `NISTmaterials' object here to force initialization
# all the common NIST materials. This object comes with `g4py' package. However,
# the `g4py' package is (was) supported only with python v2. This project seems
# to be darmant and no longer under maintenance, so instead of calling the
# `NISTmaterials.Construct()' we rely on the manual initialization (see comment
# below).
#from g4py import NISTmaterials
import Geant4
from Geant4 import G4Material, gElementTable, gMaterialTable
from functools import reduce
import Geant4.hepunit as hepunit

#import geode.GDMLParser.v3_1_6.classes as GDML  # TODO: ARG
from geode.GDMLParser.v3_1_6.classes import MaterialMixtureType, \
                                MaterialIsotopeType, \
                                MaterialElementType, \
                                fractionType, \
                                AtomType, \
                                DensityType, \
                                RLType, ALType, TType, PType, MEEType

from geode.GDMLParser.v3_1_6.classes import gdml as gdmlClass
from geode.GDMLParser.v3_1_6.classes import defineType as definesClass
from geode.GDMLParser.v3_1_6.classes import materials as materialsClass
#from geode.GDMLParser.v3_1_6.classes import solids as solidsClass
#from geode.GDMLParser.v3_1_6.classes import structure as structureClass
#from geode.GDMLParser.v3_1_6.classes import setupType as setupClass

# See comment (NOTE) at the beginning of the script
#NISTmaterials.Construct()
nistMgr = Geant4.gNistManager.Instance()
a = map( nistMgr.FindOrBuildMaterial, [
        "G4_Al",
        "G4_Si",
        "G4_Ar",
        "G4_Cu",
        "G4_Fe",
        "G4_Ge",
        "G4_Ag",
        "G4_W",
        "G4_Au",
        "G4_Pb",
        "G4_AIR",
        "G4_THYMINE",
        "G4_Galactic",
        "G4_WATER",
        "G4_CESIUM_IODIDE",
        "G4_SODIUM_IODIDE",
        "G4_PLASTIC_SC_VINYLTOLUENE",
        "G4_MYLAR",
        "G4_PLEXIGLASS",
        "G4_KAPTON"
    ])
print(list(a))

# Translation between Geant4 enumeration and textual attribute tag
# description (see MaterialAttributeGroup's restriction )
gMatStatesDict = {
    Geant4.G4materials.G4State.kStateGas        : 'gas',
    Geant4.G4materials.G4State.kStateLiquid     : 'liquid',
    Geant4.G4materials.G4State.kStateSolid      : 'solid',
    Geant4.G4materials.G4State.kStateUndefined  : 'unknown'
}

def primitive_el_ctr( GDMLQName, toUnits=None, toUnitsStr=None,
                      encodedType=None ):
    CLASS = reduce(getattr, GDMLQName.split("."), sys.modules[__name__])
    def _construct_element( val ):
        return CLASS(
                    val/(toUnits),
                    unit=toUnitsStr,
                    type_=encodedType )
    return _construct_element

make_atom_el = primitive_el_ctr(
    'AtomType', hepunit.gram/hepunit.mole, 'g/mole', 'A' )
make_density_el = primitive_el_ctr(
    'DensityType', hepunit.gram/hepunit.cm3, 'g/cm3', 'density' )
make_radlen_el = primitive_el_ctr(
    'RLType', hepunit.cm, 'cm', 'X0' )
make_absorptlen_el = primitive_el_ctr(
    'ALType', hepunit.cm, 'cm', 'lambda' )
make_temperature_el = primitive_el_ctr(
    'TType', hepunit.kelvin, 'K', 'temperature' )
make_pressure_el = primitive_el_ctr(
    'PType', hepunit.pascal, 'pascal', 'pressure' )
make_meanexce_el = primitive_el_ctr(
    'MEEType', hepunit.eV, 'eV', 'excitationE' )

#
# Isotope:
def import_NIST_isotope( g4Iso, isotopesDict={}, quiet=False ):
    """
    Produces GDML node representation from G4MaterialIsotope instance.
    """
    if str(g4Iso.GetName()) in isotopesDict.keys():
        if not quiet:
            sys.stdout.write('Reentrant isotope %s.\n'%g4Iso.GetName())
        return isotopesDict[str(gIso.GetName())]
    #for m in dir( g4Iso ):
    #    print("      ", m)
    #GetIndex
    #GetIsotope
    #GetIsotopeTable
    #GetN                   N=None
    #GetName                name=None
    #GetNumberOfIsotopes
    #GetZ
    #Print
    #SetName
    ctrKWargs = {
        #'' : g4so.GetA(),      # relates to <atom/>
        #'' : g4Iso.GetIndex(), # position in the G4 table (may be ignored)
        'N' : g4Iso.GetN(),
        'name' : g4Iso.GetName(),
        'Z' : int(g4Iso.GetZ()),
    }
    # Unused:
    #   formula=None, state='unknown', property=None, RL=None,
    #   RLref=None, AL=None, ALref=None, T=None, Tref=None, P=None, Pref=None,
    #   MEE=None, MEEref=None, N=None, Z=None, D=None, Dref=None, atom=None
    isotope = MaterialIsotopeType( **ctrKWargs )
    isotope.set_atom( make_atom_el(g4Iso.GetA()) )
    if not quiet:
        sys.stdout.write( "<!-- == Exported isotope instance:" )
        isotope.export(sys.stdout, 0, name_='isotope')
        sys.stdout.write( "-->\n" )
    isotopesDict[str(g4Iso.GetName())] = isotope
    return isotope

#
# Element (fraction)
def import_NIST_element( g4El, elementsDict={},
                isotopesDict={}, quiet=False, **kwargs ):
    """
    Produces GDML node representation from G4MaterialElement instance.
    """
    if str(g4El.GetName()) in elementsDict.keys():
        if not quiet:
            sys.stdout.write('Reentrant element %s.\n'%g4El.GetName())
        return elementsDict[str(g4El.GetName())]
    # Available properties:
    #   GetName
    #   GetA
    #   GetAtomicShell
    #   GetIndex
    #   GetIonisation
    #   GetIsotope
    #   GetIsotopeVector
    #   GetN                        N=None
    #   GetNbOfAtomicShells
    #   GetNumberOfElements
    #   GetNumberOfIsotopes
    #   GetRelativeAbundanceVector
    #   GetSymbol                   formula=None
    #   GetZ                        Z=None
    #   GetfCoulomb
    #   GetfRadTsai()  # Somehow related to Halpin-Tsai formula?
    # Unused:
    #   state='unknown',
    #   property=None,
    #   RL=None,
    #   RLref=None,
    #   AL=None,
    #   ALref=None,
    #   T=None,
    #   Tref=None,
    #   P=None,
    #   Pref=None,
    #   MEE=None,   MEEref=None,    (Ionisation potential or Mean Excitation Energy)
    #   D=None, Dref=None,
    #   fraction=None
    ctrKWargs = {
           'name' : str(g4El.GetName()),
              'N' : g4El.GetN(),
              'Z' : g4El.GetZ(),
        'formula' : g4El.GetSymbol()
    }
    gdmlElNode = MaterialElementType( **ctrKWargs )
    #gdmlElNode.set_atom( make_atom_el( g4El.GetA() ) ) # TODO: do we need it here?
    #for pres in g4El.GetRelativeAbundanceVector():
    #    print( '## ', pres )  ## XXX
    iIdx = 0
    for iso in g4El.GetIsotopeVector():
        gdmlIsoObj = import_NIST_isotope( iso,
                                          isotopesDict=isotopesDict,
                                          quiet=quiet )
        gdmlFractionEl = fractionType( ref=gdmlIsoObj.get_name(),
                                       n=g4El.GetRelativeAbundanceVector()[iIdx] )
        gdmlElNode.add_fraction( gdmlFractionEl )
        iIdx += 1

    if not quiet:
        print("<!--\n=== Original G4Element:")
        g4El.Print()
        print("-->\n")
        gdmlElNode.export(sys.stdout, 0, name_='element')  # XXX
    elementsDict[str(g4El.GetName())] = gdmlElNode
    return gdmlElNode

def import_NIST_material( g4Mat, matsDict={}, elementsDict={},
                          isotopesDict={}, quiet=False ):
    if str(g4Mat.GetName()) in matsDict.keys():
        if not quiet:
            sys.stdout.write('Reentrant material %s.\n'%g4Mat.GetName())
        return matsDict[str(g4Mat.GetName())]
    # Available properties
    #   AddElement
    #   AddMaterial
    #   GetA
    #   GetAtomicNumDensityVector
    #   GetAtomsVector
    #   GetChemicalFormula              formula=None
    #   GetDensity
    #   GetElectronDensity
    #   GetElement
    #   GetElementVector
    #   GetFractionVector
    #   GetIndex
    #   GetIonisation                   MEE?
    #   GetMaterial
    #   GetMaterialPropertiesTable
    #   GetMaterialTable
    #   GetName                         name=None
    #   GetNuclearInterLength           AL
    #   GetNumberOfMaterials
    #   GetPressure                     P=None
    #   GetRadlen                       RL=None
    #   GetSandiaTable
    #   GetState                        state='unknown'
    #   GetTemperature                  T=None
    #   GetTotNbOfAtomsPerVolume
    #   GetTotNbOfElectPerVolume
    #   GetVecNbOfAtomsPerVolume
    #   GetZ                            Z=None
    #   Print
    #   SetChemicalFormula
    #   SetMaterialPropertiesTable
    #   SetName                         name=None
    # Unused:
    #   property=None,
    #   RLref=None              (directly specified)
    #   AL=None, ALref=None,    (TODO: absorption length/coeff, matters!)
    #   Tref=None,              (temperature directly specified)
    #   Pref=None,              (pressure)
    #   MEE=None, MEEref=None,  (TODO: Ionisation potential or Mean Excitation Energy)
    #   Z=None,
    #   D=None, Dref=None,
    #   atom=None,
    #   composite=None,
    #   fraction=None
    kwargs = {
           'name' : str(g4Mat.GetName()),
        'formula' : g4Mat.GetChemicalFormula(),
          'state' : gMatStatesDict.get( g4Mat.GetState(), 'undefined' ),
             #'RL' : g4Mat.GetRadlen(),  # TODO: units
              #'T' : g4Mat.GetTemperature(),
              #'P' : g4Mat.GetPressure(),
              #'Z' : g4Mat.GetZ()  # TODO: nonsense for mixtures
    }
    gdmlMatNode = MaterialMixtureType( **kwargs )
    
    iIdx = 0
    for el in g4Mat.GetElementVector():
        gdmlEl = import_NIST_element( el, elementsDict=elementsDict,
                            isotopesDict=isotopesDict, quiet=quiet )
        gdmlFractionEl = fractionType( ref=gdmlEl.get_name(),
                                         n=g4Mat.GetFractionVector()[iIdx] )
        gdmlMatNode.add_fraction( gdmlFractionEl )
        iIdx += 1
        #el.Print()

    gdmlMatNode.set_D(   make_density_el(       g4Mat.GetDensity()          ) )
    gdmlMatNode.set_RL(  make_radlen_el(        g4Mat.GetRadlen()           ) )
    gdmlMatNode.set_AL(  make_absorptlen_el(    g4Mat.GetNuclearInterLength()))
    gdmlMatNode.set_T(   make_temperature_el(   g4Mat.GetTemperature()      ) )
    gdmlMatNode.set_P(   make_pressure_el(      g4Mat.GetPressure()         ) )
    #gdmlMatNode.set_MEE( make_meanexce_el(      g4Mat.GetIonisation()      ) )

    if not quiet:
        sys.stdout.write("<!--\n=== Original material entity:\n")
        g4Mat.Print()
        sys.stdout.write("\n-->\n")
        gdmlMatNode.export(sys.stdout, 0, name_='material')  # XXX
    matsDict[str(g4Mat.GetName())] = gdmlMatNode
    return gdmlMatNode


def test_import():
    matsDict={}
    elementsDict={}
    isotopesDict={}
    air = G4Material.GetMaterial("G4_AIR")
    import_NIST_material( air, matsDict=matsDict,
                               elementsDict=elementsDict,
                               isotopesDict=isotopesDict,
                               quiet=True )
    for k, isotope in isotopesDict.iteritems():
        isotope.export( sys.stdout, 0, name_='isotope' )
    for k, element in elementsDict.iteritems():
        element.export( sys.stdout, 0, name_='element' )
    for k, mat in matsDict.iteritems():
        mat.export( sys.stdout, 0, name_='material' )

    sys.stdout.write( "<!-- Original material:\n" )
    air.Print()
    sys.stdout.flush()
    sys.stdout.write( "-->\n" )

#for el in gElementTable:

def import_all_NIST_materials( matLst=[], quiet=False ):
    n, nMat2bePrinted = 0, 1  # XXX
    for mat in gMaterialTable:
        import_NIST_material( mat, destLst=matLst, quiet=quiet )
        if not quiet:
            print("\n")
        n += 1  # XXX
        if n > nMat2bePrinted:  # XXX
            break  # XXX

#import_all_element_table( quiet=True )
#import_all_NIST_materials( quiet=False )

gMinimalGDMLStr = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE gdml>

<!-- This is an auto-generated GDML file indexing NIST materials database
     as they where found in Geant4 of version
     {GEANT4_VERSION_STR}
  -->

<gdml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd">
    <define/>
{NIST_MATERIALS_STR}

    <solids>
        <box name="solidBox" x="1" y="1" z="1" lunit="m"/>
    </solids>

    <structure>
        <volume name="NISTMatsWorld">
            <materialref ref="G4_AIR"/>
            <solidref ref="solidBox"></solidref>
        </volume>
    </structure>

    <setup name="Default" version="1">
        <world ref="NISTMatsWorld"/>
    </setup>
</gdml>
"""

if "__main__" == __name__:
    matsDict={}
    elementsDict={}
    isotopesDict={}
    for mat in gMaterialTable:
        import_NIST_material( mat, matsDict=matsDict,
                              elementsDict=elementsDict,
                              isotopesDict=isotopesDict,
                              quiet=True )
    root = gdmlClass()
    root.set_define( definesClass() )
    materials = materialsClass()

    print( "Isotopes to be imported (%d):"%len(isotopesDict.keys()) )
    for k in sorted(isotopesDict.keys()):
        print( " - ", k )
        materials.add_isotope( isotopesDict[k] )
        #isotopesDict[k].export(f, 0, name_='isotope')
        #isotopesDict[k].exportLiteral(sys.stdout, 0, name_='isotope')

    print( "Elements to be imported (%d):"%len(elementsDict.keys()) )
    for k in sorted(elementsDict.keys()):
        print( " - ", k )
        materials.add_element( elementsDict[k] )
        #elementsDict[k].export(f, 0, name_='element')

    print( "Materials to be imported (%d):"%len(matsDict.keys()) )
    for k in sorted(matsDict.keys()):
        print( " - ", k )
        materials.add_material( matsDict[k] )
        #matsDict[k].export(f, 0, name_='material')

    tio = StringIO()
    materials.export( tio, 1, name_='materials' )
    with open( sys.argv[1], 'w' ) as f:
        f.write( gMinimalGDMLStr.format( **{
                'GEANT4_VERSION_STR' : Geant4.G4Version,
                'NIST_MATERIALS_STR' : tio.getvalue() } ) )

