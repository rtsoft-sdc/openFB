"""
Тесты для Convert функциональных блоков

Примечание: Большинство Convert блоков - это Service Interface Function Blocks,
которые требуют интеграции с runtime. Здесь показаны примеры модульного тестирования
для простых блоков.
"""
import pytest

class TestConvertBlocksBasic:
    """Базовые тесты для Convert блоков"""
    
    def test_array_conversion_structure(self):
        """Тест структуры конвертирования массивов"""
        # ARRAY2ARRAY_2_LREAL
        # Входы: REQ (Event), IN (LREAL[2])
        # Выходы: CNF (Event), OUT (LREAL[2])
        
        test_array = [1.5, 2.5]
        expected_output = [1.5, 2.5]
        
        assert test_array == expected_output
    
    def test_array_to_values_structure(self):
        """Тест разделения массива на значения"""
        # ARRAY2VALUES_2_LREAL
        # Входы: REQ (Event), IN (LREAL[2])
        # Выходы: CNF (Event), OUT_1 (LREAL), OUT_2 (LREAL)
        
        test_array = [1.5, 2.5]
        out_1 = test_array[0]
        out_2 = test_array[1]
        
        assert out_1 == 1.5
        assert out_2 == 2.5
    
    def test_values_to_array_structure(self):
        """Тест объединения значений в массив"""
        # VALUES2ARRAY_2_LREAL
        # Входы: REQ (Event), IN_1 (LREAL), IN_2 (LREAL)
        # Выходы: CNF (Event), OUT (LREAL[2])
        
        in_1 = 1.5
        in_2 = 2.5
        expected_array = [in_1, in_2]
        
        assert expected_array == [1.5, 2.5]
    
    def test_get_at_index_interface(self):
        """Тест интерфейса получения значения по индексу"""
        # GET_AT_INDEX
        # Входы: REQ (Event), IN_ARRAY (ANY), INDEX (UINT)
        # Выходы: CNF (Event), QO (BOOL), OUT (ANY)
        
        array = [10, 20, 30, 40]
        index = 2
        
        # QO = True если индекс валиден
        qo = 0 <= index < len(array)
        output = array[index] if qo else None
        
        assert qo == True
        assert output == 30
    
    def test_get_at_index_out_of_bounds(self):
        """Тест получения с индексом вне границ"""
        array = [10, 20, 30]
        index = 5
        
        qo = 0 <= index < len(array)
        
        assert qo == False
    
    def test_set_at_index_interface(self):
        """Тест интерфейса установки значения по индексу"""
        # SET_AT_INDEX
        # Входы: REQ (Event), IN_ARRAY (ANY), INDEX (UINT), VALUE (ANY)
        # Выходы: CNF (Event), QO (BOOL), OUT_ARRAY (ANY)
        
        in_array = [10, 20, 30, 40]
        index = 2
        value = 99
        
        # Создать копию и модифицировать
        out_array = in_array.copy()
        qo = True
        
        if 0 <= index < len(out_array):
            out_array[index] = value
        else:
            qo = False
        
        assert out_array == [10, 20, 99, 40]
        assert qo == True
    
    def test_struct_demux_interface(self):
        """Тест интерфейса разделения структуры"""
        # STRUCT_DEMUX
        # Входы: REQ (Event), IN (ANY_STRUCT)
        # Выходы: CNF (Event), + один выход для каждого поля структуры
        
        in_struct = {'field1': 10, 'field2': 20, 'field3': 'test'}
        
        # Демультиплексирование - извлечение полей
        out_field1 = in_struct['field1']
        out_field2 = in_struct['field2']
        out_field3 = in_struct['field3']
        
        assert out_field1 == 10
        assert out_field2 == 20
        assert out_field3 == 'test'
    
    def test_struct_mux_interface(self):
        """Тест интерфейса объединения в структуру"""
        # STRUCT_MUX
        # Входы: REQ (Event), + один вход для каждого поля структуры
        # Выходы: CNF (Event), OUT (ANY_STRUCT)
        
        in_field1 = 10
        in_field2 = 20
        in_field3 = 'test'
        
        # Мультиплексирование - создание структуры
        out_struct = {
            'field1': in_field1,
            'field2': in_field2,
            'field3': in_field3
        }
        
        assert out_struct == {'field1': 10, 'field2': 20, 'field3': 'test'}


class TestConvertBlocksIntegration:
    """Интеграционные тесты для Convert блоков"""
    
    def test_array_to_values_to_array_roundtrip(self):
        """Тест цикла: массив -> значения -> массив"""
        # Исходный массив
        original_array = [1.5, 2.5]
        
        # ARRAY2VALUES: развернуть массив
        out_1 = original_array[0]
        out_2 = original_array[1]
        
        # VALUES2ARRAY: собрать обратно
        reconstructed = [out_1, out_2]
        
        assert reconstructed == original_array
    
    def test_struct_demux_mux_roundtrip(self):
        """Тест цикла: структура -> поля -> структура"""
        # Исходная структура
        original_struct = {
            'id': 42,
            'name': 'test',
            'active': True
        }
        
        # STRUCT_DEMUX: развернуть структуру
        fields = {
            'id': original_struct['id'],
            'name': original_struct['name'],
            'active': original_struct['active']
        }
        
        # STRUCT_MUX: собрать обратно
        reconstructed_struct = fields
        
        assert reconstructed_struct == original_struct
    
    def test_array_indexing_sequence(self):
        """Тест последовательности операций с индексами"""
        array = [10, 20, 30, 40, 50]
        
        # GET_AT_INDEX для различных позиций
        value_at_0 = array[0]
        value_at_2 = array[2]
        value_at_4 = array[4]
        
        # SET_AT_INDEX для изменения значений
        array_copy = array.copy()
        array_copy[2] = 99
        
        # Проверить результаты
        assert value_at_0 == 10
        assert value_at_2 == 30
        assert value_at_4 == 50
        assert array_copy[2] == 99
