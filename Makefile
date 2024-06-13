DOD_PDF=doc/ZeroTrustOverlays-2024Feb.pdf
DOD_MAPPINGS=dod-mappings.yaml

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
