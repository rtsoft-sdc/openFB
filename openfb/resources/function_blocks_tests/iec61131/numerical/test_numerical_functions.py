import unittest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.numerical.F_ABS import F_ABS
from openfb.resources.function_blocks.iec61131.numerical.F_SQRT import F_SQRT
from openfb.resources.function_blocks.iec61131.numerical.F_SIN import F_SIN
from openfb.resources.function_blocks.iec61131.numerical.F_COS import F_COS
from openfb.resources.function_blocks.iec61131.numerical.F_TAN import F_TAN
from openfb.resources.function_blocks.iec61131.numerical.F_ASIN import F_ASIN
from openfb.resources.function_blocks.iec61131.numerical.F_ACOS import F_ACOS
from openfb.resources.function_blocks.iec61131.numerical.F_ATAN import F_ATAN
from openfb.resources.function_blocks.iec61131.numerical.F_LN import F_LN
from openfb.resources.function_blocks.iec61131.numerical.F_LOG import F_LOG
from openfb.resources.function_blocks.iec61131.numerical.F_EXP import F_EXP

class TestF_ABS(unittest.TestCase):

    def setUp(self):
        self.block = F_ABS()

    def test_abs_positive(self):
        result = self.block.schedule('REQ', True, 5)
        self.assertEqual(result, (True, 5))

    def test_abs_negative(self):
        result = self.block.schedule('REQ', True, -5)
        self.assertEqual(result, (True, 5))

    def test_abs_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertEqual(result, (True, 0))

    def test_abs_float(self):
        result = self.block.schedule('REQ', True, -5.5)
        self.assertEqual(result, (True, 5.5))

    def test_abs_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_SQRT(unittest.TestCase):

    def setUp(self):
        self.block = F_SQRT()

    def test_sqrt_perfect_square(self):
        result = self.block.schedule('REQ', True, 9)
        self.assertEqual(result, (True, 3.0))

    def test_sqrt_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertEqual(result, (True, 0.0))

    def test_sqrt_one(self):
        result = self.block.schedule('REQ', True, 1)
        self.assertEqual(result, (True, 1.0))

    def test_sqrt_fraction(self):
        result = self.block.schedule('REQ', True, 2.25)
        self.assertAlmostEqual(result[1], 1.5, places=5)

    def test_sqrt_large_number(self):
        result = self.block.schedule('REQ', True, 10000)
        self.assertEqual(result, (True, 100.0))

    def test_sqrt_negative(self):
        result = self.block.schedule('REQ', True, -1)
        self.assertEqual(result, (True, None))

    def test_sqrt_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_SIN(unittest.TestCase):

    def setUp(self):
        self.block = F_SIN()

    def test_sin_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_sin_pi_half(self):
        result = self.block.schedule('REQ', True, math.pi / 2)
        self.assertAlmostEqual(result[1], 1, places=5)

    def test_sin_pi(self):
        result = self.block.schedule('REQ', True, math.pi)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_sin_negative(self):
        result = self.block.schedule('REQ', True, -math.pi / 2)
        self.assertAlmostEqual(result[1], -1, places=5)

    def test_sin_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_COS(unittest.TestCase):

    def setUp(self):
        self.block = F_COS()

    def test_cos_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertAlmostEqual(result[1], 1, places=5)

    def test_cos_pi_half(self):
        result = self.block.schedule('REQ', True, math.pi / 2)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_cos_pi(self):
        result = self.block.schedule('REQ', True, math.pi)
        self.assertAlmostEqual(result[1], -1, places=5)

    def test_cos_negative(self):
        result = self.block.schedule('REQ', True, -math.pi)
        self.assertAlmostEqual(result[1], -1, places=5)

    def test_cos_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_TAN(unittest.TestCase):

    def setUp(self):
        self.block = F_TAN()

    def test_tan_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_tan_pi_quarter(self):
        result = self.block.schedule('REQ', True, math.pi / 4)
        self.assertAlmostEqual(result[1], 1, places=5)

    def test_tan_negative(self):
        result = self.block.schedule('REQ', True, -math.pi / 4)
        self.assertAlmostEqual(result[1], -1, places=5)

    def test_tan_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_ASIN(unittest.TestCase):

    def setUp(self):
        self.block = F_ASIN()

    def test_asin_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_asin_one(self):
        result = self.block.schedule('REQ', True, 1)
        self.assertAlmostEqual(result[1], math.pi / 2, places=5)

    def test_asin_minus_one(self):
        result = self.block.schedule('REQ', True, -1)
        self.assertAlmostEqual(result[1], -math.pi / 2, places=5)

    def test_asin_half(self):
        result = self.block.schedule('REQ', True, 0.5)
        self.assertAlmostEqual(result[1], math.pi / 6, places=5)

    def test_asin_out_of_range(self):
        result = self.block.schedule('REQ', True, 1.5)
        self.assertEqual(result, (True, None))

    def test_asin_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_ACOS(unittest.TestCase):

    def setUp(self):
        self.block = F_ACOS()

    def test_acos_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertAlmostEqual(result[1], math.pi / 2, places=5)

    def test_acos_one(self):
        result = self.block.schedule('REQ', True, 1)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_acos_minus_one(self):
        result = self.block.schedule('REQ', True, -1)
        self.assertAlmostEqual(result[1], math.pi, places=5)

    def test_acos_half(self):
        result = self.block.schedule('REQ', True, 0.5)
        self.assertAlmostEqual(result[1], math.pi / 3, places=5)

    def test_acos_out_of_range(self):
        result = self.block.schedule('REQ', True, -1.5)
        self.assertEqual(result, (True, None))

