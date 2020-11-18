#!/usr/bin/env python

#
# Generated Wed Nov 18 09:47:08 2020 by generateDS.py version 2.37.1.
# Python 3.7.8 (default, Aug 15 2020, 19:20:38)  [GCC 9.3.0]
#
# Command line options:
#   ('-m', '')
#   ('-f', '')
#   ('-o', 'classes.py')
#   ('--export', 'write literal etree')
#   ('--root-element', 'gdml')
#   ('-s', 'subclasses.py')
#
# Command line arguments:
#   GDML_3_1_6/schema/gdml.xsd
#
# Command line:
#   /var/src/.venv/bin/generateDS.py -m -f -o "classes.py" --export="write literal etree" --root-element="gdml" -s "subclasses.py" GDML_3_1_6/schema/gdml.xsd
#
# Current working directory (os.getcwd()):
#   v3_1_6
#

import os
import sys
from lxml import etree as etree_

import ??? as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True

#
# Data representation classes
#


class IdentifiableVolumeTypeSub(supermod.IdentifiableVolumeType):
    def __init__(self, name=None, extensiontype_=None, **kwargs_):
        super(IdentifiableVolumeTypeSub, self).__init__(name, extensiontype_,  **kwargs_)
supermod.IdentifiableVolumeType.subclass = IdentifiableVolumeTypeSub
# end class IdentifiableVolumeTypeSub


class SinglePlacementTypeSub(supermod.SinglePlacementType):
    def __init__(self, name=None, copynumber=None, file=None, volumeref=None, position=None, positionref=None, rotation=None, rotationref=None, scale=None, scaleref=None, **kwargs_):
        super(SinglePlacementTypeSub, self).__init__(name, copynumber, file, volumeref, position, positionref, rotation, rotationref, scale, scaleref,  **kwargs_)
supermod.SinglePlacementType.subclass = SinglePlacementTypeSub
# end class SinglePlacementTypeSub


class DivisionPlacementTypeSub(supermod.DivisionPlacementType):
    def __init__(self, axis=None, number=None, width=None, offset=None, unit='mm', volumeref=None, **kwargs_):
        super(DivisionPlacementTypeSub, self).__init__(axis, number, width, offset, unit, volumeref,  **kwargs_)
supermod.DivisionPlacementType.subclass = DivisionPlacementTypeSub
# end class DivisionPlacementTypeSub


class VolumeTypeSub(supermod.VolumeType):
    def __init__(self, name=None, materialref=None, solidref=None, physvol=None, divisionvol=None, replicavol=None, paramvol=None, loop=None, auxiliary=None, **kwargs_):
        super(VolumeTypeSub, self).__init__(name, materialref, solidref, physvol, divisionvol, replicavol, paramvol, loop, auxiliary,  **kwargs_)
supermod.VolumeType.subclass = VolumeTypeSub
# end class VolumeTypeSub


class AssemblyVolumeTypeSub(supermod.AssemblyVolumeType):
    def __init__(self, name=None, physvol=None, replicavol=None, paramvol=None, **kwargs_):
        super(AssemblyVolumeTypeSub, self).__init__(name, physvol, replicavol, paramvol,  **kwargs_)
supermod.AssemblyVolumeType.subclass = AssemblyVolumeTypeSub
# end class AssemblyVolumeTypeSub


class LogicalSurfaceTypeSub(supermod.LogicalSurfaceType):
    def __init__(self, name=None, surfaceproperty=None, extensiontype_=None, **kwargs_):
        super(LogicalSurfaceTypeSub, self).__init__(name, surfaceproperty, extensiontype_,  **kwargs_)
supermod.LogicalSurfaceType.subclass = LogicalSurfaceTypeSub
# end class LogicalSurfaceTypeSub


class bordersurfaceSub(supermod.bordersurface):
    def __init__(self, name=None, surfaceproperty=None, physvolref=None, **kwargs_):
        super(bordersurfaceSub, self).__init__(name, surfaceproperty, physvolref,  **kwargs_)
supermod.bordersurface.subclass = bordersurfaceSub
# end class bordersurfaceSub


class skinsurfaceSub(supermod.skinsurface):
    def __init__(self, name=None, surfaceproperty=None, volumeref=None, **kwargs_):
        super(skinsurfaceSub, self).__init__(name, surfaceproperty, volumeref,  **kwargs_)
supermod.skinsurface.subclass = skinsurfaceSub
# end class skinsurfaceSub


class structureSub(supermod.structure):
    def __init__(self, volume=None, assembly=None, loop=None, ParameterisationAlgorithm=None, Surface=None, **kwargs_):
        super(structureSub, self).__init__(volume, assembly, loop, ParameterisationAlgorithm, Surface,  **kwargs_)
supermod.structure.subclass = structureSub
# end class structureSub


class gdmlSub(supermod.gdml):
    def __init__(self, version='3.1.6', define=None, materials=None, solids=None, structure=None, userinfo=None, setup=None, **kwargs_):
        super(gdmlSub, self).__init__(version, define, materials, solids, structure, userinfo, setup,  **kwargs_)
supermod.gdml.subclass = gdmlSub
# end class gdmlSub


class IdentifiableExpressionTypeSub(supermod.IdentifiableExpressionType):
    def __init__(self, name=None, valueOf_=None, **kwargs_):
        super(IdentifiableExpressionTypeSub, self).__init__(name, valueOf_,  **kwargs_)
supermod.IdentifiableExpressionType.subclass = IdentifiableExpressionTypeSub
# end class IdentifiableExpressionTypeSub


class ConstantTypeSub(supermod.ConstantType):
    def __init__(self, value=None, extensiontype_=None, **kwargs_):
        super(ConstantTypeSub, self).__init__(value, extensiontype_,  **kwargs_)
supermod.ConstantType.subclass = ConstantTypeSub
# end class ConstantTypeSub


class VariableTypeSub(supermod.VariableType):
    def __init__(self, value=None, extensiontype_=None, **kwargs_):
        super(VariableTypeSub, self).__init__(value, extensiontype_,  **kwargs_)
supermod.VariableType.subclass = VariableTypeSub
# end class VariableTypeSub


class IdentifiableConstantTypeSub(supermod.IdentifiableConstantType):
    def __init__(self, value=None, name=None, **kwargs_):
        super(IdentifiableConstantTypeSub, self).__init__(value, name,  **kwargs_)
