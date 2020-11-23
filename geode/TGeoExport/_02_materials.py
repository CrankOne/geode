# -*- coding: utf8 -*-

"""
File describes routines for conversion the GDML material definitions into
corresponding ROOT structures.

Shouldn't be used as a separate module. Import `geode.TGeoExport.bindings'
instead.
"""

import ROOT
import logging

def read_NIST( I, NISTMaterialsGDML, quiet=False ):
    from extGDML.gdmlExport import export
    export( NISTMaterialsGDML, I,
            exportFormat='ROOT',
            #outFilePath=None,  xxx
            quiet=quiet,
            readDefinitions=False,
            readMaterials=True,
            readSolids=False,
            readStructure=False,
            readSetup=False,
            finalizeGeometry=False )

def read_materials( gdml, I,
                    quiet=False, *args, **kwargs ):
    """
    This function will create entities found in <materials/> section of GDML
    document: isotopes, elements, and materials. No explicit ROOT storage
    specified here. All corresponded ROOT instances will be referenced in
    'materials/' section of `defs' dictionary.
    """
    L = logging.getLogger(__name__)
    nistMatsGDML = kwargs.get('NISTMaterialsGDML', None)
    if nistMatsGDML:
        read_NIST(I.new_subindex( 'NISTMat' ), nistMatsGDML, quiet=quiet )
        L.info( "NIST materials converted." )
    from geode.TGeoExport.loop import treat_loop_element
    # TODO: isotopes; TGeoElementRN
    #   or:
    # https://github.com/dawehner/root/blob/master/geom/gdml/src/TGDMLParse.cxx#L728
    for isotopeEl in gdml.get_materials().get_isotope():
        #isotopeObj = ROOT.TGeoIsotope.FindIsotope( isotopeEl.get_name() )
        # doesn't work ^^^
        isotopeObj = ROOT.gGeoManager \
                .GetElementTable() \
                .FindIsotope( str(isotopeEl.get_name()) )
        # doesn't work as expected as well ^^^
        if not isotopeObj:
            isotopeObj = ROOT.TGeoIsotope(
                        isotopeEl.get_name(),       # const char * name
                        int(isotopeEl.get_Z()),     # Int_t Z (from xs:double)
                        isotopeEl.get_N(),          # Int_t n
                        isotopeEl \
                            .get_atom(). \
                            convert_value_in_units(I.E, 'g/mole') # Double_t a
                )
            L.debug( 'Isotope %s added.'%isotopeEl.get_name() )
        else:
            L.debug( 'Isotope %s already known to ROOT. Skipping construction.'% \
                        isotopeEl.get_name() )
        I.set_isotope( isotopeObj, name=isotopeEl.get_name() )

    #
    # Elements:
    #elementsDict = {}
    for chemElObj in gdml.get_materials().get_element():
        chemEl = ROOT.TGeoElement.GetElementTable().FindElement(
                str(chemElObj.get_name()) )
        if not chemEl:
            if chemElObj.get_atom():
                Z = int(I.E.evaluate( '%s'%chemElObj.get_Z() ))
                A = chemElObj.get_atom().convert_value_in_units(I.E, 'g/mole')
                chemEl = ROOT.TGeoElement( chemElObj.get_name(), # name
                                           chemElObj.get_formula(), # title
                                           Z, A )
            else:
                # elements can be also defined with their <fraction/>s composition:
                raise NotImplementedError('Elements with isotopic fractions are '
                                          'not implemented.')
            L.debug( 'New chemical element %s, (%s): A=%d, Z=%d, N=%d.'%(
                            chemEl.GetName(), chemEl.GetTitle(),
                            chemEl.A(), chemEl.Z(), chemEl.N()) )
        else:
            L.debug( 'Element %s is already known to ROOT. '
                       'Skipping construction.'%chemElObj.get_name() )
        I.set_element( chemEl, name=chemElObj.get_name() )

    #
    # Materials:
    #matsDict = {}
    for mat in gdml.get_materials().get_material():
        matName = mat.get_name()
        matTObj = ROOT.gGeoManager.GetMaterial( matName )
        if not matTObj:
            # Three ways to define a material:
            # 1. by its density and atom
            # 2. by its density and references to atoms (<composite/>)
            # 3. by its density and presence of fraction
            density = mat.get_D().convert_value_in_units(I.E, 'g/cm3')
            # TODO: support for material group properties
            if mat.get_atom():
                # material defined via atom (chemical pure)
                A = mat.get_atom().convert_value_in_units( I.E, 'g/mole' )
                #L.info( "Z=", mat.get_Z(), type(mat.get_Z()) )
                Z = mat.get_Z()
                if Z is None:
                    raise ValueError( 'While defining material "%s" '%matName +
                        'as a chemical-pure material, the Z number is not set.' )
                matTObj = ROOT.TGeoMaterial( matName, A, mat.get_Z(), density,
                    0, 0 # TODO: radlen, intlen
                    )
                #L.info( matName, matTObj )  # XXX
                L.debug( ('Mat. {name} defined as a pure chem. element: A={A} u., ' +
                            'Z={Z}, rho={rho} g/cm3, radlen={rl}, intlen={il}.').format(**{
                        'name' : matTObj.GetName(),
                           'A' : matTObj.GetA(),
                           'Z' : matTObj.GetZ(),
                         'rho' : matTObj.GetDensity(),
                          'rl' : matTObj.GetRadLen(),
                          'il' : matTObj.GetIntLen()
                    }) )
            elif mat.get_composite():
                # material defined by <composite/>: A composite material is defined
                # by a set of elements by specifying the number of atoms. 
                # Elements of this composite material specified as a set of local
                # references to already defined simple elements where value of n in
                # each means the number of atoms
                # Corresponded ROOT class is TGeoMixture (descendant of
                # TGeoMaterial).
                resolvedElRefs = []
                for comp in mat.get_composite():
                    n = comp.get_n()  # number of atoms
                    ref = comp.get_ref()  # reference of type str (refers to el)
                    el = I.get_element( ref, noexcept=True )
                    if el is None:
                        raise GDMLError( 'Element "%s" is not defined while been '
                            'used as a component in definition material "%s".'%(
                            ref, matName ) )
                    resolvedElRefs.append([ el, n ])
                matTObj = ROOT.TGeoMixture( matName, len(resolvedElRefs), density )
                #L.info( matName, matTObj )  # XXX
                for el in resolvedElRefs:
                    matTObj.AddElement( el[0], el[1] )
                    L.debug( '    ...el %s of %s atoms added (%s)'%(
                            el[0].GetName(), str(el[1]), str(el[0])
                        ) )
                L.debug( 'Mat. %s defined as a composite one from %d elements, ' 
                           'radlen=%e, intlen=%e'%( matName,
                                                    matTObj.GetNelements(),
                                                    matTObj.GetRadLen(),
                                                    matTObj.GetIntLen()) )
            elif mat.get_fraction():
                # The fractions can be either simple elements or other complex
                # materials. Fractions of this mixture specified as a set of local
                # references to already defined elements or other mixtures where
                # value of n in each means the fraction of the whole material in
                # the range 0.0 < n < 1.0
                resolvedFracRefs = []
                nSum = 0.
                nEls = 0
                nMats = 0
                for frac in mat.get_fraction():
                    n = frac.get_n()  # fraction value
                    #ref = frac.get_ref()  # reference of type str (refers to el)
                    #el = elementsDict.get( ref, None )
                    el = I.get_element( frac.get_ref(), noexcept=True )
                    if el is None:
                        try:
                            el = I.get_material( frac.get_ref() )
                        except KeyError:
                            raise KeyError( 'Element or material "%s" is not '
                                'defined while been used as a fraction in '
                                'definition material "%s".'%(
                                    frac.get_ref(), matName ) )
                        else:
                            nMats += 1
                    else:
                        nEls += 1
                    resolvedFracRefs.append([ el, n ])
                if nSum >= 1.:
                    raise ValueError( 'While defininf material "%s" as a fractional '
                                     'mixture the sum of fractions is %e > 1.'%(
                                     matName, nSum) )
                matTObj = ROOT.TGeoMixture( matName, len(resolvedFracRefs), density )
                #L.info( matName, matTObj )  # XXX
                for el in resolvedFracRefs:
                    matTObj.AddElement( el[0], el[1] )
                L.debug( 'Mat. %s defined as a fractional mixture of %d '
                           'components (%d chem. elements, %d mixtures)'%(
                           matName, len(resolvedFracRefs), nEls, nMats) )
            else:
                from extGDML.gdmlError import GDMLError
                # Basically the schema validation routine makes this case
                # impossible.
                raise GDMLError( 'While defining material "%s" '%matName +
                                 '--- could not determine material definition.' )
            if mat.get_state():
                matState = mat.get_state()
                if 'gas' == matState:
                    matTObj.SetState( ROOT.TGeoMaterial.kMatStateGas )
                elif 'solid' == matState:
                    matTObj.SetState( ROOT.TGeoMaterial.kMatStateSolid )
                elif 'liquid' == matState:
                    matTObj.SetState( ROOT.TGeoMaterial.kMatStateLiquid )
                elif 'unknown' == matState:
                    matTObj.SetState( ROOT.TGeoMaterial.kMatStateUndefined )
                else:
                    raise ValueError( 'Unable to identify '
                        'material state "%s"'%matState )
        else:
            L.debug( 'Material %s is already known to ROOT. '
                    'Skipping construction.'%mat.get_name() )
        I.set_material( matTObj, name=matName )

