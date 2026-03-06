import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.comparison.F_EQ import F_EQ
from openfb.resources.function_blocks.iec61131.comparison.F_NE import F_NE
from openfb.resources.function_blocks.iec61131.comparison.F_LT import F_LT
from openfb.resources.function_blocks.iec61131.comparison.F_LE import F_LE
from openfb.resources.function_blocks.iec61131.comparison.F_GT import F_GT
from openfb.resources.function_blocks.iec61131.comparison.F_GE import F_GE


class TestF_EQ(unittest.TestCase):
    def setUp(self):
        self.block = F_EQ()

    def test_eq_integers_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, True))

    def test_eq_integers_not_equal(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, False))

    def test_eq_floats_equal(self):
        result = self.block.schedule('REQ', True, 5.0, 5.0)
        self.assertEqual(result, (True, True))

    def test_eq_floats_not_equal(self):
        result = self.block.schedule('REQ', True, 5.1, 5.2)
        self.assertEqual(result, (True, False))

    def test_eq_strings_equal(self):
        result = self.block.schedule('REQ', True, "Hello", "Hello")
        self.assertEqual(result, (True, True))

    def test_eq_strings_not_equal(self):
        result = self.block.schedule('REQ', True, "Hello", "World")
        self.assertEqual(result, (True, False))

    def test_eq_string_case_sensitive(self):
        result = self.block.schedule('REQ', True, "Hello", "hello")
        self.assertEqual(result, (True, False))

    def test_eq_mixed_types(self):
        result = self.block.schedule('REQ', True, 5, 5.0)
        self.assertEqual(result, (True, True))

    def test_eq_zero(self):
        result = self.block.schedule('REQ', True, 0, 0)
        self.assertEqual(result, (True, True))

    def test_eq_negative_numbers(self):
        result = self.block.schedule('REQ', True, -5, -5)
        self.assertEqual(result, (True, True))

    def test_eq_booleans(self):
        result = self.block.schedule('REQ', True, True, True)
        self.assertEqual(result, (True, True))

    def test_eq_none_values(self):
        result = self.block.schedule('REQ', True, None, None)
        self.assertEqual(result, (True, True))

    def test_eq_wrong_event(self):
        result = self.block.schedule('WRONG', True, 5, 5)
        self.assertIsNone(result)


class TestF_NE(unittest.TestCase):
    def setUp(self):
        self.block = F_NE()

    def test_ne_integers_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, False))

    def test_ne_integers_not_equal(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, True))

    def test_ne_strings_equal(self):
        result = self.block.schedule('REQ', True, "Hello", "Hello")
        self.assertEqual(result, (True, False))

    def test_ne_strings_not_equal(self):
        result = self.block.schedule('REQ', True, "Hello", "World")
        self.assertEqual(result, (True, True))

    def test_ne_zero(self):
        result = self.block.schedule('REQ', True, 0, 0)
        self.assertEqual(result, (True, False))

    def test_ne_negative_numbers(self):
        result = self.block.schedule('REQ', True, -5, -3)
        self.assertEqual(result, (True, True))


class TestF_LT(unittest.TestCase):
    def setUp(self):
        self.block = F_LT()

    def test_lt_basic(self):
        result = self.block.schedule('REQ', True, 3, 5)
        self.assertEqual(result, (True, True))

    def test_lt_false(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, False))

    def test_lt_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, False))

    def test_lt_floats(self):
        result = self.block.schedule('REQ', True, 3.5, 5.2)
        self.assertEqual(result, (True, True))

    def test_lt_negative(self):
        result = self.block.schedule('REQ', True, -5, -3)
        self.assertEqual(result, (True, True))

    def test_lt_mixed_signs(self):
        result = self.block.schedule('REQ', True, -5, 3)
        self.assertEqual(result, (True, True))

    def test_lt_strings(self):
        result = self.block.schedule('REQ', True, "a", "b")
        self.assertEqual(result, (True, True))

    def test_lt_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "invalid")
        self.assertEqual(result, (True, None))


class TestF_LE(unittest.TestCase):
    def setUp(self):
        self.block = F_LE()

    def test_le_less(self):
        result = self.block.schedule('REQ', True, 3, 5)
        self.assertEqual(result, (True, True))

    def test_le_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, True))

    def test_le_greater(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, False))

    def test_le_floats(self):
        result = self.block.schedule('REQ', True, 5.0, 5.0)
        self.assertEqual(result, (True, True))

    def test_le_negative(self):
        result = self.block.schedule('REQ', True, -5, -3)
        self.assertEqual(result, (True, True))

    def test_le_strings(self):
        result = self.block.schedule('REQ', True, "a", "a")
        self.assertEqual(result, (True, True))


class TestF_GT(unittest.TestCase):
    def setUp(self):
        self.block = F_GT()

    def test_gt_basic(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, True))

    def test_gt_false(self):
        result = self.block.schedule('REQ', True, 3, 5)
        self.assertEqual(result, (True, False))

    def test_gt_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, False))

    def test_gt_floats(self):
        result = self.block.schedule('REQ', True, 5.2, 3.5)
        self.assertEqual(result, (True, True))

    def test_gt_negative(self):
        result = self.block.schedule('REQ', True, -3, -5)
        self.assertEqual(result, (True, True))

    def test_gt_mixed_signs(self):
        result = self.block.schedule('REQ', True, 3, -5)
        self.assertEqual(result, (True, True))

    def test_gt_strings(self):
        result = self.block.schedule('REQ', True, "b", "a")
        self.assertEqual(result, (True, True))


class TestF_GE(unittest.TestCase):
    def setUp(self):
        self.block = F_GE()

    def test_ge_greater(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, True))

    def test_ge_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, True))

    def test_ge_less(self):
        result = self.block.schedule('REQ', True, 3, 5)
        self.assertEqual(result, (True, False))

    def test_ge_floats(self):
        result = self.block.schedule('REQ', True, 5.0, 5.0)
        self.assertEqual(result, (True, True))

    def test_ge_negative(self):
        result = self.block.schedule('REQ', True, -3, -5)
        self.assertEqual(result, (True, True))

    def test_ge_strings(self):
        result = self.block.schedule('REQ', True, "b", "b")
        self.assertEqual(result, (True, True))


if __name__ == '__main__':
    unittest.main(verbosity=2)