supermod.IdentifiableConstantType.subclass = IdentifiableConstantTypeSub
# end class IdentifiableConstantTypeSub


class IdentifiableVariableTypeSub(supermod.IdentifiableVariableType):
    def __init__(self, value=None, name=None, **kwargs_):
        super(IdentifiableVariableTypeSub, self).__init__(value, name,  **kwargs_)
supermod.IdentifiableVariableType.subclass = IdentifiableVariableTypeSub
# end class IdentifiableVariableTypeSub


class QuantityTypeSub(supermod.QuantityType):
    def __init__(self, value=None, unit=None, type_=None, extensiontype_=None, **kwargs_):
        super(QuantityTypeSub, self).__init__(value, unit, type_, extensiontype_,  **kwargs_)
supermod.QuantityType.subclass = QuantityTypeSub
# end class QuantityTypeSub


class IdentifiableQuantityTypeSub(supermod.IdentifiableQuantityType):
    def __init__(self, value=None, unit=None, type_=None, name=None, **kwargs_):
        super(IdentifiableQuantityTypeSub, self).__init__(value, unit, type_, name,  **kwargs_)
supermod.IdentifiableQuantityType.subclass = IdentifiableQuantityTypeSub
# end class IdentifiableQuantityTypeSub


class ThreeVectorTypeSub(supermod.ThreeVectorType):
    def __init__(self, x='0.0', y='0.0', z='0.0', extensiontype_=None, **kwargs_):
        super(ThreeVectorTypeSub, self).__init__(x, y, z, extensiontype_,  **kwargs_)
supermod.ThreeVectorType.subclass = ThreeVectorTypeSub
# end class ThreeVectorTypeSub


class MatrixTypeSub(supermod.MatrixType):
    def __init__(self, name=None, coldim=None, values=None, **kwargs_):
        super(MatrixTypeSub, self).__init__(name, coldim, values,  **kwargs_)
supermod.MatrixType.subclass = MatrixTypeSub
# end class MatrixTypeSub


class IdentifiableThreeVectorTypeSub(supermod.IdentifiableThreeVectorType):
    def __init__(self, x='0.0', y='0.0', z='0.0', name=None, **kwargs_):
        super(IdentifiableThreeVectorTypeSub, self).__init__(x, y, z, name,  **kwargs_)
supermod.IdentifiableThreeVectorType.subclass = IdentifiableThreeVectorTypeSub
# end class IdentifiableThreeVectorTypeSub


class QuantityVectorTypeSub(supermod.QuantityVectorType):
    def __init__(self, x='0.0', y='0.0', z='0.0', unit=None, type_=None, extensiontype_=None, **kwargs_):
        super(QuantityVectorTypeSub, self).__init__(x, y, z, unit, type_, extensiontype_,  **kwargs_)
supermod.QuantityVectorType.subclass = QuantityVectorTypeSub
# end class QuantityVectorTypeSub


class IdentifiableQuantityVectorTypeSub(supermod.IdentifiableQuantityVectorType):
    def __init__(self, x='0.0', y='0.0', z='0.0', unit=None, type_=None, name=None, **kwargs_):
        super(IdentifiableQuantityVectorTypeSub, self).__init__(x, y, z, unit, type_, name,  **kwargs_)
supermod.IdentifiableQuantityVectorType.subclass = IdentifiableQuantityVectorTypeSub
# end class IdentifiableQuantityVectorTypeSub


class ReferenceTypeSub(supermod.ReferenceType):
    def __init__(self, ref=None, extensiontype_=None, **kwargs_):
        super(ReferenceTypeSub, self).__init__(ref, extensiontype_,  **kwargs_)
supermod.ReferenceType.subclass = ReferenceTypeSub
# end class ReferenceTypeSub


class FileReferenceTypeSub(supermod.FileReferenceType):
    def __init__(self, name=None, volname=None, **kwargs_):
        super(FileReferenceTypeSub, self).__init__(name, volname,  **kwargs_)
supermod.FileReferenceType.subclass = FileReferenceTypeSub
# end class FileReferenceTypeSub


class ReferenceListTypeSub(supermod.ReferenceListType):
    def __init__(self, refs=None, **kwargs_):
        super(ReferenceListTypeSub, self).__init__(refs,  **kwargs_)
supermod.ReferenceListType.subclass = ReferenceListTypeSub
# end class ReferenceListTypeSub


class AuxiliaryTypeSub(supermod.AuxiliaryType):
    def __init__(self, auxtype=None, auxvalue=None, auxunit=None, auxiliary=None, **kwargs_):
        super(AuxiliaryTypeSub, self).__init__(auxtype, auxvalue, auxunit, auxiliary,  **kwargs_)
supermod.AuxiliaryType.subclass = AuxiliaryTypeSub
# end class AuxiliaryTypeSub


class defineTypeSub(supermod.defineType):
    def __init__(self, loop=None, constant=None, variable=None, matrix=None, quantity=None, expression=None, position=None, rotation=None, scale=None, **kwargs_):
        super(defineTypeSub, self).__init__(loop, constant, variable, matrix, quantity, expression, position, rotation, scale,  **kwargs_)
supermod.defineType.subclass = defineTypeSub
# end class defineTypeSub


class positionTypeSub(supermod.positionType):
    def __init__(self, x='0.0', y='0.0', z='0.0', unit=None, type_=None, name=None, **kwargs_):
        super(positionTypeSub, self).__init__(x, y, z, unit, type_, name,  **kwargs_)
supermod.positionType.subclass = positionTypeSub
# end class positionTypeSub


class rotationTypeSub(supermod.rotationType):
    def __init__(self, x='0.0', y='0.0', z='0.0', unit=None, type_=None, name=None, **kwargs_):
        super(rotationTypeSub, self).__init__(x, y, z, unit, type_, name,  **kwargs_)
supermod.rotationType.subclass = rotationTypeSub
# end class rotationTypeSub


class scaleTypeSub(supermod.scaleType):
    def __init__(self, x='0.0', y='0.0', z='0.0', unit=None, type_=None, name=None, **kwargs_):
        super(scaleTypeSub, self).__init__(x, y, z, unit, type_, name,  **kwargs_)
supermod.scaleType.subclass = scaleTypeSub
# end class scaleTypeSub


