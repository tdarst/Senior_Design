import unittest
import Class_TestVars
import parselib

class TestParseRet(unittest.TestCase):
    
    def setUp(self):
        super().setUp()
        self.test_vars = Class_TestVars.TestVars()

    # Test
    # x3000 NOT R1, R2
    def test_Given_RET_Produce_Correct_Binary_String(self):
        test_vars = self.test_vars
        address = test_vars.ADDRESS_0X3000
        tokens = test_vars.generate_tester_symbol_table(opcode=test_vars.TOK_RET, 
                                                        operands=[], 
                                                        labels=[])
        
        self.assertEqual(parselib.parse_ret(address, tokens, []), '1100000111000000')