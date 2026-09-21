# Modbus and OPC UA Communication Modules for IEC 61499

This document describes the architecture and configuration of the client, server, and I/O function blocks (`BaseIO`).

---

## Modbus

### Architecture

The Modbus communication module consists of three components:

* **Connection manager (`MBUS8TCP` / `MBUSLAVE8TCP`)**: A client or server that supports up to 8 (by the ordinal number in the name for convenience; easy to modify by expanding the quantity) I/O blocks.
* **Communication layer (`ModbusChannel` / `ModbusChannelAdapter`)**: A wrapper around the `pymodbus` library that converts IEC data types (`QX`, `IX`, and others) into Modbus operations.
* **I/O blocks (`BaseIO`)**: Provide direct data read/write operations, timing control, and synchronous or asynchronous execution modes.

### 1. Configuring the `MBUS8TCP` Client

The block is initialized by the `MAP` event and operates as a Modbus TCP master.

* **Input parameters:**
  * `QI` (`BOOL`): `True` connects to the server and binds the blocks; `False` disconnects.
  * `PARAMS` (`STRING`): Connection parameters:
    * `Host` — the server IP address.
    * `Port` — the server port (default: `502`).
    * `Unit ID` — the device identifier (default: `1`).
    * `delay` — postponing the start moment by a certain number of mks, ms, s.
    * `mode` — the mode of the read operation (ind – asynchronous read mode, req – synchronous mode, upon receiving the REQ event).
    * `update` — update frequency, a number with the suffix ms, mks, hz, khz; the default is mks.
  * `IO0` ... `IO7`: String identifiers of the `BaseIO` blocks registered with the adapter.
* **Output parameters:**
  * `STATUS` (`STRING`): The current status (`CREATED`, `CONNECTED <ip>:<port>`, `CONNECTION FAILED`, or `DISABLED`).

e.g. `"{"host":"127.0.0.1:1502", "update":"500ms","id":"1"}"`

### 2. Configuring the `MBUSLAVE8TCP` Server

This block starts a Modbus TCP server in a background daemon thread and creates a local memory map. Configuration is performed in response to the `MAP` event.

* **Input parameters:**
  * `QI` (`BOOL`): `True` starts the server and allocates memory; `False` stops the server and sets the status to `Disabled`.
  * `PARAMS` (`STRING`): Connection parameters:
    * `Host` — the IP address (`0.0.0.0` for all interfaces or `127.0.0.1`).
    * `Port` — the port (`502` default).
    * `Unit ID` — the slave device identifier (default: `1`).
  * `IO0` ... `IO7`: Identifiers of the `BaseIO` blocks to register.
* **Memory configuration:**
  * The server allocates 65,536 elements for each of the four memory regions: `co` (Coils, `0x01`), `di` (Discrete Inputs, `0x01`), `hr` (Holding Registers, `0x01`), and `ir` (Input Registers, `0x01`).
* **Output parameters:**
  * `STATUS` (`STRING`): One of the following values: `Created`, `LISTENING on <host>:<port>`, `Disabled / Stopped`, or `ERROR: <text>`.

The PARAMS of the block are used exclusively to configure the modbus component, for example:
`"{"host":"127.0.0.1:1502", "id":"1"}"`

### 3. Configuring I/O Blocks (`BaseIO`)

Configure the blocks through the `PARAMS` parameter using the following format:

`"<Address_and_Type>, <Update_Interval>, <Delay>, <Mode>"`

например, `"{“addr”:”C22”, "update":"1000ms", "delay":"3s"}"`
#### Modbus Register Types

| Code | Register type | Access | Description |
| :---: | :--- | :---: | :--- |
| `c` | Coils | R/W | Read and write bits |
| `d` | Discrete Inputs | Read | Read-only bits |
| `h` | Holding Registers | R/W | Read and write 16-bit registers |
| `i` | Input Registers | Read | Read-only 16-bit registers |

> **Addressing example:** `с21` or `h10`. IEC 61499 data types are converted into the corresponding register operations automatically.