class loopSub(supermod.loop):
    def __init__(self, for_=None, from_=None, to=None, step=None, Solid=None, volume=None, physvol=None, loop_member=None, **kwargs_):
        super(loopSub, self).__init__(for_, from_, to, step, Solid, volume, physvol, loop_member,  **kwargs_)
supermod.loop.subclass = loopSub
# end class loopSub


class AtomTypeSub(supermod.AtomType):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(AtomTypeSub, self).__init__(value, unit, type_,  **kwargs_)
supermod.AtomType.subclass = AtomTypeSub
# end class AtomTypeSub


class DensityTypeSub(supermod.DensityType):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(DensityTypeSub, self).__init__(value, unit, type_,  **kwargs_)
supermod.DensityType.subclass = DensityTypeSub
# end class DensityTypeSub


class MaterialTypeSub(supermod.MaterialType):
    def __init__(self, name=None, formula=None, state='unknown', property=None, RL=None, RLref=None, AL=None, ALref=None, T=None, Tref=None, P=None, Pref=None, MEE=None, MEEref=None, extensiontype_=None, **kwargs_):
        super(MaterialTypeSub, self).__init__(name, formula, state, property, RL, RLref, AL, ALref, T, Tref, P, Pref, MEE, MEEref, extensiontype_,  **kwargs_)
supermod.MaterialType.subclass = MaterialTypeSub
# end class MaterialTypeSub


class materialsSub(supermod.materials):
    def __init__(self, loop=None, define=None, isotope=None, element=None, material=None, **kwargs_):
        super(materialsSub, self).__init__(loop, define, isotope, element, material,  **kwargs_)
supermod.materials.subclass = materialsSub
# end class materialsSub


class MaterialIsotopeTypeSub(supermod.MaterialIsotopeType):
    def __init__(self, name=None, formula=None, state='unknown', property=None, RL=None, RLref=None, AL=None, ALref=None, T=None, Tref=None, P=None, Pref=None, MEE=None, MEEref=None, N=None, Z=None, D=None, Dref=None, atom=None, **kwargs_):
        super(MaterialIsotopeTypeSub, self).__init__(name, formula, state, property, RL, RLref, AL, ALref, T, Tref, P, Pref, MEE, MEEref, N, Z, D, Dref, atom,  **kwargs_)
supermod.MaterialIsotopeType.subclass = MaterialIsotopeTypeSub
# end class MaterialIsotopeTypeSub


class MaterialElementTypeSub(supermod.MaterialElementType):
    def __init__(self, name=None, formula=None, state='unknown', property=None, RL=None, RLref=None, AL=None, ALref=None, T=None, Tref=None, P=None, Pref=None, MEE=None, MEEref=None, N=None, Z=None, D=None, Dref=None, atom=None, fraction=None, **kwargs_):
        super(MaterialElementTypeSub, self).__init__(name, formula, state, property, RL, RLref, AL, ALref, T, Tref, P, Pref, MEE, MEEref, N, Z, D, Dref, atom, fraction,  **kwargs_)
supermod.MaterialElementType.subclass = MaterialElementTypeSub
# end class MaterialElementTypeSub


class MaterialMixtureTypeSub(supermod.MaterialMixtureType):
    def __init__(self, name=None, formula=None, state='unknown', property=None, RL=None, RLref=None, AL=None, ALref=None, T=None, Tref=None, P=None, Pref=None, MEE=None, MEEref=None, Z=None, D=None, Dref=None, atom=None, composite=None, fraction=None, **kwargs_):
        super(MaterialMixtureTypeSub, self).__init__(name, formula, state, property, RL, RLref, AL, ALref, T, Tref, P, Pref, MEE, MEEref, Z, D, Dref, atom, composite, fraction,  **kwargs_)
supermod.MaterialMixtureType.subclass = MaterialMixtureTypeSub
# end class MaterialMixtureTypeSub


class SolidTypeSub(supermod.SolidType):
    def __init__(self, lunit='mm', aunit='radian', name=None, extensiontype_=None, **kwargs_):
        super(SolidTypeSub, self).__init__(lunit, aunit, name, extensiontype_,  **kwargs_)
supermod.SolidType.subclass = SolidTypeSub
# end class SolidTypeSub


class BooleanSolidTypeSub(supermod.BooleanSolidType):
    def __init__(self, lunit='mm', aunit='radian', name=None, first=None, second=None, position=None, positionref=None, rotation=None, rotationref=None, firstposition=None, firstpositionref=None, firstrotation=None, firstrotationref=None, **kwargs_):
        super(BooleanSolidTypeSub, self).__init__(lunit, aunit, name, first, second, position, positionref, rotation, rotationref, firstposition, firstpositionref, firstrotation, firstrotationref,  **kwargs_)
supermod.BooleanSolidType.subclass = BooleanSolidTypeSub
# end class BooleanSolidTypeSub


class multiUnionNodeSub(supermod.multiUnionNode):
    def __init__(self, lunit='mm', aunit='radian', name=None, solid=None, position=None, positionref=None, rotation=None, rotationref=None, **kwargs_):
        super(multiUnionNodeSub, self).__init__(lunit, aunit, name, solid, position, positionref, rotation, rotationref,  **kwargs_)
supermod.multiUnionNode.subclass = multiUnionNodeSub
# end class multiUnionNodeSub


class multiUnionSub(supermod.multiUnion):
    def __init__(self, lunit='mm', aunit='radian', name=None, multiUnionNode=None, **kwargs_):
        super(multiUnionSub, self).__init__(lunit, aunit, name, multiUnionNode,  **kwargs_)
supermod.multiUnion.subclass = multiUnionSub
# end class multiUnionSub


class reflectedSolidSub(supermod.reflectedSolid):
    def __init__(self, lunit='mm', aunit='radian', name=None, solid=None, sx='1.0', sy='1.0', sz='1.0', rx='0.0', ry='0.0', rz='0.0', dx='0.0', dy='0.0', dz='0.0', **kwargs_):
        super(reflectedSolidSub, self).__init__(lunit, aunit, name, solid, sx, sy, sz, rx, ry, rz, dx, dy, dz,  **kwargs_)
supermod.reflectedSolid.subclass = reflectedSolidSub
# end class reflectedSolidSub


