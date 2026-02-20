# Среда исполнения IEC 61499 для ML задач

OpenFB - это платформа для выполнения функциональных блоков в соответствии со стандартом IEC 61499. OpenFB базируется на открытом исходном коде и позволяет разработчикам:

1. Создавать пользовательские функциональные блоки без привязки к конкретному производителю оборудования
2. Разворачивать приложения на любой платформе, поддерживающей Python 3 (Linux, Windows, встраиваемые OS, RTOS)
3. Комбинировать компоненты, написанные на Python, C++, промышленных языках IEC 61131-3 в единую систему с использованием стандартизированных сетевых протоколов (OPC UA, MQTT и др.)
4. Избежать технологической зависимости от одного поставщика

Среда исполнения OpenFB совместима с [FORGELOGIC](https://it.severstal.com/products/oasu-tp/#downloads), [4diac IDE 3](https://eclipse.dev/4diac/4diac_ide/).
Проект основан на базе проекта [DINASORE](https://github.com/DIGI2-FEUP/dinasore)

## Лицензия

[EPL 2.0](LICENSE.md).

## Contributing

We use [contribution policy](CONTRIBUTING.md), which means we can only accept contributions under
the terms of [Eclipse Contributor Agreement](http://www.eclipse.org/legal/ECA.php).

# Запуск OpenFB

### 1. Клонировать репозиторий

``` bash
git clone https://gitverse.ru/rtsoft/OpenFB.git
cd OpenFB
```

### 2. Установить Python и зависимости

1.  Убедиться, что Python3 установлен.
2.  Создать виртуальное окружение:

``` bash
python3 -m venv .venv
source .venv/bin/activate   # unix
.venv\Scripts\activate      # windows
```

3.  Установить зависимости:

``` bash
pip install -r requirements.txt
```

### 3. Запустить OpenFB

``` bash
python3 core/main.py
```

### 4. Подключение через ide

Поддерживаются [FORGELOGIC](https://it.severstal.com/products/oasu-tp/#downloads), [4diac IDE 3](https://eclipse.dev/4diac/4diac_ide/).
Важно настроить соединение на порт OpenFB по умолчанию 61499, так же можно подключится по opcua к порту 4840 (по умолчанию)

------------------------------------------------------------------------

# **Как создать новый функциональный блок**

### 1. Создать .fbt файл
Необходимо создать файл с ТОЧНЫМ названием фукционального блока и расширением .fbt\
Необходимо описать в структуре xml все входы и выходы блока и их связи\
Сам блок можно создать в 4diac-ide, а потом найти и скопировать сгенерированый файл.
``` xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<FBType Name="Hello_FB" OpcUa="SERVICE">
  <InterfaceList>
    <EventInputs>
      <Event Name="INIT" Type="Event"/>
      <Event Name="REQ" Type="Event">
        <With Var="IN1"/>
      </Event>
    </EventInputs>
    <EventOutputs>
      <Event Name="INIT_O" Type="Event"/>
      <Event Name="CNF" Type="Event">
        <With Var="OUT1"/>
      </Event>
    </EventOutputs>
    <InputVars>
      <VarDeclaration Name="IN1" Type="STRING"/>
    </InputVars>
    <OutputVars>
      <VarDeclaration Name="OUT1" Type="STRING"/>
    </OutputVars>
  </InterfaceList>
</FBType>
```

### 2. Реализовать Python логику
Необходимо создать файл с ТОЧНЫМ названием фукционального блока и расширением .py\
Далее создаем класс с названием функционального блока и реализуем всю основную логику в функции ```def schedule()```, так как она будет вызываться при любом ивенте, который прийдет на блок.

``` python
class Hello_FB:

    def schedule(self, event_input_name, event_input_value, input_var1):
        if event_input_name == 'INIT':
            return event_input_value, None, "initialized"
        elif event_input_name == 'REQ':
            out = "hello " + input_var1
            return None, event_input_value, out
```

### 3. Разместить файлы

- Папка OpenFB: `resources/function_blocks/...`
- Папка 4diac-ide: `workspace/typelibrary/...`

------------------------------------------------------------------------

### **ВАЖНО**

- После добавления блока перезапустить OpenFB
- Проверить наличие .fbt файла в TypeLibrary ide

------------------------------------------------------------------------

# Примеры

***Все актуальные системы примеров лежат в папке  4diac_sys***
## Поиск шайб(Общее описание)

 Пример адаптирован под плату OrangePi с RK3588s (на текущий момент на других платформах **работать не будет**). В примере используется yolo v7 для детекции: 
 - шайб
 - бракованных шайб 
 - мусор  

## Пример 1. washer_detector
### Смешанная система OpenFB + forte
В примере собрана система с разными средами исполнения:
- Python
- C++
В данном примере среда под С++ публикует сообщения по MQQT, а среда под Python ожидает сообщение и запускает цикл обработки изображения для поиска шайб, их дефектов и прочих объектов (мусора).

## Пример 2. washer_detector_py
### Cистема исполнения OpenFB 
В примере реализовано детектирование брака шайб.

## Пример 3. washer_detector_relay
### Cистема исполнения OpenFB 
В примере реализовано детектирование брака шайб. Обнаружение брака приводит к переключению USB-реле, которое комммутирует линиию питания конвейера.
В этом примере доступен мониторинг блока *PY_RELAY_CTRL* через OPC UA. Для мониторинга доступны события и переменные блока.

#### Тонкости использования
Необходимо дать права на управление устройствами группе пользователя, который будет запускать среду исполнения.
Пример:   
`SUBSYSTEM=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05df", MODE:="0660", GROUP="dialout"`

Строку записывать в файл (Запись только с правами администратора): /etc/udev/rules.d/90-hidusb-relay.rules

# **Примечание! У систем одинковые имена, поэтому при открытие новой системы удаляйте из дерева проектов предыдущую.**

# Подготовка
1. Скачать и установить IDE FL (https://it.severstal.com/products/oasu-tp/#downloads)
2. Скачать репозиторий  https://gitverse.ru/rtsoft/OpenFB.git
3. Запустить IDE
4. Импортировать систему из репозитория  4diac_sys: *demo_whashers*
5. Заменить пути к файлам у блока *Detector_N_Drawer*

# Системные требования

- python3.10 
- python3-pip
- libgl1
- libxrender1
- libxext6
- libgl1-mesa-glx
- libqt5widgets5
- libqt5gui5
- libqt5core5a 
### Python 
Все необходимые библиотеки описаны в файле: **docker/requirements.txt**
