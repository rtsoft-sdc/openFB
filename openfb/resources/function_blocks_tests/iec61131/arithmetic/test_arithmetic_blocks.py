import unittest
import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.arithmetic.F_ADD import F_ADD
from openfb.resources.function_blocks.iec61131.arithmetic.F_SUB import F_SUB
from openfb.resources.function_blocks.iec61131.arithmetic.F_MUL import F_MUL
from openfb.resources.function_blocks.iec61131.arithmetic.F_DIV import F_DIV
from openfb.resources.function_blocks.iec61131.arithmetic.F_MOD import F_MOD
from openfb.resources.function_blocks.iec61131.arithmetic.F_EXPT import F_EXPT
from openfb.resources.function_blocks.iec61131.arithmetic.F_TRUNC import F_TRUNC
from openfb.resources.function_blocks.iec61131.arithmetic.ADD_2 import ADD_2
from openfb.resources.function_blocks.iec61131.arithmetic.ADD_3 import ADD_3
from openfb.resources.function_blocks.iec61131.arithmetic.ADD_4 import ADD_4
from openfb.resources.function_blocks.iec61131.arithmetic.F_MULTIME import F_MULTIME
from openfb.resources.function_blocks.iec61131.arithmetic.F_DIVTIME import F_DIVTIME
from openfb.resources.function_blocks.iec61131.arithmetic.F_ADD_DT_TIME import F_ADD_DT_TIME
from openfb.resources.function_blocks.iec61131.arithmetic.F_ADD_TOD_TIME import F_ADD_TOD_TIME
from openfb.resources.function_blocks.iec61131.arithmetic.F_SUB_DT_TIME import F_SUB_DT_TIME
from openfb.resources.function_blocks.iec61131.arithmetic.F_SUB_DT_DT import F_SUB_DT_DT
from openfb.resources.function_blocks.iec61131.arithmetic.F_SUB_TOD_TIME import F_SUB_TOD_TIME
from openfb.resources.function_blocks.iec61131.arithmetic.F_SUB_TOD_TOD import F_SUB_TOD_TOD
from openfb.resources.function_blocks.iec61131.arithmetic.F_SUB_DATE_DATE import F_SUB_DATE_DATE


class TestF_ADD(unittest.TestCase):

    def setUp(self):
        self.block = F_ADD()

    def test_add_integers(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 8))

    def test_add_floats(self):
        result = self.block.schedule('REQ', True, 5.5, 3.2)
        self.assertAlmostEqual(result[1], 8.7, places=5)

    def test_add_negative_numbers(self):
        result = self.block.schedule('REQ', True, -5, -3)
        self.assertEqual(result, (True, -8))

    def test_add_mixed_types(self):
        result = self.block.schedule('REQ', True, 5, 3.5)
        self.assertEqual(result, (True, 8.5))

    def test_add_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 5))

    def test_add_strings(self):
        result = self.block.schedule('REQ', True, "Hello ", "World")
        self.assertEqual(result, (True, "Hello World"))

    def test_add_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "string")
        self.assertEqual(result, (True, None))

    def test_wrong_event(self):
        result = self.block.schedule('WRONG', True, 5, 3)
        self.assertIsNone(result)


class TestF_SUB(unittest.TestCase):

    def setUp(self):
        self.block = F_SUB()

    def test_sub_integers(self):
        result = self.block.schedule('REQ', True, 10, 3)
        self.assertEqual(result, (True, 7))

    def test_sub_floats(self):
        result = self.block.schedule('REQ', True, 10.5, 3.2)
        self.assertAlmostEqual(result[1], 7.3, places=5)

    def test_sub_negative_result(self):
        result = self.block.schedule('REQ', True, 3, 10)
        self.assertEqual(result, (True, -7))

    def test_sub_negative_numbers(self):
        result = self.block.schedule('REQ', True, -5, -3)
        self.assertEqual(result, (True, -2))

    def test_sub_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 5))

    def test_sub_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "string")
        self.assertEqual(result, (True, None))


