import os
from unittest import skip
from django.test import TestCase
from mmLib import FileIO

dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(dir_path, 'PDB', '1HTB.cif')


class GeometryDictTestCase(TestCase):
    @skip('seems to be broke')
    def test_geometry_dict(self):
        struct = FileIO.LoadStructure(fil=test_file)
        print "Structure Loaded"
        gdict = XYZDict(2.0)
        cnt = 0
        for atm in struct.iter_atoms():
            gdict.add(atm.position, atm)
            cnt += 1
        print "Hashed %d Atoms" % (cnt)
        cnt = 0
        for (p1, atm1),(p2,atm2), dist in gdict.iter_contact_distance(1.9):
            cnt += 1
        print "%d Bonds" % (cnt)
