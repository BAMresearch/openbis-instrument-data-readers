import pytest
from bam_masterdata.datamodel.object_types import ExperimentalStep
from bam_masterdata.logger import logger
from bam_masterdata.metadata.entities import CollectionType
from bam_masterdata.parsing import AbstractParser

from src.bam_upload_parsers import (
    DLSParser,
    IRParser,
    NMRParser,
    PlateReaderParser,
    SEMParser,
    TEMParser,
)


@pytest.mark.parametrize(
    "parser_class",
    [DLSParser, IRParser, NMRParser, PlateReaderParser, SEMParser, TEMParser],
    ids=lambda parser_class: parser_class.__name__,
)
def test_parser_basic(parser_class):
    """Load each parser and check empty input preserves collection contents."""
    parser = parser_class()
    assert isinstance(parser, AbstractParser)

    collection = CollectionType()
    parser.parse([], collection, logger)
    assert len(collection.attached_objects) == 0
    assert len(collection.relationships) == 0

    id1 = collection.add(ExperimentalStep(name="test"))
    id2 = collection.add(ExperimentalStep(name="test2"))
    collection.add_relationship(id1, id2)
    objects_before = collection.attached_objects.copy()
    relationships_before = collection.relationships.copy()

    parser.parse([], collection, logger)

    assert collection.attached_objects == objects_before
    assert collection.relationships == relationships_before
