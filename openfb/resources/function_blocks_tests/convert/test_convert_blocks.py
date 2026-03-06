import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from openfb.resources.function_blocks.convert.ARRAY2ARRAY_2_LREAL import ARRAY2ARRAY_2_LREAL
from openfb.resources.function_blocks.convert.ARRAY2VALUES_2_LREAL import ARRAY2VALUES_2_LREAL
from openfb.resources.function_blocks.convert.GET_AT_INDEX import GET_AT_INDEX
from openfb.resources.function_blocks.convert.GET_STRUCT_VALUE import GET_STRUCT_VALUE
from openfb.resources.function_blocks.convert.SET_AT_INDEX import SET_AT_INDEX
from openfb.resources.function_blocks.convert.SET_STRUCT_VALUE import SET_STRUCT_VALUE
from openfb.resources.function_blocks.convert.STRUCT_DEMUX import STRUCT_DEMUX
from openfb.resources.function_blocks.convert.STRUCT_MUX import STRUCT_MUX
from openfb.resources.function_blocks.convert.VALUES_TO_ARRAY import VALUES_TO_ARRAY


class DummyObj:
    def __init__(self):
        self.a = 10
        self.b = "x"


class NestedDummy:
    def __init__(self):
        self.cfg = DummyObj()


class TestARRAY2ARRAY_2_LREAL(unittest.TestCase):
    def setUp(self):
        self.block = ARRAY2ARRAY_2_LREAL()

    def test_convert_numbers(self):
        result = self.block.schedule('REQ', True, [1, 2.5])
        self.assertEqual(result, (True, [1.0, 2.5]))

    def test_convert_strings(self):
        result = self.block.schedule('REQ', True, ["3.14", "2"])
        self.assertEqual(result, (True, [3.14, 2.0]))

    def test_invalid_input(self):
        result = self.block.schedule('REQ', True, ["abc", 2])
        self.assertEqual(result, (True, None))

    def test_wrong_event(self):
        result = self.block.schedule('CNF', True, [1, 2])
        self.assertIsNone(result)


class TestARRAY2VALUES_2_LREAL(unittest.TestCase):
    def setUp(self):
        self.block = ARRAY2VALUES_2_LREAL()

    def test_convert_numbers(self):
        result = self.block.schedule('REQ', True, [1, 2.5])
        self.assertEqual(result, (True, 1.0, 2.5))

    def test_short_array(self):
        result = self.block.schedule('REQ', True, [1])
        self.assertEqual(result, (True, None))

    def test_invalid_input(self):
        result = self.block.schedule('REQ', True, [1, "x"])
        self.assertEqual(result, (True, None))


class TestVALUES_TO_ARRAY(unittest.TestCase):
    def setUp(self):
        self.block = VALUES_TO_ARRAY()

    def test_from_args(self):
        result = self.block.schedule('REQ', True, 1, 2, 3)
        self.assertEqual(result, (True, [1, 2, 3]))

    def test_from_list(self):
        result = self.block.schedule('REQ', True, [1, 2])
        self.assertEqual(result, (True, [1, 2]))

    def test_from_tuple(self):
        result = self.block.schedule('REQ', True, (1, 2))
        self.assertEqual(result, (True, [1, 2]))

    def test_from_dict(self):
        result = self.block.schedule('REQ', True, {'a': 1, 'b': 2})
        self.assertEqual(result, (True, [1, 2]))

    def test_from_kwargs(self):
        result = self.block.schedule('REQ', True, a=7, b=8)
        self.assertEqual(result, (True, [7, 8]))


class TestGET_AT_INDEX(unittest.TestCase):
    def setUp(self):
        self.block = GET_AT_INDEX()

    def test_valid_list_index(self):
        result = self.block.schedule('REQ', True, [10, 20, 30], 1)
        self.assertEqual(result, (True, True, 20))

    def test_valid_tuple_index(self):
        result = self.block.schedule('REQ', True, ("a", "b"), 0)
        self.assertEqual(result, (True, True, "a"))

    def test_out_of_range(self):
        result = self.block.schedule('REQ', True, [1, 2], 5)
        self.assertEqual(result, (True, False, None))

    def test_negative_index_not_allowed(self):
        result = self.block.schedule('REQ', True, [1, 2], -1)
        self.assertEqual(result, (True, False, None))

    def test_not_array(self):
        result = self.block.schedule('REQ', True, "not_array", 0)
        self.assertEqual(result, (True, False, None))


