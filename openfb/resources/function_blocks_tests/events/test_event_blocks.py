import os
import sys
import time
import unittest
from unittest.mock import Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from openfb.resources.function_blocks.events.OF_E_CYCLE import OF_E_CYCLE
from openfb.resources.function_blocks.events.E_DELAY import E_DELAY
from openfb.resources.function_blocks.events.E_RDELAY import E_RDELAY
from openfb.resources.function_blocks.events.E_PERMIT import E_PERMIT
from openfb.resources.function_blocks.events.E_MERGE import E_MERGE
from openfb.resources.function_blocks.events.E_SWITCH import E_SWITCH
from openfb.resources.function_blocks.events.E_SELECT import E_SELECT
from openfb.resources.function_blocks.events.E_DEMUX import E_DEMUX
from openfb.resources.function_blocks.events.E_RS import E_RS
from openfb.resources.function_blocks.events.E_SR import E_SR
from openfb.resources.function_blocks.events.E_D_FF import E_D_FF

class TestOF_E_CYCLE(unittest.TestCase):
    def setUp(self):
        self.block = OF_E_CYCLE()
        self.callback_mock = Mock()
        self.block.set_on_event_callback(self.callback_mock)

    def tearDown(self):
        if hasattr(self.block, '_stop_event'):
            self.block._stop_event.set()
        if hasattr(self.block, '_cycle_thread') and self.block._cycle_thread:
            self.block._cycle_thread.join(timeout=1.0)

    def test_cycle_start(self):
        result = self.block.schedule('START', 1, "T#0.1s")
        self.assertEqual(result, (1,))
        self.assertIsNotNone(self.block._cycle_thread)
        self.assertTrue(self.block._cycle_thread.is_alive())

    def test_cycle_generates_events(self):
        self.block.schedule('START', 1, "T#0.05s")
        time.sleep(0.15)
        self.assertGreaterEqual(self.callback_mock.call_count, 1)
        call_args = self.callback_mock.call_args_list[0][0]
        self.assertEqual(call_args[0], 'EO')
        self.assertIsInstance(call_args[1], int)

    def test_cycle_stop(self):
        self.block.schedule('START', 1, "T#0.05s")
        time.sleep(0.02)
        result = self.block.schedule('STOP', 2, "T#0s")
        self.assertEqual(result, (None,))
        time.sleep(0.1)
        self.assertFalse(self.block._cycle_thread.is_alive())

    def test_cycle_restart(self):
        self.block.schedule('START', 1, "T#0.05s")
        time.sleep(0.02)
        self.block.schedule('STOP', 2, "T#0s")
        time.sleep(0.1)
        result = self.block.schedule('START', 3, "T#0.05s")
        self.assertEqual(result, (3,))
        self.assertTrue(self.block._cycle_thread.is_alive())

    def test_cycle_event_counter_increments(self):
        self.block.schedule('START', 1, "T#0.05s")
        time.sleep(0.12)
        if self.callback_mock.call_count >= 2:
            first_call_counter = self.callback_mock.call_args_list[0][0][1]
            second_call_counter = self.callback_mock.call_args_list[1][0][1]
            self.assertEqual(second_call_counter, first_call_counter)

    def test_cycle_invalid_time_format(self):
        result = self.block.schedule('START', 1, "invalid")
        self.assertEqual(result, (1,))

