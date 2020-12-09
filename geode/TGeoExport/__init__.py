import os
import ROOT
#ROOT.TGeoMaterial.__init__._creates = False  # Get.
#ROOT.TGeoMedium.__init__._creates   = False  # The fuck.
#ROOT.TGeoElement.__init__._creates  = False  # Off!
#ROOT.TGeoVolume.__init__._creates  = False  # Off!

#
# Load the common C-definitions via CINT:
ROOT.gROOT.SetMacroPath( ROOT.gROOT.GetMacroPath() \
                    + os.path.dirname(__file__) \
                    + '/../..' )
ROOT.gROOT.LoadMacro("structs.C")
# ^^^NOTE: ROOT may silently fail to load the definitions, causing fatal issues
# rendering GDML -> TGeo.
# TODO: consider instead:
#ROOT.gInterpreter.Declare("""
#class A {};
#void foo(A* a) {}
#""")

#
# Initialize damn manager:
#ROOT.gGeoManager.SetVerboseLevel( 0 if quiet else 1 )
if not ROOT.gGeoManager:
    ROOT.gROOT.ProcessLine('GeoManager = new TGeoManager("geo", '
                           '"Imported GDML geometry.")')

# Initialize default materials database:
ROOT.gGeoManager.BuildDefaultMaterials()

# NOTE: according to
# https://root.cern.ch/root/html534/guides/users-guide/Geometry.html#units
# the system of units used in TGeo:
#    - length: cm                                (vs mm, default for G4)
#    - angle: degrees                            (same)
#    - density: g/cm3                            (same)
#    - atomic mass is expressed in u (Da, emu)   (same)
# Note: deprecated, see issue #159
SystemOfUnits = {
    "meter"         : 1e+2,
    "kilogram"      : 1e+3,
    "second"        : 1,
    "density"       : 1,
    "ampere"        : 1,
    "kelvin"        : 1.0,
    "mole"          : 1.0,
    "candela"       : 1.0
}

#def open_ROOT_output_file( filename, inMemory=False ):
#    inst = None
#    if inMemory:
#        inst = ROOT.TMemFile(filename, 'recreate')
#    else:
#        inst = ROOT.TFile(filename, 'recreate')
#    ROOT.gFile = inst
#    return inst

#    f = None
#    if outFilePath:
#        f = ROOT.TFile(outFilePath, 'recreate')