class scaledSolidSub(supermod.scaledSolid):
    def __init__(self, lunit='mm', aunit='radian', name=None, solidref=None, scale=None, scaleref=None, **kwargs_):
        super(scaledSolidSub, self).__init__(lunit, aunit, name, solidref, scale, scaleref,  **kwargs_)
supermod.scaledSolid.subclass = scaledSolidSub
# end class scaledSolidSub


class SurfacePropertyTypeSub(supermod.SurfacePropertyType):
    def __init__(self, name=None, type_='dielectric_dielectric', property=None, extensiontype_=None, **kwargs_):
        super(SurfacePropertyTypeSub, self).__init__(name, type_, property, extensiontype_,  **kwargs_)
supermod.SurfacePropertyType.subclass = SurfacePropertyTypeSub
# end class SurfacePropertyTypeSub


class solidsSub(supermod.solids):
    def __init__(self, define=None, Solid=None, SurfaceProperty=None, loop=None, **kwargs_):
        super(solidsSub, self).__init__(define, Solid, SurfaceProperty, loop,  **kwargs_)
supermod.solids.subclass = solidsSub
# end class solidsSub


class boxSub(supermod.box):
    def __init__(self, lunit='mm', aunit='radian', name=None, x=None, y=None, z=None, **kwargs_):
        super(boxSub, self).__init__(lunit, aunit, name, x, y, z,  **kwargs_)
supermod.box.subclass = boxSub
# end class boxSub


class twistedboxSub(supermod.twistedbox):
    def __init__(self, lunit='mm', aunit='radian', name=None, x=None, y=None, z=None, PhiTwist=None, **kwargs_):
        super(twistedboxSub, self).__init__(lunit, aunit, name, x, y, z, PhiTwist,  **kwargs_)
supermod.twistedbox.subclass = twistedboxSub
# end class twistedboxSub


class twistedtrapSub(supermod.twistedtrap):
    def __init__(self, lunit='mm', aunit='radian', name=None, PhiTwist=None, z=None, Theta=None, Phi=None, y1=None, x1=None, y2=None, x2=None, x3=None, x4=None, Alph=None, **kwargs_):
        super(twistedtrapSub, self).__init__(lunit, aunit, name, PhiTwist, z, Theta, Phi, y1, x1, y2, x2, x3, x4, Alph,  **kwargs_)
supermod.twistedtrap.subclass = twistedtrapSub
# end class twistedtrapSub


class twistedtrdSub(supermod.twistedtrd):
    def __init__(self, lunit='mm', aunit='radian', name=None, PhiTwist=None, z=None, y1=None, x1=None, y2=None, x2=None, **kwargs_):
        super(twistedtrdSub, self).__init__(lunit, aunit, name, PhiTwist, z, y1, x1, y2, x2,  **kwargs_)
supermod.twistedtrd.subclass = twistedtrdSub
# end class twistedtrdSub


class paraboloidSub(supermod.paraboloid):
    def __init__(self, lunit='mm', aunit='radian', name=None, rlo=None, rhi=None, dz=None, **kwargs_):
        super(paraboloidSub, self).__init__(lunit, aunit, name, rlo, rhi, dz,  **kwargs_)
supermod.paraboloid.subclass = paraboloidSub
# end class paraboloidSub


class sphereSub(supermod.sphere):
    def __init__(self, lunit='mm', aunit='radian', name=None, rmin='0.0', rmax=None, startphi='0.0', deltaphi=None, starttheta='0.0', deltatheta=None, **kwargs_):
        super(sphereSub, self).__init__(lunit, aunit, name, rmin, rmax, startphi, deltaphi, starttheta, deltatheta,  **kwargs_)
supermod.sphere.subclass = sphereSub
# end class sphereSub


class ellipsoidSub(supermod.ellipsoid):
    def __init__(self, lunit='mm', aunit='radian', name=None, ax=None, by=None, cz=None, zcut1='-1000000.0', zcut2='1000000.0', **kwargs_):
        super(ellipsoidSub, self).__init__(lunit, aunit, name, ax, by, cz, zcut1, zcut2,  **kwargs_)
supermod.ellipsoid.subclass = ellipsoidSub
# end class ellipsoidSub


class tubeSub(supermod.tube):
    def __init__(self, lunit='mm', aunit='radian', name=None, z=None, rmin='0.0', rmax=None, startphi='0.0', deltaphi=None, **kwargs_):
        super(tubeSub, self).__init__(lunit, aunit, name, z, rmin, rmax, startphi, deltaphi,  **kwargs_)
supermod.tube.subclass = tubeSub
# end class tubeSub


class twistedtubsSub(supermod.twistedtubs):
    def __init__(self, lunit='mm', aunit='radian', name=None, twistedangle=None, endinnerrad='0.0', endouterrad='0.0', midinnerrad='0.0', midouterrad='0.0', negativeEndz='0.0', positiveEndz='0.0', zlen='0.0', nseg='0', totphi='0.0', phi='0.0', **kwargs_):
        super(twistedtubsSub, self).__init__(lunit, aunit, name, twistedangle, endinnerrad, endouterrad, midinnerrad, midouterrad, negativeEndz, positiveEndz, zlen, nseg, totphi, phi,  **kwargs_)
supermod.twistedtubs.subclass = twistedtubsSub
# end class twistedtubsSub


class cutTubeSub(supermod.cutTube):
    def __init__(self, lunit='mm', aunit='radian', name=None, z=None, rmin='0.0', rmax=None, startphi='0.0', deltaphi=None, lowX=None, lowY=None, lowZ=None, highX=None, highY=None, highZ=None, **kwargs_):
        super(cutTubeSub, self).__init__(lunit, aunit, name, z, rmin, rmax, startphi, deltaphi, lowX, lowY, lowZ, highX, highY, highZ,  **kwargs_)
supermod.cutTube.subclass = cutTubeSub
# end class cutTubeSub


class coneSub(supermod.cone):
    def __init__(self, lunit='mm', aunit='radian', name=None, z=None, rmin1='0.0', rmin2='0.0', rmax1=None, rmax2=None, startphi='0.0', deltaphi=None, **kwargs_):
        super(coneSub, self).__init__(lunit, aunit, name, z, rmin1, rmin2, rmax1, rmax2, startphi, deltaphi,  **kwargs_)
