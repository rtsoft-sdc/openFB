# Примеры использования и результаты

## Быстрый старт в 5 минут

### 1. Установка (1 мин)

```bash
cd openfb
pip install pytest pytest-cov pytest-timeout
```

### 2. Запуск тестов (2 мин)

```bash
# Все тесты
python run_tests.py

# Или напрямую через pytest
pytest tests/ -v
```

### 3. Просмотр результатов (2 мин)

```bash
# С подробным выводом
python run_tests.py --events -v

# С отчетом покрытия
python run_tests.py --coverage
```

## Примеры команд

### Базовое использование

```bash
# Все тесты
pytest tests/ -v

# Быстрый запуск без подробностей
pytest tests/ -q

# Останавливаться на первой ошибке
pytest tests/ -x
```

### Специальные фильтры

```bash
# Только Event блоки
pytest tests/test_events/ -v

# Только Convert блоки
pytest tests/test_convert/ -v

# Только интеграционные тесты
pytest tests/ -m integration -v

# Только unit тесты
pytest tests/ -m unit -v

# Конкретный тест
pytest tests/test_events/test_event_blocks.py::TestE_CTU::test_ctu_increment -v
```

### С отчетами

```bash
# Отчет покрытия в HTML
pytest tests/ --cov=openfb.resources.function_blocks --cov-report=html

# Отчет в консоль
pytest tests/ --cov=openfb.resources.function_blocks --cov-report=term-missing

# XML отчет для CI
pytest tests/ --junit-xml=test-results.xml
```

### С таймаутом для таймеров

```bash
# 10 сек на каждый тест
pytest tests/ --timeout=10

# 30 сек для медленных тестов
pytest tests/ -m slow --timeout=30
```

### Использование скрипта run_tests.py

```bash
# Все тесты (по умолчанию)
python run_tests.py

# Event блоки
python run_tests.py --events

# Convert блоки
python run_tests.py --convert

# С подробным выводом
python run_tests.py -v

# С отчетом покрытия
python run_tests.py --coverage

# Бенчмарки производительности
python run_tests.py --benchmark

# Комплексный сценарий
python run_tests.py --complex
```

## Ожидаемые результаты

### Запуск всех Event тестов

```
$ python run_tests.py --events -v

tests/test_events/test_event_blocks.py::TestE_CTU::test_ctu_increment PASSED
tests/test_events/test_event_blocks.py::TestE_CTU::test_ctu_overflow PASSED
tests/test_events/test_event_blocks.py::TestE_CTU::test_ctu_reset PASSED
tests/test_events/test_event_blocks.py::TestE_CTD::test_ctd_decrement PASSED
...
tests/test_events/test_event_blocks.py::TestEventBlockIntegration::test_demux_to_multiple_consumers PASSED

===================== 60+ passed in X.XXs ======================
```

### Запуск комплексного сценария

```
$ python run_tests.py --complex

============================================================
СИМУЛЯЦИЯ ПОЛНОГО ЦИКЛА СТИРКИ
============================================================
[CYCLE 1] Начало цикла стирки
[CYCLE 1] Фаза 1: ЗАПОЛНЕНИЕ (30 сек)
[CYCLE 1] Фаза 2: СТИРКА (120 сек)
[CYCLE 1] Фаза 3: ПОЛОСКАНИЕ (60 сек)
[CYCLE 1] Фаза 4: ОТЖИМ (45 сек)
Цикл ЗАВЕРШЕН

============================================================
СТАТИСТИКА:
  Цикл: 1
  Фаза: 0
  Статус: Остановлена
============================================================

===================== 6 passed in X.XXs ======================
```

### Отчет покрытия

```
$ python run_tests.py --coverage

Name                                                     Stmts   Miss  Cover
--------------------------------------------------------------------------
openfb/resources/function_blocks/events/E_CTU.py           30      0   100%
openfb/resources/function_blocks/events/E_CTD.py           30      0   100%
openfb/resources/function_blocks/events/E_RS.py            25      0   100%
...
--------------------------------------------------------------------------
TOTAL                                                     500     20    96%
```

### Бенчмарки производительности

```
$ python run_tests.py --benchmark

БЕНЧМАРКИ ПРОИЗВОДИТЕЛЬНОСТИ
============================================================
E_CTU                |    500000 calls/sec |    0.002 ms/call
E_R_TRIG             |    450000 calls/sec |    0.002 ms/call
E_DEMUX_4            |    420000 calls/sec |    0.002 ms/call
E_TON                |    380000 calls/sec |    0.003 ms/call
============================================================
```

## Примеры написания своих тестов

### Простой unit тест

