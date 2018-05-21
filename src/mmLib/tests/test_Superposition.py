import os
import sys
import random
import numpy
import math
from unittest import skip
from django.test import TestCase
from mmLib import AtomMath, FileIO, Structure, Superposition

dir_path = os.path.dirname(os.path.realpath(__file__))
test_path = os.path.join(dir_path, 'PDB', '8rxn.pdb')


class SuperpositionTestCase(TestCase):
    def test_superposition(self):
        R = AtomMath.rmatrixu(numpy.array((0.0, 0.0, 1.0), float), math.pi/2.0)
        struct1 = FileIO.LoadStructure(fil=test_path)
        struct2 = FileIO.LoadStructure(fil=test_path)

        chn1 = struct1.get_chain("A")
        chn2 = struct2.get_chain("A")

        rc = lambda: 0.1 * (random.random() - 1.0)
        for atm in chn2.iter_atoms():
            atm.position = numpy.dot(R, atm.position) + numpy.array((rc(),rc(),rc()),float)

        alist = []
        for atm1 in chn1.iter_atoms():
            if atm1.name != "CA":
                continue
            atm2 = chn2.get_equivalent_atom(atm1)
            if atm2 == None: continue
            alist.append((atm1, atm2))

        sup = Superposition.SuperimposeAtoms(alist)

        R = sup.R
        Q = sup.Q
        print Q
        print R

        so = sup.src_origin
        do = sup.dst_origin

        sup1 = Structure.Structure(structure_id = "JMP1")
        for atm in chn1.iter_atoms():
            atm.position = numpy.dot(R, atm.position - so)
            sup1.add_atom(atm)
        FileIO.SaveStructure(fil="super1.pdb", struct=sup1)

        sup2 = Structure.Structure(structure_id = "JMP2")
        for atm in chn2.iter_atoms():
            atm.position = atm.position - do
            sup2.add_atom(atm)
        FileIO.SaveStructure(fil="super2.pdb", struct=sup2)
