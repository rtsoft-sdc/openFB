import logging
import re
'''
def parse_iec_number(value):

    if not isinstance(value, str):
        return value
    
    s = value.strip()
    
    type_match = re.match(r'^([A-Z_]+)#(.+)$', s)
    if type_match:
        num_type = type_match.group(1).upper()
        num_str = type_match.group(2).strip()
    else:
        num_type = None
        num_str = s
    

    base_match = re.match(r'^(\d+)#(.+)$', num_str)
    if base_match:
        base = int(base_match.group(1))
        digits = base_match.group(2).strip()
        
        if base not in (2, 8, 10, 16):
            raise ValueError(f"Неподдерживаемая система счисления: {base} (допустимы 2, 8, 10, 16)")
        
        digits = digits.replace('_', '')
        
        try:
            result = int(digits, base)
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга числа '{digits}' в системе счисления {base}: {e}")
    else:
        num_str_clean = num_str.replace('_', '')
        
        if '.' in num_str_clean or 'e' in num_str_clean.lower():
            try:
                result = float(num_str_clean)
            except ValueError as e:
                raise ValueError(f"Ошибка парсинга вещественного числа '{num_str_clean}': {e}")
        else:
            try:
                result = int(num_str_clean)
            except ValueError as e:
                raise ValueError(f"Ошибка парсинга целого числа '{num_str_clean}': {e}")
    
    if num_type:
        type_limits = {
            # 
            'SINT':   (-128, 127, int),
            'INT':    (-32768, 32767, int),
            'DINT':   (-2147483648, 2147483647, int),
            'LINT':   (-9223372036854775808, 9223372036854775807, int),
            #
            'USINT':  (0, 255, int),
            'UINT':   (0, 65535, int),
            'UDINT':  (0, 4294967295, int),
            'ULINT':  (0, 18446744073709551615, int),
            'BYTE':   (0, 255, int),
            'WORD':   (0, 65535, int),
            'DWORD':  (0, 4294967295, int),
            'LWORD':  (0, 18446744073709551615, int),
            #
            'REAL':   (None, None, float),
            'LREAL':  (None, None, float),
        }
        
        if num_type in type_limits:
            min_val, max_val, target_type = type_limits[num_type]
            
            if target_type == float and not isinstance(result, float):
                result = float(result)
            
            if min_val is not None and result < min_val:
                raise ValueError(f"Значение {result} выходит за нижнюю границу типа {num_type} ({min_val})")
            if max_val is not None and result > max_val:
                raise ValueError(f"Значение {result} выходит за верхнюю границу типа {num_type} ({max_val})")
        else:
            pass
    
    return result
'''

class F_ADD:

    def schedule(self, event_name, event_value, IN1, IN2):    
        if event_name == 'REQ':
            return event_value, IN1 + IN2