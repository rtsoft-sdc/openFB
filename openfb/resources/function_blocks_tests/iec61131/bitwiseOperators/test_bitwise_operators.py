import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_AND import F_AND
from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_OR import F_OR
from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_XOR import F_XOR
from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_NOT import F_NOT
from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_SHL import F_SHL
from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_SHR import F_SHR
from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_ROL import F_ROL
from openfb.resources.function_blocks.iec61131.bitwiseOperators.F_ROR import F_ROR
from openfb.resources.function_blocks.iec61131.bitwiseOperators.AND_2 import AND_2
from openfb.resources.function_blocks.iec61131.bitwiseOperators.AND_3 import AND_3
from openfb.resources.function_blocks.iec61131.bitwiseOperators.AND_4 import AND_4
from openfb.resources.function_blocks.iec61131.bitwiseOperators.AND_5 import AND_5
from openfb.resources.function_blocks.iec61131.bitwiseOperators.OR_2 import OR_2
from openfb.resources.function_blocks.iec61131.bitwiseOperators.OR_3 import OR_3
from openfb.resources.function_blocks.iec61131.bitwiseOperators.OR_4 import OR_4
from openfb.resources.function_blocks.iec61131.bitwiseOperators.XOR_2 import XOR_2
from openfb.resources.function_blocks.iec61131.bitwiseOperators.XOR_3 import XOR_3
from openfb.resources.function_blocks.iec61131.bitwiseOperators.XOR_4 import XOR_4


class TestF_AND(unittest.TestCase):
    def setUp(self):
        self.block = F_AND()

    def test_and_basic(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 1))

    def test_and_same_values(self):
        result = self.block.schedule('REQ', True, 7, 7)
        self.assertEqual(result, (True, 7))

    def test_and_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 0))

    def test_and_all_ones(self):
        result = self.block.schedule('REQ', True, 5, -1)
        self.assertEqual(result, (True, 5))

    def test_and_no_common_bits(self):
        result = self.block.schedule('REQ', True, 4, 2)
        self.assertEqual(result, (True, 0))

    def test_and_all_bits(self):
        result = self.block.schedule('REQ', True, 15, 15)
        self.assertEqual(result, (True, 15))

    def test_and_large_numbers(self):
        result = self.block.schedule('REQ', True, 1024, 512)
        self.assertEqual(result, (True, 0))

    def test_and_string_numbers(self):
        result = self.block.schedule('REQ', True, "5", "3")
        self.assertEqual(result, (True, 1))

    def test_and_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "invalid")
        self.assertEqual(result, (True, None))

    def test_and_wrong_event(self):
        result = self.block.schedule('WRONG', True, 5, 3)
        self.assertIsNone(result)


class TestF_OR(unittest.TestCase):
    def setUp(self):
        self.block = F_OR()

    def test_or_basic(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 7))

    def test_or_same_values(self):
        result = self.block.schedule('REQ', True, 7, 7)
        self.assertEqual(result, (True, 7))

    def test_or_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 5))

    def test_or_no_overlap(self):
        result = self.block.schedule('REQ', True, 4, 2)
        self.assertEqual(result, (True, 6))

    def test_or_all_bits(self):
        result = self.block.schedule('REQ', True, 15, 15)
        self.assertEqual(result, (True, 15))

    def test_or_string_numbers(self):
        result = self.block.schedule('REQ', True, "5", "3")
        self.assertEqual(result, (True, 7))

    def test_or_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "invalid")
        self.assertEqual(result, (True, None))


class TestF_XOR(unittest.TestCase):
    def setUp(self):
        self.block = F_XOR()

    def test_xor_basic(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 6))

    def test_xor_same_values(self):
        result = self.block.schedule('REQ', True, 7, 7)
        self.assertEqual(result, (True, 0))

    def test_xor_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 5))

    def test_xor_all_ones(self):
        result = self.block.schedule('REQ', True, 0, -1)
        self.assertEqual(result, (True, -1))

    def test_xor_swap_property(self):
        a, b = 5, 3
        result = self.block.schedule('REQ', True, a, b)
        self.assertEqual(result[1], 6)

    def test_xor_string_numbers(self):
        result = self.block.schedule('REQ', True, "5", "3")
        self.assertEqual(result, (True, 6))

    def test_xor_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "invalid")
        self.assertEqual(result, (True, None))


