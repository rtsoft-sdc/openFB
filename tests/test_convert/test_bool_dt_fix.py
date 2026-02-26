"""Test convert_type fixes for BOOL and DATE_AND_TIME"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from openfb.core.configuration import Configuration


class TestConvertTypeBool:
    """Test BOOL conversion fixes"""
    
    def test_bool_returns_bool_type(self):
        """BOOL type should return bool, not float/int"""
        assert Configuration.convert_type('TRUE', 'BOOL') is True
        assert Configuration.convert_type('FALSE', 'BOOL') is False
        assert Configuration.convert_type('1', 'BOOL') is True
        assert Configuration.convert_type('0', 'BOOL') is False
        assert Configuration.convert_type(1, 'BOOL') is True
        assert Configuration.convert_type(0, 'BOOL') is False
        assert Configuration.convert_type(1.0, 'BOOL') is True
        assert Configuration.convert_type(0.0, 'BOOL') is False
        
    def test_bool_with_prefix(self):
        """BOOL with type prefix"""
        assert Configuration.convert_type('BOOL#TRUE', 'BOOL') is True
        assert Configuration.convert_type('BOOL#FALSE', 'BOOL') is False
        assert Configuration.convert_type('BOOL#1', 'BOOL') is True
        assert Configuration.convert_type('BOOL#0', 'BOOL') is False
    
    def test_bool_actual_type(self):
        """Verify returned value is actually bool type, not 0.0"""
        result = Configuration.convert_type(0.0, 'BOOL')
        assert isinstance(result, bool), f"Expected bool, got {type(result).__name__}"
        assert result is False
        
        result = Configuration.convert_type(1.0, 'BOOL')
        assert isinstance(result, bool), f"Expected bool, got {type(result).__name__}"
        assert result is True


class TestConvertTypeDateAndTime:
    """Test DATE_AND_TIME conversion fixes"""
    
    def test_dt_with_data(self):
        """DATE_AND_TIME with actual data"""
        result = Configuration.convert_type('DT#2024-01-15-10:30:45', 'DATE_AND_TIME')
        assert result == '2024-01-15-10:30:45'
        
        result = Configuration.convert_type('DT#2024-01-15-10:30:45', 'DT')
        assert result == '2024-01-15-10:30:45'
    
    def test_dt_empty_after_prefix(self):
        """DATE_AND_TIME with empty value after prefix should return default"""
        result = Configuration.convert_type('DT#', 'DATE_AND_TIME')
        assert result != '', "Should not return empty string"
        assert result != 'DT#', "Should not return prefix only"
        assert 'DT#' in result or '1970-01-01' in result
        
    def test_dt_completely_empty(self):
        """DATE_AND_TIME with completely empty value"""
        result = Configuration.convert_type('', 'DATE_AND_TIME')
        assert result != '', "Should not return empty string"
        # Should return default datetime
        
    def test_dt_various_formats(self):
        """DATE_AND_TIME with various input formats"""
        # Without prefix
        result = Configuration.convert_type('2024-01-15-10:30:45', 'DATE_AND_TIME')
        assert '2024-01-15-10:30:45' in result
        
        # With DATE_AND_TIME# prefix
        result = Configuration.convert_type('DATE_AND_TIME#2024-01-15-10:30:45', 'DATE_AND_TIME')
        assert '2024-01-15-10:30:45' in result


class TestConvertTypeGenericBool:
    """Test BOOL inference for generic types like ANY_BIT"""
    
    def test_any_bit_bool_inference(self):
        """ANY_BIT should infer BOOL for 0/1 values and return bool type"""
        result = Configuration.convert_type(0, 'ANY_BIT')
        assert isinstance(result, tuple), "Generic types should return (value, type)"
        val, inferred_type = result
        assert inferred_type == 'BOOL'
        assert isinstance(val, bool), f"BOOL value should be bool, not {type(val).__name__}"
        assert val is False
        
        result = Configuration.convert_type(1, 'ANY_BIT')
        val, inferred_type = result
        assert inferred_type == 'BOOL'
        assert isinstance(val, bool), f"BOOL value should be bool, not {type(val).__name__}"
        assert val is True
        
    def test_any_bit_bool_from_float(self):
        """ANY_BIT with float 0.0/1.0 should infer BOOL"""
        result = Configuration.convert_type(0.0, 'ANY_BIT')
        val, inferred_type = result
        assert inferred_type == 'BOOL'
        assert isinstance(val, bool), f"BOOL value should be bool, not {type(val).__name__}"
        
        result = Configuration.convert_type(1.0, 'ANY_BIT')
        val, inferred_type = result
        assert inferred_type == 'BOOL'
        assert isinstance(val, bool), f"BOOL value should be bool, not {type(val).__name__}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
