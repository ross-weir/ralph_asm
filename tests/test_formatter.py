from ralph_asm import disassemble_one, disassemble_all
from ralph_asm.instructions import U256Const5
from ralph_asm.formatter import InstructionFormatter


def test_format_one_basic_instruction_no_description():
    formatter = InstructionFormatter()
    instr = U256Const5(b"\x11")

    assert "0000: U256CONST5" == formatter.format_one(instr)


def test_format_one_basic_instruction_with_description():
    formatter = InstructionFormatter(show_pc=True, show_instr_descriptions=True)
    instr = U256Const5(b"\x11")

    assert (
        "0000: U256CONST5 | Push a constant 5 value on the stack"
        == formatter.format_one(instr)
    )


def test_format_one_operand_instruction_no_description():
    formatter = InstructionFormatter()
    instr = disassemble_one(bytes.fromhex("ce02"))

    assert "0000: LOADIMMFIELD, 2" == formatter.format_one(instr)


def test_format_one_operand_instruction_with_description():
    formatter = InstructionFormatter(show_pc=True, show_instr_descriptions=True)
    instr = disassemble_one(bytes.fromhex("ce02"))

    assert (
        "0000: LOADIMMFIELD, 2 | Load immutable contract field"
        == formatter.format_one(instr)
    )


def test_format_all_basic_instructions():
    formatter = InstructionFormatter(show_pc=True)
    instrs = list(disassemble_all(bytes.fromhex("ce00ce01ce02ce0302")))
    expected = [
        "0000: LOADIMMFIELD, 0",
        "0002: LOADIMMFIELD, 1",
        "0004: LOADIMMFIELD, 2",
        "0006: LOADIMMFIELD, 3",
        "0008: RETURN",
    ]

    assert expected == formatter.format_all(instrs).splitlines()