class TestF_NOT(unittest.TestCase):
    def setUp(self):
        self.block = F_NOT()

    def test_not_basic(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertEqual(result, (True, -1))

    def test_not_minus_one(self):
        result = self.block.schedule('REQ', True, -1)
        self.assertEqual(result, (True, 0))

    def test_not_positive(self):
        result = self.block.schedule('REQ', True, 5)
        self.assertEqual(result, (True, ~5))

    def test_not_double_negation(self):
        value = 5
        result = self.block.schedule('REQ', True, value)
        self.assertEqual(result[1], ~value)

    def test_not_string_number(self):
        result = self.block.schedule('REQ', True, "5")
        self.assertEqual(result, (True, ~5))

    def test_not_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))


class TestF_SHL(unittest.TestCase):
    def setUp(self):
        self.block = F_SHL()

    def test_shl_basic(self):
        result = self.block.schedule('REQ', True, 5, 1)
        self.assertEqual(result, (True, 10))

    def test_shl_zero_shift(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 5))

    def test_shl_multiple_shifts(self):
        result = self.block.schedule('REQ', True, 1, 3)
        self.assertEqual(result, (True, 8))

    def test_shl_zero_base(self):
        result = self.block.schedule('REQ', True, 0, 5)
        self.assertEqual(result, (True, 0))

    def test_shl_negative_number(self):
        result = self.block.schedule('REQ', True, -1, 1)
        self.assertEqual(result, (True, -2))

    def test_shl_large_shift(self):
        result = self.block.schedule('REQ', True, 1, 10)
        self.assertEqual(result, (True, 1024))

    def test_shl_string_numbers(self):
        result = self.block.schedule('REQ', True, "5", "1")
        self.assertEqual(result, (True, 10))

    def test_shl_invalid_shift(self):
        result = self.block.schedule('REQ', True, 5, "invalid")
        self.assertEqual(result, (True, None))


class TestF_SHR(unittest.TestCase):
    def setUp(self):
        self.block = F_SHR()

    def test_shr_basic(self):
        result = self.block.schedule('REQ', True, 10, 1)
        self.assertEqual(result, (True, 5))

    def test_shr_zero_shift(self):
        result = self.block.schedule('REQ', True, 10, 0)
        self.assertEqual(result, (True, 10))

    def test_shr_multiple_shifts(self):
        result = self.block.schedule('REQ', True, 8, 2)
        self.assertEqual(result, (True, 2))

    def test_shr_to_zero(self):
        result = self.block.schedule('REQ', True, 1, 3)
        self.assertEqual(result, (True, 0))

    def test_shr_negative_number(self):
        result = self.block.schedule('REQ', True, -4, 1)
        self.assertEqual(result, (True, -2))

    def test_shr_string_numbers(self):
        result = self.block.schedule('REQ', True, "10", "1")
        self.assertEqual(result, (True, 5))

    def test_shr_invalid_shift(self):
        result = self.block.schedule('REQ', True, 10, "invalid")
        self.assertEqual(result, (True, None))


class TestF_ROL(unittest.TestCase):
    def setUp(self):
        self.block = F_ROL()

    def test_rol_basic(self):
        result = self.block.schedule('REQ', True, 1, 1, 32)
        self.assertEqual(result, (True, 2))

    def test_rol_zero_shift(self):
        result = self.block.schedule('REQ', True, 5, 0, 32)
        self.assertEqual(result, (True, 5))

    def test_rol_wrap_around(self):
        result = self.block.schedule('REQ', True, 0x80000000, 1, 32)
        self.assertEqual(result[1], 1)

    def test_rol_default_width(self):
        result = self.block.schedule('REQ', True, 1, 1)
        self.assertEqual(result, (True, 2))

    def test_rol_negative_input(self):
        result = self.block.schedule('REQ', True, -1, 1, 32)
        self.assertIsNotNone(result[1])

    def test_rol_string_numbers(self):
        result = self.block.schedule('REQ', True, "1", "1", 32)
        self.assertEqual(result, (True, 2))

    def test_rol_invalid_shift(self):
        result = self.block.schedule('REQ', True, 5, "invalid", 32)
        self.assertEqual(result, (True, None))


class TestF_ROR(unittest.TestCase):
    def setUp(self):
        self.block = F_ROR()

    def test_ror_basic(self):
        result = self.block.schedule('REQ', True, 2, 1, 32)
        self.assertEqual(result, (True, 1))

    def test_ror_zero_shift(self):
        result = self.block.schedule('REQ', True, 5, 0, 32)
        self.assertEqual(result, (True, 5))

    def test_ror_wrap_around(self):
        result = self.block.schedule('REQ', True, 1, 1, 32)
        self.assertIsNotNone(result[1])

    def test_ror_default_width(self):
        result = self.block.schedule('REQ', True, 2, 1)
        self.assertEqual(result, (True, 1))

    def test_ror_negative_input(self):
        result = self.block.schedule('REQ', True, -1, 1, 32)
        self.assertIsNotNone(result[1])

    def test_ror_string_numbers(self):
        result = self.block.schedule('REQ', True, "2", "1", 32)
        self.assertEqual(result, (True, 1))

    def test_ror_invalid_shift(self):
        result = self.block.schedule('REQ', True, 5, "invalid", 32)
        self.assertEqual(result, (True, None))


