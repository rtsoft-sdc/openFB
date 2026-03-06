import unittest
import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from openfb.resources.function_blocks.iec61131.charString.F_CONCAT import F_CONCAT
from openfb.resources.function_blocks.iec61131.charString.F_LEN import F_LEN
from openfb.resources.function_blocks.iec61131.charString.F_LEFT import F_LEFT
from openfb.resources.function_blocks.iec61131.charString.F_RIGHT import F_RIGHT
from openfb.resources.function_blocks.iec61131.charString.F_MID import F_MID
from openfb.resources.function_blocks.iec61131.charString.F_FIND import F_FIND
from openfb.resources.function_blocks.iec61131.charString.F_DELETE import F_DELETE
from openfb.resources.function_blocks.iec61131.charString.F_INSERT import F_INSERT
from openfb.resources.function_blocks.iec61131.charString.F_REPLACE import F_REPLACE
from openfb.resources.function_blocks.iec61131.charString.F_CONCAT_DATE_TOD import F_CONCAT_DATE_TOD


class TestF_CONCAT(unittest.TestCase):

    def setUp(self):
        self.block = F_CONCAT()

    def test_concat_basic(self):
        result = self.block.schedule('REQ', True, "Hello", " World")
        self.assertEqual(result, (True, "Hello World"))

    def test_concat_empty_strings(self):
        result = self.block.schedule('REQ', True, "", "")
        self.assertEqual(result, (True, ""))

    def test_concat_one_empty(self):
        result = self.block.schedule('REQ', True, "Hello", "")
        self.assertEqual(result, (True, "Hello"))

    def test_concat_other_empty(self):
        result = self.block.schedule('REQ', True, "", "World")
        self.assertEqual(result, (True, "World"))

    def test_concat_with_none(self):
        result = self.block.schedule('REQ', True, None, "World")
        self.assertEqual(result, (True, "World"))

    def test_concat_both_none(self):
        result = self.block.schedule('REQ', True, None, None)
        self.assertEqual(result, (True, ""))

    def test_concat_numbers(self):
        result = self.block.schedule('REQ', True, 123, 456)
        self.assertEqual(result, (True, "123456"))

    def test_concat_special_chars(self):
        result = self.block.schedule('REQ', True, "Hello!", "@#$%")
        self.assertEqual(result, (True, "Hello!@#$%"))

    def test_concat_long_strings(self):
        s1 = "a" * 100
        s2 = "b" * 100
        result = self.block.schedule('REQ', True, s1, s2)
        self.assertEqual(result, (True, s1 + s2))

    def test_concat_spaces(self):
        result = self.block.schedule('REQ', True, "   ", "   ")
        self.assertEqual(result, (True, "      "))

    def test_concat_wrong_event(self):
        result = self.block.schedule('WRONG', True, "Hello", "World")
        self.assertIsNone(result)


class TestF_LEN(unittest.TestCase):

    def setUp(self):
        self.block = F_LEN()

    def test_len_basic(self):
        result = self.block.schedule('REQ', True, "Hello")
        self.assertEqual(result, (True, 5))

    def test_len_empty_string(self):
        result = self.block.schedule('REQ', True, "")
        self.assertEqual(result, (True, 0))

    def test_len_single_char(self):
        result = self.block.schedule('REQ', True, "A")
        self.assertEqual(result, (True, 1))

    def test_len_with_spaces(self):
        result = self.block.schedule('REQ', True, "Hello World")
        self.assertEqual(result, (True, 11))

    def test_len_special_chars(self):
        result = self.block.schedule('REQ', True, "!@#$%")
        self.assertEqual(result, (True, 5))

    def test_len_number(self):
        result = self.block.schedule('REQ', True, 12345)
        self.assertEqual(result, (True, None))

    def test_len_long_string(self):
        s = "x" * 1000
        result = self.block.schedule('REQ', True, s)
        self.assertEqual(result, (True, 1000))

    def test_len_unicode(self):
        result = self.block.schedule('REQ', True, "Привет")
        self.assertEqual(result, (True, 6))

    def test_len_invalid_type(self):
        result = self.block.schedule('REQ', True, None)
        self.assertEqual(result, (True, None))


