"""Direct test without pytest"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from openfb.core.configuration import Configuration

print("=== BOOL Type Tests ===")
print()

# Test 1: BOOL with 0.0
result = Configuration.convert_type(0.0, 'BOOL')
print(f"convert_type(0.0, 'BOOL') = {result!r}")
print(f"  Type: {type(result).__name__}")
print(f"  Is bool: {isinstance(result, bool)}")
print(f"  Value: {result}")
if not isinstance(result, bool):
    print("  ❌ FAIL: Expected bool type, got", type(result).__name__)
else:
    print("  ✅ PASS: Returns bool type")
print()

# Test 2: BOOL with 1.0  
result = Configuration.convert_type(1.0, 'BOOL')
print(f"convert_type(1.0, 'BOOL') = {result!r}")
print(f"  Type: {type(result).__name__}")
print(f"  Is bool: {isinstance(result, bool)}")
if not isinstance(result, bool):
    print("  ❌ FAIL: Expected bool type")
else:
    print("  ✅ PASS: Returns bool type")
print()

# Test 3: BOOL with string '0'
result = Configuration.convert_type('0', 'BOOL')
print(f"convert_type('0', 'BOOL') = {result!r}")
print(f"  Type: {type(result).__name__}")
print(f"  Value: {result}")
if not isinstance(result, bool):
    print("  ❌ FAIL: Expected bool type")
else:
    print("  ✅ PASS")
print()

# Test 4: BOOL with string 'FALSE'
result = Configuration.convert_type('FALSE', 'BOOL')
print(f"convert_type('FALSE', 'BOOL') = {result!r}")
print(f"  Value: {result}")
print(f"  ✅ PASS" if isinstance(result, bool) and result is False else "  ❌ FAIL")
print()

print("=== DATE_AND_TIME Type Tests ===")
print()

# Test 5: DT# with data
result = Configuration.convert_type('DT#2024-01-15-10:30:45', 'DATE_AND_TIME')
print(f"convert_type('DT#2024-01-15-10:30:45', 'DATE_AND_TIME') = {result!r}")
if '2024-01-15-10:30:45' in result:
    print("  ✅ PASS: Contains expected data")
else:
    print("  ❌ FAIL: Missing expected data")
print()

# Test 6: DT# empty
result = Configuration.convert_type('DT#', 'DATE_AND_TIME')
print(f"convert_type('DT#', 'DATE_AND_TIME') = {result!r}")
if result == '' or result == 'DT#':
    print("  ❌ FAIL: Returns empty or prefix-only")
else:
    print("  ✅ PASS: Returns default value")
print()

# Test 7: Empty string
result = Configuration.convert_type('', 'DATE_AND_TIME')
print(f"convert_type('', 'DATE_AND_TIME') = {result!r}")
if result == '':
    print("  ❌ FAIL: Returns empty string")
else:
    print("  ✅ PASS: Returns default value")
print()

print("=== Generic Type Tests (ANY_BIT) ===")
print()

# Test 8: ANY_BIT with 0
result = Configuration.convert_type(0, 'ANY_BIT')
print(f"convert_type(0, 'ANY_BIT') = {result!r}")
if isinstance(result, tuple):
    val, inferred_type = result
    print(f"  Value: {val!r}, Type: {inferred_type}")
    print(f"  Value type: {type(val).__name__}")
    if inferred_type == 'BOOL' and isinstance(val, bool):
        print("  ✅ PASS: Correctly inferred BOOL with bool value")
    elif inferred_type == 'BOOL':
        print(f"  ❌ FAIL: Type is BOOL but value is {type(val).__name__}, not bool")
    else:
        print(f"  Note: Inferred {inferred_type} instead of BOOL")
else:
    print(f"  ❌ FAIL: Expected tuple (value, type), got {type(result).__name__}")
print()

# Test 9: ANY_BIT with 0.0
result = Configuration.convert_type(0.0, 'ANY_BIT')
print(f"convert_type(0.0, 'ANY_BIT') = {result!r}")
if isinstance(result, tuple):
    val, inferred_type = result
    print(f"  Value: {val!r}, Type: {inferred_type}")
    print(f"  Value type: {type(val).__name__}")
    if inferred_type == 'BOOL' and isinstance(val, bool):
        print("  ✅ PASS: Correctly converted float to BOOL")
    elif inferred_type == 'BOOL':
        print(f"  ❌ FAIL: Type is BOOL but value is {type(val).__name__}")
    else:
        print(f"  Note: Inferred {inferred_type}")
print()

print("=== Summary ===")
print("Check output above for ❌ FAIL markers")