class TestF_ATAN(unittest.TestCase):

    def setUp(self):
        self.block = F_ATAN()

    def test_atan_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_atan_one(self):
        result = self.block.schedule('REQ', True, 1)
        self.assertAlmostEqual(result[1], math.pi / 4, places=5)

    def test_atan_minus_one(self):
        result = self.block.schedule('REQ', True, -1)
        self.assertAlmostEqual(result[1], -math.pi / 4, places=5)

    def test_atan_large_number(self):
        result = self.block.schedule('REQ', True, 1000)
        self.assertAlmostEqual(result[1], math.pi / 2, places=2)

    def test_atan_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_LN(unittest.TestCase):

    def setUp(self):
        self.block = F_LN()

    def test_ln_one(self):
        result = self.block.schedule('REQ', True, 1)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_ln_e(self):
        result = self.block.schedule('REQ', True, math.e)
        self.assertAlmostEqual(result[1], 1, places=5)

    def test_ln_ten(self):
        result = self.block.schedule('REQ', True, 10)
        self.assertAlmostEqual(result[1], math.log(10), places=5)

    def test_ln_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertEqual(result, (True, None))

    def test_ln_negative(self):
        result = self.block.schedule('REQ', True, -1)
        self.assertEqual(result, (True, None))

    def test_ln_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_LOG(unittest.TestCase):

    def setUp(self):
        self.block = F_LOG()

    def test_log_one(self):
        result = self.block.schedule('REQ', True, 1)
        self.assertAlmostEqual(result[1], 0, places=5)

    def test_log_ten(self):
        result = self.block.schedule('REQ', True, 10)
        self.assertAlmostEqual(result[1], 1, places=5)

    def test_log_hundred(self):
        result = self.block.schedule('REQ', True, 100)
        self.assertAlmostEqual(result[1], 2, places=5)

    def test_log_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertEqual(result, (True, None))

    def test_log_negative(self):
        result = self.block.schedule('REQ', True, -10)
        self.assertEqual(result, (True, None))

    def test_log_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

class TestF_EXP(unittest.TestCase):

    def setUp(self):
        self.block = F_EXP()

    def test_exp_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertAlmostEqual(result[1], 1, places=5)

    def test_exp_one(self):
        result = self.block.schedule('REQ', True, 1)
        self.assertAlmostEqual(result[1], math.e, places=5)

    def test_exp_negative(self):
        result = self.block.schedule('REQ', True, -1)
        self.assertAlmostEqual(result[1], 1 / math.e, places=5)

    def test_exp_two(self):
        result = self.block.schedule('REQ', True, 2)
        self.assertAlmostEqual(result[1], math.e ** 2, places=5)

    def test_exp_small_negative(self):
        result = self.block.schedule('REQ', True, -10)
        self.assertAlmostEqual(result[1], math.exp(-10), places=10)

    def test_exp_invalid_type(self):
        result = self.block.schedule('REQ', True, "invalid")
        self.assertEqual(result, (True, None))

if __name__ == '__main__':
    unittest.main(verbosity=2)