supermod.cone.subclass = coneSub
# end class coneSub


class elconeSub(supermod.elcone):
    def __init__(self, lunit='mm', aunit='radian', name=None, dx=None, dy=None, zmax=None, zcut=None, **kwargs_):
        super(elconeSub, self).__init__(lunit, aunit, name, dx, dy, zmax, zcut,  **kwargs_)
supermod.elcone.subclass = elconeSub
# end class elconeSub


class polyconeSub(supermod.polycone):
    def __init__(self, lunit='mm', aunit='radian', name=None, deltaphi=None, startphi='0.0', zplane=None, **kwargs_):
        super(polyconeSub, self).__init__(lunit, aunit, name, deltaphi, startphi, zplane,  **kwargs_)
supermod.polycone.subclass = polyconeSub
# end class polyconeSub


class ZPlaneTypeSub(supermod.ZPlaneType):
    def __init__(self, z=None, rmin='0.0', rmax=None, **kwargs_):
        super(ZPlaneTypeSub, self).__init__(z, rmin, rmax,  **kwargs_)
supermod.ZPlaneType.subclass = ZPlaneTypeSub
# end class ZPlaneTypeSub


class genericPolyconeSub(supermod.genericPolycone):
    def __init__(self, lunit='mm', aunit='radian', name=None, deltaphi=None, startphi='0.0', rzpoint=None, **kwargs_):
        super(genericPolyconeSub, self).__init__(lunit, aunit, name, deltaphi, startphi, rzpoint,  **kwargs_)
supermod.genericPolycone.subclass = genericPolyconeSub
# end class genericPolyconeSub


class RZPointTypeSub(supermod.RZPointType):
    def __init__(self, r=None, z=None, **kwargs_):
        super(RZPointTypeSub, self).__init__(r, z,  **kwargs_)
supermod.RZPointType.subclass = RZPointTypeSub
# end class RZPointTypeSub


class paraSub(supermod.para):
    def __init__(self, lunit='mm', aunit='radian', name=None, x=None, y=None, z=None, alpha=None, theta=None, phi=None, **kwargs_):
        super(paraSub, self).__init__(lunit, aunit, name, x, y, z, alpha, theta, phi,  **kwargs_)
supermod.para.subclass = paraSub
# end class paraSub


class trdSub(supermod.trd):
    def __init__(self, lunit='mm', aunit='radian', name=None, x1=None, x2=None, y1=None, y2=None, z=None, **kwargs_):
        super(trdSub, self).__init__(lunit, aunit, name, x1, x2, y1, y2, z,  **kwargs_)
supermod.trd.subclass = trdSub
# end class trdSub


class trapSub(supermod.trap):
    def __init__(self, lunit='mm', aunit='radian', name=None, z=None, theta=None, phi=None, y1=None, x1=None, x2=None, alpha1=None, y2=None, x3=None, x4=None, alpha2=None, **kwargs_):
        super(trapSub, self).__init__(lunit, aunit, name, z, theta, phi, y1, x1, x2, alpha1, y2, x3, x4, alpha2,  **kwargs_)
supermod.trap.subclass = trapSub
# end class trapSub


class torusSub(supermod.torus):
    def __init__(self, lunit='mm', aunit='radian', name=None, rmin=None, rmax=None, rtor=None, startphi=None, deltaphi=None, **kwargs_):
        super(torusSub, self).__init__(lunit, aunit, name, rmin, rmax, rtor, startphi, deltaphi,  **kwargs_)
supermod.torus.subclass = torusSub
# end class torusSub


class orbSub(supermod.orb):
    def __init__(self, lunit='mm', aunit='radian', name=None, r=None, **kwargs_):
        super(orbSub, self).__init__(lunit, aunit, name, r,  **kwargs_)
supermod.orb.subclass = orbSub
# end class orbSub


class polyhedraSub(supermod.polyhedra):
    def __init__(self, lunit='mm', aunit='radian', name=None, startphi=None, deltaphi=None, numsides=None, zplane=None, **kwargs_):
        super(polyhedraSub, self).__init__(lunit, aunit, name, startphi, deltaphi, numsides, zplane,  **kwargs_)
supermod.polyhedra.subclass = polyhedraSub
# end class polyhedraSub


class genericPolyhedraSub(supermod.genericPolyhedra):
    def __init__(self, lunit='mm', aunit='radian', name=None, startphi=None, deltaphi=None, numsides=None, rzpoint=None, **kwargs_):
        super(genericPolyhedraSub, self).__init__(lunit, aunit, name, startphi, deltaphi, numsides, rzpoint,  **kwargs_)
supermod.genericPolyhedra.subclass = genericPolyhedraSub
# end class genericPolyhedraSub


class TwoDimVertexTypeSub(supermod.TwoDimVertexType):
    def __init__(self, x=None, y=None, **kwargs_):
        super(TwoDimVertexTypeSub, self).__init__(x, y,  **kwargs_)
supermod.TwoDimVertexType.subclass = TwoDimVertexTypeSub
# end class TwoDimVertexTypeSub


class SectionTypeSub(supermod.SectionType):
    def __init__(self, zOrder=None, zPosition=None, xOffset=None, yOffset=None, scalingFactor=None, **kwargs_):
        super(SectionTypeSub, self).__init__(zOrder, zPosition, xOffset, yOffset, scalingFactor,  **kwargs_)
supermod.SectionType.subclass = SectionTypeSub
# end class SectionTypeSub


class xtruSub(supermod.xtru):
    def __init__(self, lunit='mm', aunit='radian', name=None, twoDimVertex=None, section=None, **kwargs_):
        super(xtruSub, self).__init__(lunit, aunit, name, twoDimVertex, section,  **kwargs_)
supermod.xtru.subclass = xtruSub
# end class xtruSub


class hypeSub(supermod.hype):
    def __init__(self, lunit='mm', aunit='radian', name=None, rmin=None, rmax=None, inst=None, outst=None, z=None, **kwargs_):
        super(hypeSub, self).__init__(lunit, aunit, name, rmin, rmax, inst, outst, z,  **kwargs_)
supermod.hype.subclass = hypeSub
# end class hypeSub


class eltubeSub(supermod.eltube):
    def __init__(self, lunit='mm', aunit='radian', name=None, dx=None, dy=None, dz=None, **kwargs_):
        super(eltubeSub, self).__init__(lunit, aunit, name, dx, dy, dz,  **kwargs_)