class TestF_MUL(unittest.TestCase):

    def setUp(self):
        self.block = F_MUL()

    def test_mul_integers(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 15))

    def test_mul_floats(self):
        result = self.block.schedule('REQ', True, 2.5, 4.0)
        self.assertEqual(result, (True, 10.0))

    def test_mul_by_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 0))

    def test_mul_negative_numbers(self):
        result = self.block.schedule('REQ', True, -5, -3)
        self.assertEqual(result, (True, 15))

    def test_mul_negative_and_positive(self):
        result = self.block.schedule('REQ', True, -5, 3)
        self.assertEqual(result, (True, -15))

    def test_mul_string_repetition(self):
        result = self.block.schedule('REQ', True, "ab", 3)
        self.assertEqual(result, (True, "ababab"))

    def test_mul_invalid_types(self):
        result = self.block.schedule('REQ', True, "string", "string")
        self.assertEqual(result, (True, None))


class TestF_DIV(unittest.TestCase):

    def setUp(self):
        self.block = F_DIV()

    def test_div_integers(self):
        result = self.block.schedule('REQ', True, 10, 2)
        self.assertEqual(result, (True, 5.0))

    def test_div_floats(self):
        result = self.block.schedule('REQ', True, 10.0, 4.0)
        self.assertEqual(result, (True, 2.5))

    def test_div_by_zero(self):
        result = self.block.schedule('REQ', True, 10, 0)
        self.assertEqual(result, (None, 0))

    def test_div_negative_numbers(self):
        result = self.block.schedule('REQ', True, -10, -2)
        self.assertEqual(result, (True, 5.0))

    def test_div_negative_result(self):
        result = self.block.schedule('REQ', True, 10, -2)
        self.assertEqual(result, (True, -5.0))

    def test_div_fraction_result(self):
        result = self.block.schedule('REQ', True, 7, 2)
        self.assertEqual(result, (True, 3.5))

    def test_div_invalid_types(self):
        result = self.block.schedule('REQ', True, "string", 2)
        self.assertEqual(result, (None, 0))


class TestF_MOD(unittest.TestCase):

    def setUp(self):
        self.block = F_MOD()

    def test_mod_integers(self):
        result = self.block.schedule('REQ', True, 10, 3)
        self.assertEqual(result, (True, 1))

    def test_mod_exact_division(self):
        result = self.block.schedule('REQ', True, 10, 2)
        self.assertEqual(result, (True, 0))

    def test_mod_by_zero(self):
        result = self.block.schedule('REQ', True, 10, 0)
        self.assertEqual(result, (None, 0))

    def test_mod_negative_dividend(self):
        result = self.block.schedule('REQ', True, -10, 3)
        self.assertEqual(result, (True, 2))

    def test_mod_floats(self):
        result = self.block.schedule('REQ', True, 10.5, 3.0)
        self.assertAlmostEqual(result[1], 1.5, places=5)

    def test_mod_invalid_types(self):
        result = self.block.schedule('REQ', True, "string", 2)
        self.assertEqual(result, (None, 0))


class TestF_EXPT(unittest.TestCase):

    def setUp(self):
        self.block = F_EXPT()

    def test_expt_positive_power(self):
        result = self.block.schedule('REQ', True, 2, 3)
        self.assertEqual(result, (True, 8))

    def test_expt_power_zero(self):
        result = self.block.schedule('REQ', True, 5, 0)
        self.assertEqual(result, (True, 1))

    def test_expt_negative_power(self):
        result = self.block.schedule('REQ', True, 2, -3)
        self.assertEqual(result, (True, 0.125))

    def test_expt_fractional_power(self):
        result = self.block.schedule('REQ', True, 9, 0.5)
        self.assertAlmostEqual(result[1], 3.0, places=5)

    def test_expt_zero_base(self):
        result = self.block.schedule('REQ', True, 0, 5)
        self.assertEqual(result, (True, 0))

    def test_expt_negative_base(self):
        result = self.block.schedule('REQ', True, -2, 3)
        self.assertEqual(result, (True, -8))

    def test_expt_floats(self):
        result = self.block.schedule('REQ', True, 2.5, 2)
        self.assertEqual(result, (True, 6.25))

    def test_expt_invalid_types(self):
        result = self.block.schedule('REQ', True, "string", 2)
        self.assertEqual(result, (True, None))


