import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.selection.F_LIMIT import F_LIMIT
from openfb.resources.function_blocks.iec61131.selection.F_MAX import F_MAX
from openfb.resources.function_blocks.iec61131.selection.F_MIN import F_MIN
from openfb.resources.function_blocks.iec61131.selection.F_MOVE import F_MOVE
from openfb.resources.function_blocks.iec61131.selection.F_SEL import F_SEL
from openfb.resources.function_blocks.iec61131.selection.F_MUX_2 import F_MUX_2
from openfb.resources.function_blocks.iec61131.selection.F_MUX_3 import F_MUX_3
from openfb.resources.function_blocks.iec61131.selection.F_MUX_4 import F_MUX_4

class TestF_LIMIT(unittest.TestCase):
    def setUp(self):
        self.block = F_LIMIT()
    
    def test_limit_in_range(self):
        result = self.block.schedule('REQ', True, 0, 5, 10)
        self.assertEqual(result, (True, 5))
    def test_limit_below_min(self):
        result = self.block.schedule('REQ', True, 5, 2, 10)
        self.assertEqual(result, (True, 5))
    def test_limit_above_max(self):
        result = self.block.schedule('REQ', True, 0, 15, 10)
        self.assertEqual(result, (True, 10))
    def test_limit_equal_min(self):
        result = self.block.schedule('REQ', True, 5, 5, 10)
        self.assertEqual(result, (True, 5))
    def test_limit_equal_max(self):
        result = self.block.schedule('REQ', True, 0, 10, 10)
        self.assertEqual(result, (True, 10))
    def test_limit_negative(self):
        result = self.block.schedule('REQ', True, -10, -5, 0)
        self.assertEqual(result, (True, -5))
    def test_limit_floats(self):
        result = self.block.schedule('REQ', True, 0.5, 5.5, 10.5)
        self.assertEqual(result, (True, 5.5))
    def test_limit_reversed_bounds(self):
        result = self.block.schedule('REQ', True, 10, 5, 0)
        self.assertEqual(result, (True, max(10, min(5, 0))))

class TestF_MAX(unittest.TestCase):
    def setUp(self):
        self.block = F_MAX()
    
    def test_max_first_larger(self):
        result = self.block.schedule('REQ', True, 10, 5)
        self.assertEqual(result, (True, 10))
    def test_max_second_larger(self):
        result = self.block.schedule('REQ', True, 5, 10)
        self.assertEqual(result, (True, 10))
    def test_max_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, 5))
    def test_max_negative(self):
        result = self.block.schedule('REQ', True, -10, -5)
        self.assertEqual(result, (True, -5))
    def test_max_mixed_signs(self):
        result = self.block.schedule('REQ', True, -5, 5)
        self.assertEqual(result, (True, 5))
    def test_max_floats(self):
        result = self.block.schedule('REQ', True, 5.5, 3.2)
        self.assertEqual(result, (True, 5.5))
    def test_max_with_zero(self):
        result = self.block.schedule('REQ', True, 0, 5)
        self.assertEqual(result, (True, 5))
    def test_max_invalid_types(self):
        result = self.block.schedule('REQ', True, 5, "invalid")
        self.assertEqual(result, (True, None))

class TestF_MIN(unittest.TestCase):
    def setUp(self):
        self.block = F_MIN()
    
    def test_min_first_smaller(self):
        result = self.block.schedule('REQ', True, 5, 10)
        self.assertEqual(result, (True, 5))
    def test_min_second_smaller(self):
        result = self.block.schedule('REQ', True, 10, 5)
        self.assertEqual(result, (True, 5))
    def test_min_equal(self):
        result = self.block.schedule('REQ', True, 5, 5)
        self.assertEqual(result, (True, 5))
    def test_min_negative(self):
        result = self.block.schedule('REQ', True, -10, -5)
        self.assertEqual(result, (True, -10))
    def test_min_mixed_signs(self):
        result = self.block.schedule('REQ', True, -5, 5)
        self.assertEqual(result, (True, -5))
    def test_min_floats(self):
        result = self.block.schedule('REQ', True, 5.5, 3.2)
        self.assertEqual(result, (True, 3.2))
    def test_min_with_zero(self):
        result = self.block.schedule('REQ', True, 0, 5)
        self.assertEqual(result, (True, 0))

class TestF_MOVE(unittest.TestCase):
    def setUp(self):
        self.block = F_MOVE()
    
    def test_move_integer(self):
        result = self.block.schedule('REQ', True, 5)
        self.assertEqual(result, (True, 5))
    def test_move_float(self):
        result = self.block.schedule('REQ', True, 5.5)
        self.assertEqual(result, (True, 5.5))
    def test_move_string(self):
        result = self.block.schedule('REQ', True, "Hello")
        self.assertEqual(result, (True, "Hello"))
    def test_move_zero(self):
        result = self.block.schedule('REQ', True, 0)
        self.assertEqual(result, (True, 0))
    def test_move_negative(self):
        result = self.block.schedule('REQ', True, -5)
        self.assertEqual(result, (True, -5))
    def test_move_boolean(self):
        result = self.block.schedule('REQ', True, True)
        self.assertEqual(result, (True, True))
    def test_move_none(self):
        result = self.block.schedule('REQ', True, None)
        self.assertEqual(result, (True, None))
    def test_move_empty_string(self):
        result = self.block.schedule('REQ', True, "")
        self.assertEqual(result, (True, ""))
    def test_move_list(self):
        test_list = [1, 2, 3]
        result = self.block.schedule('REQ', True, test_list)
        self.assertEqual(result, (True, test_list))

