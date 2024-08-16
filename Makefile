DOD_PDF=doc/ZeroTrustOverlays-2024Feb.pdf
DOD_MAPPINGS=dod-mappings.yaml
DOD_SUB_MAPPINGS=dod-sub-mappings.yaml

CNSWP=cnswp-v2-controls.yaml

NIST_PREFIX=NIST/oscal-content/nist.gov/SP800-53/rev5/json
NIST_SRC=$(NIST_PREFIX)/NIST_SP-800-53_rev5_catalog.json

NIST_LOW=$(NIST_PREFIX)/NIST_SP-800-53_rev5_LOW-baseline_profile.json
NIST_MODERATE=$(NIST_PREFIX)/NIST_SP-800-53_rev5_MODERATE-baseline_profile.json
NIST_HIGH=$(NIST_PREFIX)/NIST_SP-800-53_rev5_HIGH-baseline_profile.json

NIST_DOD=nist-sp-800-53-rev5-dod.json
NIST_EXT=nist-sp-800-53-rev5-extended.json
NIST_EXT_YAML=$(patsubst %.json, %.yaml, $(NIST_EXT))
DOD_VIS=dod-vis.html
NIST_VIS=nist-vis.html

vis:	## Generate a visualization of controls by pillar
vis:	$(NIST_VIS) $(DOD_VIS)

$(NIST_VIS):	$(NIST_EXT) ./gen-dod-profiles.py $(MAKEFILE_LIST)
	./gen-dod-profiles.py -f $< -b $(NIST_LOW) -b $(NIST_MODERATE) -b $(NIST_HIGH) -V -g > $@

$(DOD_VIS):	$(NIST_EXT) ./gen-dod-profiles.py $(MAKEFILE_LIST)
	./gen-dod-profiles.py -f $< -V -g > $@

$(NIST_EXT_JSON):	$(NIST_EXT)
	yq -o json $< > $@

generate:	## Generate OSCAL profiles for each DoD pillar
generate:	$(NIST_EXT)
	./gen-dod-profiles.py -f $< -p dod-profile

resolved:	## Generate resolved OSCAL catalogs for each DoD pillar
resolved:	$(NIST_EXT)
	./gen-dod-profiles.py -f $< -p dod-profile-resolved -r

merge:	## Merge the DoD and CNSWP mappings into NIST controls
merge:	$(NIST_EXT)

yaml:	## Generate a YAML version of the NIST extended controls
yaml:	$(NIST_EXT_YAML)

$(NIST_EXT_YAML):	$(NIST_EXT)
	yq -p json $< -o yaml > $@

$(NIST_EXT):	$(NIST_DOD) $(CNSWP)
	./merge-cnswp.py -f $(NIST_DOD) -c $(CNSWP) > $@

nist-dod:	$(NIST_DOD)

$(NIST_DOD):	$(NIST_SRC) $(DOD_MAPPINGS) $(DOD_SUB_MAPPINGS)
	./merge-dod.py -f $(NIST_SRC) -d $(DOD_MAPPINGS) -s $(DOD_SUB_MAPPINGS) > $@

dod:	## Extract the DoD mappings from the PDF
dod:	$(DOD_MAPPINGS) $(DOD_SUB_MAPPINGS)

$(DOD_MAPPINGS):	$(DOD_PDF) dod-extractor.py
	./dod-extractor.py -f $< > $@

$(DOD_SUB_MAPPINGS):	$(DOD_PDF) dod-extractor.py
	./dod-extractor.py -f $< -s > $@

clean:	## Remove generated files
	rm -f $(DOD_MAPPINGS)
	rm -f $(DOD_SUB_MAPPINGS)
	rm -f $(NIST_DOD)
	rm -f $(NIST_EXT)
	rm -f $(NIST_EXT_YAML)
	rm -f $(DOD_VIS)
	rm -f $(NIST_VIS)
	rm -f dod-profile-*.yaml

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' \
	$(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
