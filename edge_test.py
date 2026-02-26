"""Additional edge case tests"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from openfb.core.configuration import Configuration

print("=== Additional BOOL Edge Cases ===")
print()

# Test with various string representations
test_cases = [
    ('YES', 'BOOL'),
    ('NO', 'BOOL'),
    ('ON', 'BOOL'),
    ('OFF', 'BOOL'),
    ('T', 'BOOL'),
    ('F', 'BOOL'),
    ('true', 'BOOL'),  # lowercase
    ('false', 'BOOL'),
    ('True', 'BOOL'),  # mixed case
    ('False', 'BOOL'),
]

for value, vtype in test_cases:
    result = Configuration.convert_type(value, vtype)
    status = "✅" if isinstance(result, bool) else "❌"
    print(f"{status} convert_type({value!r:10}, 'BOOL') = {result!r:5} (type: {type(result).__name__})")

print()
print("=== TIME/DATE Empty Cases ===")
print()

time_tests = [
    ('T#', 'TIME'),
    ('', 'TIME'),
    ('D#', 'DATE'),
    ('', 'DATE'),
    ('TOD#', 'TIME_OF_DAY'),
    ('', 'TOD'),
]

for value, vtype in time_tests:
    result = Configuration.convert_type(value, vtype)
    is_ok = result != '' and result != value
    status = "✅" if is_ok else "❌"
    print(f"{status} convert_type({value!r:10}, {vtype!r:15}) = {result!r}")

print()
print("=== BOOL with Prefix ===")
print()

prefix_tests = [
    ('BOOL#TRUE', 'BOOL'),
    ('BOOL#FALSE', 'BOOL'),
    ('BOOL#1', 'BOOL'),
    ('BOOL#0', 'BOOL'),
    ('BOOL#YES', 'BOOL'),
    ('BOOL#NO', 'BOOL'),
]

for value, vtype in prefix_tests:
    result = Configuration.convert_type(value, vtype)
    status = "✅" if isinstance(result, bool) else "❌"
    print(f"{status} convert_type({value!r:15}, 'BOOL') = {result!r:5}")

print()
print("=== Generic ANY Tests ===")
print()

any_tests = [
    (True, 'ANY'),
    (False, 'ANY'),
    (0, 'ANY'),
    (1, 'ANY'),
]

for value, vtype in any_tests:
    result = Configuration.convert_type(value, vtype)
    if isinstance(result, tuple):
        val, inferred = result
        val_type_ok = (inferred != 'BOOL') or isinstance(val, bool)
        status = "✅" if val_type_ok else "❌"
        print(f"{status} convert_type({value!r:5}, 'ANY') = ({val!r:5}, {inferred!r:6}) - val type: {type(val).__name__}")
    else:
        print(f"⚠️  convert_type({value!r:5}, 'ANY') = {result!r} (not a tuple)")

print()
print("=== Test Complete ===")