supermod.eltube.subclass = eltubeSub
# end class eltubeSub


class tetSub(supermod.tet):
    def __init__(self, lunit='mm', aunit='radian', name=None, vertex1=None, vertex2=None, vertex3=None, vertex4=None, **kwargs_):
        super(tetSub, self).__init__(lunit, aunit, name, vertex1, vertex2, vertex3, vertex4,  **kwargs_)
supermod.tet.subclass = tetSub
# end class tetSub


class arb8Sub(supermod.arb8):
    def __init__(self, lunit='mm', aunit='radian', name=None, v1x=None, v1y=None, v2x=None, v2y=None, v3x=None, v3y=None, v4x=None, v4y=None, v5x=None, v5y=None, v6x=None, v6y=None, v7x=None, v7y=None, v8x=None, v8y=None, dz=None, **kwargs_):
        super(arb8Sub, self).__init__(lunit, aunit, name, v1x, v1y, v2x, v2y, v3x, v3y, v4x, v4y, v5x, v5y, v6x, v6y, v7x, v7y, v8x, v8y, dz,  **kwargs_)
supermod.arb8.subclass = arb8Sub
# end class arb8Sub


class FacetTypeSub(supermod.FacetType):
    def __init__(self, extensiontype_=None, **kwargs_):
        super(FacetTypeSub, self).__init__(extensiontype_,  **kwargs_)
supermod.FacetType.subclass = FacetTypeSub
# end class FacetTypeSub


class triangularSub(supermod.triangular):
    def __init__(self, vertex1=None, vertex2=None, vertex3=None, type_='ABSOLUTE', **kwargs_):
        super(triangularSub, self).__init__(vertex1, vertex2, vertex3, type_,  **kwargs_)
supermod.triangular.subclass = triangularSub
# end class triangularSub


class quadrangularSub(supermod.quadrangular):
    def __init__(self, vertex1=None, vertex2=None, vertex3=None, vertex4=None, type_='ABSOLUTE', **kwargs_):
        super(quadrangularSub, self).__init__(vertex1, vertex2, vertex3, vertex4, type_,  **kwargs_)
supermod.quadrangular.subclass = quadrangularSub
# end class quadrangularSub


class tessellatedSub(supermod.tessellated):
    def __init__(self, lunit='mm', aunit='radian', name=None, Facet=None, **kwargs_):
        super(tessellatedSub, self).__init__(lunit, aunit, name, Facet,  **kwargs_)
supermod.tessellated.subclass = tessellatedSub
# end class tessellatedSub


class opticalsurfaceSub(supermod.opticalsurface):
    def __init__(self, name=None, type_='dielectric_dielectric', property=None, model='glisur', finish='polished', value='1.0', **kwargs_):
        super(opticalsurfaceSub, self).__init__(name, type_, property, model, finish, value,  **kwargs_)
supermod.opticalsurface.subclass = opticalsurfaceSub
# end class opticalsurfaceSub


class ReplicationAlgorithmTypeSub(supermod.ReplicationAlgorithmType):
    def __init__(self, extensiontype_=None, **kwargs_):
        super(ReplicationAlgorithmTypeSub, self).__init__(extensiontype_,  **kwargs_)
supermod.ReplicationAlgorithmType.subclass = ReplicationAlgorithmTypeSub
# end class ReplicationAlgorithmTypeSub


class AxisReplicationAlgorithmTypeSub(supermod.AxisReplicationAlgorithmType):
    def __init__(self, position=None, positionref=None, rotation=None, rotationref=None, direction=None, directionref=None, width=None, offset=None, **kwargs_):
        super(AxisReplicationAlgorithmTypeSub, self).__init__(position, positionref, rotation, rotationref, direction, directionref, width, offset,  **kwargs_)
supermod.AxisReplicationAlgorithmType.subclass = AxisReplicationAlgorithmTypeSub
# end class AxisReplicationAlgorithmTypeSub


class ReplicaPlacementTypeSub(supermod.ReplicaPlacementType):
    def __init__(self, number=None, copy_num_start=1, copy_num_step=1, volumeref=None, ReplicationAlgorithm=None, **kwargs_):
        super(ReplicaPlacementTypeSub, self).__init__(number, copy_num_start, copy_num_step, volumeref, ReplicationAlgorithm,  **kwargs_)
supermod.ReplicaPlacementType.subclass = ReplicaPlacementTypeSub
# end class ReplicaPlacementTypeSub


class directionTypeSub(supermod.directionType):
    def __init__(self, x='0.0', y='0.0', z='0.0', phi='0.0', rho='0.0', **kwargs_):
        super(directionTypeSub, self).__init__(x, y, z, phi, rho,  **kwargs_)
supermod.directionType.subclass = directionTypeSub
# end class directionTypeSub


class DimensionsTypeSub(supermod.DimensionsType):
    def __init__(self, extensiontype_=None, **kwargs_):
        super(DimensionsTypeSub, self).__init__(extensiontype_,  **kwargs_)
supermod.DimensionsType.subclass = DimensionsTypeSub
# end class DimensionsTypeSub


class BoxDimensionsTypeSub(supermod.BoxDimensionsType):
    def __init__(self, x='1.0', y='1.0', z='1.0', lunit='mm', **kwargs_):
        super(BoxDimensionsTypeSub, self).__init__(x, y, z, lunit,  **kwargs_)
supermod.BoxDimensionsType.subclass = BoxDimensionsTypeSub
# end class BoxDimensionsTypeSub


class TrdDimensionsTypeSub(supermod.TrdDimensionsType):
    def __init__(self, x1='1.0', x2='1.0', y1='1.0', y2='1.0', z='1.0', lunit='mm', **kwargs_):
        super(TrdDimensionsTypeSub, self).__init__(x1, x2, y1, y2, z, lunit,  **kwargs_)
supermod.TrdDimensionsType.subclass = TrdDimensionsTypeSub
# end class TrdDimensionsTypeSub


class TrapDimensionsTypeSub(supermod.TrapDimensionsType):
    def __init__(self, z='1.0', theta='1.0', phi='1.0', y1='1.0', x1='1.0', x2='1.0', alpha1='1.0', y2='1.0', x3='1.0', x4='1.0', alpha2='1.0', lunit='mm', aunit='radian', **kwargs_):
        super(TrapDimensionsTypeSub, self).__init__(z, theta, phi, y1, x1, x2, alpha1, y2, x3, x4, alpha2, lunit, aunit,  **kwargs_)
