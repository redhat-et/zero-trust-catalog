DOD_PDF=doc/ZeroTrustOverlays-2024Feb.pdf
DOD_MAPPINGS=dod-mappings.yaml

NIST_SRC=NIST/oscal-content/nist.gov/SP800-53/rev5/yaml/NIST_SP-800-53_rev5_catalog.yaml
NIST_DST=nist-sp-800-53-rev5-extended.yaml

merge:	## Merge the DoD mappings into NIST controls
	./merge-mappings.py -f $(NIST_SRC) -d $(DOD_MAPPINGS)

dod:	## Extract the DoD mappings from the PDF
dod:	$(DOD_MAPPINGS)

$(DOD_MAPPINGS):	$(DOD_PDF)
	./dod-extractor.py -f $< > $@

clean:	## Remove generated files
	rm -f $(DOD_MAPPINGS)

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' \
	$(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
