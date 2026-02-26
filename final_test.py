"""Final comprehensive test for BOOL and DATE_AND_TIME fixes"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from openfb.core.configuration import Configuration

print("=" * 70)
print("FINAL COMPREHENSIVE TEST: BOOL and DATE_AND_TIME Fixes")
print("=" * 70)
print()

total_tests = 0
passed_tests = 0

def test(description, condition):
    global total_tests, passed_tests
    total_tests += 1
    if condition:
        passed_tests += 1
        print(f"✅ PASS: {description}")
        return True
    else:
        print(f"❌ FAIL: {description}")
        return False

print("--- BOOL Type Tests ---")
print()

# Test 1: BOOL returns actual bool type, not 0.0
result = Configuration.convert_type(0.0, 'BOOL')
test("convert_type(0.0, 'BOOL') returns bool type", isinstance(result, bool))
test("convert_type(0.0, 'BOOL') == False", result is False)

result = Configuration.convert_type(1.0, 'BOOL')
test("convert_type(1.0, 'BOOL') returns bool type", isinstance(result, bool))
test("convert_type(1.0, 'BOOL') == True", result is True)

# Test 2: String '0.0' correctly parsed
result = Configuration.convert_type('0.0', 'BOOL')
test("convert_type('0.0', 'BOOL') == False", result is False)
test("convert_type('0.0', 'BOOL') is bool", isinstance(result, bool))

# Test 3: String '1.0' correctly parsed
result = Configuration.convert_type('1.0', 'BOOL')
test("convert_type('1.0', 'BOOL') == True", result is True)

# Test 4: Various string representations
test("convert_type('TRUE', 'BOOL') == True", 
     Configuration.convert_type('TRUE', 'BOOL') is True)
test("convert_type('FALSE', 'BOOL') == False", 
     Configuration.convert_type('FALSE', 'BOOL') is False)
test("convert_type('YES', 'BOOL') == True", 
     Configuration.convert_type('YES', 'BOOL') is True)
test("convert_type('NO', 'BOOL') == False", 
     Configuration.convert_type('NO', 'BOOL') is False)

# Test 5: Integer values
test("convert_type(0, 'BOOL') == False", 
     Configuration.convert_type(0, 'BOOL') is False)
test("convert_type(1, 'BOOL') == True", 
     Configuration.convert_type(1, 'BOOL') is True)

# Test 6: With prefix
result = Configuration.convert_type('BOOL#0', 'BOOL')
test("convert_type('BOOL#0', 'BOOL') == False", result is False)
test("convert_type('BOOL#0', 'BOOL') is bool", isinstance(result, bool))

print()
print("--- DATE_AND_TIME Type Tests ---")
print()

# Test 7: DT# with data
result = Configuration.convert_type('DT#2024-01-15-10:30:45', 'DATE_AND_TIME')
test("convert_type('DT#2024-01-15-10:30:45', 'DATE_AND_TIME') contains data",
     '2024-01-15-10:30:45' in result)

# Test 8: DT# empty - should NOT return empty or just 'DT#'
result = Configuration.convert_type('DT#', 'DATE_AND_TIME')
test("convert_type('DT#', 'DATE_AND_TIME') is not empty", result != '')
test("convert_type('DT#', 'DATE_AND_TIME') is not just 'DT#'", result != 'DT#')
test("convert_type('DT#', 'DATE_AND_TIME') contains 'DT#'", 'DT#' in result)

# Test 9: Empty string - should return default
result = Configuration.convert_type('', 'DATE_AND_TIME')
test("convert_type('', 'DATE_AND_TIME') is not empty", result != '')
test("convert_type('', 'DATE_AND_TIME') has DT# prefix", result.startswith('DT#'))

# Test 10: Other time/date types with empty values
result = Configuration.convert_type('T#', 'TIME')
test("convert_type('T#', 'TIME') is not empty", result != '' and result != 'T#')

result = Configuration.convert_type('D#', 'DATE')
test("convert_type('D#', 'DATE') is not empty", result != '' and result != 'D#')

result = Configuration.convert_type('TOD#', 'TIME_OF_DAY')
test("convert_type('TOD#', 'TIME_OF_DAY') is not empty", result != '' and result != 'TOD#')

print()
print("--- Generic Type Tests (ANY_BIT) ---")
print()

# Test 11: ANY_BIT with 0/1 should infer BOOL with bool values
result = Configuration.convert_type(0, 'ANY_BIT')
test("convert_type(0, 'ANY_BIT') returns tuple", isinstance(result, tuple))
if isinstance(result, tuple):
    val, vtype = result
    test("convert_type(0, 'ANY_BIT') infers BOOL", vtype == 'BOOL')
    test("convert_type(0, 'ANY_BIT') value is bool type", isinstance(val, bool))
    test("convert_type(0, 'ANY_BIT') value == False", val is False)

result = Configuration.convert_type(0.0, 'ANY_BIT')
if isinstance(result, tuple):
    val, vtype = result
    test("convert_type(0.0, 'ANY_BIT') infers BOOL", vtype == 'BOOL')
    test("convert_type(0.0, 'ANY_BIT') value is bool type", isinstance(val, bool))

print()
print("=" * 70)
print(f"RESULTS: {passed_tests}/{total_tests} tests passed")
print("=" * 70)

if passed_tests == total_tests:
    print()
    print("✅✅✅ ALL TESTS PASSED! ✅✅✅")
    print()
    print("Summary of fixes:")
    print("  1. BOOL type now correctly returns bool (True/False) instead of 0.0/1.0")
    print("  2. String numbers like '0.0' are parsed correctly as False")
    print("  3. DATE_AND_TIME with empty value after 'DT#' returns default")
    print("  4. All time/date types handle empty values gracefully")
    print("  5. Generic types (ANY_BIT) correctly infer BOOL with bool values")
    sys.exit(0)
else:
    print()
    print(f"❌ {total_tests - passed_tests} test(s) failed")
    sys.exit(1)
