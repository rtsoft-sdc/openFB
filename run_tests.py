#!/usr/bin/env python
"""
Скрипт для запуска и управления тестами функциональных блоков OpenFB

Использование:
    python run_tests.py                    # Запустить все тесты
    python run_tests.py --events          # Только event блоки
    python run_tests.py --convert         # Только convert блоки
    python run_tests.py --verbose         # Подробный вывод
    python run_tests.py --benchmark       # Запустить бенчмарки
    python run_tests.py --coverage        # С отчетом покрытия
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path


class TestRunner:
    """Управляющий класс для запуска тестов"""
    
    def __init__(self, root_dir: str = None):
        if root_dir is None:
            root_dir = Path(__file__).parent
        self.root_dir = Path(root_dir)
        self.tests_dir = self.root_dir / 'tests'
    
    def run_pytest(self, args: list) -> int:
        """Запустить pytest с аргументами"""
        cmd = ['python', '-m', 'pytest'] + args
        print(f"Запуск: {' '.join(cmd)}")
        print("="*60)
        return subprocess.run(cmd, cwd=self.root_dir).returncode
    
    def run_all_tests(self, verbose: bool = False) -> int:
        """Запустить все тесты"""
        args = ['tests/']
        if verbose:
            args.append('-vv')
        else:
            args.append('-v')
        return self.run_pytest(args)
    
    def run_event_tests(self, verbose: bool = False) -> int:
        """Запустить тесты event блоков"""
        args = ['tests/test_events/']
        if verbose:
            args.append('-vv')
        else:
            args.append('-v')
        return self.run_pytest(args)
    
    def run_convert_tests(self, verbose: bool = False) -> int:
        """Запустить тесты convert блоков"""
        args = ['tests/test_convert/']
        if verbose:
            args.append('-vv')
        else:
            args.append('-v')
        return self.run_pytest(args)
    
    def run_iec61131_tests(self, verbose: bool = False) -> int:
        """Запустить тесты IEC 61131 функций"""
        args = ['tests/test_iec61131/']
        if verbose:
            args.append('-vv')
        else:
            args.append('-v')
        return self.run_pytest(args)
    
    def run_integration_tests(self, verbose: bool = False) -> int:
        """Запустить интеграционные тесты"""
        args = ['tests/', '-m', 'integration']
        if verbose:
            args.append('-vv')
        else:
            args.append('-v')
        return self.run_pytest(args)
    
    def run_unit_tests(self, verbose: bool = False) -> int:
        """Запустить unit тесты"""
        args = ['tests/', '-m', 'unit']
        if verbose:
            args.append('-vv')
        else:
            args.append('-v')
        return self.run_pytest(args)
    
    def run_complex_scenario(self, verbose: bool = False) -> int:
        """Запустить комплексный сценарий"""
        args = ['tests/test_complex_scenario.py']
        if verbose:
            args.append('-vv')
        else:
            args.append('-v')
        args.append('-s')  # Показывать print'ы
        return self.run_pytest(args)
    
    def run_with_coverage(self) -> int:
        """Запустить тесты с отчетом покрытия"""
        args = [
            'tests/',
            '--cov=openfb.resources.function_blocks',
            '--cov-report=html',
            '--cov-report=term-missing',
            '-v'
        ]
        return self.run_pytest(args)
    
    def run_with_timeout(self, timeout: int = 10) -> int:
        """Запустить тесты с таймаутом"""
        args = ['tests/', f'--timeout={timeout}', '-v']
        return self.run_pytest(args)
    
    def run_benchmark(self) -> int:
        """Запустить бенчмарки производительности"""
        # Создать простой скрипт для бенчмарков
        benchmark_code = '''
from tests.test_utils_py import PerformanceBenchmark
from openfb.resources.function_blocks.events.E_CTU import E_CTU
from openfb.resources.function_blocks.events.E_R_TRIG import E_R_TRIG
from openfb.resources.function_blocks.events.E_DEMUX_4 import E_DEMUX_4
from openfb.resources.function_blocks.events.timers.E_TON import E_TON

print("\\nБЕНЧМАРКИ ПРОИЗВОДИТЕЛЬНОСТИ")
print("="*60)

blocks = [E_CTU, E_R_TRIG, E_DEMUX_4, E_TON]
results = PerformanceBenchmark.compare_blocks(blocks, iterations=1000)

for result in results:
    if 'error' in result:
        print(f"{result['block_name']}: ОШИБКА - {result['error']}")
    else:
        print(f"{result['block_name']:20} | "
              f"{result['calls_per_second']:10.0f} calls/sec | "
              f"{result['milliseconds_per_call']:8.3f} ms/call")

print("="*60)
'''
        
        # Выполнить скрипт
        return subprocess.run(
            [sys.executable, '-c', benchmark_code],
            cwd=self.root_dir
        ).returncode
    
    def print_help(self):
        """Вывести справку"""
        print("""
OpenFB Функциональные блоки - Утилита для тестирования

Использование:
    python run_tests.py [OPTIONS]

Опции:
    --all              Запустить все тесты (по умолчанию)
    --events           Только event блоки
    --convert          Только convert блоки
    --iec61131         Только IEC 61131 функции
    --integration      Только интеграционные тесты
    --unit             Только unit тесты
    --complex          Комплексный сценарий со множеством блоков
    
    --verbose, -v      Подробный вывод
    --coverage         Отчет покрытия кода
    --timeout N        Таймаут N секунд на каждый тест
    --benchmark        Бенчмарки производительности
    
    --help, -h         Эта справка

Примеры:
    python run_tests.py --events -v
    python run_tests.py --coverage
    python run_tests.py --complex --verbose
    python run_tests.py --benchmark
        """)


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description='OpenFB Утилита для тестирования функциональных блоков',
        add_help=False
    )
    
    parser.add_argument('--all', action='store_true', help='Все тесты')
    parser.add_argument('--events', action='store_true', help='Event блоки')
    parser.add_argument('--convert', action='store_true', help='Convert блоки')
    parser.add_argument('--iec61131', action='store_true', help='IEC 61131')
    parser.add_argument('--utils', action='store_true', help='Utils блоки')
    parser.add_argument('--integration', action='store_true', help='Интеграционные')
    parser.add_argument('--unit', action='store_true', help='Unit тесты')
    parser.add_argument('--complex', action='store_true', help='Комплексный сценарий')
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Подробный вывод')
    parser.add_argument('--coverage', action='store_true', help='Отчет покрытия')
    parser.add_argument('--timeout', type=int, default=10, help='Таймаут (сек)')
    parser.add_argument('--benchmark', action='store_true', help='Бенчмарки')
    
    parser.add_argument('-h', '--help', action='store_true', help='Справка')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.help:
        runner.print_help()
        return 0
    
    # Определить, какие тесты запустить
    if args.benchmark:
        return runner.run_benchmark()
    elif args.coverage:
        return runner.run_with_coverage()
    elif args.complex:
        return runner.run_complex_scenario(args.verbose)
    elif args.events:
        return runner.run_event_tests(args.verbose)
    elif args.convert:
        return runner.run_convert_tests(args.verbose)
    elif args.iec61131:
        return runner.run_iec61131_tests(args.verbose)
    elif args.integration:
        return runner.run_integration_tests(args.verbose)
    elif args.unit:
        return runner.run_unit_tests(args.verbose)
    else:
        # По умолчанию - все тесты
        return runner.run_all_tests(args.verbose)


if __name__ == '__main__':
    sys.exit(main())
