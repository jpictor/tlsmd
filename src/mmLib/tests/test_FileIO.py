import os
import sys
from unittest import skip
from django.test import TestCase
from mmLib.FileIO import LoadStructure, SaveStructure

dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(dir_path, 'PDB', '1HTB.pdb')


class FileIOTestCase(TestCase):
    def test_load_and_save_structure(self):
        struct = LoadStructure(fil = test_file)
        SaveStructure(fil=sys.stdout, struct=struct)