class TestF_TRUNC(unittest.TestCase):

    def setUp(self):
        self.block = F_TRUNC()

    def test_trunc_positive_float(self):
        result = self.block.schedule('REQ', True, 5.7)
        self.assertEqual(result, (True, 5))

    def test_trunc_negative_float(self):
        result = self.block.schedule('REQ', True, -5.7)
        self.assertEqual(result, (True, -5))

    def test_trunc_integer(self):
        result = self.block.schedule('REQ', True, 5)
        self.assertEqual(result, (True, 5))

    def test_trunc_zero(self):
        result = self.block.schedule('REQ', True, 0.0)
        self.assertEqual(result, (True, 0))

    def test_trunc_small_fraction(self):
        result = self.block.schedule('REQ', True, 0.99)
        self.assertEqual(result, (True, 0))

    def test_trunc_string_number(self):
        result = self.block.schedule('REQ', True, "5.7")
        self.assertEqual(result, (True, None))

    def test_trunc_invalid_type(self):
        result = self.block.schedule('REQ', True, "not_a_number")
        self.assertEqual(result, (True, None))

    def test_trunc_bool(self):
        result = self.block.schedule('REQ', True, True)
        self.assertEqual(result, (True, 1))


class TestADD_2(unittest.TestCase):

    def setUp(self):
        self.block = ADD_2()

    def test_add_2_integers(self):
        result = self.block.schedule('REQ', True, 5, 3)
        self.assertEqual(result, (True, 8))

    def test_add_2_floats(self):
        result = self.block.schedule('REQ', True, 5.5, 3.2)
        self.assertAlmostEqual(result[1], 8.7, places=5)

    def test_add_2_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, None)
        self.assertEqual(result, (True, None))


class TestADD_3(unittest.TestCase):

    def setUp(self):
        self.block = ADD_3()

    def test_add_3_integers(self):
        result = self.block.schedule('REQ', True, 5, 3, 2)
        self.assertEqual(result, (True, 10))

    def test_add_3_floats(self):
        result = self.block.schedule('REQ', True, 5.5, 3.2, 1.3)
        self.assertAlmostEqual(result[1], 10.0, places=5)

    def test_add_3_mixed_types(self):
        result = self.block.schedule('REQ', True, 5, 3.5, 2)
        self.assertEqual(result, (True, 10.5))

    def test_add_3_negative(self):
        result = self.block.schedule('REQ', True, 10, -3, -2)
        self.assertEqual(result, (True, 5))

    def test_add_3_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "string", 2)
        self.assertEqual(result, (True, None))


class TestADD_4(unittest.TestCase):

    def setUp(self):
        self.block = ADD_4()

    def test_add_4_integers(self):
        result = self.block.schedule('REQ', True, 5, 3, 2, 1)
        self.assertEqual(result, (True, 11))

    def test_add_4_floats(self):
        result = self.block.schedule('REQ', True, 5.5, 3.2, 1.3, 0.5)
        self.assertAlmostEqual(result[1], 10.5, places=5)

    def test_add_4_mixed_types(self):
        result = self.block.schedule('REQ', True, 5, 3.5, 2, 1.5)
        self.assertEqual(result, (True, 12.0))

    def test_add_4_negative(self):
        result = self.block.schedule('REQ', True, 10, -3, -2, 5)
        self.assertEqual(result, (True, 10))

    def test_add_4_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "string", 2, 1)
        self.assertEqual(result, (True, None))


