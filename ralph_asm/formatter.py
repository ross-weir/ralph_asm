from ralph_asm.instructions import Instruction


class InstructionFormatter:
    def __init__(self, show_pc=True, show_instr_descriptions=False):
        self._show_pc = show_pc
        self._show_instr_descriptions = show_instr_descriptions

    def format_one(self, instr: Instruction) -> str:
        s = ""
        if self._show_pc:
            s += f"{instr.pc:04x}: "
        s += instr.mnemonic
        if instr.has_operand:
            s += f", {instr.operand}"
        if self._show_instr_descriptions:
            s += f" | {instr.description}"
        return s

    def format_all(self, instrs: list[Instruction]) -> str:
        return "\n".join([self.format_one(i) for i in instrs])
