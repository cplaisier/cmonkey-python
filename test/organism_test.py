"""organism_test.py - unit tests for organism module

This file is part of cMonkey Python. Please see README and LICENSE for
more information and licensing details.
"""
import unittest
from util import DelimitedFile
from organism import KeggCodeMapper, GoTaxonomyMapper
from organism import OrganismFactory

TAXONOMY_FILE_PATH = "testdata/KEGG_taxonomy"
PROT2TAXID_FILE_PATH = "testdata/proteome2taxid"


# pylint: disable-msg=R0904
class KeggOrganismCodeMapperTest(unittest.TestCase):
    """Test class for KeggCodeMapper"""

    def test_get_existing_organism(self):
        """retrieve existing organism"""
        dfile = DelimitedFile.read(TAXONOMY_FILE_PATH, sep='\t',
                                   has_header=True, comment='#')
        mapper = KeggCodeMapper(dfile)
        self.assertEquals('Helicobacter pylori 26695',
                          mapper.get_organism('hpy'))

    def test_get_non_existing_organism(self):
        """retrieve non-existing organism"""
        dfile = DelimitedFile.read(TAXONOMY_FILE_PATH, sep='\t',
                                   has_header=True, comment='#')
        mapper = KeggCodeMapper(dfile)
        self.assertIsNone(mapper.get_organism('nope'))


class GoTaxonomyMapperTest(unittest.TestCase):  # pylint: disable-msg=R0904
    """Test class for get_go_taxonomy_id"""

    def test_get_existing(self):
        """retrieve an existing id"""
        dfile = DelimitedFile.read(PROT2TAXID_FILE_PATH, sep='\t',
                                   has_header=False)
        mapper = GoTaxonomyMapper(dfile)
        self.assertEquals('64091',
                          mapper.get_taxonomy_id('Halobacterium salinarium'))

    def test_get_non_existing(self):
        """retrieve None for a non-existing organism"""
        dfile = DelimitedFile.read(PROT2TAXID_FILE_PATH, sep='\t',
                                   has_header=False)
        mapper = GoTaxonomyMapper(dfile)
        self.assertIsNone(mapper.get_taxonomy_id('does not exist'))


class MockKeggOrganismMapper:
    """mock KEGG organism mapper"""

    def get_organism(self, _):
        """returns an organism for the given code"""
        return "KEGG organism"


class MockRsatOrganismMapper:
    """mock RSAT organism mapper"""

    def get_organism(self, _):
        """returns an organism for a KEGG organism"""
        return "RSAT organism"


class MockGoTaxonomyMapper:
    """mock GO taxonomy mapper"""

    def get_taxonomy_id(self, _):
        """returns a taxonomy id for an RSAT organism"""
        return "GO taxonomy id"


class OrganismTest(unittest.TestCase):  # pylint: disable-msg=R0904
    """Test class for Organism"""

    def test_create(self):
        """tests the create function"""
        factory = OrganismFactory(MockKeggOrganismMapper(),
                                  MockRsatOrganismMapper(),
                                  MockGoTaxonomyMapper())
        organism = factory.create('hpy')
        self.assertEquals('hpy', organism.code)
        self.assertEquals('KEGG organism', organism.kegg_organism)
        self.assertEquals('RSAT organism', organism.rsat_organism)
        self.assertEquals('GO taxonomy id', organism.go_taxonomy_id)
        self.assertTrue(organism.is_prokaryote())
        self.assertFalse(organism.is_eukaryote())