```python
def test_my_counter(self, fb_fixture, event_helper):
    """Тест моего счетчика"""
    block = fb_fixture(E_CTU).create()
    
    # Первое увеличение
    result = block.call('CU', 'CU_EVENT', 10)
    event_helper.assert_event_output(result, 'CU_EVENT', False, 1)
    
    # Второе увеличение
    result = block.call('CU', 'CU_EVENT', 10)
    event_helper.assert_event_output(result, 'CU_EVENT', False, 2)
```

### Интеграционный тест

```python
def test_my_workflow(self, fb_fixture):
    """Тест моего рабочего процесса"""
    trigger = fb_fixture(E_R_TRIG).create()
    counter = fb_fixture(E_CTU).create()
    
    # Обнаружить фронт
    edge_result = trigger.call('EI', 'TRIG_EVENT', True)
    
    # Увеличить счетчик при фронте
    if edge_result:
        count_result = counter.call('CU', edge_result, 10)
        assert count_result is not None
```

### Тест с таймерами

```python
def test_my_timer_logic(self, fb_fixture):
    """Тест с таймерами"""
    timer = fb_fixture(E_TON).create()
    
    # Запустить таймер на 0.1 сек
    timer.call('REQ', 'START', True, 0.1)
    
    # Дождаться истечения
    time.sleep(0.15)
    
    # Проверить результат
    assert timer.Q == True
```

## Структура файлов проекта после создания тестов

```
openfb/
├── openfb/                     # Основной пакет
│   └── resources/
│       └── function_blocks/    # Блоки
│
├── tests/                      # Тесты ← НОВОЕ
│   ├── conftest.py             # Конфигурация
│   ├── test_utils_py.py        # Утилиты
│   ├── test_complex_scenario.py # Комплексные сценарии
│   ├── test_events/            # Event блоки
│   ├── test_convert/           # Convert блоки
│   ├── test_iec61131/          # IEC блоки
│   ├── test_utils/             # Utils блоки
│   └── README.md               # Документация
│
├── pytest.ini                  # Конфигурация pytest ← НОВОЕ
├── run_tests.py                # Скрипт запуска ← НОВОЕ
├── requirements-test.txt       # Зависимости ← НОВОЕ
├── TESTING_GUIDE.md            # Полное руководство ← НОВОЕ
├── TESTS_SUMMARY.md            # Резюме ← НОВОЕ
├── TESTS_INDEX.md              # Индекс файлов ← НОВОЕ
└── ...
```

## Проверка корректности установки

```bash
# Проверить pytest
pytest --version
# Должна быть версия >= 7.0.0

# Проверить импорты
python -c "from tests.conftest import FunctionBlockTestFixture; print('OK')"

# Запустить один простой тест
pytest tests/test_convert/test_convert_blocks.py::TestConvertBlocksBasic::test_array_conversion_structure -v
```

## Интеграция с CI/CD

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements-test.txt
      - run: pytest tests/ --cov=openfb
```

### GitLab CI

```yaml
test:
  script:
    - pip install -r requirements-test.txt
    - pytest tests/ --junit-xml=report.xml --cov=openfb
  artifacts:
    reports:
      junit: report.xml
```

## Отладка при проблемах

### Тест зависает

```bash
# Использовать таймаут
pytest tests/ --timeout=10
```

### Видеть print'ы в тестах

```bash
# Флаг -s для показа вывода
pytest tests/ -s
```

### Подробный вывод ошибок

```bash
# Флаг -vv для очень подробного вывода
pytest tests/ -vv

# Полная трассировка
pytest tests/ --tb=long
```

### Выполнять тесты медленнее (для отладки)

```bash
# Добавить sleep в тестовые функции или использовать pdb
import pdb; pdb.set_trace()
```

## Проверка работоспособности после создания

```bash
# 1. Проверить что все файлы созданы
ls -la tests/
ls -la tests/test_*/
ls -la pytest.ini run_tests.py

# 2. Запустить быстрый тест
python run_tests.py --convert -v

# 3. Запустить Event тесты (дольше из-за таймеров)
python run_tests.py --events

# 4. Запустить комплексный сценарий
python run_tests.py --complex --verbose

# 5. Проверить отчет покрытия
python run_tests.py --coverage
# открыть htmlcov/index.html
```

## Что дальше?

После проверки базовых тестов:

1. **Расширить тесты для Convert блоков** - добавить реальные тесты с данными
2. **Добавить IEC 61131 тесты** - протестировать стандартные функции
3. **Создать свой сценарий** - адаптировать WashingMachineController под вашу задачу
4. **Настроить CI/CD** - автоматические тесты при каждом push
5. **Добавить performance тесты** - проверить скорость критичных операций

---

**Готовая к использованию инфраструктура для тестирования всех функциональных блоков OpenFB!**
