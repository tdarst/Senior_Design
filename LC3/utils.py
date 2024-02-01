IMM5_INT_RANGE = range(-16, 15)

# 3 bits
REGISTERS = {
    'R0':0x0,
    'R1':0x1,
    'R2':0x2,
    'R3':0x3,
    'R4':0x4,
    'R5':0x5,
    'R6':0x6,
    'R7':0x7
}

# 8 bits
TRAPS = {
    'GETC': 0x20,
    'OUT' : 0x21,
    'PUTS': 0x22,
    'IN'  : 0x23,
    'HALT': 0x25
} #PUTS, GETC, etc. 

# 4 bits
OPCODE = {
    'BR'   : 0x0,
    'BRn'  : 0x0,
    'BRz'  : 0x0,
    'BRp'  : 0x0,
    'BRnz' : 0x0,
    'BRnp' : 0x0,
    'BRzp' : 0x0,
    'BRnzp': 0x0,

    'ADD' : 0x1,
    'LD'  : 0x2,
    'ST'  : 0x3,
    'JSR' : 0x4,
    'JSRR': 0x4,
    'AND' : 0x5,
    'LDR' : 0x6,
    'STR' : 0X7,
    'RTI' : 0X8,
    'NOT' : 0x9,
    'LDI' : 0xA,
    'STI' : 0xB,
    'JMP' : 0xC,
    'RET' : 0xC,
    'RES' : 0xD,
    'LEA' : 0xE,
    'TRAP': 0xF,

    **TRAPS # includes the TRAPS dictionary
}

PSEUDOS = {
    '.ORIG'   : None,
    '.END'    : None,
    '.FILL'   : None,
    '.BLKW'   : None,
    '.STRINGZ': None
}

overall_dictionary = {
    **OPCODE,
    **REGISTERS,
    **PSEUDOS
}

opcode_dictionary = {
    **OPCODE,
    **PSEUDOS
}

KEY_ADDRESS = 'address'
KEY_OPCODE = 'opcode'
KEY_OPERANDS = 'operands'
KEY_LABELS = 'labels'

def int_to_bin(num: int) -> str:
    return bin(num)[2:]

def imm5_to_int(imm_str: str) -> int:
    return int(imm_str.replace('#', ''))

def hex_to_int(hex_str: str) -> int:
    return int(hex_str, 16)

def is_register(tok: str) -> bool:
    return tok in REGISTERS

#TODO: FIX THIS RETURN
def is_imm5(tok: str) -> bool:
    return tok.startswith('#')
    
def is_label(tok: str, label_lookup: dict) -> bool:
    tok_is_label = tok in label_lookup
    return tok_is_label

def is_offset6(tok: str) -> bool: pass     

def calc_offset(label_address: str, current_address: str) -> str:
    label_address = hex_to_int(label_address)
    current_address = hex_to_int(current_address)
    return label_address - current_address - 1