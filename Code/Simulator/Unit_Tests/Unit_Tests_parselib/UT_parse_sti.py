import unittest
from . import Class_TestVars_asemlib
from ...Supporting_Libraries import asemlib

class TestParseSti(unittest.TestCase):
    
    def setUp(self):
        super().setUp()
        self.test_vars = Class_TestVars_asemlib.TestVars()

    # Test
    # x3000 STI R1 NUM
    # x3001 NUM .FILL 0x3010
    def test_Given_STI_R1_LABEL_Offset_Positive_Produce_Correct_Binary_String(self):
        test_vars = self.test_vars
        address = test_vars.ADDRESS_0X3000
        tokens = test_vars.generate_tester_symbol_table(opcode=test_vars.TOK_STI, 
                                                        operands=[test_vars.TOK_R1, test_vars.TOK_LABEL_NUM], 
                                                        labels=[test_vars.TOK_LABEL_NUM])
        
        label_lookup = test_vars.generate_tester_label_lookup(label=test_vars.TOK_LABEL_NUM,
                                                              address=test_vars.ADDRESS_0X3001)
        
        self.assertEqual(asemlib.asem_sti(address, tokens, label_lookup), '1011001000000000')

    # Test
    # x3000 NUM .FILL 0x3010
    # x3001 STI R1 NUM
    def test_Given_STI_R1_LABEL_Offset_Negative_Produce_Correct_Binary_String(self):
        test_vars = self.test_vars
        address = test_vars.ADDRESS_0X3001
        tokens = test_vars.generate_tester_symbol_table(opcode=test_vars.TOK_STI, 
                                                        operands=[test_vars.TOK_R1, test_vars.TOK_LABEL_NUM], 
                                                        labels=[test_vars.TOK_LABEL_NUM])
        
        label_lookup = test_vars.generate_tester_label_lookup(label=test_vars.TOK_LABEL_NUM,
                                                              address=test_vars.ADDRESS_0X3000)
        
        self.assertEqual(asemlib.asem_sti(address, tokens, label_lookup), '1011001111111110')