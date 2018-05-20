import os
import pprint
from django.test import TestCase
from mmLib.CIF import CIFFile, Lexer, formatMessage, L_EOF
from mmLib.Library import MMLIB_MONOMER_DATA_PATH, ELEMENT_DATA_PATH

dir_path = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(dir_path, 'PDB', '1HTB.cif')


class CIFTestCase(TestCase):
    def test_lexer(self):
        f = open(test_file)
        lexer = Lexer(f, test_file)
        while True:
            token = lexer.next_token()
            if token.type is L_EOF:
                break
            #print formatMessage(test_file, token.line, "%s: %s" % (token.type, token.value))

        f.close()

    def test_parser(self):
        cif = CIFFile()
        cif.load_file(test_file)
        #print "%d data blocks" % len(cif.data_blocks)
        for db in cif.data_blocks:
            pass
            #print "%s: %d tags, %d tables" % (db.name, len(db.tags), len(db.tables))
            #pprint.pprint(db.tags)
