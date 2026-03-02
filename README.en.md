**IEC 61499 Runtime for ML related tasks**

OpenFB is a platform for executing function blocks according to the IEC 61499 standard. OpenFB is based on open source code and allows developers to:

- Create custom function blocks without binding to specific hardware manufacturers
- Deploy applications on any platform supporting Python 3 (Linux, Windows, embedded OS, RTOS)
- Combine components written in Python, C++, and industrial IEC 61131-3 languages into a unified system using standardized network protocols (OPC UA, MQTT, etc.)
- Avoid technological dependence on a single vendor

The OpenFB runtime environment is compatible with [FORGELOGIC](https://it.severstal.com/products/oasu-tp/#downloads), [4diac IDE 3](https://eclipse.dev/4diac/4diac_ide/). The project is based on the [DINASORE](https://github.com/DIGI2-FEUP/dinasore) project.

**License**

[EPL 2.0](https://github.com/rtsoft-sdc/openFB/blob/master/LICENSE.md).

**Contributing**

We use [contribution policy](https://github.com/rtsoft-sdc/openFB/blob/master/CONTRIBUTING.md), which means we can only accept contributions under the terms of [Eclipse Contributor Agreement](http://www.eclipse.org/legal/ECA.php).

**Running OpenFB**

**1. Clone repository**

git clone https://gitverse.ru/rtsoft/OpenFB.git

cd OpenFB

**2. Install Python and dependencies**

1. Ensure Python3 is installed.
1. Create a virtual environment:

python3 -m venv .venv

source .venv/bin/activate   # unix

.venv\Scripts\activate      # windows

3. Install dependecies:

pip install -r requirements.txt

**3. Run OpenFB**

python3 core/main.py

**4. Connect via IDE**

[FORGELOGIC](https://it.severstal.com/products/oasu-tp/#downloads), [4diac IDE 3](https://eclipse.dev/4diac/4diac_ide/). are supported. It is important to configure the connection to the default OpenFB port 61499. You can also connect via OPC UA to port 4840 (default).

-----
**How to create a new function block**

**1. Create .fbt file**

You need to create a file with the EXACT name of the function block and the .fbt extension. You need to describe all inputs and outputs of the block and their connections in the XML structure. The block itself can be created in 4diac-ide, then find and copy the generated file.

<?xml version="1.0" encoding="UTF-8" standalone="no"?>

<FBType Name="Hello\_FB" OpcUa="SERVICE">

`  `<InterfaceList>

`    `<EventInputs>

`      `<Event Name="INIT" Type="Event"/>

`      `<Event Name="REQ" Type="Event">

`        `<With Var="IN1"/>

`      `</Event>

`    `</EventInputs>

`    `<EventOutputs>

`      `<Event Name="INIT\_O" Type="Event"/>

`      `<Event Name="CNF" Type="Event">

`        `<With Var="OUT1"/>

`      `</Event>

`    `</EventOutputs>

`    `<InputVars>

`      `<VarDeclaration Name="IN1" Type="STRING"/>

`    `</InputVars>

`    `<OutputVars>

`      `<VarDeclaration Name="OUT1" Type="STRING"/>

`    `</OutputVars>

`  `</InterfaceList>

</FBType>

**2. Implement Python logic**

You need to create a file with the EXACT name of the function block and the .py extension. Then create a class with the name of the function block and implement all main logic in the def schedule() function, as it will be called for any event that comes to the block.

class Hello\_FB:

`    `def schedule(self, event\_input\_name, event\_input\_value, input\_var1):

`        `if event\_input\_name == 'INIT':

`            `return event\_input\_value, None, "initialized"

`        `elif event\_input\_name == 'REQ':

`            `out = "hello " + input\_var1

`            `return None, event\_input\_value, out

**3. Place the files**

- OpenFB folder: resources/function\_blocks/...
- 4diac-ide folder: workspace/typelibrary/...
-----
**IMPORTANT**

- Restart OpenFB after adding a block
- Check for the .fbt file in the IDE TypeLibrary
-----
**Examples**

All current example systems are located in the 4diac\_sys folder.


**Washer Detection (General Description)**

The example is adapted for the OrangePi board with RK3588s (currently will not work on other platforms). The example uses YOLO v7 for detection of:

- Washers
- Defective washers
- Trash

**Example 1. washer\_detector**

**Mixed system система OpenFB + forte**

The example demonstrates a system with different runtime environments:

- Python
- C++

In this example, the C++ runtime publishes messages via MQTT, while the Python runtime waits for messages and launches an image processing cycle to search for washers, their defects, and other objects (trash).

**Example 2. washer\_detector\_py**

**OpenFB Runtime**

The example implements detection of defective washers.

**Example 3. washer\_detector\_relay**

**OpenFB Runtime**

The example implements detection of defective washers. Detection of defects leads to switching of a USB relay, which switches the conveyor power line. In this example, monitoring of the PY\_RELAY\_CTRL block is available via OPC UA. Events and variables of the block are available for monitoring.

**Usage Nuances** 

You need to grant device control permissions to the user group that will run the runtime environment. Example:

\
SUBSYSTEM=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="05df", MODE:="0660", GROUP="dialout"

Write this line to a file (write only with administrator privileges): /etc/udev/rules.d/90-hidusb-relay.rules

Note! Systems have identical names, so when opening a new system, delete the previous one from the project tree.

**Preparation**

1. Download and install IDE FL (<https://it.severstal.com/products/oasu-tp/#downloads>)
1. Download repository  <https://gitverse.ru/rtsoft/OpenFB.git>
1. Launch the IDE
1. Import the system from the repository 4diac\_sys: demo\_whashers
1. Replace file paths for the Detector\_N\_Drawer block

**System requirements**

- python3.10
- python3-pip
- libgl1
- libxrender1
- libxext6
- libgl1-mesa-glx
- libqt5widgets5
- libqt5gui5
- libqt5core5a

**Python**

All required libraries are described in the file: **docker/requirements.txt**

