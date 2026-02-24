# Тестирование функциональных блоков OpenFB

Этот директорий содержит комплексные интеграционные тесты для всех функциональных блоков OpenFB.

## Структура

```
tests/
├── conftest.py                 # Конфигурация pytest и общие фиксстуры
├── test_events/                # Тесты для event блоков
│   ├── __init__.py
│   └── test_event_blocks.py    # Тесты для всех event блоков
├── test_convert/               # Тесты для convert блоков
│   ├── __init__.py
│   └── test_convert_blocks.py  # Тесты для всех convert блоков
├── test_iec61131/              # Тесты для IEC 61131 функций
│   ├── __init__.py
│   └── test_iec61131_blocks.py # Тесты для стандартных функций
├── test_utils/                 # Тесты для утилит
│   ├── __init__.py
│   └── test_utils_blocks.py    # Тесты для утилит
└── README.md                   # Этот файл
```

## Запуск тестов

### Установка зависимостей

```bash
pip install pytest pytest-cov pytest-timeout
```

### Запуск всех тестов

```bash
pytest tests/
```

### Запуск тестов для конкретной категории

```bash
# Event блоки
pytest tests/test_events/

# Convert блоки
pytest tests/test_convert/

# IEC 61131 блоки
pytest tests/test_iec61131/

# Utils блоки
pytest tests/test_utils/
```

### Запуск с подробным выводом

```bash
pytest tests/ -v
```

### Запуск с покрытием кода

```bash
pytest tests/ --cov=openfb.resources.function_blocks --cov-report=html
```

### Запуск с таймаутом (предотвращение зависания при работе с таймерами)

```bash
pytest tests/ --timeout=10
```

### Запуск конкретного теста

```bash
pytest tests/test_events/test_event_blocks.py::TestE_CTU::test_ctu_increment -v
```

## Архитектура тестов

### Базовые компоненты (conftest.py)

#### FunctionBlockTestFixture
Фиксстура для создания и управления экземплярами блоков:

```python
fixture = FunctionBlockTestFixture(E_CTU)
block = fixture.create()
result = fixture.call('CU', 'CU_EVENT', 10)
fixture.destroy()
```

#### EventBlockTestHelper
Вспомогательный класс для проверки выходов event блоков:

```python
helper = EventBlockTestHelper()
helper.assert_event_output(result, 'EVENT_NAME', True, 5)  # проверить событие и значения
helper.assert_output_count(result, 2)  # проверить количество выходов
```

### Шаблон тестирования

Каждый блок тестируется с использованием следующего шаблона:

```python
class TestBlockName:
    """Тесты для блока BlockName"""
    
    def test_basic_functionality(self, fb_fixture, event_helper):
        """Основная функциональность"""
        block = fb_fixture(BlockClass).create()
        result = block.call('InputEvent', 'event_value', arg1, arg2)
        event_helper.assert_event_output(result, 'ExpectedEvent', expected_output)
    
    def test_edge_case(self, fb_fixture):
        """Граничный случай"""
        block = fb_fixture(BlockClass).create()
        # тест
```

## Примеры тестов

### Тест счетчика (E_CTU)

```python
def test_ctu_increment(self, fb_fixture, event_helper):
    """Тест увеличения счетчика"""
    block = fb_fixture(E_CTU).create()
    
    # Первое увеличение
    result = block.call('CU', 'CU_EVENT', 10)
    event_helper.assert_event_output(result, 'CU_EVENT', False, 1)
    
    # Второе увеличение
    result = block.call('CU', 'CU_EVENT', 10)
    event_helper.assert_event_output(result, 'CU_EVENT', False, 2)
```

### Тест таймера (E_TON)

```python
def test_ton_delay(self, fb_fixture, event_helper):
    """Тест задержки включения"""
    block = fb_fixture(E_TON).create()
    
    # Включить с задержкой 0.1 сек
    result = block.call('REQ', 'REQ_EVENT', True, 0.1)
    
    # Дождаться истечения задержки
    time.sleep(0.15)
    
    # После задержки Q должен быть True
    assert block.Q == True
```

