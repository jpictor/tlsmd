import os
import sys
from unittest import skip
from django.test import TestCase
from mmLib.PDB import PDBFile

dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(dir_path, 'PDB', '1HTB.pdb')


class PDBTestCase(TestCase):
    def test_load_and_save(self):
        pdbfil = PDBFile()
        pdbfil.load_file(test_file)
        pdbfil.save_file(sys.stdout)
