from ralph_asm import disassemble_all, disassemble_one


def test_disassemble_one_basic_instruction():
    instr = disassemble_one(b"\x11")

    assert instr.mnemonic == "U256CONST5"


def test_disassemble_one_byte_operand_instruction():
    instr = disassemble_one(bytes.fromhex("ce02"))

    assert instr.mnemonic == "LOADIMMFIELD"
    assert instr.operand == 2


def test_disassemble_one_int_operand_instruction():
    instr = disassemble_one(bytes([76, 64, 44]))  # SCALE encoded signed int

    assert instr.mnemonic == "IFFALSE"
    assert instr.operand == 44
    assert instr.size == 3


def test_disassemble_one_int_operand_one_byte_instruction():
    instr = disassemble_one(bytes([76, 13]))  # SCALE encoded signed int

    assert instr.mnemonic == "IFFALSE"
    assert instr.operand == 13
    assert instr.size == 2


def test_disassemble_all_simple_instructions():
    instrs = list(disassemble_all(bytes.fromhex("ce00ce01ce02ce0302")))

    assert len(instrs) == 5
    assert instrs[0].mnemonic == "LOADIMMFIELD"
    assert instrs[1].mnemonic == "LOADIMMFIELD"
    assert instrs[2].mnemonic == "LOADIMMFIELD"
    assert instrs[3].mnemonic == "LOADIMMFIELD"
    assert instrs[4].mnemonic == "RETURN"


def test_disassemble_all_medium_instructions():
    instrs = list(
        disassemble_all(
            bytes.fromhex(
                "b3ce00410c7b16006716014366441601441702a0004317030c170416041603314c402ca000160416040e2a626d1705a00016040e2a16040f2a626c170616040f2a16062a1707160516002f4c0da0000c160462160244a000160716036244a10002160717044a7fd0a000160244a100"
            )
        )
    )

    assert len(instrs) == 71

    assert instrs[4].mnemonic == "ASSERTWITHERRORCODE"
    assert instrs[27].mnemonic == "U256ADD"
    assert instrs[53].mnemonic == "LOADLOCAL"
    assert instrs[70].mnemonic == "STOREMUTFIELD"
