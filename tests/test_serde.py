from ralph_asm.serde import Signed


def test_int_one_byte_decode():
    b = bytes([13])
    result = Signed.decode_int(b)

    assert result.value == 13


def test_int_two_byte_decode():
    b = bytes([64, 44])
    result = Signed.decode_int(b)

    assert result.value == 44


def test_int_negative_decode():
    b = bytes([127, 208])
    result = Signed.decode_int(b)

    assert result.value == -48
