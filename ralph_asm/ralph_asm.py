from ralph_asm.instructions import Instruction, instr_cls_for_opcode


def disassemble_one(bytecode: bytes, pc=0) -> Instruction:
    opcode = bytecode[pc]
    cls = instr_cls_for_opcode(opcode)
    instr = cls(bytecode, pc)
    return instr


def disassemble_all(bytecode: bytes, pc=0):
    while pc < len(bytecode):
        instr = disassemble_one(bytecode, pc)
        pc += instr.size
        yield instr
