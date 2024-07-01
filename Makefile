DOD_PDF=doc/ZeroTrustOverlays-2024Feb.pdf
DOD_MAPPINGS=dod-mappings.yaml

CNSWP=cnswp-v2-controls.yaml

NIST_SRC=NIST/oscal-content/nist.gov/SP800-53/rev5/yaml/NIST_SP-800-53_rev5_catalog.yaml
NIST_DOD=nist-sp-800-53-rev5-dod.yaml
NIST_EXT=nist-sp-800-53-rev5-extended.yaml

generate:	## Generate OSCAL profiles for each DoD pillar
generate:	$(NIST_EXT)
	./gen-dod-profiles.py -f $< -p dod-profile

merge:	## Merge the DoD and CNSWP mappings into NIST controls
merge:	$(NIST_EXT)

$(NIST_EXT):	$(NIST_DOD) $(DOD_MAPPINGS)
	./merge-cnswp.py -f $(NIST_DOD) -c $(CNSWP) > $@

$(NIST_DOD):	$(NIST_SRC) $(DOD_MAPPINGS)
	./merge-dod.py -f $(NIST_SRC) -d $(DOD_MAPPINGS) > $@

dod:	## Extract the DoD mappings from the PDF
dod:	$(DOD_MAPPINGS)

$(DOD_MAPPINGS):	$(DOD_PDF)
	./dod-extractor.py -f $< > $@

clean:	## Remove generated files
	rm -f $(DOD_MAPPINGS)
	rm -f $(NIST_DOD)
	rm -f $(NIST_DST)

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' \
	$(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
