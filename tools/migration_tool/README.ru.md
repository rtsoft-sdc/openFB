# Использование приложения для конвертации проектов IDE 2.0.0->3.0.0
[![English](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![Russian](https://img.shields.io/badge/lang-ru-green.svg)](README.ru.md)

## Установка зависимостей


```
pip install -r ./requirements.txt
```

## Конвертация одного проекта

```
python main.py --project <путь_к_проекту> --typelibrary <путь_к_typelibrary> [--out <выходная_директория>]
```

Пример:
```
python main.py --project ./projects/washer_detector_2.0.1 --typelibrary ./projects/typelibrary --out ./converted_projects
```

## Конвертация нескольких проектов

Создайте JSON-файл конфигурации:

```json
{
    "typelibrary": "./projects/typelibrary",
    "projects": [
        "./projects/project1",
        "./projects/project2"
    ]
}
```

Запустите:
```
python main.py --config test.json [--out ./converted_projects]
```
