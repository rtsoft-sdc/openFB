# Примеры 4diac IDE для исполнения под Python (dinasore)

***Все актуальные системы примеров лежат в папке  4diac_sys***
## Поиск шайб(Общее описание)

 Пример адаптирован под плату OrangePi с RK3588s (на текущий момент на других платформах **работать не будет**). В примере используется yolov7 для детекции: 
 - шайб
 - бракованных шайб 
 - мусор  

## Пример 1. washer_detector
### Смешанная система dinasore + forte
В примере собрана система с разными средами исполнения:
- Python
- C++
В данном примере среда под С++ публикует сообщения по MQQT, а среда под Python ожидаем сообщение и запускает цикл обработки изображения для поиска шайб, их дефектов и прочих объектов(мусора).

## Пример 2. washer_detector_py
### Cистема исполнения dinasore 
В примере реализовано детектирование брака шайб.

## Пример 3. washer_detector_relay
### Cистема исполнения dinasore 
В примере реализовано детектирование брака шайб. Обнаружение брака приводит к переключению USB-реле, которое комммутирует линиию питания конвейера.
В этом примере доступен мониторинг блока *PY_RELAY_CTRL* через OPC UA. Для мониторинга доступны события и переменные блока.

#### Тонкости использования
Возможно необходимо дать права на управление устройствами группе пользователя, который будет запускать среду исполнения.
Пример:   
`SUBSYSTEM=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05df", MODE:="0660", GROUP="dialout"`

Строку записывать файл(Запись только с правами администратора): /etc/udev/rules.d/90-hidusb-relay.rules

# **Примечание! У систем одинковые имена, поэтому при открытие новой системы удаляйте из дерева проектов предыдущую.**

# Подготовка
1. Скачать и установить 4diac IDE 3.0
2. Скачать репозиторий https://git.dev.rtsoft.ru/git/rtsedu/dinasore.git
3. Скачать архив из Cloud: https://cloud.dev.rtsoft.ru/index.php/f/6618348
4. Распаковать архив в удобное место
5. Запустить IDE
6. Импортировать систему из репозитория  4diac_sys: *demo_whashers*
7. Заменить пути к файлам у блока *Detector_N_Drawer*


# Software prerequisites
### System 
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




# Общее руководство по работе с Dinasore

**Dynamic INtelligent Architecture for Software and MOdular REconfiguration - DINASORE**

------------------------------------------------------------------------

# Запускать dinasore

### 1. Клонировать репозиторий

``` bash
git clone https://git.dev.rtsoft.ru/git/rtsedu/dinasore.git
cd dinasore
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
pip install -r docker/requirements.txt
```

### 3. Запустить Dinasore

``` bash
python3 core/main.py
```

### 4. Подключение через 4diac-ide

Важно настроить соединение на порт dinasore по умолчанию 61499, так же можно подключится по opcua к порту 4840, который тоже установлен по умолчанию

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

- Папка dinasore: `resources/function_blocks/...`
- Папка 4diac-ide: `workspace/typelibrary/...`

------------------------------------------------------------------------

### **ВАЖНО**

- После добавления блока перезапустить dinasore
- Проверить наличие .fbt файла в TypeLibrary 4diac-ide

------------------------------------------------------------------------