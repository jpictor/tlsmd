from django.test import TestCase
from mmLib.AtomMath import (
    calc_torsion_angle,
    calc_angle
)
from mmLib import Structure

class AtomMathTestCase(TestCase):
    def test_torsion_angle(self):
        """
        ## Example taken from 1HMP.pdb
        #ATOM     25  N   VAL A   8      55.799  56.415  16.693  1.00 25.51           N
        #ATOM     26  CA  VAL A   8      55.049  57.431  15.929  1.00 20.42           C
        #ATOM     27  C   VAL A   8      55.655  57.849  14.605  1.00 21.66           C
        #ATOM     28  O   VAL A   8      56.846  58.112  14.504  1.00 31.38           O
        #ATOM     29  CB  VAL A   8      54.697  58.659  16.709  1.00 16.90           C
        #ATOM     30  CG1 VAL A   8      54.131  59.664  15.699  1.00 19.06           C
        #ATOM     31  CG2 VAL A   8      53.640  58.304  17.738  1.00 14.10           C
        #ATOM     32  N   ILE A   9      54.810  57.974  13.593  1.00 20.18           N
        #ATOM     33  CA  ILE A   9      55.221  58.358  12.242  1.00 16.49           C
        #ATOM     34  C   ILE A   9      54.461  59.575  11.722  1.00 28.07           C
        #ATOM     35  O   ILE A   9      53.439  59.455  11.009  1.00 31.82           O
        #ATOM     36  CB  ILE A   9      55.028  57.196  11.301  1.00 13.73           C
        #ATOM     37  CG1 ILE A   9      55.941  56.045  11.712  1.00 20.33           C
        #ATOM     38  CG2 ILE A   9      55.327  57.611   9.860  1.00 13.91           C
        #ATOM     39  CD1 ILE A   9      55.871  54.892  10.733  1.00 21.80           C
        #ATOM     40  N   SER A  10      54.985  60.748  12.087  1.00 30.09           N
        """
        a1 = Structure.Atom(x=0.0, y=-1.0, z=0.0)
        a2 = Structure.Atom(x=0.0, y=0.0,  z=0.0)
        a3 = Structure.Atom(x=1.0, y=0.0,  z=0.0)
        #a4 = Structure.Atom(x=1.0, y=1.0,  z=-1.0)
        a4 = Structure.Atom(res_name='GLY', x=1.0, y=1.0,  z=-1.0)
        # PHI: C'-N-CA-C'
        a1 = Structure.Atom(x=55.655, y=57.849, z=14.605, res_name='VAL')
        a2 = Structure.Atom(x=54.810, y=57.974, z=13.593, res_name='ILE')
        a3 = Structure.Atom(x=55.221, y=58.358, z=12.242, res_name='ILE')
        a4 = Structure.Atom(x=54.461, y=59.575, z=11.722, res_name='ILE')
        #print "PHI: %.3f" % calc_torsion_angle(a1, a2, a3, a4)
        # PSI: N-CA-C'-N
        a1 = Structure.Atom(x=54.810, y=57.974, z=13.593, res_name='ILE')
        a2 = Structure.Atom(x=55.221, y=58.358, z=12.242, res_name='ILE')
        a3 = Structure.Atom(x=54.461, y=59.575, z=11.722, res_name='ILE')
        a4 = Structure.Atom(x=54.985, y=60.748, z=12.087, res_name='SER')
        #print "PSI: %.3f" % calc_torsion_angle(a1, a2, a3, a4)
        #print "="*40
        #print "a1:", a1.position
        #print "calc_angle:", calc_angle(a1, a2, a3)
        #print "calc_torsion_angle:", calc_torsion_angle(a1, a2, a3, a4)
