# Тестирование функциональных блоков OpenFB - Полное руководство

## Обзор

Инфраструктура тестирования OpenFB предоставляет:

1. **Модульные тесты** для отдельных функциональных блоков
2. **Интеграционные тесты** для комбинаций блоков
3. **Комплексные сценарии** с большим количеством взаимодействующих блоков
4. **Бенчмарки производительности**
5. **Инструменты для отладки и анализа**

## Структура проекта

```
openfb/
├── openfb/
│   └── resources/
│       └── function_blocks/
│           ├── events/          # Event-driven блоки
│           ├── convert/         # Блоки преобразования данных
│           ├── iec61131/        # Стандартные функции
│           └── utils/           # Утилиты
│
├── tests/                       # Директория с тестами
│   ├── __init__.py
│   ├── conftest.py              # Конфигурация pytest
│   ├── test_utils_py.py         # Вспомогательные утилиты
│   ├── test_complex_scenario.py # Комплексные сценарии
│   │
│   ├── test_events/
│   │   ├── __init__.py
│   │   └── test_event_blocks.py # Тесты для event блоков
│   │
│   ├── test_convert/
│   │   ├── __init__.py
│   │   └── test_convert_blocks.py # Тесты для convert блоков
│   │
│   ├── test_iec61131/
│   │   ├── __init__.py
│   │   └── test_iec61131_blocks.py # Тесты для стандартных функций
│   │
│   ├── test_utils/
│   │   ├── __init__.py
│   │   └── test_utils_blocks.py # Тесты для утилит
│   │
│   └── README.md                # Документация по тестам
│
├── pytest.ini                   # Конфигурация pytest
├── run_tests.py                 # Скрипт для запуска тестов
└── allBlocks.md                 # Описание всех блоков
```

## Быстрый старт

### Установка

```bash
# Установить зависимости
pip install pytest pytest-cov pytest-timeout

# Или использовать requirements.txt
pip install -r requirements-test.txt
```

### Запуск тестов

```bash
# Все тесты
python run_tests.py

# Event блоки
python run_tests.py --events

# С подробным выводом
python run_tests.py --verbose

# С отчетом покрытия
python run_tests.py --coverage

# Комплексный сценарий
python run_tests.py --complex

# Бенчмарки
python run_tests.py --benchmark
```

## Архитектура тестирования

### 1. Базовые компоненты (conftest.py)

#### FunctionBlockTestFixture
Создание и управление экземплярами блоков:

```python
@pytest.fixture
def fb_fixture():
    return FunctionBlockTestFixture

def test_example(fb_fixture):
    block = fb_fixture(E_CTU).create()
    result = block.call('CU', 'CU_EVENT', 10)
    assert result is not None
    fb_fixture.destroy()
```

#### EventBlockTestHelper
Проверка выходов event блоков:

```python
@pytest.fixture
def event_helper():
    return EventBlockTestHelper()

def test_output(event_helper):
    # Проверить событие и значения
    event_helper.assert_event_output(result, 'EVENT', True, 5)
    # Проверить количество выходов
    event_helper.assert_output_count(result, 3)
```

### 2. Категории тестов

#### Unit тесты (test_events/test_event_blocks.py)

Тестируют функциональность отдельных блоков:

```python
class TestE_CTU:
    """Тесты для E_CTU"""
    
    def test_ctu_increment(self, fb_fixture, event_helper):
        """Основное увеличение счетчика"""
        block = fb_fixture(E_CTU).create()
        result = block.call('CU', 'CU_EVENT', 10)
        event_helper.assert_event_output(result, 'CU_EVENT', False, 1)
```

#### Интеграционные тесты

Тестируют взаимодействие нескольких блоков:

```python
class TestEventBlockIntegration:
    """Интеграционные тесты"""
    
    def test_counter_with_trigger(self, fb_fixture):
        """Счетчик с детектором фронта"""
        counter = fb_fixture(E_CTU).create()
        trigger = fb_fixture(E_R_TRIG).create()
        
        result = trigger.call('EI', 'TRIG_EVENT', True)
        if result:
            counter.call('CU', result, 10)
```