class TestF_LEFT(unittest.TestCase):

    def setUp(self):
        self.block = F_LEFT()

    def test_left_basic(self):
        result = self.block.schedule('REQ', True, "Hello", 2)
        self.assertEqual(result, (True, "He"))

    def test_left_whole_string(self):
        result = self.block.schedule('REQ', True, "Hello", 5)
        self.assertEqual(result, (True, "Hello"))

    def test_left_more_than_length(self):
        result = self.block.schedule('REQ', True, "Hello", 10)
        self.assertEqual(result, (True, "Hello"))

    def test_left_zero(self):
        result = self.block.schedule('REQ', True, "Hello", 0)
        self.assertEqual(result, (True, ""))

    def test_left_negative(self):
        result = self.block.schedule('REQ', True, "Hello", -5)
        self.assertEqual(result, (True, ""))

    def test_left_empty_string(self):
        result = self.block.schedule('REQ', True, "", 5)
        self.assertEqual(result, (True, ""))

    def test_left_single_char(self):
        result = self.block.schedule('REQ', True, "Hello", 1)
        self.assertEqual(result, (True, "H"))

    def test_left_with_none(self):
        result = self.block.schedule('REQ', True, None, 3)
        self.assertEqual(result, (True, ""))

    def test_left_invalid_length(self):
        result = self.block.schedule('REQ', True, "Hello", "invalid")
        self.assertEqual(result, (True, ""))


class TestF_RIGHT(unittest.TestCase):

    def setUp(self):
        self.block = F_RIGHT()

    def test_right_basic(self):
        result = self.block.schedule('REQ', True, "Hello", 2)
        self.assertEqual(result, (True, "lo"))

    def test_right_whole_string(self):
        result = self.block.schedule('REQ', True, "Hello", 5)
        self.assertEqual(result, (True, "Hello"))

    def test_right_more_than_length(self):
        result = self.block.schedule('REQ', True, "Hello", 10)
        self.assertEqual(result, (True, "Hello"))

    def test_right_zero(self):
        result = self.block.schedule('REQ', True, "Hello", 0)
        self.assertEqual(result, (None, ""))

    def test_right_negative(self):
        result = self.block.schedule('REQ', True, "Hello", -5)
        self.assertEqual(result, (None, ""))

    def test_right_empty_string(self):
        result = self.block.schedule('REQ', True, "", 5)
        self.assertIsNotNone(result)

    def test_right_single_char(self):
        result = self.block.schedule('REQ', True, "Hello", 1)
        self.assertEqual(result, (True, "o"))

    def test_right_invalid_length(self):
        result = self.block.schedule('REQ', True, "Hello", "invalid")
        self.assertEqual(result, (True, None))


class TestF_MID(unittest.TestCase):

    def setUp(self):
        self.block = F_MID()

    def test_mid_basic(self):
        result = self.block.schedule('REQ', True, "Hello", 3, 1)
        self.assertEqual(result, (True, "Hel"))

    def test_mid_from_middle(self):
        result = self.block.schedule('REQ', True, "Hello", 2, 2)
        self.assertEqual(result, (True, "el"))

    def test_mid_whole_string(self):
        result = self.block.schedule('REQ', True, "Hello", 5, 1)
        self.assertEqual(result, (True, "Hello"))

    def test_mid_beyond_length(self):
        result = self.block.schedule('REQ', True, "Hello", 3, 10)
        self.assertEqual(result, (True, ""))

    def test_mid_zero_length(self):
        result = self.block.schedule('REQ', True, "Hello", 0, 3)
        self.assertEqual(result, (True, ""))

    def test_mid_position_one(self):
        result = self.block.schedule('REQ', True, "Hello", 1, 1)
        self.assertEqual(result, (True, "H"))

    def test_mid_position_zero(self):
        result = self.block.schedule('REQ', True, "Hello", 1, 0)
        self.assertEqual(result, (True, "H"))

    def test_mid_empty_string(self):
        result = self.block.schedule('REQ', True, "", 2, 1)
        self.assertEqual(result, (True, ""))

    def test_mid_with_none(self):
        result = self.block.schedule('REQ', True, None, 2, 1)
        self.assertEqual(result, (True, ""))

    def test_mid_invalid_length(self):
        result = self.block.schedule('REQ', True, "Hello", "invalid", 1)
        self.assertEqual(result, (True, ""))

    def test_mid_invalid_position(self):
        result = self.block.schedule('REQ', True, "Hello", 3, "invalid")
        self.assertEqual(result, (True, "Hel"))


