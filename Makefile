#! /usr/bin/env gmake
# not that you need to define targets with wildcard first
# so `make` knows about targets, implicit targets
# % do not work on their own with just make
DEP1 = $(wildcard propertyLineViolations/*.csv)
DEP2 = $(wildcard 75FeetViolations/*.csv)
TAR1 = $(DEP1:.csv=.html)
TAR2 = $(DEP2:.csv=.html)

.PHONY: all clean

all: $(TAR1) $(TAR2) 

propertyLineViolations/%.html : propertyLineViolations/%.csv
	./trimHeader.sh metaData.yaml "$<" > "${<}_trimmed"
	python createPlots.py  "${<}_trimmed" "metaData.yaml" True

75FeetViolations/%.html : 75FeetViolations/%.csv
	./trimHeader.sh metaData.yaml "$<" > "${<}_trimmed"
	python createPlots.py "${<}_trimmed" "metaData.yaml" False

clean:
	rm -f $(TAR1)
	rm -f $(TAR2)
