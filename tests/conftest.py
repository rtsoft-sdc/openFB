"""
Pytest configuration и общие фиксстуры для тестирования функциональных блоков OpenFB
"""
import sys
import os
from pathlib import Path

# Добавить путь к openfb пакету
OPENFB_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(OPENFB_ROOT))

import pytest


class FunctionBlockTestFixture:
    """Базовый класс для тестирования функциональных блоков"""
    
    def __init__(self, block_class):
        """Инициализация фиксстуры с классом блока"""
        self.block_class = block_class
        self.block = None
    
    def create(self, **kwargs):
        """Создать экземпляр блока"""
        self.block = self.block_class(**kwargs)
        return self.block
    
    def destroy(self):
        """Уничтожить блок и очистить ресурсы"""
        if hasattr(self.block, '_timer') and self.block._timer:
            self.block._timer.cancel()
        self.block = None
    
    def call(self, event_name, event_value, *args, **kwargs):
        """Вызвать метод schedule блока"""
        if self.block is None:
            raise RuntimeError("Блок не был инициализирован. Используйте create() перед вызовом.")
        return self.block.schedule(event_name, event_value, *args, **kwargs)
    
    def reset(self):
        """Сбросить состояние блока"""
        if hasattr(self.block, '__dict__'):
            # Переинициализировать блок
            for attr_name in list(self.block.__dict__.keys()):
                if attr_name.startswith('_'):
                    delattr(self.block, attr_name)


@pytest.fixture
def fb_fixture():
    """Фиксстура для работы с функциональными блоками"""
    return FunctionBlockTestFixture


class EventBlockTestHelper:
    """Вспомогательный класс для тестирования event блоков"""
    
    @staticmethod
    def assert_event_output(result, expected_event, *expected_outputs):
        """
        Проверить, что результат вызова блока содержит ожидаемое событие и выходы.
        
        Args:
            result: результат вызова schedule()
            expected_event: ожидается ли событие (True/False/None)
            expected_outputs: ожидаемые значения выходов
        """
        if expected_event is None:
            assert result is None, f"Ожидается None, получено {result}"
        else:
            assert result is not None, "Ожидается событие, получено None"
            if isinstance(result, tuple):
                assert result[0] == expected_event, f"Ожидается событие {expected_event}, получено {result[0]}"
                if expected_outputs:
                    for i, expected in enumerate(expected_outputs, 1):
                        assert result[i] == expected, f"Выход {i}: ожидается {expected}, получено {result[i]}"
            else:
                assert result == expected_event, f"Ожидается {expected_event}, получено {result}"
    
    @staticmethod
    def assert_output_count(result, expected_count):
        """Проверить количество выходов"""
        if result is None:
            actual_count = 0
        elif isinstance(result, tuple):
            actual_count = len(result)
        else:
            actual_count = 1
        assert actual_count == expected_count, \
            f"Ожидается {expected_count} выходов, получено {actual_count}"


@pytest.fixture
def event_helper():
    """Фиксстура для помощи в тестировании event блоков"""
    return EventBlockTestHelper()


@pytest.fixture(autouse=True)
def cleanup_timers():
    """Автоматическая очистка таймеров после каждого теста"""
    yield
    # Очистка происходит в teardown
    import gc
    gc.collect()