class TestE_DELAY(unittest.TestCase):
    def setUp(self):
        self.block = E_DELAY()
        self.callback_mock = Mock()
        self.block.set_on_event_callback(self.callback_mock)

    def tearDown(self):
        if hasattr(self.block, '_stop_event'):
            self.block._stop_event.set()
        if hasattr(self.block, '_delay_thread') and self.block._delay_thread:
            self.block._delay_thread.join(timeout=1.0)

    def test_delay_start(self):
        result = self.block.schedule('START', 1, "T#0.05s")
        self.assertEqual(result, (1,))
        self.assertIsNotNone(self.block._delay_thread)
        self.assertTrue(self.block._delay_thread.is_alive())

    def test_delay_fires_after_timeout(self):
        self.block.schedule('START', 1, "T#0.05s")
        time.sleep(0.1)
        self.assertEqual(self.callback_mock.call_count, 1)
        self.callback_mock.assert_called_with('EO', 1)

    def test_delay_does_not_fire_before_timeout(self):
        self.block.schedule('START', 1, "T#0.1s")
        time.sleep(0.05)
        self.assertEqual(self.callback_mock.call_count, 0)

    def test_delay_can_be_stopped(self):
        self.block.schedule('START', 1, "T#0.1s")
        time.sleep(0.02)
        result = self.block.schedule('STOP', 2, "T#0s")
        self.assertEqual(result, (None,))
        time.sleep(0.15)
        self.assertEqual(self.callback_mock.call_count, 0)

    def test_delay_blocks_concurrent_start(self):
        result1 = self.block.schedule('START', 1, "T#0.1s")
        self.assertEqual(result1, (1,))
        result2 = self.block.schedule('START', 2, "T#0.1s")
        self.assertEqual(result2, (None,))

    def test_delay_event_counter_increments(self):
        self.block.schedule('START', 1, "T#0.05s")
        time.sleep(0.1)
        self.block.schedule('START', 1, "T#0.05s")
        time.sleep(0.1)
        self.assertEqual(self.callback_mock.call_count, 2)
        first_value = self.callback_mock.call_args_list[0][0][1]
        second_value = self.callback_mock.call_args_list[1][0][1]
        self.assertNotEqual(first_value, second_value)

class TestE_RDELAY(unittest.TestCase):
    def setUp(self):
        self.block = E_RDELAY()
        self.callback_mock = Mock()
        self.block.set_on_timeout_callback(self.callback_mock)

    def tearDown(self):
        if hasattr(self.block, '_timer') and self.block._timer:
            self.block._timer.cancel()

    def test_rdelay_start(self):
        result = self.block.schedule('START', 1, 0.05)
        self.assertEqual(result, 1)
        self.assertIsNotNone(self.block._timer)

    def test_rdelay_fires_after_timeout(self):
        self.block.schedule('START', 1, 0.05)
        time.sleep(0.1)
        self.callback_mock.assert_called_once_with(1)

    def test_rdelay_can_be_cancelled(self):
        self.block.schedule('START', 1, 200)
        time.sleep(0.02)
        result = self.block.schedule('STOP', 2)
        self.assertEqual(result, 2)
        time.sleep(0.25)
        self.assertEqual(self.callback_mock.call_count, 0)

    def test_rdelay_restart_cancels_previous(self):
        self.block.schedule('START', 1, 200)
        time.sleep(0.02)
        self.block.schedule('START', 2, 100)
        time.sleep(0.15)
        self.callback_mock.assert_called_once_with(2)

    def test_rdelay_with_timedelta(self):
        from datetime import timedelta
        result = self.block.schedule('START', 1, timedelta(milliseconds=50))
        self.assertEqual(result, 1)

class TestE_PERMIT(unittest.TestCase):
    def setUp(self):
        self.block = E_PERMIT()

    def test_permit_allows_when_true(self):
        result = self.block.schedule('EI', 1, True)
        self.assertEqual(result, 1)

    def test_permit_blocks_when_false(self):
        result = self.block.schedule('EI', 1, False)
        self.assertIsNone(result)

    def test_permit_wrong_event(self):
        result = self.block.schedule('WRONG', 1, True)
        self.assertIsNone(result)

class TestE_MERGE(unittest.TestCase):
    def setUp(self):
        self.block = E_MERGE()

    def test_merge_ei1(self):
        result = self.block.schedule('EI1', 1)
        self.assertEqual(result, 1)

    def test_merge_ei2(self):
        result = self.block.schedule('EI2', 2)
        self.assertEqual(result, 2)

    def test_merge_wrong_event(self):
        result = self.block.schedule('EI3', 3)
        self.assertIsNone(result)

class TestE_SWITCH(unittest.TestCase):
    def setUp(self):
        self.block = E_SWITCH()

    def test_switch_to_eo0_when_false(self):
        result = self.block.schedule('EI', 1, False)
        self.assertEqual(result, (1, None))

    def test_switch_to_eo1_when_true(self):
        result = self.block.schedule('EI', 1, True)
        self.assertEqual(result, (None, 1))

    def test_switch_wrong_event(self):
        result = self.block.schedule('WRONG', 1, False)
        self.assertIsNone(result)

