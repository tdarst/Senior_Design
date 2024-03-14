import os
from ..Supporting_Libraries import parselib, validlib, utils

KEY_OPCODE = utils.KEY_OPCODE
KEY_OPERANDS = utils.KEY_OPERANDS
KEY_LABELS = utils.KEY_LABELS

# ==============================================================================
# Name: ready_code_for_parsing
# Purpose: Takes all of the raw code and strips it of uneccesary elements such
#          as tabs, newlines, and comments. 
# ==============================================================================
def ready_code_for_parsing(code: str) -> str:
    # Get rid of all tabs and split the code into a list seperated by lines
    code_list = code.replace("\t", " ").split("\n")

    # Get rid of all comments left
    code_list_comments_removed = [line.split(";")[0].strip() 
                                  for line in code_list 
                                  if line.split(';')[0]]
    
    final_strip_pass = [x for x in code_list_comments_removed if x]
    
    return final_strip_pass

# ==============================================================================
# Name: check_if_solo_label
# Purpose: Check if a line is a solo label, and returns the label if it is,
#          returns None if not.
# ==============================================================================
def line_is_solo_label(tokens: list) -> str:
    is_solo_label = False
    if tokens[0] is tokens[-1] and tokens[0] not in utils.overall_dictionary:
        is_solo_label = True
    return is_solo_label

# ==============================================================================
# Name: find_opcode_in_tokens
# Purpose: Iterates through tokens, if opcode is found returns it and it's index
#          otherwise it returns None for opcode and 0 for index.
# ==============================================================================
def find_opcode_in_tokens(tokens: list) -> tuple[str, int]:
    # print(tokens)
    # asdf = next(((token, tokens.index(token)) for token in tokens if utils.lookup_all_caps(token, utils.opcode_dictionary)), (None, 0))
    # return asdf
    found_opcode = tokens[0]
    found_opcode_index = 0
    for token in tokens:
        if token.upper() in utils.opcode_dictionary:
            found_opcode = token
            found_opcode_index = tokens.index(token)
    return found_opcode, found_opcode_index

# ==============================================================================
# Name: generate_tokens
# Purpose: Take a string of assembly code and separate the tokens into list 
#          elements.
# ==============================================================================
def generate_tokens(line: str) -> list:
    split_line = line.replace(',',' ').split(' ')
    tokens_no_blanks = [item for item in split_line if item.strip()]
    return tokens_no_blanks

# ==============================================================================
# Name: update_label_lookup
# Purpose: Take a list of labels and address and update the label_lookup dict
#          with them
# ==============================================================================
def update_label_lookup(address: str, labels: list, label_lookup: dict) -> dict:
    [label_lookup.update({label:address}) for label in labels if labels]
    return label_lookup

# ==============================================================================
# Name: get_operands
# Purpose: Takes a list of tokens and the opcode index in that list and produces
#          from it, a list of operands.
# ==============================================================================
def get_operands(tokens: list, opcode_index: int) -> list:
    return [token for token in tokens[opcode_index+1:]]

# ==============================================================================
# Name: get_labels
# Purpose: Takes a list of tokens and the opcode index in that list and produces
#          from it, a list of labels.
# ==============================================================================
def get_labels(tokens: list, opcode_index: int) -> list:
    return [token for token in tokens[:opcode_index]]

# ==============================================================================
# Name: check_for_ORIG
# Purpose: Checks if opcode is .ORIG, if it is it sets the address counter
#          to the address specified by the operand following .ORIG
# ==============================================================================
def check_for_ORIG(address_counter: int, opcode: str, operands: list) -> tuple[int, bool]:
    if opcode == utils.ORIG_OPCODE_NAME:
        address_counter = utils.hex_to_int(operands[0])
    return address_counter