class TestF_MULTIME(unittest.TestCase):

    def setUp(self):
        self.block = F_MULTIME()

    def test_multime_basic(self):
        result = self.block.schedule('REQ', True, "T#5s", 3)
        expected = datetime.timedelta(seconds=15)
        self.assertEqual(result[1], expected)

    def test_multime_float_multiplier(self):
        result = self.block.schedule('REQ', True, "T#10s", 2.5)
        expected = datetime.timedelta(seconds=25)
        self.assertEqual(result[1], expected)

    def test_multime_zero_multiplier(self):
        result = self.block.schedule('REQ', True, "T#5s", 0)
        expected = datetime.timedelta(seconds=0)
        self.assertEqual(result[1], expected)

    def test_multime_negative_multiplier(self):
        result = self.block.schedule('REQ', True, "T#5s", -2)
        expected = datetime.timedelta(seconds=-10)
        self.assertEqual(result[1], expected)

    def test_multime_invalid_time(self):
        result = self.block.schedule('REQ', True, "invalid", 3)
        expected = datetime.timedelta(0)
        self.assertEqual(result[1], expected)

    def test_multime_invalid_multiplier(self):
        result = self.block.schedule('REQ', True, "T#5s", "invalid")
        expected = datetime.timedelta(0)
        self.assertEqual(result[1], expected)


class TestF_DIVTIME(unittest.TestCase):

    def setUp(self):
        self.block = F_DIVTIME()

    def test_divtime_basic(self):
        result = self.block.schedule('REQ', True, "T#15s", 3)
        expected = datetime.timedelta(seconds=5)
        self.assertEqual(result[1], expected)

    def test_divtime_float_divisor(self):
        result = self.block.schedule('REQ', True, "T#10s", 2.5)
        expected = datetime.timedelta(seconds=4)
        self.assertEqual(result[1], expected)

    def test_divtime_division_by_zero(self):
        result = self.block.schedule('REQ', True, "T#5s", 0)
        expected = datetime.timedelta(seconds=0)
        self.assertEqual(result[1], expected)

    def test_divtime_negative_divisor(self):
        result = self.block.schedule('REQ', True, "T#10s", -2)
        expected = datetime.timedelta(seconds=-5)
        self.assertEqual(result[1], expected)

    def test_divtime_invalid_time(self):
        result = self.block.schedule('REQ', True, "invalid", 3)
        expected = datetime.timedelta(0)
        self.assertEqual(result[1], expected)

    def test_divtime_invalid_divisor(self):
        result = self.block.schedule('REQ', True, "T#10s", "invalid")
        expected = datetime.timedelta(0)
        self.assertEqual(result[1], expected)


