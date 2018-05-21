import os
import sys
import numpy
from unittest import skip
from django.test import TestCase
from mmLib.TLS import TLSGroup


class TLSTestCase(TestCase):
    def test_tls_group(self):
        tls = TLSGroup()
        tls.name = "All protein"
        tls.set_origin(18.885, 49.302, 13.315)
        tls.set_T(0.0263, 0.0561, 0.0048, -0.0128, 0.0065, -0.0157)
        tls.set_L(0.9730, 5.1496, 0.8488,  0.2151,-0.1296,  0.0815)
        tls.set_S(0.0007, 0.0281, 0.0336, -0.0446,-0.2288, -0.0551, 0.0487, 0.0163)
        print tls
        print "eigenvalues(T)"
        print numpy.linalg.eig(tls.T)
        print "eigenvalues(L)"
        print numpy.linalg.eig(tls.L)
