from abc import ABC, abstractmethod

from ralph_asm.serde import Signed


class Instruction(ABC):
    def __init__(self, bytecode: bytes, pc: int = 0):
        self._pc = pc
        self._operand = None
        self._bytes = bytecode[pc : pc + self.size]

        if self.has_operand:
            self._operand = self.parse_operand()

    @property
    def operand_size(self) -> int:
        """Size of the operand in bytes."""
        return 0

    @property
    def has_operand(self) -> bool:
        return self.operand_size > 0

    def parse_operand(self):
        pass

    @property
    def mnemonic(self) -> str:
        return self.__class__.__name__.upper()

    @property
    def operand(self):
        return self._operand

    @property
    def size(self):
        return self.operand_size + 1

    @property
    def pc(self) -> int:
        return self._pc

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    def description(self) -> str:
        return f"{self.__class__.__name__} description TODO"


class ByteOperandInstruction(Instruction):
    def parse_operand(self):
        return int.from_bytes(self.bytes[1:], "big")

    @property
    def operand_size(self) -> int:
        """Size of the operand in bytes."""
        return 1


class IntOperandInstruction(Instruction):
    def __init__(self, bytecode: bytes, pc: int = 0):
        self._pc = pc
        operand_start_bytes = bytecode[pc + 1 :]
        signed = Signed.decode_int(operand_start_bytes)
        self._operand_byte_length = len(operand_start_bytes) - len(signed.rest)
        self._operand = signed.value
        self._bytes = bytecode[pc : pc + self.size]

    def parse_operand(self):
        return Signed.decode_int(self.bytes[1:]).value

    @property
    def operand_size(self) -> int:
        """Size of the operand in bytes."""
        return self._operand_byte_length


class CallLocal(ByteOperandInstruction):
    @property
    def description(self) -> str:
        return "Call a local function by index"


class CallExternal(ByteOperandInstruction):
    @property
    def description(self) -> str:
        return "Call external function by index"


class Return(Instruction):
    @property
    def description(self) -> str:
        return "Return from a function call"


class ConstInstruction(Instruction):
    @property
    @abstractmethod
    def const_value(self):
        pass

    @property
    def description(self) -> str:
        const_str = str(self.const_value).lower()
        return f"Push a constant {const_str} value on the stack"


class ConstTrue(ConstInstruction):
    @property
    def const_value(self) -> bool:
        return True


class ConstFalse(ConstInstruction):
    @property
    def const_value(self) -> bool:
        return False


class I256Const0(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 0


class I256Const1(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 1


class I256Const2(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 2


class I256Const3(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 3


class I256Const4(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 4


class I256Const5(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 5


class I256ConstN1(ConstInstruction):
    @property
    def const_value(self) -> int:
        return -1


class U256Const0(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 0


class U256Const1(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 1


class U256Const2(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 2


class U256Const3(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 3


class U256Const4(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 4


class U256Const5(ConstInstruction):
    @property
    def const_value(self) -> int:
        return 5


class LoadLocal(ByteOperandInstruction):
    pass


class StoreLocal(ByteOperandInstruction):
    pass


class U256Add(Instruction):
    pass


class U256Lt(Instruction):
    pass


class IfFalse(IntOperandInstruction):
    pass


class ByteVecSize(Instruction):
    pass


class ByteVecConcat(Instruction):
    pass


class ByteVecSlice(Instruction):
    pass


class U256To1Byte(Instruction):
    pass


class U256To2Byte(Instruction):
    pass


class ByteVecEq(Instruction):
    pass


class U256From1Byte(Instruction):
    pass


class U256From2Byte(Instruction):
    pass


class AssertWithErrorCode(Instruction):
    pass


class U256Eq(Instruction):
    pass


class CallerContractId(Instruction):
    @property
    def description(self) -> str:
        return "TODO"


class Jump(IntOperandInstruction):
    pass


class U256Ge(Instruction):
    pass


class LoadMutField(ByteOperandInstruction):
    pass


class StoreMutField(ByteOperandInstruction):
    pass


class LoadImmField(ByteOperandInstruction):
    @property
    def description(self) -> str:
        return "Load immutable contract field"


_opcode_to_cls_map = {
    0: CallLocal,
    1: CallExternal,
    2: Return,
    3: ConstTrue,
    4: ConstFalse,
    5: I256Const0,
    6: I256Const1,
    7: I256Const2,
    8: I256Const3,
    9: I256Const4,
    10: I256Const5,
    11: I256ConstN1,
    12: U256Const0,
    13: U256Const1,
    14: U256Const2,
    15: U256Const3,
    16: U256Const4,
    17: U256Const5,
    22: LoadLocal,
    23: StoreLocal,
    42: U256Add,
    47: U256Eq,
    49: U256Lt,
    52: U256Ge,
    65: ByteVecEq,
    67: ByteVecSize,
    68: ByteVecConcat,
    74: Jump,
    76: IfFalse,
    98: ByteVecSlice,
    102: U256To1Byte,
    103: U256To2Byte,
    108: U256From1Byte,
    109: U256From2Byte,
    123: AssertWithErrorCode,
    160: LoadMutField,
    161: StoreMutField,
    179: CallerContractId,
    206: LoadImmField,
}


def instr_cls_for_opcode(opcode: int):
    return _opcode_to_cls_map[opcode]
