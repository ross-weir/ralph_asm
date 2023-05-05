# VERY rushed and probably bug ridden port of https://github.com/alephium/alephium/blob/58c93b302b5ee6ffc7d93f81a0dbe53082570efe/serde/src/main/scala/org/alephium/serde/CompactInteger.scala#L158
from typing import Tuple
import numpy as np


class SerdeError(Exception):
    pass


class Mode:
    mask_mode = 0x3F
    mask_rest = 0xC0
    mask_mode_neg = 0xFFFFFFC0

    @classmethod
    def decode(cls, bs: bytearray) -> Tuple["Mode", bytearray, bytearray]:
        if not bs:
            raise SerdeError()
        else:
            mode_byte = bs[0] & cls.mask_rest
            if mode_byte == SingleByte.prefix:
                return (SingleByte(), bs[:1], bs[1:])
            elif mode_byte == TwoByte.prefix:
                return cls.check_size(bs, 2, TwoByte())
            elif mode_byte == FourByte.prefix:
                return cls.check_size(bs, 4, FourByte())
            else:
                return cls.check_size(bs, (bs[0] & cls.mask_mode) + 4 + 1, MultiByte())

    @staticmethod
    def check_size(
        bs: bytearray, expected: int, mode: "Mode"
    ) -> Tuple["Mode", bytearray, bytearray]:
        if len(bs) >= expected:
            return (mode, bs[:expected], bs[expected:])
        else:
            raise SerdeError()


class FixedWidth(Mode):
    pass


class SingleByte(FixedWidth):
    prefix = 0x00
    neg_prefix = 0xC0


class TwoByte(FixedWidth):
    prefix = 0x40
    neg_prefix = 0x80


class FourByte(FixedWidth):
    prefix = 0x80
    neg_prefix = 0x40


class MultiByte(Mode):
    prefix = 0xC0
    neg_prefix = None


class Staging:
    def __init__(self, value, rest):
        self.value = value
        self.rest = rest


class Signed:
    sign_flag = 0x20
    one_byte_bound = 0x20
    two_byte_bound = one_byte_bound << 8
    four_byte_bound = one_byte_bound << (8 * 3)

    @staticmethod
    def decode_int(bs: bytearray) -> Staging:
        result = Mode.decode(bs)
        tuple_result = result
        return Signed._decode_int(tuple_result[0], tuple_result[1], tuple_result[2])

    @staticmethod
    def _decode_int(mode: Mode, body: bytearray, rest: bytearray) -> Staging:
        if isinstance(mode, FixedWidth):
            return Signed._decode_int_fixed_width(mode, body, rest)
        elif isinstance(mode, MultiByte):
            if len(body) >= 5:
                value = int.from_bytes(body[1:], "big")
                return Staging(value, rest)

    @staticmethod
    def _decode_int_fixed_width(
        mode: FixedWidth, body: bytearray, rest: bytearray
    ) -> Staging:
        is_positive = (body[0] & Signed.sign_flag) == 0
        if is_positive:
            return Signed._decode_positive_int(mode, body, rest)
        else:
            return Signed._decode_negative_int(mode, body, rest)

    @staticmethod
    def _decode_positive_int(
        mode: FixedWidth, body: bytearray, rest: bytearray
    ) -> Staging:
        if isinstance(mode, SingleByte):
            return Staging(body[0], rest)
        elif isinstance(mode, TwoByte):
            value = ((body[0] & Mode.mask_mode) << 8) | (body[1] & 0xFF)
            return Staging(value, rest)
        elif isinstance(mode, FourByte):
            value = (
                ((body[0] & Mode.mask_mode) << 24)
                | ((body[1] & 0xFF) << 16)
                | ((body[2] & 0xFF) << 8)
                | (body[3] & 0xFF)
            )
        return Staging(value, rest)

    @staticmethod
    def _decode_negative_int(
        mode: FixedWidth, body: bytearray, rest: bytearray
    ) -> Staging:
        if isinstance(mode, SingleByte):
            return Staging(body[0] | Mode.mask_mode_neg, rest)
        elif isinstance(mode, TwoByte):
            assert len(body) == 2
            value = ((body[0] | Mode.mask_mode_neg) << 8) | (body[1] & 0xFF)
            value = np.array(value).astype(np.int32)
            return Staging(value, rest)
        elif isinstance(mode, FourByte):
            assert len(body) == 4
            value = (
                ((body[0] | Mode.mask_mode_neg) << 24)
                | ((body[1] & 0xFF) << 16)
                | ((body[2] & 0xFF) << 8)
                | (body[3] & 0xFF)
            )
            value = np.array(value).astype(np.int32)
        return Staging(value, rest)
