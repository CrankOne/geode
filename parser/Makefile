# Makefile used to generate the GDML parser based on XSD schema of certain
# version via the generateDS util (see: http://www.davekuhlman.org/generateDS.html)

SCHEMA_VERSION=3_1_6
GENERATE_DS_EXEC=generateDS.py

SCHEMA_URI="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/downloads/GDML_$(SCHEMA_VERSION).tar.gz"

all: gdmlClasses.py

gdmlClasses.py: schema-$(SCHEMA_VERSION)/gdml.xsd
	mkdir -p parser_$(SCHEMA_VERSION)
	$(GENERATE_DS_EXEC) -m -f -o parser_$(SCHEMA_VERSION)/gdmlClasses.py \
		--export='write literal etree' --root-element gdml \
		-s parser_$(SCHEMA_VERSION)/gdmlSubclasses.py $<

schema-$(SCHEMA_VERSION)/gdml.xsd: GDML_$(SCHEMA_VERSION).tar.gz
	tar xf $<
	ln -fs GDML_$(SCHEMA_VERSION)/schema schema-$(SCHEMA_VERSION)

GDML_$(SCHEMA_VERSION).tar.gz:
	wget $(SCHEMA_URI) -O $@

