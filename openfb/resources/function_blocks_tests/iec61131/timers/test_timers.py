import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.timers.FB_TON import FB_TON
from openfb.resources.function_blocks.iec61131.timers.FB_TOF import FB_TOF
from openfb.resources.function_blocks.iec61131.timers.FB_TP import FB_TP


class TestFB_TON(unittest.TestCase):

    def setUp(self):
        self.block = FB_TON()

    def test_ton_not_triggered(self):
        result = self.block.schedule('REQ', True, False, "T#5s")
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], timedelta(0))

    def test_ton_triggered_not_elapsed(self):
        result = self.block.schedule('REQ', True, True, "T#5s")
        self.assertEqual(result[1], False)

    def test_ton_timer_with_mocked_time(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TON.time.monotonic') as mock_time:
            times = [0, 3, 6]
            mock_time.side_effect = times
            result1 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result1[1], False)
            result2 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result2[1], False)
            result3 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result3[1], True)

    def test_ton_reset_by_input(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TON.time.monotonic') as mock_time:
            times = [0, 2, 4, 4, 6]
            mock_time.side_effect = times
            self.block.schedule('REQ', True, True, "T#5s")
            self.block.schedule('REQ', True, True, "T#5s")
            result = self.block.schedule('REQ', True, False, "T#5s")
            self.assertEqual(result[1], False)
            self.assertEqual(result[2], timedelta(0))

    def test_ton_invalid_time_format(self):
        result = self.block.schedule('REQ', True, True, "invalid")
        self.assertEqual(result[1], None)

    def test_ton_edge_case_zero_time(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TON.time.monotonic') as mock_time:
            times = [0, 0.001]
            mock_time.side_effect = times
            result1 = self.block.schedule('REQ', True, True, "T#0s")
            self.assertEqual(result1[1], True)


class TestFB_TOF(unittest.TestCase):

    def setUp(self):
        self.block = FB_TOF()

    def test_tof_input_high(self):
        result = self.block.schedule('REQ', True, True, "T#5s")
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], timedelta(0))

    def test_tof_input_transitions_low(self):
        self.block.schedule('REQ', True, True, "T#5s")
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TOF.time.monotonic') as mock_time:
            times = [0, 0]
            mock_time.side_effect = times
            result = self.block.schedule('REQ', True, False, "T#5s")
            self.assertEqual(result[1], True)

    def test_tof_delay_elapsed(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TOF.time.monotonic') as mock_time:
            times = [0, 0, 6]
            mock_time.side_effect = times
            self.block.schedule('REQ', True, True, "T#5s")
            self.block.schedule('REQ', True, False, "T#5s")
            result = self.block.schedule('REQ', True, False, "T#5s")
            self.assertEqual(result[1], False)

    def test_tof_input_high_again_resets(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TOF.time.monotonic') as mock_time:
            times = [0, 0, 2, 2]
            mock_time.side_effect = times
            self.block.schedule('REQ', True, True, "T#5s")
            self.block.schedule('REQ', True, False, "T#5s")
            result1 = self.block.schedule('REQ', True, False, "T#5s")
            self.assertEqual(result1[1], True)
            result2 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result2[1], True)

    def test_tof_invalid_time_format(self):
        result = self.block.schedule('REQ', True, True, "invalid")
        self.assertEqual(result[1], None)


class TestFB_TP(unittest.TestCase):

    def setUp(self):
        self.block = FB_TP()

    def test_tp_not_triggered(self):
        result = self.block.schedule('REQ', True, False, "T#5s")
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], timedelta(0))

    def test_tp_rising_edge_starts_pulse(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TP.time.monotonic') as mock_time:
            times = [0, 0]
            mock_time.side_effect = times
            self.block.schedule('REQ', True, False, "T#5s")
            result = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result[1], True)

    def test_tp_pulse_duration(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TP.time.monotonic') as mock_time:
            times = [0, 0, 3, 6]
            mock_time.side_effect = times
            self.block.schedule('REQ', True, False, "T#5s")
            self.block.schedule('REQ', True, True, "T#5s")
            result1 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result1[1], True)
            result2 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result2[1], False)

    def test_tp_input_high_does_not_restart_pulse(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TP.time.monotonic') as mock_time:
            times = [0, 0, 1, 2]
            mock_time.side_effect = times
            self.block.schedule('REQ', True, False, "T#5s")
            self.block.schedule('REQ', True, True, "T#5s")
            result1 = self.block.schedule('REQ', True, True, "T#5s")
            result2 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertIsNotNone(result1[1])
            self.assertIsNotNone(result2[1])

    def test_tp_input_low_then_high_restarts(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TP.time.monotonic') as mock_time:
            times = [0, 0, 6, 6, 6]
            mock_time.side_effect = times
            self.block.schedule('REQ', True, False, "T#5s")
            self.block.schedule('REQ', True, True, "T#5s")
            self.block.schedule('REQ', True, True, "T#5s")
            result1 = self.block.schedule('REQ', True, False, "T#5s")
            self.assertEqual(result1[1], False)
            result2 = self.block.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result2[1], True)

    def test_tp_invalid_time_format(self):
        result = self.block.schedule('REQ', True, True, "invalid")
        self.assertEqual(result[1], None)


class TestTimersComparison(unittest.TestCase):

    def test_ton_tof_complementary(self):
        ton = FB_TON()
        tof = FB_TOF()
        ton_result = ton.schedule('REQ', True, True, "T#5s")[1]
        tof_result = tof.schedule('REQ', True, True, "T#5s")[1]
        self.assertEqual(ton_result, False)
        self.assertEqual(tof_result, True)

    def test_tp_single_pulse(self):
        with patch('openfb.resources.function_blocks.iec61131.timers.FB_TP.time.monotonic') as mock_time:
            times = [0, 0, 1, 2]
            mock_time.side_effect = times
            tp = FB_TP()
            tp.schedule('REQ', True, False, "T#5s")
            result1 = tp.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result1[1], True)
            result2 = tp.schedule('REQ', True, True, "T#5s")
            self.assertEqual(result2[1], True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
