import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.counters.FB_CTU import FB_CTU
from openfb.resources.function_blocks.iec61131.counters.FB_CTD import FB_CTD
from openfb.resources.function_blocks.iec61131.counters.FB_CTUD import FB_CTUD

class TestFB_CTU(unittest.TestCase):
    def setUp(self):
        self.counter = FB_CTU()

    def test_ctu_no_action(self):
        result = self.counter.schedule('REQ', True, False, False, 5)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], 0)

    def test_ctu_reset(self):
        self.counter.schedule('REQ', True, True, False, 5)
        self.counter.schedule('REQ', True, True, False, 5)
        result = self.counter.schedule('REQ', True, False, True, 5)
        self.assertEqual(result[2], 0)

    def test_ctu_increment(self):
        result1 = self.counter.schedule('REQ', True, True, False, 5)
        self.assertEqual(result1[2], 1)
        result2 = self.counter.schedule('REQ', True, True, False, 5)
        self.assertEqual(result2[2], 2)
        result3 = self.counter.schedule('REQ', True, True, False, 5)
        self.assertEqual(result3[2], 3)

    def test_ctu_multiple_increments(self):
        for _ in range(5):
            self.counter.schedule('REQ', True, True, False, 10)
        result = self.counter.schedule('REQ', True, False, False, 10)
        self.assertEqual(result[2], 5)

    def test_ctu_output_q_trigger(self):
        result1 = self.counter.schedule('REQ', True, True, False, 3)
        self.assertEqual(result1[1], False)
        result2 = self.counter.schedule('REQ', True, True, False, 3)
        self.assertEqual(result2[1], False)
        result3 = self.counter.schedule('REQ', True, True, False, 3)
        self.assertEqual(result3[1], True)

    def test_ctu_output_q_stays_high(self):
        for _ in range(3):
            self.counter.schedule('REQ', True, True, False, 3)
        for _ in range(2):
            result = self.counter.schedule('REQ', True, True, False, 3)
            self.assertEqual(result[1], True)

    def test_ctu_overflow_protection(self):
        self.counter.cv = 32767
        result = self.counter.schedule('REQ', True, True, False, 10000)
        self.assertEqual(result[2], 32767)

    def test_ctu_reset_priority(self):
        for _ in range(5):
            self.counter.schedule('REQ', True, True, False, 10)
        result = self.counter.schedule('REQ', True, True, True, 10)
        self.assertEqual(result[2], 0)

    def test_ctu_cu_false_no_increment(self):
        result1 = self.counter.schedule('REQ', True, False, False, 10)
        self.assertEqual(result1[2], 0)
        result2 = self.counter.schedule('REQ', True, False, False, 10)
        self.assertEqual(result2[2], 0)

    def test_ctu_wrong_event(self):
        result = self.counter.schedule('WRONG', True, True, False, 5)
        self.assertIsNone(result)

class TestFB_CTD(unittest.TestCase):
    def setUp(self):
        self.counter = FB_CTD()

    def test_ctd_no_action(self):
        result = self.counter.schedule('REQ', True, False, False, 5)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], 0)

    def test_ctd_load(self):
        result = self.counter.schedule('REQ', True, False, True, 5)
        self.assertEqual(result[2], 5)

    def test_ctd_decrement(self):
        self.counter.schedule('REQ', True, False, True, 5)
        result1 = self.counter.schedule('REQ', True, True, False, 5)
        self.assertEqual(result1[2], 4)
        result2 = self.counter.schedule('REQ', True, True, False, 5)
        self.assertEqual(result2[2], 3)

    def test_ctd_multiple_decrements(self):
        self.counter.schedule('REQ', True, False, True, 10)
        for _ in range(5):
            self.counter.schedule('REQ', True, True, False, 10)
        result = self.counter.schedule('REQ', True, False, False, 10)
        self.assertEqual(result[2], 5)

    def test_ctd_output_q_at_zero(self):
        self.counter.schedule('REQ', True, False, True, 2)
        result1 = self.counter.schedule('REQ', True, True, False, 2)
        self.assertEqual(result1[1], False)
        result2 = self.counter.schedule('REQ', True, True, False, 2)
        self.assertEqual(result2[1], True)

    def test_ctd_underflow_protection(self):
        self.counter.cv = -32768
        result = self.counter.schedule('REQ', True, True, False, -10000)
        self.assertEqual(result[2], -32768)

    def test_ctd_load_priority(self):
        self.counter.schedule('REQ', True, False, True, 10)
        result = self.counter.schedule('REQ', True, True, True, 10)
        self.assertEqual(result[2], 10)

    def test_ctd_cd_false_no_decrement(self):
        self.counter.schedule('REQ', True, False, True, 10)
        result1 = self.counter.schedule('REQ', True, False, False, 10)
        self.assertEqual(result1[2], 10)
        result2 = self.counter.schedule('REQ', True, False, False, 10)
        self.assertEqual(result2[2], 10)