supermod.TrapDimensionsType.subclass = TrapDimensionsTypeSub
# end class TrapDimensionsTypeSub


class TubeDimensionsTypeSub(supermod.TubeDimensionsType):
    def __init__(self, DeltaPhi='1.0', InR='1.0', OutR='1.0', StartPhi='0.0', hz='1.0', lunit='mm', aunit='radian', **kwargs_):
        super(TubeDimensionsTypeSub, self).__init__(DeltaPhi, InR, OutR, StartPhi, hz, lunit, aunit,  **kwargs_)
supermod.TubeDimensionsType.subclass = TubeDimensionsTypeSub
# end class TubeDimensionsTypeSub


class ConeDimensionsTypeSub(supermod.ConeDimensionsType):
    def __init__(self, rmin1='1.0', rmax1='1.0', rmin2='1.0', rmax2='1.0', z='1.0', startphi='0.0', deltaphi='1.0', lunit='mm', aunit='radian', **kwargs_):
        super(ConeDimensionsTypeSub, self).__init__(rmin1, rmax1, rmin2, rmax2, z, startphi, deltaphi, lunit, aunit,  **kwargs_)
supermod.ConeDimensionsType.subclass = ConeDimensionsTypeSub
# end class ConeDimensionsTypeSub


class SphereDimensionsTypeSub(supermod.SphereDimensionsType):
    def __init__(self, rmin='1.0', rmax='1.0', starttheta='0.0', deltatheta='1.0', startphi='0.0', deltaphi='1.0', lunit='mm', aunit='radian', **kwargs_):
        super(SphereDimensionsTypeSub, self).__init__(rmin, rmax, starttheta, deltatheta, startphi, deltaphi, lunit, aunit,  **kwargs_)
supermod.SphereDimensionsType.subclass = SphereDimensionsTypeSub
# end class SphereDimensionsTypeSub


class OrbDimensionsTypeSub(supermod.OrbDimensionsType):
    def __init__(self, r='1.0', lunit='mm', **kwargs_):
        super(OrbDimensionsTypeSub, self).__init__(r, lunit,  **kwargs_)
supermod.OrbDimensionsType.subclass = OrbDimensionsTypeSub
# end class OrbDimensionsTypeSub


class TorusDimensionsTypeSub(supermod.TorusDimensionsType):
    def __init__(self, rmin='1.0', rmax='1.0', rtor='1.0', startphi='0.0', deltaphi='1.0', lunit='mm', aunit='radian', **kwargs_):
        super(TorusDimensionsTypeSub, self).__init__(rmin, rmax, rtor, startphi, deltaphi, lunit, aunit,  **kwargs_)
supermod.TorusDimensionsType.subclass = TorusDimensionsTypeSub
# end class TorusDimensionsTypeSub


class EllipsoidDimensionsTypeSub(supermod.EllipsoidDimensionsType):
    def __init__(self, ax='1.0', by='1.0', cz='1.0', zcut1='-1000000.0', zcut2='1000000.0', lunit='mm', **kwargs_):
        super(EllipsoidDimensionsTypeSub, self).__init__(ax, by, cz, zcut1, zcut2, lunit,  **kwargs_)
supermod.EllipsoidDimensionsType.subclass = EllipsoidDimensionsTypeSub
# end class EllipsoidDimensionsTypeSub


class ParaDimensionsTypeSub(supermod.ParaDimensionsType):
    def __init__(self, x='1.0', y='1.0', z='1.0', alpha='1.0', theta='1.0', phi='1.0', lunit='mm', aunit='radian', **kwargs_):
        super(ParaDimensionsTypeSub, self).__init__(x, y, z, alpha, theta, phi, lunit, aunit,  **kwargs_)
supermod.ParaDimensionsType.subclass = ParaDimensionsTypeSub
# end class ParaDimensionsTypeSub


class PolyconeDimensionsTypeSub(supermod.PolyconeDimensionsType):
    def __init__(self, numRZ='1.0', startPhi='0.0', openPhi='1.0', lunit='mm', aunit='radian', zplane=None, **kwargs_):
        super(PolyconeDimensionsTypeSub, self).__init__(numRZ, startPhi, openPhi, lunit, aunit, zplane,  **kwargs_)
supermod.PolyconeDimensionsType.subclass = PolyconeDimensionsTypeSub
# end class PolyconeDimensionsTypeSub


class PolyhedraDimensionsTypeSub(supermod.PolyhedraDimensionsType):
    def __init__(self, numRZ='1.0', numSide='1.0', startPhi='1.0', openPhi='1.0', lunit='mm', aunit='radian', zplane=None, **kwargs_):
        super(PolyhedraDimensionsTypeSub, self).__init__(numRZ, numSide, startPhi, openPhi, lunit, aunit, zplane,  **kwargs_)
supermod.PolyhedraDimensionsType.subclass = PolyhedraDimensionsTypeSub
# end class PolyhedraDimensionsTypeSub


class ZPlaneParamTypeSub(supermod.ZPlaneParamType):
    def __init__(self, z='0.0', rmin='0.0', rmax='1.0', **kwargs_):
        super(ZPlaneParamTypeSub, self).__init__(z, rmin, rmax,  **kwargs_)
supermod.ZPlaneParamType.subclass = ZPlaneParamTypeSub
# end class ZPlaneParamTypeSub


class HypeDimensionsTypeSub(supermod.HypeDimensionsType):
    def __init__(self, rmin='1.0', rmax='1.0', inst='1.0', outst='1.0', z='1.0', lunit='mm', aunit='radian', **kwargs_):
        super(HypeDimensionsTypeSub, self).__init__(rmin, rmax, inst, outst, z, lunit, aunit,  **kwargs_)
supermod.HypeDimensionsType.subclass = HypeDimensionsTypeSub
# end class HypeDimensionsTypeSub


class ParameterisationAlgorithmTypeSub(supermod.ParameterisationAlgorithmType):
    def __init__(self, extensiontype_=None, **kwargs_):
        super(ParameterisationAlgorithmTypeSub, self).__init__(extensiontype_,  **kwargs_)