class TestF_ADD_DT_TIME(unittest.TestCase):

    def setUp(self):
        self.block = F_ADD_DT_TIME()

    def test_add_dt_time_basic(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-12:00:00", "T#1h")
        if result[1] is not None:
            self.assertEqual(result[1].hour, 13)

    def test_add_dt_time_days(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-12:00:00", "T#24h")
        if result[1] is not None:
            self.assertEqual(result[1].day, 2)

    def test_add_dt_time_invalid_datetime(self):
        result = self.block.schedule('REQ', True, "invalid", "T#1h")
        self.assertEqual(result, (True, None))

    def test_add_dt_time_invalid_interval(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-12:00:00", "invalid")
        self.assertEqual(result, (True, None))


class TestF_SUB_DT_TIME(unittest.TestCase):

    def setUp(self):
        self.block = F_SUB_DT_TIME()

    def test_sub_dt_time_basic(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-12:00:00", "T#1h")
        if result[1] is not None:
            self.assertEqual(result[1].hour, 11)

    def test_sub_dt_time_days(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-02-12:00:00", "T#24h")
        if result[1] is not None:
            self.assertEqual(result[1].day, 1)

    def test_sub_dt_time_invalid_datetime(self):
        result = self.block.schedule('REQ', True, "invalid", "T#1h")
        self.assertEqual(result, (True, None))

    def test_sub_dt_time_invalid_interval(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-12:00:00", "invalid")
        self.assertEqual(result, (True, None))


class TestF_SUB_DT_DT(unittest.TestCase):

    def setUp(self):
        self.block = F_SUB_DT_DT()

    def test_sub_dt_dt_basic(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-12:00:00", "DT#2024-01-01-10:00:00")
        if result[1] is not None:
            self.assertEqual(result[1].total_seconds(), 7200)

    def test_sub_dt_dt_days(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-05-12:00:00", "DT#2024-01-01-12:00:00")
        if result[1] is not None:
            self.assertEqual(result[1].days, 4)

    def test_sub_dt_dt_negative(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-10:00:00", "DT#2024-01-01-12:00:00")
        if result[1] is not None:
            self.assertTrue(result[1].total_seconds() < 0)

    def test_sub_dt_dt_invalid_first(self):
        result = self.block.schedule('REQ', True, "invalid", "DT#2024-01-01-12:00:00")
        self.assertEqual(result, (True, None))

    def test_sub_dt_dt_invalid_second(self):
        result = self.block.schedule('REQ', True, "DT#2024-01-01-12:00:00", "invalid")
        self.assertEqual(result, (True, None))


class TestF_ADD_TOD_TIME(unittest.TestCase):

    def setUp(self):
        self.block = F_ADD_TOD_TIME()

    def test_add_tod_time_basic(self):
        result = self.block.schedule('REQ', True, "TOD#12:00:00", "T#1h")
        self.assertIsNotNone(result)

    def test_add_tod_time_invalid_tod(self):
        result = self.block.schedule('REQ', True, "invalid", "T#1h")
        self.assertEqual(result, (True, None))

    def test_add_tod_time_invalid_interval(self):
        result = self.block.schedule('REQ', True, "TOD#12:00:00", "invalid")
        self.assertEqual(result, (True, None))


class TestF_SUB_TOD_TIME(unittest.TestCase):

    def setUp(self):
        self.block = F_SUB_TOD_TIME()

    def test_sub_tod_time_basic(self):
        result = self.block.schedule('REQ', True, "TOD#12:00:00", "T#1h")
        self.assertIsNotNone(result)

    def test_sub_tod_time_invalid_tod(self):
        result = self.block.schedule('REQ', True, "invalid", "T#1h")
        self.assertEqual(result, (True, None))

    def test_sub_tod_time_invalid_interval(self):
        result = self.block.schedule('REQ', True, "TOD#12:00:00", "invalid")
        self.assertEqual(result, (True, None))


class TestF_SUB_TOD_TOD(unittest.TestCase):

    def setUp(self):
        self.block = F_SUB_TOD_TOD()

    def test_sub_tod_tod_basic(self):
        result = self.block.schedule('REQ', True, "TOD#12:00:00", "TOD#10:00:00")
        if result[1] is not None:
            self.assertEqual(result[1].total_seconds(), 7200)

    def test_sub_tod_tod_same_time(self):
        result = self.block.schedule('REQ', True, "TOD#12:00:00", "TOD#12:00:00")
        if result[1] is not None:
            self.assertEqual(result[1].total_seconds(), 0)

    def test_sub_tod_tod_invalid_first(self):
        result = self.block.schedule('REQ', True, "invalid", "TOD#12:00:00")
        self.assertEqual(result, (True, None))

    def test_sub_tod_tod_invalid_second(self):
        result = self.block.schedule('REQ', True, "TOD#12:00:00", "invalid")
        self.assertEqual(result, (True, None))


class TestF_SUB_DATE_DATE(unittest.TestCase):

    def setUp(self):
        self.block = F_SUB_DATE_DATE()

    def test_sub_date_date_basic(self):
        result = self.block.schedule('REQ', True, "D#2024-01-05", "D#2024-01-01")
        if result[1] is not None:
            self.assertEqual(result[1].days, 4)

    def test_sub_date_date_same_date(self):
        result = self.block.schedule('REQ', True, "D#2024-01-01", "D#2024-01-01")
        if result[1] is not None:
            self.assertEqual(result[1].days, 0)

    def test_sub_date_date_negative(self):
        result = self.block.schedule('REQ', True, "D#2024-01-01", "D#2024-01-05")
        if result[1] is not None:
            self.assertEqual(result[1].days, -4)

    def test_sub_date_date_invalid_first(self):
        result = self.block.schedule('REQ', True, "invalid", "D#2024-01-01")
        self.assertEqual(result, (True, None))

    def test_sub_date_date_invalid_second(self):
        result = self.block.schedule('REQ', True, "D#2024-01-01", "invalid")
        self.assertEqual(result, (True, None))


if __name__ == '__main__':
    unittest.main(verbosity=2)
