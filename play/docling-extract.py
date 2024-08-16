#!/usr/bin/env python
#
# Experiment with using docling to extract markdown from
# the DoD ZeroTrustOverlays-2024Feb.pdf
#
# https://github.com/DS4SD/docling
#

from docling.document_converter import DocumentConverter
from docling.datamodel.document import InputDocument, ConvertedDocument
from docling.datamodel.settings import DocumentLimits
from pathlib import Path

source = "doc/Test.pdf"
converter = DocumentConverter()

# input = DocumentConversionInput.from_paths(
#     paths=[Path(source)],
#     limits=DocumentLimits(max_num_pages=90)
# )

input = InputDocument(Path(source), limits=DocumentLimits(max_num_pages=90))
doc = converter.process_document(input)
print(doc.to_ds_document().export_to_markdown())