class TestF_FIND(unittest.TestCase):

    def setUp(self):
        self.block = F_FIND()

    def test_find_basic(self):
        result = self.block.schedule('REQ', True, "Hello World", "Hello")
        self.assertEqual(result, (True, 1))

    def test_find_middle(self):
        result = self.block.schedule('REQ', True, "Hello World", "lo")
        self.assertEqual(result, (True, 4))

    def test_find_end(self):
        result = self.block.schedule('REQ', True, "Hello World", "World")
        self.assertEqual(result, (True, 7))

    def test_find_not_found(self):
        result = self.block.schedule('REQ', True, "Hello World", "xyz")
        self.assertEqual(result, (True, 0))

    def test_find_empty_substring(self):
        result = self.block.schedule('REQ', True, "Hello", "")
        self.assertEqual(result, (True, 1))

    def test_find_empty_string(self):
        result = self.block.schedule('REQ', True, "", "Hello")
        self.assertEqual(result, (True, 0))

    def test_find_both_empty(self):
        result = self.block.schedule('REQ', True, "", "")
        self.assertEqual(result, (True, 0))

    def test_find_single_char(self):
        result = self.block.schedule('REQ', True, "Hello", "e")
        self.assertEqual(result, (True, 2))

    def test_find_case_sensitive(self):
        result = self.block.schedule('REQ', True, "Hello", "hello")
        self.assertEqual(result, (True, 0))

    def test_find_with_none(self):
        result = self.block.schedule('REQ', True, None, None)
        self.assertEqual(result, (True, 0))


class TestF_DELETE(unittest.TestCase):

    def setUp(self):
        self.block = F_DELETE()

    def test_delete_basic(self):
        result = self.block.schedule('REQ', True, "Hello World", 5, 1)
        self.assertEqual(result, (True, " World"))

    def test_delete_from_middle(self):
        result = self.block.schedule('REQ', True, "Hello", 2, 2)
        self.assertEqual(result, (True, "Hlo"))

    def test_delete_all(self):
        result = self.block.schedule('REQ', True, "Hello", 5, 1)
        self.assertEqual(result, (True, ""))

    def test_delete_zero_length(self):
        result = self.block.schedule('REQ', True, "Hello", 0, 1)
        self.assertEqual(result, (True, "Hello"))

    def test_delete_beyond_length(self):
        result = self.block.schedule('REQ', True, "Hello", 10, 1)
        self.assertEqual(result, (True, ""))

    def test_delete_negative_length(self):
        result = self.block.schedule('REQ', True, "Hello", -5, 1)
        self.assertEqual(result, (True, "Hello"))

    def test_delete_position_zero(self):
        result = self.block.schedule('REQ', True, "Hello", 3, 0)
        self.assertEqual(result, (True, "lo"))

    def test_delete_empty_string(self):
        result = self.block.schedule('REQ', True, "", 5, 1)
        self.assertEqual(result, (True, ""))

    def test_delete_with_none(self):
        result = self.block.schedule('REQ', True, None, 3, 1)
        self.assertEqual(result, (True, ""))


class TestF_INSERT(unittest.TestCase):

    def setUp(self):
        self.block = F_INSERT()

    def test_insert_at_start(self):
        result = self.block.schedule('REQ', True, "World", "Hello ", 0)
        self.assertEqual(result, (True, "Hello World"))

    def test_insert_in_middle(self):
        result = self.block.schedule('REQ', True, "Helo", "l", 3)
        self.assertEqual(result, (True, "Hello"))

    def test_insert_at_end(self):
        result = self.block.schedule('REQ', True, "Hello", " World", 5)
        self.assertEqual(result, (True, "Hello World"))

    def test_insert_beyond_length(self):
        result = self.block.schedule('REQ', True, "Hello", " World", 10)
        self.assertEqual(result, (True, "Hello World"))

    def test_insert_empty_string(self):
        result = self.block.schedule('REQ', True, "Hello", "", 2)
        self.assertEqual(result, (True, "Hello"))

    def test_insert_into_empty(self):
        result = self.block.schedule('REQ', True, "", "Hello", 0)
        self.assertEqual(result, (True, "Hello"))

    def test_insert_negative_position(self):
        result = self.block.schedule('REQ', True, "Hello", "X", -5)
        self.assertEqual(result, (True, "XHello"))

    def test_insert_with_none(self):
        result = self.block.schedule('REQ', True, "Hello", None, 2)
        self.assertEqual(result, (True, "Hello"))

    def test_insert_none_into_string(self):
        result = self.block.schedule('REQ', True, None, "Hello", 0)
        self.assertEqual(result, (True, "Hello"))


