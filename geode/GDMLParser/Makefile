# Makefile used to generate the GDML parser based on XSD schema of certain
# version via the generateDS util (see: http://www.davekuhlman.org/generateDS.html)

SCHEMA_VERSION=3_1_6
GENERATE_DS_EXEC=generateDS.py

SCHEMA_URI="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/downloads/GDML_$(SCHEMA_VERSION).tar.gz"

all: v$(SCHEMA_VERSION)/__init__.py

v$(SCHEMA_VERSION)/__init__.py: v$(SCHEMA_VERSION)/GDML_$(SCHEMA_VERSION)/schema/gdml.xsd
	cd v$(SCHEMA_VERSION) ; \
	$(GENERATE_DS_EXEC) -m -f -o classes.py \
		--export='write literal etree' --root-element gdml \
		-s subclasses.py -u ../gdml_methods.py GDML_$(SCHEMA_VERSION)/schema/gdml.xsd

v$(SCHEMA_VERSION)/GDML_$(SCHEMA_VERSION)/schema/gdml.xsd: v$(SCHEMA_VERSION)/GDML_$(SCHEMA_VERSION).tar.gz
	cd v$(SCHEMA_VERSION) ; \
	tar xf GDML_$(SCHEMA_VERSION).tar.gz

v$(SCHEMA_VERSION)/GDML_$(SCHEMA_VERSION).tar.gz:
	mkdir -p v$(SCHEMA_VERSION)
	wget $(SCHEMA_URI) -O $@

