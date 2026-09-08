import pytest
from CAN_Frame_Parser import parse_line

@pytest.mark.parametrize("line,expected_valid", [
    ("(1000000000.000001) vcan0 123#1122334455667788", True),
    ("(1000000000.100000) vcan0 0C8#AABB", True),
    ("(1000000000.200000) vcan0 456#11223344556677889900", False),
    ("(1000000000.300000) vcan0 XYZ#1122", False),
    ("(1000000000.400000) vcan0 18FF1234#01020304", True),
    ("(1000000000.500000) vcan0 123#AAB", False),
])
def test_is_valid(line, expected_valid):
    frame = parse_line(line)
    valid, reason = frame.is_valid()
    assert valid == expected_valid