class TestAND_2(unittest.TestCase):
    def setUp(self):
        self.block = AND_2()

    def test_and_2_basic(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 1))

    def test_and_2_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 0))

    def test_and_2_same(self):
        result = self.block.schedule('REQ', True, 7, 7)
        self.assertEqual(result, (True, 7))


class TestAND_3(unittest.TestCase):
    def setUp(self):
        self.block = AND_3()

    def test_and_3_basic(self):
        result = self.block.schedule('REQ', True, 7, 5, 3)
        self.assertEqual(result, (True, 1))

    def test_and_3_one_zero(self):
        result = self.block.schedule('REQ', True, 5, 0, 3)
        self.assertEqual(result, (True, 0))

    def test_and_3_same_values(self):
        result = self.block.schedule('REQ', True, 5, 5, 5)
        self.assertEqual(result, (True, 5))


class TestAND_4(unittest.TestCase):
    def setUp(self):
        self.block = AND_4()

    def test_and_4_basic(self):
        result = self.block.schedule('REQ', True, 15, 7, 3, 1)
        self.assertEqual(result, (True, 1))

    def test_and_4_zero(self):
        result = self.block.schedule('REQ', True, 15, 7, 3, 0)
        self.assertEqual(result, (True, 0))


class TestAND_5(unittest.TestCase):
    def setUp(self):
        self.block = AND_5()

    def test_and_5_basic(self):
        result = self.block.schedule('REQ', True, 15, 7, 3, 1, 1)
        self.assertEqual(result, (True, 1))

    def test_and_5_zero(self):
        result = self.block.schedule('REQ', True, 15, 7, 3, 1, 0)
        self.assertEqual(result, (True, 0))


class TestOR_2(unittest.TestCase):
    def setUp(self):
        self.block = OR_2()

    def test_or_2_basic(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 7))

    def test_or_2_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 5))

    def test_or_2_same(self):
        result = self.block.schedule('REQ', True, 7, 7)
        self.assertEqual(result, (True, 7))


class TestOR_3(unittest.TestCase):
    def setUp(self):
        self.block = OR_3()

    def test_or_3_basic(self):
        result = self.block.schedule('REQ', True, 1, 2, 4)
        self.assertEqual(result, (True, 7))

    def test_or_3_with_zero(self):
        result = self.block.schedule('REQ', True, 5, 0, 3)
        self.assertEqual(result, (True, 7))


class TestOR_4(unittest.TestCase):
    def setUp(self):
        self.block = OR_4()

    def test_or_4_basic(self):
        result = self.block.schedule('REQ', True, 1, 2, 4, 8)
        self.assertEqual(result, (True, 15))

    def test_or_4_with_zero(self):
        result = self.block.schedule('REQ', True, 1, 2, 0, 8)
        self.assertEqual(result, (True, 11))


class TestXOR_2(unittest.TestCase):
    def setUp(self):
        self.block = XOR_2()

    def test_xor_2_basic(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 6))

    def test_xor_2_same(self):
        result = self.block.schedule('REQ', True, 7, 7)
        self.assertEqual(result, (True, 0))

    def test_xor_2_with_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 5))


class TestXOR_3(unittest.TestCase):
    def setUp(self):
        self.block = XOR_3()

    def test_xor_3_basic(self):
        result = self.block.schedule('REQ', True, 1, 2, 3)
        self.assertEqual(result, (True, 0))

    def test_xor_3_associative(self):
        result = self.block.schedule('REQ', True, 5, 3, 6)
        self.assertIsNotNone(result[1])


class TestXOR_4(unittest.TestCase):
    def setUp(self):
        self.block = XOR_4()

    def test_xor_4_basic(self):
        result = self.block.schedule('REQ', True, 1, 2, 4, 7)
        self.assertEqual(result, (True, 0))

    def test_xor_4_all_same(self):
        result = self.block.schedule('REQ', True, 5, 5, 5, 5)
        self.assertEqual(result, (True, 0))


if __name__ == '__main__':
    unittest.main(verbosity=2)