supermod.ParameterisationAlgorithmType.subclass = ParameterisationAlgorithmTypeSub
# end class ParameterisationAlgorithmTypeSub


class PositionSizeParameterisationAlgorithmTypeSub(supermod.PositionSizeParameterisationAlgorithmType):
    def __init__(self, parameters=None, **kwargs_):
        super(PositionSizeParameterisationAlgorithmTypeSub, self).__init__(parameters,  **kwargs_)
supermod.PositionSizeParameterisationAlgorithmType.subclass = PositionSizeParameterisationAlgorithmTypeSub
# end class PositionSizeParameterisationAlgorithmTypeSub


class ParameterisedPlacementTypeSub(supermod.ParameterisedPlacementType):
    def __init__(self, ncopies=None, volumeref=None, ParameterisationAlgorithm=None, **kwargs_):
        super(ParameterisedPlacementTypeSub, self).__init__(ncopies, volumeref, ParameterisationAlgorithm,  **kwargs_)
supermod.ParameterisedPlacementType.subclass = ParameterisedPlacementTypeSub
# end class ParameterisedPlacementTypeSub


class ParametersTypeSub(supermod.ParametersType):
    def __init__(self, number=None, position=None, Dimensions=None, **kwargs_):
        super(ParametersTypeSub, self).__init__(number, position, Dimensions,  **kwargs_)
supermod.ParametersType.subclass = ParametersTypeSub
# end class ParametersTypeSub


class userinfoTypeSub(supermod.userinfoType):
    def __init__(self, auxiliary=None, **kwargs_):
        super(userinfoTypeSub, self).__init__(auxiliary,  **kwargs_)
supermod.userinfoType.subclass = userinfoTypeSub
# end class userinfoTypeSub


class setupTypeSub(supermod.setupType):
    def __init__(self, name=None, version=None, world=None, **kwargs_):
        super(setupTypeSub, self).__init__(name, version, world,  **kwargs_)
supermod.setupType.subclass = setupTypeSub
# end class setupTypeSub


class propertyTypeSub(supermod.propertyType):
    def __init__(self, ref=None, name=None, **kwargs_):
        super(propertyTypeSub, self).__init__(ref, name,  **kwargs_)
supermod.propertyType.subclass = propertyTypeSub
# end class propertyTypeSub


class RLTypeSub(supermod.RLType):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(RLTypeSub, self).__init__(value, unit, type_,  **kwargs_)
supermod.RLType.subclass = RLTypeSub
# end class RLTypeSub


class ALTypeSub(supermod.ALType):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(ALTypeSub, self).__init__(value, unit, type_,  **kwargs_)
supermod.ALType.subclass = ALTypeSub
# end class ALTypeSub


class TTypeSub(supermod.TType):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(TTypeSub, self).__init__(value, unit, type_,  **kwargs_)
supermod.TType.subclass = TTypeSub
# end class TTypeSub


class PTypeSub(supermod.PType):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(PTypeSub, self).__init__(value, unit, type_,  **kwargs_)
supermod.PType.subclass = PTypeSub
# end class PTypeSub


class MEETypeSub(supermod.MEEType):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(MEETypeSub, self).__init__(value, unit, type_,  **kwargs_)
supermod.MEEType.subclass = MEETypeSub
# end class MEETypeSub


class propertyType1Sub(supermod.propertyType1):
    def __init__(self, ref=None, name=None, **kwargs_):
        super(propertyType1Sub, self).__init__(ref, name,  **kwargs_)
supermod.propertyType1.subclass = propertyType1Sub
# end class propertyType1Sub


class RLType2Sub(supermod.RLType2):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(RLType2Sub, self).__init__(value, unit, type_,  **kwargs_)
supermod.RLType2.subclass = RLType2Sub
# end class RLType2Sub


class ALType3Sub(supermod.ALType3):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(ALType3Sub, self).__init__(value, unit, type_,  **kwargs_)
supermod.ALType3.subclass = ALType3Sub
# end class ALType3Sub


class TType4Sub(supermod.TType4):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(TType4Sub, self).__init__(value, unit, type_,  **kwargs_)
supermod.TType4.subclass = TType4Sub
# end class TType4Sub


class PType5Sub(supermod.PType5):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(PType5Sub, self).__init__(value, unit, type_,  **kwargs_)
supermod.PType5.subclass = PType5Sub
# end class PType5Sub


class MEEType6Sub(supermod.MEEType6):
    def __init__(self, value=None, unit=None, type_=None, **kwargs_):
        super(MEEType6Sub, self).__init__(value, unit, type_,  **kwargs_)
supermod.MEEType6.subclass = MEEType6Sub
# end class MEEType6Sub


class fractionTypeSub(supermod.fractionType):
    def __init__(self, ref=None, n=None, **kwargs_):
        super(fractionTypeSub, self).__init__(ref, n,  **kwargs_)
supermod.fractionType.subclass = fractionTypeSub
# end class fractionTypeSub


class compositeTypeSub(supermod.compositeType):
    def __init__(self, ref=None, n=None, **kwargs_):
        super(compositeTypeSub, self).__init__(ref, n,  **kwargs_)
supermod.compositeType.subclass = compositeTypeSub
# end class compositeTypeSub


class fractionType7Sub(supermod.fractionType7):
    def __init__(self, ref=None, n=None, **kwargs_):
        super(fractionType7Sub, self).__init__(ref, n,  **kwargs_)
supermod.fractionType7.subclass = fractionType7Sub
# end class fractionType7Sub


class propertyType8Sub(supermod.propertyType8):
    def __init__(self, ref=None, name=None, **kwargs_):
        super(propertyType8Sub, self).__init__(ref, name,  **kwargs_)
supermod.propertyType8.subclass = propertyType8Sub
# end class propertyType8Sub


class propertyType9Sub(supermod.propertyType9):
    def __init__(self, ref=None, name=None, **kwargs_):
        super(propertyType9Sub, self).__init__(ref, name,  **kwargs_)
supermod.propertyType9.subclass = propertyType9Sub
# end class propertyType9Sub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'gdml'
        rootClass = supermod.gdml
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'gdml'
        rootClass = supermod.gdml
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'gdml'
        rootClass = supermod.gdml
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'gdml'
        rootClass = supermod.gdml
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
