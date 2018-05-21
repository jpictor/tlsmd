import os
import sys
import numpy
from unittest import skip
from django.test import TestCase
from mmLib.UnitCell import UnitCell


class UnitCellTestCase(TestCase):
    def test_triclinic_unit_cell(self):
        """
        TEST CASE: Triclinic unit cell
        """
        uc = UnitCell(7.877, 7.210, 7.891, 105.563, 116.245, 79.836)
        e = numpy.array([[1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [0.0, 0.0, 1.0]], float)

        print uc
        print "volume                   = ", uc.calc_v()
        print "cell volume              = ", uc.calc_volume()
        print "fractionalization matrix =\n", uc.calc_fractionalization_matrix()
        print "orthogonalization matrix =\n", uc.calc_orthogonalization_matrix()
        print "orth * e =\n", numpy.dot(uc.calc_orthogonalization_matrix(), e)
        print "calc_frac_to_orth"

        vlist = [
            numpy.array([0.0, 0.0, 0.0]),
            numpy.array([0.5, 0.5, 0.5]),
            numpy.array([1.0, 1.0, 1.0]),
            numpy.array([-0.13614, 0.15714, -0.07165])
        ]

        for v in vlist:
            ov = uc.calc_frac_to_orth(v)
            v2 = uc.calc_orth_to_frac(ov)
            print "----"
            print "    ",v
            print "    ",ov
            print "    ",v2
            print "----"

    def test_triclinic_reciprocal_unit_cell(self):
        """
        TEST CASE: Reciprocal of above unit cell
        """
        uc = UnitCell(7.877, 7.210, 7.891, 105.563, 116.245, 79.836)
        ruc = uc.calc_reciprocal_unit_cell()
        print ruc
        print "volume      = ", ruc.calc_v()
        print "cell volume = ", ruc.calc_volume()

    def test_orthogonal_space_symmetry_operations(self):
        """
        TEST CASE: Orthogonal space symmetry operations
        """
        unitx = UnitCell(
            a = 64.950,
            b = 64.950,
            c = 68.670,
            alpha = 90.00,
            beta = 90.00,
            gamma = 120.00,
            space_group = "P 32 2 1"
        )
        print unitx
        print
        for symop in unitx.space_group.iter_symops():
            print "Fractional Space SymOp:"
            print symop
            print "Orthogonal Space SymOp:"
            print unitx.calc_orth_symop(symop)
            print