#### Комплексные сценарии (test_complex_scenario.py)

Демонстрируют использование множества блоков:

```python
class WashingMachineController:
    """Контроллер стиральной машины с 10+ блоками"""
    
    def __init__(self):
        self.start_trigger = E_R_TRIG()
        self.phase_counter = E_CTU()
        self.power_control = E_RS()
        self.phase_timers = {...}
        # и т.д.
```

### 3. Вспомогательные утилиты (test_utils_py.py)

#### BlockTestRunner
Запуск и отслеживание результатов:

```python
runner = BlockTestRunner(verbose=True)
runner.run_test('E_CTU', 'test_increment', test_func)
summary = runner.get_summary()
runner.print_summary()
```

#### EventSequenceSimulator
Симуляция последовательности событий:

```python
simulator = EventSequenceSimulator(E_CTU)
simulator.add_event('CU', 'CU_EVENT', (10,))
simulator.add_event('CU', 'CU_EVENT', (10,))
results = simulator.execute_sequence()
trace = simulator.get_event_trace()
```

#### PerformanceBenchmark
Бенчмарки производительности:

```python
benchmark = PerformanceBenchmark.benchmark_block(E_CTU, iterations=1000)
print(f"{benchmark['calls_per_second']:.0f} calls/sec")

results = PerformanceBenchmark.compare_blocks([E_CTU, E_R_TRIG], iterations=1000)
```

## Примеры использования

### Тест счетчика

```python
def test_ctu_overflow(self, fb_fixture, event_helper):
    """Тест переполнения счетчика"""
    block = fb_fixture(E_CTU).create()
    
    # Увеличить счетчик до значения переполнения
    for _ in range(10):
        result = block.call('CU', 'CU_EVENT', 5)
    
    # Проверить Q=True при переполнении
    assert result[1] == True
```

### Тест таймера

```python
def test_ton_delay(self, fb_fixture):
    """Тест задержки включения"""
    block = fb_fixture(E_TON).create()
    
    # Включить с задержкой
    block.call('REQ', 'REQ_EVENT', True, 0.1)
    
    # Дождаться истечения задержки
    time.sleep(0.15)
    
    # Проверить, что Q=True
    assert block.Q == True
```

### Тест демультиплексера

```python
def test_demux_routing(self, fb_fixture):
    """Тест маршрутизации"""
    block = fb_fixture(E_DEMUX_4).create()
    
    # Проверить маршрутизацию на каждый выход
    for k in range(4):
        result = block.call('EI', 'EVENT', k)
        for i in range(4):
            if i == k:
                assert result[i] == 'EVENT'
            else:
                assert result[i] is None
```

## Запуск различных сценариев

### Быстрые unit тесты

```bash
pytest tests/ -m unit -v --tb=short
```

### Полные интеграционные тесты

```bash
pytest tests/ -m integration -v
```

### Медленные тесты с таймерами

```bash
pytest tests/ -m slow -v --timeout=30
```

### С отчетом покрытия

```bash
pytest tests/ --cov=openfb.resources.function_blocks --cov-report=html
```

## Работа с комплексными сценариями

### Запуск примера стиральной машины

```bash
python run_tests.py --complex --verbose
```

Результат:
```
============================================================
СИМУЛЯЦИЯ ПОЛНОГО ЦИКЛА СТИРКИ
============================================================
[CYCLE 1] Начало цикла стирки
[CYCLE 1] Фаза 1 выполняется (0.3s)
[CYCLE 1] Фаза 2: СТИРКА выполняется (0.5s)
[CYCLE 1] Фаза 3: ПОЛОСКАНИЕ выполняется (0.3s)
[CYCLE 1] Фаза 4: ОТЖИМ выполняется (0.4s)
Цикл ЗАВЕРШЕН
============================================================
```

### Добавление собственного сценария

Создайте файл `tests/test_my_scenario.py`:

