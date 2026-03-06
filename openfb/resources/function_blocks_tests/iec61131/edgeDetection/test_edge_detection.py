import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.edgeDetection.FB_F_TRIG import FB_F_TRIG
from openfb.resources.function_blocks.iec61131.edgeDetection.FB_R_TRIG import FB_R_TRIG


class TestFB_F_TRIG(unittest.TestCase):
    
    def setUp(self):
        self.block = FB_F_TRIG()
    
    def test_f_trig_initial_state(self):
        result = self.block.schedule('REQ', True, True)
        self.assertEqual(result, (True, False))
    
    def test_f_trig_falling_edge(self):
        self.block.schedule('REQ', True, True)
        result = self.block.schedule('REQ', True, False)
        self.assertEqual(result, (True, True))
    
    def test_f_trig_no_falling_edge(self):
        self.block.schedule('REQ', True, True)
        self.block.schedule('REQ', True, False)
        result = self.block.schedule('REQ', True, False)
        self.assertEqual(result, (True, False))
    
    def test_f_trig_multiple_transitions(self):
        self.block.schedule('REQ', True, True)
        result1 = self.block.schedule('REQ', True, False)
        self.assertEqual(result1, (True, True))

        result2 = self.block.schedule('REQ', True, False)
        self.assertEqual(result2, (True, False))

        result3 = self.block.schedule('REQ', True, True)
        self.assertEqual(result3, (True, False))
        
        result4 = self.block.schedule('REQ', True, False)
        self.assertEqual(result4, (True, True))
    
    def test_f_trig_false_start(self):
        self.block.schedule('REQ', True, False)
        result = self.block.schedule('REQ', True, True)
        self.assertEqual(result, (True, False))
    
    def test_f_trig_boolean_input(self):
        self.block.schedule('REQ', True, 1)
        result = self.block.schedule('REQ', True, 0)
        self.assertEqual(result, (True, True))
    
    def test_f_trig_wrong_event(self):
        result = self.block.schedule('WRONG', True, True)
        self.assertIsNone(result)


class TestFB_R_TRIG(unittest.TestCase):
    
    def setUp(self):
        self.block = FB_R_TRIG()
    
    def test_r_trig_initial_state(self):
        result = self.block.schedule('REQ', True, False)
        self.assertEqual(result, (True, False))
    
    def test_r_trig_rising_edge(self):
        self.block.schedule('REQ', True, False)
        result = self.block.schedule('REQ', True, True)
        self.assertEqual(result, (True, True))
    
    def test_r_trig_no_rising_edge(self):
        self.block.schedule('REQ', True, False)
        self.block.schedule('REQ', True, True)
        result = self.block.schedule('REQ', True, True)
        self.assertEqual(result, (True, False))
    
    def test_r_trig_multiple_transitions(self):
        self.block.schedule('REQ', True, False)
        result1 = self.block.schedule('REQ', True, True)
        self.assertEqual(result1, (True, True))
        
        result2 = self.block.schedule('REQ', True, True)
        self.assertEqual(result2, (True, False))
        
        result3 = self.block.schedule('REQ', True, False)
        self.assertEqual(result3, (True, False))
        
        result4 = self.block.schedule('REQ', True, True)
        self.assertEqual(result4, (True, True))
    
    def test_r_trig_true_start(self):
        
        self.block.schedule('REQ', True, True)
        result = self.block.schedule('REQ', True, False)
        self.assertEqual(result, (True, False))
    
    def test_r_trig_boolean_input(self):
        self.block.schedule('REQ', True, 0)
        result = self.block.schedule('REQ', True, 1)
        self.assertEqual(result, (True, True))
    
    def test_r_trig_wrong_event(self):
        result = self.block.schedule('WRONG', True, True)
        self.assertIsNone(result)


class TestEdgeDetectionComparison(unittest.TestCase):
    
    def test_complementary_behavior(self):
        f_trig = FB_F_TRIG()
        r_trig = FB_R_TRIG()

        f_trig.schedule('REQ', True, False)
        r_trig.schedule('REQ', True, False)
        
        r_result = r_trig.schedule('REQ', True, True)
        f_result = f_trig.schedule('REQ', True, True)
        
        self.assertEqual(r_result[1], True)
        self.assertEqual(f_result[1], False)
    
    def test_edge_detection_sequence(self):
        
        f_trig = FB_F_TRIG()
        r_trig = FB_R_TRIG()
        
        f_trig.schedule('REQ', True, False)
        r_trig.schedule('REQ', True, False)
        
        f1 = f_trig.schedule('REQ', True, True)[1]
        r1 = r_trig.schedule('REQ', True, True)[1]
        self.assertEqual(f1, False)  
        self.assertEqual(r1, True)
        
        f2 = f_trig.schedule('REQ', True, False)[1]
        r2 = r_trig.schedule('REQ', True, False)[1]
        self.assertEqual(f2, True)
        self.assertEqual(r2, False)

if __name__ == '__main__':
    unittest.main(verbosity=2)
