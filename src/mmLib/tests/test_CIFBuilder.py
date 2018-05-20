import os
from unittest import skip
from django.test import TestCase
from mmLib.CIFBuilder import CIFStructureBuilder
from mmLib.Library import MMLIB_MONOMER_DATA_PATH, ELEMENT_DATA_PATH

dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(dir_path, 'PDB', '1HTB.cif')


class CIFBuilderTestCase(TestCase):
    @skip('seems to be broke')
    def test_builder(self):
        csb = CIFStructureBuilder(fil=test_file)
        s = csb.struct
        #print s