* **Timing parameters:**
  * `Update Interval` — the polling interval in seconds. When set to `0`, polling occurs on every cycle without restrictions.
  * `Delay` — the startup delay in seconds, used to prevent network load spikes.
* **Operating modes (`Mode`):**
  * `sync` (synchronous) — a read/write operation blocks the thread until the server responds or the request times out.
  * `ind` (asynchronous) — tasks are submitted to `THREAD_POOL` without blocking the main IEC 61499 cycle; the block returns the last known value.
* **Operation logic:**
  * **Client mode:** The blocks send requests over the network.
  * **Server mode:** The block uses `execute_read` to read data written by an external master to the `ModbusServerContext` memory map. It uses `execute_write` to update local cells for subsequent reading by the master.

---

## OPC UA

### Architecture

The OPC UA communication system consists of three layers:

* **Connection manager (`OPCUAC_8`)**: A client that supports up to eight I/O blocks and manages an asynchronous event loop in a daemon thread.
* **Communication layer (`OpcUaChannel` / `OpcUaChannelAdapter`)**: A wrapper around the `asyncua` library that converts data types, resolves `NodeId` and `BrowsePath` addresses, and manages subscriptions.
* **I/O blocks (`BaseIO`)**: Provide direct data read/write operations.

### 1. Configuring the `OPCUAC_8` Client

The block is initialized by a `MAP` event and operates as an OPC UA client.

* **Input parameters:**
  * `QI` (`BOOL`): `True` connects to the OPC UA server and starts the asynchronous thread; `False` stops the thread, terminates the connection, and sets the status to `Disabled`.
  * `PARAMS` (`STRING` / `JSON` / `DICT`): Connection parameters:
    * `url` — the server endpoint URL (default: `opc.tcp://127.0.0.1:4840`).
    * `mode` — the operating mode (`ind` for asynchronous subscriptions or `sync` for direct requests).
    * `poll_period` — the subscription/polling period in seconds (default: `0.1`).
    * `timeout` — the connection timeout in seconds (default: `5.0`).
  * `IO0` ... `IO7`: Identifiers of the `BaseIO` blocks registered with the adapter.
* **Output parameters:**
  * `STATUS` (`STRING`): The current status (`Created`, `CONNECTED to <url> [<mode> mode]`, `Disabled`, `STOPPED`, or `ERROR: <text>`).

### 2. Configuring I/O Blocks (`BaseIO`)

Configure the blocks through the `PARAMS` parameter, which specifies the OPC UA node address.

#### Addressing Methods

* **`BrowsePath`** (relative or complete path): `Objects/MyDevice/Temperature` or `0:Objects/2:MyDevice`.
* **`NodeId`** (node identifier): `,2:s=Path.To.MyVariable`.

> **Note:** Addresses are automatically resolved to actual `NodeId` values and cached on first access.

#### Data Type Mapping (IEC 61499 → `ua.VariantType`)

| IEC 61499 type | OPC UA variant type |
| :--- | :--- |
| `IX`, `QX` | `Boolean` |
| `IB`, `QB` | `Byte` |
| `IW`, `QW` | `UInt16` |
| `ID`, `QD` | `UInt32` |
| `IL`, `QL` | `UInt64` |
| `IR`, `QR` | `Float` |
| `ILR`, `QLR` | `Double` |
| `IStr`, `QStr`, `IWStr`, `QWStr` | `String` |

#### Operating Modes and Logic

* **`ind` (asynchronous):** An OPC UA `DataChange Notification` subscription is created. Values are read from the `SubscriptionHandler` cache without blocking the IEC 61499 event loop.
* **`sync` (synchronous):** Each read and write operation sends a direct request to the server through the event loop.
* **Operation logic:**
  * **Read (`execute_read`):** The block retrieves the current value from the subscription cache or performs a direct read from the server.
  * **Write (`execute_write`):** The block wraps the value in a `ua.Variant` object with the appropriate data type and writes it to the OPC UA server node.

