import os
from django.test import TestCase
from mmLib.Structure import Structure, Atom

dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(dir_path, 'PDB', '1HTB.cif')


class StructureTestCase(TestCase):
    def test_structure(self):
        struct = make_test_structure()

        for cx in struct.iter_chains():
            print "iter_chains: ",cx

        for fx in struct.iter_fragments():
            print "iter_fragments: ",fx
            for ax in fx.iter_all_atoms():
                print "iter_all_atoms: ",ax

        for ax in struct.iter_atoms():
            print "iter_atoms: ",ax

        struct.set_default_alt_loc("C")
        for ax in struct.iter_atoms():
            print "iter_atoms: ",ax


def make_test_structure():
    struct = Structure()
    for mx in xrange(1, 4):
        mid = str(mx)
        for cid in ["A", "B", "C", "D"]:
            for fx in xrange(1, 4):
                fid = str(fx)
                for name in ["N", "CA", "C", "O"]:
                    for alt_loc in ["A", "B", "C"]:
                        if alt_loc == "C" and name == "CA": continue
                        atm = Atom(
                            name = name,
                            alt_loc = alt_loc,
                            model = mid,
                            chain_id = cid,
                            res_name = "GLY",
                            fragment_id = fid)
                        struct.add_atom(atm)
    return struct