# ==============================================================================
# Name: pass1
# Purpose: Pass one of the assembler parses the raw assembly code and formats
#          each line into a dctionary symbol table. When a label declaration is
#          found, the label and address in which it's declared is added to a dict
#          called label_lookup to allow for easy offset calculation. The symbol
#          table and the label_lookup are returned to be used by pass2.
# ==============================================================================
def pass1(code_to_parse: str) -> tuple[dict, dict]:

    # Program Counter defaults to starting at 0
    address_counter = 0x0

    # Count lines for error output.
    line_counter = 0

    symbol_table = {
        # address : {opcode : [ops, pseudoOps, dots, etc.],
        #            operands : [registers, labels, strings, etc.] 
        #            labels: [label1, label2, etc.]}
    }

    label_lookup = {
        # label_name : label_address
    }
    
    solo_label = None

    for line in ready_code_for_parsing(code_to_parse):
        line_counter += 1
        if line and not line.startswith(';'):
            # Get parts of line as a list of tokens
            tokens = generate_tokens(line)

            # Check if line is a solo label
            if line_is_solo_label(tokens):
                solo_label = tokens[0]
                line_counter += 1
                continue

            # If there is a solo label in the last line, add it to the current
            elif solo_label:
                tokens.insert(0, solo_label)
                solo_label = None

            # Find the opcode, save it's name and it's index so it can be used as a dividing line for parsing
            opcode, opcode_index = find_opcode_in_tokens(tokens)

            # Operands are all tokens occurring after the opcode,
            # Labels are all tokens occurring before the opcode
            operands = get_operands(tokens, opcode_index)
            labels   = get_labels(tokens, opcode_index)

            # If .ORIG is in the line then set address_counter to it and don't increment address_counter.
            address_counter = check_for_ORIG(address_counter, opcode, operands)

            # Create a dictionary 
            # Key: line's hex address 
            # Values: token categories.
            address = hex(address_counter)
            symbol_table[line_counter] = {
                'address' : address,
                KEY_OPCODE : opcode,
                KEY_OPERANDS : operands,
                KEY_LABELS : labels
            }

            # Update label_lookup with any labels
            label_lookup = update_label_lookup(address, labels, label_lookup)
            
            # Increment the address_counter
            address_counter += 0x1

    return symbol_table, label_lookup

# ==============================================================================
# Name: pass2
# Purpose: In pass2, each symbol table entry is translated into it's equivalent
#          binary format by passing the opcode for each entry into a dictionary
#          that maps it's opcode string to it's respective parsing function. 
#          In doing this, labels that are used in operands are resolved so that
#          the simulator knows where to look for the label's value.
# ==============================================================================
def pass2(symbol_table: dict, label_lookup: dict) -> tuple[str, bool]:
    machine_code = ''
    error_string = ''
    for line_number, tokens in symbol_table.items():
        error_string = validlib.validate_line(line_number, tokens, label_lookup)
        
        if error_string:
            print(error_string)
            return error_string, True
        
        opcode = tokens[KEY_OPCODE]
        parse_func = utils.lookup_all_caps(opcode, parselib.PARSE_DICT)
        bin_string = parse_func(tokens['address'], tokens, label_lookup)
        
        machine_code += f"{bin_string}\n"

    return machine_code.rstrip('\n'), False

# ===============================================================================
# Name: main
# Purpose: Takes asm_path as a command line argument from runAssembler.py.
#          Runs pass1 and pass2 on the given file and then sends the output to
#          LC3_Bin_Files in LOCALAPPDATA. If no file is given then it just prints
#          a message letting the user know.
# ===============================================================================
def assemble(asm_path: str) -> tuple[str, bool]:
    if asm_path:
        with open(asm_path,'r') as asm_file:
            readLines = asm_file.read()

        symbol_table, label_lookup = pass1(readLines)
        assembler_return_string, error = pass2(symbol_table, label_lookup)
        
        return assembler_return_string, error
    
if __name__ == "__main__":
    file_path = r"C:\lc3_assembly_work\chatgptfactorial.asm"
    assemble(file_path)