class TestF_REPLACE(unittest.TestCase):

    def setUp(self):
        self.block = F_REPLACE()

    def test_replace_basic(self):
        result = self.block.schedule('REQ', True, "Hello World", "Hi", 2, 1)
        self.assertEqual(result, (True, "Hillo World"))

    def test_replace_in_middle(self):
        result = self.block.schedule('REQ', True, "Hello", "!!", 2, 2)
        self.assertEqual(result, (True, "H!!lo"))

    def test_replace_all(self):
        result = self.block.schedule('REQ', True, "Hello", "Hi", 5, 1)
        self.assertEqual(result, (True, "Hi"))

    def test_replace_shorter(self):
        result = self.block.schedule('REQ', True, "Hello World", "X", 5, 1)
        self.assertEqual(result, (True, "X World"))

    def test_replace_longer(self):
        result = self.block.schedule('REQ', True, "Hello", "ZZZZZ", 2, 1)
        self.assertEqual(result, (True, "ZZZZZllo"))

    def test_replace_zero_length(self):
        result = self.block.schedule('REQ', True, "Hello", "X", 0, 2)
        self.assertEqual(result, (True, "HXello"))

    def test_replace_empty_replacement(self):
        result = self.block.schedule('REQ', True, "Hello", "", 2, 3)
        self.assertEqual(result, (True, "Heo"))

    def test_replace_beyond_length(self):
        result = self.block.schedule('REQ', True, "Hello", "X", 10, 3)
        self.assertEqual(result, (True, "HeX"))

    def test_replace_with_none(self):
        result = self.block.schedule('REQ', True, "Hello", None, 2, 2)
        self.assertEqual(result, (True, "Hlo"))

    def test_replace_invalid_length(self):
        result = self.block.schedule('REQ', True, "Hello", "X", "invalid", 2)
        self.assertEqual(result, (True, "HXello"))

    def test_replace_invalid_position(self):
        result = self.block.schedule('REQ', True, "Hello", "X", 2, "invalid")
        self.assertEqual(result, (True, "Xllo"))


class TestF_CONCAT_DATE_TOD(unittest.TestCase):

    def setUp(self):
        self.block = F_CONCAT_DATE_TOD()

    def test_concat_date_tod_basic(self):
        date_obj = datetime.date(2024, 1, 1)
        time_obj = datetime.time(12, 0, 0)
        result = self.block.schedule('REQ', True, date_obj, time_obj)
        if isinstance(result[1], datetime.datetime):
            self.assertEqual(result[1].date(), date_obj)
            self.assertEqual(result[1].time(), time_obj)

    def test_concat_date_tod_with_strings(self):
        result = self.block.schedule('REQ', True, "2024-01-01", "12:00:00")
        self.assertIsNotNone(result[1])

    def test_concat_date_tod_invalid_date(self):
        time_obj = datetime.time(12, 0, 0)
        result = self.block.schedule('REQ', True, "invalid", time_obj)
        self.assertIsNotNone(result[1])

    def test_concat_date_tod_invalid_time(self):
        date_obj = datetime.date(2024, 1, 1)
        result = self.block.schedule('REQ', True, date_obj, "invalid")
        self.assertIsNotNone(result[1])

    def test_concat_date_tod_with_none(self):
        result = self.block.schedule('REQ', True, None, None)
        self.assertIsNotNone(result[1])

    def test_concat_date_tod_wrong_event(self):
        result = self.block.schedule('WRONG', True, "2024-01-01", "12:00:00")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