```python
class TestMyAutomation:
    """Мой сценарий автоматизации"""
    
    def __init__(self):
        # Инициализировать блоки
        self.block1 = E_CTU()
        self.block2 = E_RS()
        # и т.д.
    
    def execute_logic(self):
        # Ваша логика
        pass
    
    def test_scenario(self):
        controller = TestMyAutomation()
        controller.execute_logic()
        # Проверки
```

## Советы и рекомендации

### 1. Организация тестов

```python
# ✓ Хорошо: Ясное название теста
def test_ctu_increments_counter_on_cu_event(self, fb_fixture):
    pass

# ✗ Плохо: Неясное название
def test_ctu_1(self, fb_fixture):
    pass
```

### 2. Использование фиксстур

```python
# ✓ Хорошо: Использование fb_fixture
def test_block(self, fb_fixture):
    block = fb_fixture(E_CTU).create()
    # test code
    # Автоматическая очистка

# ✗ Плохо: Ручное управление
def test_block(self):
    block = E_CTU()
    # может остаться зависший таймер
```

### 3. Проверка состояния

```python
# ✓ Хорошо: Проверка внутреннего состояния
assert block.Q == True
assert block.CV == 5

# ✗ Плохо: Полагаться только на возвращаемое значение
result = block.call('REQ', 'EVENT')
assert result == 'EVENT'  # Недостаточно
```

### 4. Обработка таймеров

```python
# ✓ Хорошо: Дождаться завершения таймера
block = fb_fixture(E_TON).create()
block.call('REQ', 'REQ_EVENT', True, 0.1)
time.sleep(0.15)  # Дождаться завершения
assert block.Q == True

# ✗ Плохо: Не учитывать задержку
block.call('REQ', 'REQ_EVENT', True, 0.1)
assert block.Q == True  # Может быть False!
```

## Отладка тестов

### Включить подробный вывод

```bash
pytest tests/test_events/test_event_blocks.py::TestE_CTU::test_ctu_increment -vv -s
```

### Запустить с логированием

```bash
pytest tests/ -v --log-cli-level=DEBUG
```

### Использовать pdb для отладки

```python
def test_example(self, fb_fixture):
    block = fb_fixture(E_CTU).create()
    result = block.call('CU', 'CU_EVENT', 10)
    
    import pdb; pdb.set_trace()  # Остановиться здесь для отладки
    assert result is not None
```

## Расширение тестов

### Добавить новый тест

1. Найдите соответствующий файл в `tests/test_*/`
2. Добавьте новый класс `TestBlockName` или метод к существующему
3. Используйте фиксстуры `fb_fixture` и `event_helper`
4. Запустите `pytest tests/test_*/ -v`

### Добавить новый комплексный сценарий

1. Создайте класс-контроллер с логикой
2. Создайте класс-тест с методами `test_*`
3. Используйте маркер `@pytest.mark.integration` для интеграционных тестов
4. Используйте маркер `@pytest.mark.slow` для медленных тестов

## Известные проблемы и их решение

### Проблема: Зависшие таймеры после тестов

**Решение**: Используйте фиксстуру `fb_fixture`, которая автоматически отменяет таймеры

### Проблема: Медленные тесты с таймерами

**Решение**: Используйте сокращенные значения времени в тестах:
```python
# Вместо 30 секунд использовать 0.3 секунды
block.call('REQ', 'EVENT', True, 0.3)
time.sleep(0.35)
```

### Проблема: Конфликты состояния между тестами

**Решение**: Убедитесь, что каждый тест использует отдельный экземпляр блока через фиксстуру

## Дополнительные ресурсы

- [pytest документация](https://docs.pytest.org/)
- [OpenFB документация](../README.md)
- [Описание функциональных блоков](../allBlocks.md)

## Заключение

Инфраструктура тестирования OpenFB обеспечивает:

- ✓ Простоту в написании и запуске тестов
- ✓ Автоматизацию управления ресурсами
- ✓ Гибкость для различных типов тестов
- ✓ Готовые примеры и шаблоны
- ✓ Инструменты для анализа и отладки

Используйте эту инфраструктуру для обеспечения качества вашего кода!
