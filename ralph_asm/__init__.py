from ralph_asm.instructions import Instruction, instr_cls_for_opcode
from ralph_asm.ralph_asm import disassemble_all, disassemble_one
from ralph_asm.formatter import InstructionFormatter


def random_test():
    instrs = list(
        disassemble_all(
            bytes.fromhex(
                "b3ce00410c7b16006716014366441601441702a0004317030c170416041603314c402ca000160416040e2a626d1705a00016040e2a16040f2a626c170616040f2a16062a1707160516002f4c0da0000c160462160244a000160716036244a10002160717044a7fd0a000160244a100"
            )
        )
    )
    formatter = InstructionFormatter()

    print(formatter.format_all(instrs))