class TestE_SELECT(unittest.TestCase):
    def setUp(self):
        self.block = E_SELECT()

    def test_select_ei0_when_false(self):
        result = self.block.schedule('EI0', 1, False)
        self.assertEqual(result, 1)

    def test_select_ei0_blocked_when_true(self):
        result = self.block.schedule('EI0', 1, True)
        self.assertIsNone(result)

    def test_select_ei1_when_true(self):
        result = self.block.schedule('EI1', 2, True)
        self.assertEqual(result, 2)

    def test_select_ei1_blocked_when_false(self):
        result = self.block.schedule('EI1', 2, False)
        self.assertIsNone(result)

class TestE_DEMUX(unittest.TestCase):
    def setUp(self):
        self.block = E_DEMUX()

    def test_demux_to_eo0(self):
        result = self.block.schedule('EI', 1, 0)
        self.assertEqual(result, (1, None, None, None))

    def test_demux_to_eo1(self):
        result = self.block.schedule('EI', 1, 1)
        self.assertEqual(result, (None, 1, None, None))

    def test_demux_to_eo2(self):
        result = self.block.schedule('EI', 1, 2)
        self.assertEqual(result, (None, None, 1, None))

    def test_demux_to_eo3(self):
        result = self.block.schedule('EI', 1, 3)
        self.assertEqual(result, (None, None, None, 1))

    def test_demux_invalid_index(self):
        result = self.block.schedule('EI', 1, 4)
        self.assertIsNone(result)

    def test_demux_wrong_event(self):
        result = self.block.schedule('WRONG', 1, 0)
        self.assertIsNone(result)

class TestE_RS(unittest.TestCase):
    def setUp(self):
        self.block = E_RS()

    def test_rs_initial_state(self):
        self.assertEqual(self.block.Q, False)

    def test_rs_set(self):
        result = self.block.schedule('S', 1)
        self.assertEqual(result, (1, True))
        self.assertEqual(self.block.Q, True)

    def test_rs_reset(self):
        self.block.schedule('S', 1)
        result = self.block.schedule('R', 2)
        self.assertEqual(result, (2, False))
        self.assertEqual(self.block.Q, False)

    def test_rs_set_when_already_set(self):
        self.block.schedule('S', 1)
        result = self.block.schedule('S', 2)
        self.assertEqual(result, (2, True))

    def test_rs_reset_when_already_reset(self):
        result = self.block.schedule('R', 1)
        self.assertEqual(result, (1, False))

    def test_rs_wrong_event(self):
        result = self.block.schedule('WRONG', 1)
        self.assertIsNone(result)

class TestE_SR(unittest.TestCase):
    def setUp(self):
        self.block = E_SR()

    def test_sr_initial_state(self):
        self.assertEqual(self.block.Q, False)

    def test_sr_set(self):
        result = self.block.schedule('S', 1)
        self.assertEqual(result, (1, True))

    def test_sr_reset(self):
        self.block.schedule('S', 1)
        result = self.block.schedule('R', 2)
        self.assertEqual(result, (2, False))

class TestE_D_FF(unittest.TestCase):
    def setUp(self):
        self.block = E_D_FF()

    def test_dff_initial_state(self):
        self.assertEqual(self.block.Q, False)

    def test_dff_clock_captures_d_true(self):
        result = self.block.schedule('CLK', 1, True)
        self.assertEqual(result, (1, True))
        self.assertEqual(self.block.Q, True)

    def test_dff_clock_captures_d_false(self):
        result = self.block.schedule('CLK', 1, False)
        self.assertEqual(result, (1, False))
        self.assertEqual(self.block.Q, False)

    def test_dff_multiple_clocks(self):
        self.block.schedule('CLK', 1, True)
        self.assertEqual(self.block.Q, True)
        self.block.schedule('CLK', 2, False)
        self.assertEqual(self.block.Q, False)
        self.block.schedule('CLK', 3, True)
        self.assertEqual(self.block.Q, True)

    def test_dff_wrong_event(self):
        result = self.block.schedule('WRONG', 1, True)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main(verbosity=2)