class TestSET_AT_INDEX(unittest.TestCase):
    def setUp(self):
        self.block = SET_AT_INDEX()

    def test_set_list_index(self):
        src = [1, 2, 3]
        result = self.block.schedule('REQ', True, src, 1, 99)
        self.assertEqual(result, (True, True, [1, 99, 3]))
        self.assertEqual(src, [1, 2, 3])

    def test_set_tuple_index(self):
        src = (1, 2, 3)
        result = self.block.schedule('REQ', True, src, 2, 77)
        self.assertEqual(result, (True, True, [1, 2, 77]))

    def test_out_of_range(self):
        result = self.block.schedule('REQ', True, [1, 2], 2, 9)
        self.assertEqual(result, (True, False, None))

    def test_invalid_array(self):
        result = self.block.schedule('REQ', True, {'a': 1}, 0, 9)
        self.assertEqual(result, (True, False, None))


class TestSTRUCT_MUX(unittest.TestCase):
    def setUp(self):
        self.block = STRUCT_MUX()

    def test_from_kwargs(self):
        result = self.block.schedule('REQ', True, a=1, b=2)
        self.assertEqual(result, (True, {'a': 1, 'b': 2}))

    def test_from_dict(self):
        result = self.block.schedule('REQ', True, {'x': 5})
        self.assertEqual(result, (True, {'x': 5}))

    def test_from_object(self):
        obj = DummyObj()
        result = self.block.schedule('REQ', True, obj)
        self.assertEqual(result, (True, {'a': 10, 'b': 'x'}))

    def test_from_args(self):
        result = self.block.schedule('REQ', True, 10, 20)
        self.assertEqual(result, (True, {'field1': 10, 'field2': 20}))


class TestSTRUCT_DEMUX(unittest.TestCase):
    def setUp(self):
        self.block = STRUCT_DEMUX()

    def test_from_dict(self):
        result = self.block.schedule('REQ', True, {'a': 1, 'b': 2})
        self.assertEqual(result, (True, 1, 2))

    def test_from_object(self):
        obj = DummyObj()
        result = self.block.schedule('REQ', True, obj)
        self.assertEqual(result, (True, 10, 'x'))

    def test_from_list(self):
        result = self.block.schedule('REQ', True, [7, 8])
        self.assertEqual(result, (True, 7, 8))

    def test_invalid_input(self):
        result = self.block.schedule('REQ', True, 123)
        self.assertEqual(result, True)


class TestGET_STRUCT_VALUE(unittest.TestCase):
    def setUp(self):
        self.block = GET_STRUCT_VALUE()

    def test_get_from_nested_dict(self):
        src = {'cfg': {'name': 'openfb'}}
        result = self.block.schedule('REQ', True, 'cfg.name', src)
        self.assertEqual(result, (True, True, 'openfb'))

    def test_get_from_object(self):
        obj = NestedDummy()
        result = self.block.schedule('REQ', True, 'cfg.a', obj)
        self.assertEqual(result, (True, True, 10))

    def test_missing_path_returns_special_tuple(self):
        src = {'cfg': {}}
        result = self.block.schedule('REQ', True, 'cfg.name.value', src)
        self.assertEqual(result, (None, False, None))

    def test_wrong_event(self):
        result = self.block.schedule('CNF', True, 'cfg.a', {'cfg': {'a': 1}})
        self.assertIsNone(result)


class TestSET_STRUCT_VALUE(unittest.TestCase):
    def setUp(self):
        self.block = SET_STRUCT_VALUE()

    def test_set_in_dict(self):
        src = {'cfg': {'name': 'old'}}
        result = self.block.schedule('REQ', True, 'cfg.name', src, 'new')
        self.assertEqual(result, (True, True, {'cfg': {'name': 'new'}}))
        self.assertEqual(src, {'cfg': {'name': 'new'}})

    def test_create_missing_path_in_dict(self):
        src = {}
        result = self.block.schedule('REQ', True, 'cfg.name', src, 'openfb')
        self.assertEqual(result, (True, True, {'cfg': {'name': 'openfb'}}))

    def test_set_in_object(self):
        obj = NestedDummy()
        result = self.block.schedule('REQ', True, 'cfg.b', obj, 'new')
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2].cfg.b, 'new')

    def test_invalid_target(self):
        result = self.block.schedule('REQ', True, 'a.b', 123, 1)
        self.assertEqual(result, (True, False, 123))


if __name__ == '__main__':
    unittest.main(verbosity=2)
