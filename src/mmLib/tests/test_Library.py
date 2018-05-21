import os
from unittest import skip
from django.test import TestCase
from mmLib.Library import library_get_element_desc, ELEMENT_CIF_FILE


class LibraryTestCase(TestCase):
    def test_library_get_element_desc(self):
        h = library_get_element_desc("H")

    def test_element_file(self):
        for cif_data in ELEMENT_CIF_FILE:
            if len(cif_data.name) == 1:
                print '    "%s" : True, "%s" : True,' % (cif_data.name, cif_data.name.lower())
            else:
                print '    "%s": True, "%s": True, "%s": True,' % (cif_data.name, cif_data.name.lower(), cif_data.name.upper())
