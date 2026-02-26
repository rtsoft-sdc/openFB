# OpenFB AI Coding Assistant Instructions

## Project Overview
OpenFB is a **Python-based IEC 61499 function block runtime environment** for machine learning tasks, compatible with 4diac IDE. It executes function blocks (FBs) defined as XML type definitions (`.fbt`) with Python implementations (`.py`).

**Core architecture**: Messages flow through function block networks → FB execution engine → OPC-UA and 4diac-IDE integration.

## Critical Architecture Patterns

### Function Block Execution Model
- **Every FB has two files**: 
  - `.fbt` (XML): Interface definition (inputs, outputs, events)
  - `.py`: Implementation with required `schedule(event_name, event_value, *input_vars)` method
- **Key files**: [openfb/core/fb.py](openfb/core/fb.py), [openfb/core/configuration.py](openfb/core/configuration.py)
- **Threading model**: Each FB runs in its own thread; FB.schedule() is called for every event on the block
- **Hot-reload**: Uses [openfb/core/sniffer.py](openfb/core/sniffer.py) to watch `.py` files and reload FB code during runtime without restarting

### Manager & Configuration Hierarchy
- **Manager** ([openfb/core/manager.py](openfb/core/manager.py)): Parses 4diac XML commands, creates/destroys configurations
- **Configuration**: Represents a connected FB network, manages FB lifecycle
- **FB Thread**: Executes block logic, communicates via event queues
- Data flows: TCP input → Manager.parse_general() → Configuration.create_fb() → FB.schedule() → outputs

### OPC-UA Integration
- **Dual interface**: 4diac (port 61499, TCP) + OPC-UA (port 4840, OPC-UA protocol)
- **Type mapping**: [openfb/data_model_fboot/utils.py](openfb/data_model_fboot/utils.py) contains `UA_TYPES` dict mapping IEC types to OPC-UA types
- **Data model**: [openfb/resources/data_model.fboot](openfb/resources/data_model.fboot) defines OPC-UA node structure
- See [openfb/opc_ua/](openfb/opc_ua/) for client/server/handler implementations

## Developer Workflows

### Running the Application
```bash
# After installing dependencies (pip install -r requirements.txt)
python3 run.py                              # Default: 0.0.0.0:61499
python3 run.py -a 192.168.1.1 -p 9999     # Custom IP/port
python3 run.py -g                          # Enable self-organizing agent
python3 run.py -m 10 20                    # Enable monitoring (10 samples, 20s each)
python3 run.py -f path/to/config.fboot     # Load custom FBOOT file
```

### Testing
```bash
python run_tests.py               # All tests
python run_tests.py --events      # Event block tests only
python run_tests.py --convert     # Type conversion block tests
python run_tests.py --verbose     # Detailed output
```
- Tests use pytest; fixtures in [tests/conftest.py](tests/conftest.py)
- Test utilities in [tests/test_utils_py.py](tests/test_utils_py.py) provide `TestRunner` class for FB testing

### Building/Packaging
```bash
make install    # Setup with uv package manager
make whl        # Build Python wheel (dist/)
make deb        # Create .deb package for Linux
make clean      # Remove build artifacts
```

## Project-Specific Conventions

### Creating a New Function Block
1. **Create `.fbt` file** in [openfb/resources/function_blocks/](openfb/resources/function_blocks/): Define inputs/outputs/events in XML
2. **Create `.py` file** (same name): Implement class with `schedule(self, event_name, event_value, *input_vars)` returning tuple of output values
3. **Output tuple order** must match `.fbt` EventOutputs declaration order
4. Examples: [SLEEP.py](openfb/resources/function_blocks/MISCELLANEOUS/SLEEP.py), [PY_MQTT_SUB.py](openfb/resources/function_blocks/MISCELLANEOUS/PY_MQTT_SUB.py)

### Error Handling in FBs
- Try-catch in schedule() logs via `logging.error()` (see [openfb/core/fb.py](openfb/core/fb.py) line 55-70)
- TypeError → argument mismatch with `.fbt` declaration
- Generic exceptions → logs and stops FB thread

### Environment Configuration
- **Resource path**: Set `OPENFB_LOCAL_DIR` env var to override default resource folder ([openfb/core/main.py](openfb/core/main.py) line 11)
- **Logging**: File path `resources/error_list.log`, control via `-l {ERROR|WARN|INFO|DEBUG}` flag

## Key Dependencies & Integration Points
- **OPC-UA**: `python-opcua` (0.98.13+) for UA protocol
- **OpenCV**: Used by ML function blocks (camera, YOLO detection)
- **4diac IDE**: Sends FB network definitions as XML; expects responses via TCP
- **Shared memory**: `shared-memory-dict` (0.7.2+) for inter-process communication in distributed setups

## Important Implementation Details

### Variable Type System
- IEC 61131-3 types → Python native types (see utils.py `UA_TYPES` dict)
- Special handling: TIME → STRING, ANY → STRING (serialized)
- Type validation happens at OPC-UA layer, not in Python FBs

### Event-Driven Execution
- FBs **don't have main loops**; `schedule()` called only when an event arrives
- Events include: INIT, REQ, custom events defined in `.fbt`
- Multiple simultaneous events queued; each triggers separate schedule() call

### Monitoring & Anomaly Detection
- Enabled via `-m N T` flag: captures N behavioral samples, T seconds each
- Files written to `resources/monitoring/` (auto-cleared on new configuration)
- Uses data-model for tracking state changes

## Common Pitfalls to Avoid
- **Don't assume persistent state** across events unless explicitly managed (FB instances are recreated)
- **Schedule signature mismatch**: All inputs from `.fbt` must appear as parameters, in order
- **Return tuple length**: Must match number of EventOutputs in `.fbt` or TypeError occurs
- **Threading**: FBs are thread-safe (own thread), but shared resources need locks
- **Hot-reload bugs**: Changes to `.py` files are picked up, but old instances may still run briefly