class TestF_SEL(unittest.TestCase):
    def setUp(self):
        self.block = F_SEL()
    
    def test_sel_true_first(self):
        result = self.block.schedule('REQ', True, True, "First", "Second")
        self.assertEqual(result, (True, "First"))
    def test_sel_false_second(self):
        result = self.block.schedule('REQ', True, False, "First", "Second")
        self.assertEqual(result, (True, "Second"))
    def test_sel_with_numbers(self):
        result = self.block.schedule('REQ', True, True, 10, 20)
        self.assertEqual(result, (True, 10))
    def test_sel_false_with_numbers(self):
        result = self.block.schedule('REQ', True, False, 10, 20)
        self.assertEqual(result, (True, 20))
    def test_sel_with_zero(self):
        result = self.block.schedule('REQ', True, 0, "First", "Second")
        self.assertEqual(result, (True, "Second"))
    def test_sel_with_one(self):
        result = self.block.schedule('REQ', True, 1, "First", "Second")
        self.assertEqual(result, (True, "First"))
    def test_sel_none_first(self):
        result = self.block.schedule('REQ', True, True, None, "Second")
        self.assertEqual(result, (True, None))
    def test_sel_none_second(self):
        result = self.block.schedule('REQ', True, False, "First", None)
        self.assertEqual(result, (True, None))

class TestF_MUX_2(unittest.TestCase):
    def setUp(self):
        self.block = F_MUX_2()
    
    def test_mux_2_select_first(self):
        result = self.block.schedule('REQ', True, "First", "Second", 0)
        self.assertEqual(result, (True, "First"))
    def test_mux_2_select_second(self):
        result = self.block.schedule('REQ', True, "First", "Second", 1)
        self.assertEqual(result, (True, "Second"))
    def test_mux_2_invalid_index(self):
        result = self.block.schedule('REQ', True, "First", "Second", 5)
        self.assertEqual(result, (True, "Second"))
    def test_mux_2_with_numbers(self):
        result = self.block.schedule('REQ', True, 10, 20, 0)
        self.assertEqual(result, (True, 10))
    def test_mux_2_negative_index(self):
        result = self.block.schedule('REQ', True, "A", "B", -1)
        self.assertEqual(result, (True, "B"))

class TestF_MUX_3(unittest.TestCase):
    def setUp(self):
        self.block = F_MUX_3()
    
    def test_mux_3_select_first(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", 0)
        self.assertEqual(result, (True, "A"))
    def test_mux_3_select_second(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", 1)
        self.assertEqual(result, (True, "B"))
    def test_mux_3_select_third(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", 2)
        self.assertEqual(result, (True, "C"))
    def test_mux_3_invalid_index_high(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", 5)
        self.assertEqual(result, (True, "C"))
    def test_mux_3_with_numbers(self):
        result = self.block.schedule('REQ', True, 10, 20, 30, 1)
        self.assertEqual(result, (True, 20))
    def test_mux_3_with_mixed_types(self):
        result = self.block.schedule('REQ', True, 1, "B", 3.5, 2)
        self.assertEqual(result, (True, 3.5))

class TestF_MUX_4(unittest.TestCase):
    def setUp(self):
        self.block = F_MUX_4()
    
    def test_mux_4_select_first(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", "D", 0)
        self.assertEqual(result, (True, "A"))
    def test_mux_4_select_second(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", "D", 1)
        self.assertEqual(result, (True, "B"))
    def test_mux_4_select_third(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", "D", 2)
        self.assertEqual(result, (True, "C"))
    def test_mux_4_select_fourth(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", "D", 3)
        self.assertEqual(result, (True, "D"))
    def test_mux_4_invalid_index_high(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", "D", 10)
        self.assertEqual(result, (True, "D"))
    def test_mux_4_with_numbers(self):
        result = self.block.schedule('REQ', True, 10, 20, 30, 40, 2)
        self.assertEqual(result, (True, 30))
    def test_mux_4_negative_index(self):
        result = self.block.schedule('REQ', True, "A", "B", "C", "D", -1)
        self.assertEqual(result, (True, "D"))
    def test_mux_4_with_none(self):
        result = self.block.schedule('REQ', True, None, "B", None, "D", 1)
        self.assertEqual(result, (True, "B"))

class TestSelectionComparison(unittest.TestCase):
    def test_max_min_complementary(self):
        max_block = F_MAX()
        min_block = F_MIN()
        max_result = max_block.schedule('REQ', True, 5, 10)[1]
        min_result = min_block.schedule('REQ', True, 5, 10)[1]
        
        self.assertEqual(max_result, 10)
        self.assertEqual(min_result, 5)
    
    def test_limit_with_max_min(self):
        limit_block = F_LIMIT()
        result = limit_block.schedule('REQ', True, 0, 5, 10)[1]
        self.assertEqual(result, 5)
        
        result = limit_block.schedule('REQ', True, 0, 15, 10)[1]
        self.assertEqual(result, 10)

if __name__ == '__main__':
    unittest.main(verbosity=2)
