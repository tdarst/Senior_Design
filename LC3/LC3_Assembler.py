import parselib
import utils
import types
from Class_Line import Line

line = Class_Line()

KEY_ADDRESS = utils.KEY_ADDRESS
KEY_OPCODE = utils.KEY_OPCODE
KEY_OPERANDS = utils.KEY_OPERANDS
KEY_LABELS = utils.KEY_LABELS

PARSE_DICT = {
    'BR'   : parselib.parse_br,
    'BRn'  : parselib.parse_br,
    'BRz'  : parselib.parse_br,
    'BRp'  : parselib.parse_br,
    'BRnz' : parselib.parse_br,
    'BRnp' : parselib.parse_br,
    'BRzp' : parselib.parse_br,
    'BRnzp': parselib.parse_br,

    'ADD' : parselib.parse_add,
    'LD'  : parselib.parse_ld,
    'ST'  : parselib.parse_st,
    'JSR' : parselib.parse_jsr,
    'JSRR': parselib.parse_jsrr,
    'AND' : parselib.parse_and,
    'LDR' : parselib.parse_ldr,
    'STR' : parselib.parse_str,
    'RTI' : parselib.parse_rti,
    'NOT' : parselib.parse_not,
    'LDI' : parselib.parse_ldi,
    'STI' : parselib.parse_sti,
    'JMP' : parselib.parse_jmp,
    'RET' : parselib.parse_ret,
    'LEA' : parselib.parse_lea,

    'TRAP': parselib.parse_trap,
    'GETC': parselib.parse_explicit_trap,
    'OUT' : parselib.parse_explicit_trap,
    'PUTS': parselib.parse_explicit_trap,
    'IN'  : parselib.parse_explicit_trap,
    'HALT': parselib.parse_explicit_trap,

    '.ORIG': parselib.parse_orig,
    '.END' : parselib.parse_end,
    '.FILL': parselib.parse_fill,
    '.BLKW': parselib.parse_blkw,
    '.STRINGZ': parselib.parse_stringz
}

def create_opcode_token_object(tok: str) -> object:
    OPCODE_LENGTH = 4 
    TOK_TYPE_OPCODE = 'opcode'
    int_value = utils.OPCODE[tok]
    hex_value = hex(int_value)
    bin_value = utils.int_to_bin(int_value).zfill(OPCODE_LENGTH)
    obj = types.SimpleNamespace(
        token = tok,
        tok_type = TOK_TYPE_OPCODE,
        int_val = int_value,
        hex_val = hex_value,
        bin_val = bin_value
    )

    return obj

def create_register_token_object(tok: str) -> object:
    REGISTER_LENGTH = 3
    TOK_TYPE_REGISTER = 'register'
    int_value = utils.REGISTERS[tok]
    hex_value = hex(int_value)
    bin_value = utils.int_to_bin(int_value).zfill(REGISTER_LENGTH)
    obj = types.SimpleNamespace(
        token = tok,
        tok_type = TOK_TYPE_REGISTER,
        int_val = int_value,
        hex_val = hex_value,
        bin_val = bin_value
    )

    return obj

def create_label_token_object(tok: str, label_lookup: dict) -> object:
    TOK_TYPE_LABEL = 'label'
    label_address = label_lookup[tok]
    int_value = label_address
    hex_value = hex(label_address)
    bin_value = utils.int_to_bin(int_value)
    obj = types.SimpleNamespace(
        token = tok,
        address = label_address,
        tok_type = TOK_TYPE_LABEL,
        int_val = int_value,
        hex_val = hex_value,
        bin_val = bin_value
    )

def create_imm5_token_object(tok: str) -> object:
    TOK_TYPE_IMM5 = 'imm5'

def createTokenObject(tok: str) -> object:
    int_value = utils.overall_dictionary[tok]
    hex_value = hex(int_value)
    bin_value = utils.int_to_bin(int_value)
    obj = types.SimpleNamespace(
        token = tok,
        int_val = int_value,
        hex_val = hex_value,
        bin_val = bin_value
    )

def pass1(code_to_parse: str) -> dict:

    # Program Counter defaults to starting at 0
    address_counter = 0x0

    symbol_table = {
        # address : {opcode : opcode,
        #            operands : [operand1, operand2, etc] 
        #            unresolved: [var1, label1]}
    }

    label_lookup = {}

    solo_label = None
    
    # Gets rid of tabs and newlines
    for line in code_to_parse.replace("\t", " ").split("\n"):
        
        # Gets rid of comments
        line = line.split(";")[0].strip()

        # Get parts of line as a list of tokens
        tokens = line.replace(',','').split(' ')

        # If line is blank
        if not line:
            continue

        # Start address counter at .ORIG
        elif '.ORIG' in line:
            # add .ORIG to symbol table
            address_counter = int(line.split(' ')[1], 16)

        # If .END is reached then break
        elif '.END' in line:
            break

        # If label is solo
        elif tokens[0] is tokens[-1] \
            and tokens[0] not in utils.overall_dictionary:
            solo_label = tokens[0]

        # Any other line
        else:
            # Get parts of line as a list of tokens
            tokens = line.replace(',','').split(' ')

            # If there is a solo label in the last line, add it to the current
            if solo_label:
                tokens.insert(0, solo_label)
                solo_label = None

            # Find the opcode, save it's name and it's index so it can be used as a dividing line for parsing
            find_opcode = next(((token, tokens.index(token)) for token in tokens if token in utils.opcode_dictionary))
            opcode = find_opcode[0]
            opcode_index = find_opcode[1]

            # Operands are all tokens occurring after the opcode,
            # Labels are all tokens occurring before the opcode
            operands = [token for token in tokens[opcode_index+1:]]
            labels   = [token for token in tokens[:opcode_index]]

            # Create a key value pair of the hex'd address and the tokens in the line.
            address = hex(address_counter)
            symbol_table[address] = {
                KEY_ADDRESS: address,
                KEY_OPCODE : opcode,
                KEY_OPERANDS : operands,
                KEY_LABELS : labels
            }

            if labels:
                for label in labels:
                    label_lookup.update({label : address})
            
            # Increment the address_counter
            address_counter += 0x1

    obj_symbol_table = [Line(line, label_lookup) for line in symbol_table]
    return obj_symbol_table, label_lookup

def pass2(symbol_table, label_lookup):
    machine_code = ''
    for address, tokens in symbol_table.items():
        opcode = tokens[KEY_OPCODE]
        bin_string = parselib.PARSE_DICT[opcode](address, tokens, label_lookup)
        machine_code += f"{bin_string}\n"

    return machine_code.rstrip('\n')

def main():
    addTest = r'LC3\Test_Code\add_test.txt'
    debugString = r'LC3\Test_Code\Assembly_Test.txt'
    debugString2 = r"LC3\Test_Code\2048.asm"

    path = addTest

    def runBothPasses():
        with open(path, 'r') as file:
            readLines = file.read()
            return pass2(pass1(readLines))

    def runPass1():
        with open(path, 'r') as file:
            readLines = file.read()
            return pass1(readLines) 

    symbol_table, label_lookup = runPass1()
    print(pass2(symbol_table, label_lookup))
    
    #unitTest_Assembly_Test(runBothPasses())

main()