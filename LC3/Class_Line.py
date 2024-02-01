import utils

class Line:
    def __init__(self, line, label_lookup):
        self.address = [x for x in line.keys()][0]
        self.opcode = line[utils.KEY_OPCODE]