class TestFB_CTUD(unittest.TestCase):
    def setUp(self):
        self.counter = FB_CTUD()

    def test_ctud_no_action(self):
        result = self.counter.schedule('REQ', True, False, False, False, False, 5)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)
        self.assertEqual(result[3], 0)

    def test_ctud_reset(self):
        self.counter.cv = 10
        result = self.counter.schedule('REQ', True, False, False, True, False, 5)
        self.assertEqual(result[3], 0)

    def test_ctud_load(self):
        result = self.counter.schedule('REQ', True, False, False, False, True, 5)
        self.assertEqual(result[3], 5)

    def test_ctud_count_up(self):
        result1 = self.counter.schedule('REQ', True, True, False, False, False, 10)
        self.assertEqual(result1[3], 1)
        result2 = self.counter.schedule('REQ', True, True, False, False, False, 10)
        self.assertEqual(result2[3], 2)

    def test_ctud_count_down(self):
        self.counter.schedule('REQ', True, False, False, False, True, 5)
        result1 = self.counter.schedule('REQ', True, False, True, False, False, 5)
        self.assertEqual(result1[3], 4)
        result2 = self.counter.schedule('REQ', True, False, True, False, False, 5)
        self.assertEqual(result2[3], 3)

    def test_ctud_qu_output(self):
        for _ in range(3):
            self.counter.schedule('REQ', True, True, False, False, False, 3)
        result = self.counter.schedule('REQ', True, False, False, False, False, 3)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], False)

    def test_ctud_qd_output(self):
        self.counter.schedule('REQ', True, False, False, False, True, 2)
        self.counter.schedule('REQ', True, False, True, False, False, 2)
        self.counter.schedule('REQ', True, False, True, False, False, 2)
        result = self.counter.schedule('REQ', True, False, False, False, False, 2)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)

    def test_ctud_cu_and_cd_together(self):
        result = self.counter.schedule('REQ', True, True, True, False, False, 10)
        self.assertEqual(result[3], 0)

    def test_ctud_reset_priority(self):
        self.counter.cv = 10
        result = self.counter.schedule('REQ', True, True, False, True, True, 5)
        self.assertEqual(result[3], 0)

    def test_ctud_load_priority_over_cu_cd(self):
        result = self.counter.schedule('REQ', True, True, False, False, True, 5)
        self.assertEqual(result[3], 5)

    def test_ctud_overflow_up(self):
        self.counter.cv = 32767
        result = self.counter.schedule('REQ', True, True, False, False, False, 10000)
        self.assertEqual(result[3], 32767)

    def test_ctud_underflow_down(self):
        self.counter.cv = -32768
        result = self.counter.schedule('REQ', True, False, True, False, False, -10000)
        self.assertEqual(result[3], -32768)

    def test_ctud_sequence_operations(self):
        self.counter.schedule('REQ', True, False, False, False, True, 10)
        self.assertEqual(self.counter.cv, 10)
        self.counter.schedule('REQ', True, True, False, False, False, 10)
        self.assertEqual(self.counter.cv, 11)
        self.counter.schedule('REQ', True, False, True, False, False, 10)
        self.assertEqual(self.counter.cv, 10)
        self.counter.schedule('REQ', True, False, False, True, False, 10)
        self.assertEqual(self.counter.cv, 0)

    def test_ctud_wrong_event(self):
        result = self.counter.schedule('WRONG', True, True, False, False, False, 5)
        self.assertIsNone(result)

class TestCountersComparison(unittest.TestCase):
    def test_ctu_vs_ctd(self):
        ctu = FB_CTU()
        ctd = FB_CTD()
        ctu.schedule('REQ', True, True, False, 10)
        ctu_result = ctu.schedule('REQ', True, True, False, 10)[2]
        ctd.schedule('REQ', True, False, True, 10)
        ctd.schedule('REQ', True, True, False, 10)
        ctd_result = ctd.schedule('REQ', True, True, False, 10)[2]
        self.assertEqual(ctu_result, 2)
        self.assertEqual(ctd_result, 8)

    def test_ctud_combines_ctu_ctd(self):
        ctud = FB_CTUD()
        ctud.schedule('REQ', True, False, False, False, True, 10)
        ctud.schedule('REQ', True, True, False, False, False, 10)
        ctud_up = ctud.schedule('REQ', True, True, False, False, False, 10)[3]
        ctud.schedule('REQ', True, False, True, False, False, 10)
        ctud_down = ctud.schedule('REQ', True, False, True, False, False, 10)[3]
        self.assertEqual(ctud_up, 12)
        self.assertEqual(ctud_down, 10)

    def test_counter_output_signals(self):
        ctu = FB_CTU()
        ctd = FB_CTD()
        ctud = FB_CTUD()
        ctu.schedule('REQ', True, True, False, 2)
        ctu_q1 = ctu.schedule('REQ', True, True, False, 2)[1]
        ctd.schedule('REQ', True, False, True, 2)
        ctd.schedule('REQ', True, True, False, 2)
        ctd.schedule('REQ', True, True, False, 2)
        ctd_q1 = ctd.schedule('REQ', True, False, False, 2)[1]
        for _ in range(2):
            ctud.schedule('REQ', True, True, False, False, False, 2)
        ctud_qu = ctud.schedule('REQ', True, False, False, False, False, 2)[1]
        self.assertEqual(ctu_q1, True)
        self.assertEqual(ctd_q1, True)
        self.assertEqual(ctud_qu, True)

if __name__ == '__main__':
    unittest.main(verbosity=2)
