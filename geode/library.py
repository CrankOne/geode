import os
import io
import logging
from lxml import etree as lxmlETree
import pkg_resources as pkgResources

# List of generated parser modules
import geode.GDMLParser.v3_1_6.classes as GDML_3_1_6
# ... (add new parsers here)

# Collection of GDML root class constructors
# TODO: assets path on install from setup.py?
gGDMLStructs = {
    (3, 1, 6): GDML_3_1_6
    # ... (add new parsers here)
}
def get_root_tag(node, module):
    tag = module.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = module.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(module, tag):
        rootClass = getattr(module, tag)
    return tag, rootClass

class WarningsCollector(object):
    """
    Collects warning messages that are produced when the value of a simple type
    fails to validate against its restrictions.
    """
    def __init__(self, messages=None):
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    def add_message(self, msg):
        self.messages.append(msg)

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []

def parse_GDML( gdml
              , version=None
              , schema=None
              , lxmlParseKwargs={}
              ):
    """
    Converts XML semantics into Python data entities (GenerateDS classes).
        @param gdml file-like object or string text to parse XML/GDML from
        @param version is expected to be a 3-ints tuple denoting one of the
            available schema version
        @param lxmlParseKwargs is keyword arguments that have to be forwarded
            into coresponding functions of `lxml.parse*()`
    Returns three entities:
        - GDML data (instance of GenerateDS `gdml') or `None' if exception occurred
        - list of warnings (may be empty)
        - exception if occurred, otherwise `None'

    Performs validation and parsing of GDML document applying XSD-schema
    validation (if schema document is provided). On the validation stage all
    the <restricition/> (including fixed="", and default="" tags) will be taken
    into account and, thus, output XML object will be supplied with additional
    information.

    Note, that contrary to usual behaviour when XML parser generates the
    separate PSVI object, lxml module will modify original document after
    validation.
    """
    L = logging.getLogger(__name__)
    parser = None
    try:
        parser = lxmlETree.ETCompatXMLParser(schema=schema, attribute_defaults=True)
    except AttributeError:
        L.debug('Failed to instantiate ETCompatXMLParser; fallback to xml.etree')
        parser = lxmlETree.XMLParser(schema=schema, attribute_defaults=True)
    try:
        if isinstance(gdml, io.TextIOBase):
            lxmlDoc = lxmlETree.parse(gdml, parser=parser, **lxmlParseKwargs)
        else:
            lxmlDoc = lxmlETree.fromstring(gdml, parser=parser, **lxmlParseKwargs)
    except Exception as e:
        return None, [], e
    if version is None:
        version = sorted(gGDMLStructs.keys())[-1]
        L.debug('No GDML schema version forced; assuming %s'%(
            '.'.join([str(v) for v in version])))
    m = gGDMLStructs[version]
    # get tag of root node
    rootNode = lxmlDoc.getroot()
    rootTag, rootClass = get_root_tag(rootNode, m)
    rootObj = m.gdml.factory()
    warnings = []
    try:
        rootObj.build(rootNode, gds_collector_=WarningsCollector(warnings))
    except Exception as e:
        return None, warnings, e
    return rootObj, warnings, None


def files_at( baseDir, criteria ):
    """
    A generator function returning files matching certain criterion from
    a directory recursively.
    """
    for root, dirs, files in os.walk(baseDir, followlinks=True):
        relPath = os.path.relpath(root, baseDir)
        for f in files:
            if criteria(f):
                fullPath = os.path.normpath(os.path.join(relPath, f))
                keys = fullPath.split(os.sep)
                yield (keys, os.path.join(root, f))

class GeoLibrary(object):
    """
    Geometry library representation.
    """
    def __init__(self, schemaVersion=None):
        L = logging.getLogger(__name__)
        # imported entities are stored here
        self.items = {}
        # set the latest version if not forced
        if schemaVersion is None:
            schemaVersion = sorted(gGDMLStructs.keys())[-1]
            L.debug('No GDML schema version forced for library; assuming %s'%(
                '.'.join([str(v) for v in schemaVersion])))
        self._schemaVersion = schemaVersion
        self._dataStructures = gGDMLStructs[self._schemaVersion]
        # initialize schema object
        schemaPath = pkgResources.resource_filename( 'geode'
                , 'GDMLParser/v{version}/GDML_{version}/schema/gdml.xsd'.format(
                            version='_'.join([str(v) for v in schemaVersion]))
                )
        with open(schemaPath) as f:
            schemaDoc = lxmlETree.parse(f)
        #schemaDoc = parse_xml(sys.argv[1])
        self._schema = lxmlETree.XMLSchema( schemaDoc )

    def import_fs_subtree( self
                         , baseDir
                         , gdmlExtensions={'.gdml',}
                         , lxmlParseKwargs={}
                         ):
        """
        Recursively imports files from a dir by extension criteria.
        """
        L = logging.getLogger(__name__)
        for keys, fPath in files_at(baseDir,
                lambda fn: any( map(lambda ext: fn.endswith(ext), gdmlExtensions) )):
            with open(fPath, 'r') as f:
                gdmlData, warns, err = parse_GDML( f
                        , version=self._schemaVersion
                        , lxmlParseKwargs=lxmlParseKwargs
                        , schema=self._schema
                        )
            if not err:
                self.items[tuple(keys)] = { 'file': fPath
                                          , 'warnings': warns
                                          , 'data': gdmlData
                                          }
                if warns:
                    for w in warns:
                        L.warning('File "%s" import warning: %s'%(fPath, w))
                L.info('File "%s" imported.'%fPath)
            else:
                L.error('Failed to import "%s". Error:'%fPath)
                L.exception(err)


import sys  # XXX
# any( map( lambda ext: f.endswith(ext), templateExtensions ))
#collect_templates(sys.argv[1])

#doc = parse_3_1_6('../ext.gdml/examples/csg-basic.gdml', silence=True)
#print(doc)

#
# XXX
#with open(sys.argv[1]) as f:
#    schemaDoc = lxmlETree.parse(f)
##schemaDoc = parse_xml(sys.argv[1])
#schemaObj = lxmlETree.XMLSchema( schemaDoc )
#
#asString = False
#with open(sys.argv[2]) as f:
#    doc, warns = None, None
#    if asString:
#        xml = f.read()
#        root, warns = parse_GDML(xml.encode())
#    else:
#        root, warns, error = parse_GDML(f, schema=schemaObj)
#print(warns, error)
#if root:
#    root.export( sys.stdout, 0, name_='gdml' )

lib = GeoLibrary()
lib.import_fs_subtree(sys.argv[1])
for k in lib.items.keys():
    print(k)


