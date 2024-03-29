import unittest
from . import Class_TestVars_asemlib
from ...Supporting_Libraries import asemlib

class TestParseJsrr(unittest.TestCase):
    
    def setUp(self):
        super().setUp()
        self.test_vars = Class_TestVars_asemlib.TestVars()

    # Test
    # JSRR R1
    def test_Given_JSRR_R1_Produce_Correct_BinString(self):
        test_vars = self.test_vars
        address = test_vars.ADDRESS_0X3000
        tokens = test_vars.generate_tester_symbol_table(opcode=test_vars.TOK_JSRR, 
                                                        operands=[test_vars.TOK_R1], 
                                                        labels=[])
        
        self.assertEqual(asemlib.asem_jsrr(address, tokens, []), '0100000001000000')