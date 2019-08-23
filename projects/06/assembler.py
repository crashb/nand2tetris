from argparse import ArgumentParser
from pathlib import Path


A_TOKEN = '@'
L_START_TOKEN = '('
DEST_TOKEN = '='
JUMP_TOKEN = ';'
JUMPS = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}
COMPS = {
    '0':   '101010',
    '1':   '111111',
    '-1':  '111010',
    'D':   '001100',
    'A':   '110000',
    '!D':  '001101',
    '!A':  '110001',
    '-D':  '001111',
    '-A':  '110011',
    'D+1': '011111',
    'A+1': '110111',
    'D-1': '001110',
    'A-1': '110010',
    'D+A': '000010',
    'D-A': '010011',
    'A-D': '000111',
    'D&A': '000000',
    'D|A': '010101'
}
SYMBOLS = {
    'SP':     0,
    'LCL':    1,
    'ARG':    2,
    'THIS':   3,
    'THAT':   4,
    'R0':     0,
    'R1':     1,
    'R2':     2,
    'R3':     3,
    'R4':     4,
    'R5':     5,
    'R6':     6,
    'R7':     7,
    'R8':     8,
    'R9':     9,
    'R10':    10,
    'R11':    11,
    'R12':    12,
    'R13':    13,
    'R14':    14,
    'R15':    15,
    'SCREEN': 16384,
    'KBD':    24576
}
VAR_SYMBOL_POS = 16


def add_var_symbol(name):
    global VAR_SYMBOL_POS
    SYMBOLS[name] = VAR_SYMBOL_POS
    VAR_SYMBOL_POS += 1
    if VAR_SYMBOL_POS >= SYMBOLS['SCREEN']:
        raise MemoryError("Out of memory - allocating new variables would write to the screen")
    return SYMBOLS[name]


def is_a_instruction(inst):
    return inst[0] == A_TOKEN


def is_l_instruction(inst):
    return inst[0] == L_START_TOKEN


def assemble_a_instruction(inst):
    if inst[1:] in SYMBOLS:
        a_val = SYMBOLS[inst[1:]]
    else:
        try:
            a_val = int(inst[1:])
        except ValueError:
            a_val = add_var_symbol(inst[1:])
    return '{0:016b}'.format(a_val)


def c_instruction_dest_bits(inst):
    if DEST_TOKEN in inst:
        dest = inst.split(DEST_TOKEN)[0]
        bits = ('A' in dest, 'D' in dest, 'M' in dest)
    else:  # no dest
        bits = (False, False, False)
    return ''.join(['1' if b else '0' for b in bits])


def c_instruction_jump_bits(inst):
    if JUMP_TOKEN in inst:
        jump = inst.split(JUMP_TOKEN)[1]
        try:
            return JUMPS[jump]
        except KeyError as e:  # invalid jump code
            print(e)
    return '000'  # no jump or invalid jump


def c_instruction_a_and_c_bits(inst):
    if DEST_TOKEN in inst:
        comp_jump = inst.split(DEST_TOKEN)[1]
    else:
        comp_jump = inst
    if JUMP_TOKEN in inst:
        comp = comp_jump.split(JUMP_TOKEN)[0]
    else:
        comp = comp_jump

    if 'M' in comp:
        a_bit = '1'
        comp = comp.replace('M', 'A')
    else:
        a_bit = '0'

    try:
        return a_bit + COMPS[comp]
    except KeyError as e:  # invalid computation
        print(e)
        return a_bit + '000000'


def assemble_c_instruction(inst):
    return '111' + c_instruction_a_and_c_bits(inst) + c_instruction_dest_bits(inst) + c_instruction_jump_bits(inst)


def assemble_instruction(inst):
    if is_a_instruction(inst):
        return assemble_a_instruction(inst)
    else:
        return assemble_c_instruction(inst)


def assemble(assembly):
    return [assemble_instruction(line) + '\n' for line in assembly if not is_l_instruction(line)]


def clean_assembly(assembly):
    return [line.split('//')[0].strip() for line in assembly if line.split('//')[0].strip() != '']


def load_symbols(assembly):
    pos = 0
    for line in assembly:
        if is_l_instruction(line):
            SYMBOLS[line[1:-1]] = pos
        else:
            pos += 1


def assemble_file(input_file, output_file):
    with open(input_file, 'r') as f:
        assembly = [line.strip() for line in f.readlines()]
    cleaned = clean_assembly(assembly)
    load_symbols(cleaned)

    machine_code = assemble(cleaned)
    with open(output_file, 'w') as f:
        f.writelines(machine_code)


if __name__ == "__main__":
    ap = ArgumentParser(description='Assemble a .asm file to a .hack file.')
    # noinspection PyTypeChecker
    ap.add_argument('input', type=Path)
    args = ap.parse_args()
    assemble_file(args.input, args.input.with_suffix('.hack'))