### Тест демультиплексера (E_DEMUX_2)

```python
def test_demux_2_routing(self, fb_fixture, event_helper):
    """Тест маршрутизации сигнала"""
    block = fb_fixture(E_DEMUX_2).create()
    
    # Маршрутизировать на выход 0
    result = block.call('EI', 'EI_EVENT', 0)
    assert result[0] == 'EI_EVENT'
    assert result[1] is None
```

## Интеграционные тесты

Интеграционные тесты проверяют взаимодействие между несколькими блоками:

```python
def test_counter_with_trigger(self, fb_fixture, event_helper):
    """Тест счетчика с детектором фронта"""
    counter = fb_fixture(E_CTU).create()
    trigger = fb_fixture(E_R_TRIG).create()
    
    # Генерировать нарастающий фронт
    trigger_result = trigger.call('EI', 'TRIG_EVENT', True)
    
    # Если фронт обнаружен, увеличить счетчик
    if trigger_result:
        counter_result = counter.call('CU', trigger_result, 10)
        assert counter_result is not None
```

## Структура результатов тестов

Результаты тестов хранятся в следующем формате:

- **None**: событие не произошло или условие не выполнено
- **event_value**: одиночное событие
- **(event_value, output1, output2, ...)**: событие с несколькими выходами
- **[event1, event2, ...]**: множество событий (для split)

## Советы по написанию тестов

1. **Используйте фиксстуры**: `fb_fixture` и `event_helper` предоставляют удобные методы работы с блоками.

2. **Проверяйте граничные случаи**: переполнение, underflow, невалидные входы.

3. **Тестируйте состояние**: проверяйте внутреннее состояние блока после выполнения операций.

4. **Используйте таймауты**: при работе с таймерами используйте `--timeout` флаг.

5. **Изолируйте тесты**: каждый тест должен быть независимым от других.

## Запуск больших примеров

После написания тестов для отдельных блоков, можно создавать сценарии с большим количеством блоков:

```python
def test_complex_automation_scenario(self):
    """Сложный сценарий автоматизации"""
    # Инициализировать несколько блоков
    sensor_trigger = fb_fixture(E_R_TRIG).create()
    debounce_timer = fb_fixture(E_TON).create()
    action_counter = fb_fixture(E_CTU).create()
    action_limiter = fb_fixture(E_RS).create()
    
    # Реализовать сложную логику с взаимодействием блоков
    # ...
```

## Известные ограничения

1. **Service Interface Blocks**: Некоторые Convert блоки требуют интеграции с runtime и тестируются на структурном уровне.

2. **Асинхронные операции**: Таймеры и задержки тестируются с использованием `time.sleep()`, что может быть медленным на больших наборах тестов.

3. **Типы данных ANY**: Блоки, работающие с универсальным типом ANY, требуют дополнительной валидации типов.

## Расширение тестов

Для добавления новых тестов:

1. Создайте новый класс теста в соответствующем файле (`test_events/`, `test_convert/` и т.д.)

2. Используйте фиксстуры `fb_fixture` и `event_helper`

3. Следуйте шаблону: arrange → act → assert

4. Документируйте ожидаемое поведение в docstring

## Непрерывная интеграция

Для интеграции в CI/CD pipeline:

```bash
# В GitHub Actions, GitLab CI, или другом CI
pytest tests/ --junit-xml=test-results.xml --cov=openfb --cov-report=xml
```

## Рекомендуемые дополнения

1. **Performance testing**: тесты производительности для критичных по скорости блоков

2. **Stress testing**: тестирование с большим количеством вызовов

3. **Memory profiling**: проверка утечек памяти при длительной работе

4. **Fuzzing**: генерирование случайных входов для поиска багов
