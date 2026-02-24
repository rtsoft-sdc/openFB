"""
Вспомогательные утилиты для тестирования функциональных блоков
"""
import time
from typing import Any, Tuple, Optional, List, Union
from dataclasses import dataclass


@dataclass
class TestResult:
    """Результат выполнения теста функционального блока"""
    passed: bool
    block_name: str
    test_name: str
    duration: float
    error_message: Optional[str] = None
    
    def __str__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        message = f"{status} | {self.block_name}.{self.test_name} | {self.duration:.3f}s"
        if self.error_message:
            message += f"\n  Error: {self.error_message}"
        return message


class BlockTestRunner:
    """Утилита для запуска и отслеживания результатов тестирования блоков"""
    
    def __init__(self, verbose: bool = True):
        self.results: List[TestResult] = []
        self.verbose = verbose
    
    def run_test(self, block_name: str, test_name: str, test_func, *args, **kwargs) -> TestResult:
        """
        Запустить тест и записать результат.
        
        Args:
            block_name: Имя функционального блока
            test_name: Имя теста
            test_func: Функция теста
            *args, **kwargs: Аргументы для функции теста
        
        Returns:
            TestResult с результатом выполнения
        """
        start_time = time.time()
        try:
            test_func(*args, **kwargs)
            duration = time.time() - start_time
            result = TestResult(
                passed=True,
                block_name=block_name,
                test_name=test_name,
                duration=duration
            )
        except AssertionError as e:
            duration = time.time() - start_time
            result = TestResult(
                passed=False,
                block_name=block_name,
                test_name=test_name,
                duration=duration,
                error_message=str(e)
            )
        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(
                passed=False,
                block_name=block_name,
                test_name=test_name,
                duration=duration,
                error_message=f"{type(e).__name__}: {str(e)}"
            )
        
        self.results.append(result)
        
        if self.verbose:
            print(result)
        
        return result
    
    def get_summary(self) -> dict:
        """Получить сводку по всем результатам"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        total_duration = sum(r.duration for r in self.results)
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / total * 100) if total > 0 else 0,
            'total_duration': total_duration,
            'avg_duration': total_duration / total if total > 0 else 0
        }
    
    def print_summary(self):
        """Вывести сводку по результатам"""
        summary = self.get_summary()
        print("\n" + "="*60)
        print("ТЕСТИРОВАНИЕ ФУНКЦИОНАЛЬНЫХ БЛОКОВ - СВОДКА")
        print("="*60)
        print(f"Всего тестов:    {summary['total']}")
        print(f"Успешно:         {summary['passed']} ({summary['success_rate']:.1f}%)")
        print(f"Неудачно:        {summary['failed']}")
        print(f"Общее время:     {summary['total_duration']:.3f}s")
        print(f"Среднее время:   {summary['avg_duration']:.3f}s")
        print("="*60)


class BlockStateValidator:
    """Валидатор состояния функционального блока"""
    
    @staticmethod
    def validate_output_structure(result: Any, expected_structure: Tuple) -> bool:
        """
        Проверить структуру выходных данных блока.
        
        Args:
            result: Результат вызова block.schedule()
            expected_structure: Кортеж с ожидаемыми типами (e.g., (str, bool, int))
        
        Returns:
            True если структура совпадает, False иначе
        """
        if result is None:
            return expected_structure is None
        
        if not isinstance(result, tuple):
            return len(expected_structure) == 1 and isinstance(result, expected_structure[0])
        
        if len(result) != len(expected_structure):
            return False
        
        for actual, expected_type in zip(result, expected_structure):
            if actual is not None and not isinstance(actual, expected_type):
                return False
        
        return True
    
    @staticmethod
    def validate_state_transition(initial_state: dict, final_state: dict, 
                                  expected_changes: dict) -> bool:
        """
        Проверить переход состояния блока.
        
        Args:
            initial_state: Начальное состояние
            final_state: Финальное состояние
            expected_changes: Ожидаемые изменения {key: expected_value}
        
        Returns:
            True если все ожидаемые изменения произошли
        """
        for key, expected_value in expected_changes.items():
            if key not in final_state:
                return False
            if final_state[key] != expected_value:
                return False
        
        return True


class EventSequenceSimulator:
    """Симулятор последовательности событий для тестирования"""
    
    def __init__(self, block_class):
        self.block_class = block_class
        self.block = block_class()
        self.events: List[Tuple[str, Any, Tuple]] = []
        self.results: List[Any] = []
    
    def add_event(self, event_name: str, event_value: Any, args: Tuple = ()):
        """Добавить событие в последовательность"""
        self.events.append((event_name, event_value, args))
    
    def execute_sequence(self) -> List[Any]:
        """
        Выполнить последовательность событий.
        
        Returns:
            Список результатов для каждого события
        """
        self.results = []
        for event_name, event_value, args in self.events:
            result = self.block.schedule(event_name, event_value, *args)
            self.results.append(result)
        return self.results
    
    def get_event_trace(self) -> List[dict]:
        """Получить трассировку выполнения событий"""
        trace = []
        for i, ((event_name, event_value, args), result) in enumerate(
            zip(self.events, self.results)
        ):
            trace.append({
                'index': i,
                'event': event_name,
                'value': event_value,
                'args': args,
                'result': result
            })
        return trace


class PerformanceBenchmark:
    """Инструмент для бенчмарка производительности блоков"""
    
    @staticmethod
    def benchmark_block(block_class, iterations: int = 1000) -> dict:
        """
        Выполнить бенчмарк производительности блока.
        
        Args:
            block_class: Класс функционального блока
            iterations: Количество итераций
        
        Returns:
            Словарь с метриками производительности
        """
        block = block_class()
        
        # Простой вызов schedule
        start_time = time.time()
        for _ in range(iterations):
            result = block.schedule('REQ', 'EVENT', )
        elapsed = time.time() - start_time
        
        calls_per_sec = iterations / elapsed
        time_per_call = (elapsed * 1000) / iterations  # в миллисекундах
        
        return {
            'block_name': block_class.__name__,
            'iterations': iterations,
            'total_time': elapsed,
            'calls_per_second': calls_per_sec,
            'milliseconds_per_call': time_per_call
        }
    
    @staticmethod
    def compare_blocks(block_classes: List, iterations: int = 1000) -> List[dict]:
        """
        Сравнить производительность нескольких блоков.
        
        Args:
            block_classes: Список классов блоков для сравнения
            iterations: Количество итераций
        
        Returns:
            Список результатов бенчмарков
        """
        results = []
        for block_class in block_classes:
            try:
                benchmark = PerformanceBenchmark.benchmark_block(block_class, iterations)
                results.append(benchmark)
            except Exception as e:
                results.append({
                    'block_name': block_class.__name__,
                    'error': str(e)
                })
        
        return results
