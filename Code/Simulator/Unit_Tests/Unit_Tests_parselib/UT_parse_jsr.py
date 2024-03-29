import unittest
from . import Class_TestVars_asemlib
from ...Supporting_Libraries import asemlib

class TestParseJsr(unittest.TestCase):
    
    def setUp(self):
        super().setUp()
        self.test_vars = Class_TestVars_asemlib.TestVars()

    # Test
    # x3000 JSR LOOP
    # x3001 LOOP
    def test_Given_JSR_LABEL_Offset_Positive_Produce_Correct_BinString(self):
        test_vars = self.test_vars
        address = test_vars.ADDRESS_0X3000
        tokens = test_vars.generate_tester_symbol_table(opcode=test_vars.TOK_JSR, 
                                                        operands=[test_vars.TOK_LABEL_LOOP], 
                                                        labels=[test_vars.TOK_LABEL_LOOP])
        
        label_lookup = test_vars.generate_tester_label_lookup(label=test_vars.TOK_LABEL_LOOP,
                                                              address=test_vars.ADDRESS_0X3001)
        
        self.assertEqual(asemlib.asem_jsr(address, tokens, label_lookup), '0100100000000000')

    # Test
    # x3000 LOOP
    # x3001 JSR LOOP
    def test_Given_JSR_LABEL_Offset_Negative_Produce_Correct_BinString(self):
        test_vars = self.test_vars
        address = test_vars.ADDRESS_0X3001
        tokens = test_vars.generate_tester_symbol_table(opcode=test_vars.TOK_JSR, 
                                                        operands=[test_vars.TOK_LABEL_LOOP], 
                                                        labels=[test_vars.TOK_LABEL_LOOP])
        
        label_lookup = test_vars.generate_tester_label_lookup(label=test_vars.TOK_LABEL_LOOP,
                                                              address=test_vars.ADDRESS_0X3000)
        
        self.assertEqual(asemlib.asem_jsr(address, tokens, label_lookup), '0100111111111110')