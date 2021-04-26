# Blepy

[![MIT-shield](https://img.shields.io/pypi/l/bluezero.svg)](https://github.com/TrinaryLabs/blepy/blob/main/LICENSE)

[python-bluezero]: https://github.com/ukBaz/python-bluezero.
[BlueZ]: http://www.bluez.org/

A class-based wrapper for the peripheral functionalities provided by the library 
[python-bluezero].

## About

The primary goal of this library is to make it easier and more clearer about how to implement Bluetooth low energy ``Peripherals``, 
including the associated ``Services``, ``Characteristics`` and ``Descriptors``. This is done by using a class-based wrapper for the 
[BlueZ] based [python-bluezero] library.

As seen in the figure below, a ``Service`` has one to many ``Characteristics`` and a ``Characteristic`` has (often) one to many 
``Descriptors``, which is what this library is built to follow.

<img src="https://github.com/TrinaryLabs/blepy/blob/development/docs/ble-overview.png?raw=true" alt="BLE overview" width="550"/>

## Usage

### Import ``blepy``
To use ``blepy`` in your project, simply import the whole package:

```python
import blepy
```
### Service

Create unique BLE services by inheriting ``blepy.Service``, including associated ``characteristics``:

```python
class ExampleService(blepy.Service):
   def __init__(self, primary):
      super().__init__(self, "UUID", primary)
      self.characteristics = [ExampleCharacteristic()]
```
### Characteristic

Create unique BLE characteristics by inheriting ``blepy.Characteristic``, including associated ``descriptors``:

```python
class ExampleCharacteristic(blepy.Characteristic):
   def __init__(self):
      super().__init__(self, "UUID")
      self.descriptors = [ExampleDescriptor()]     
```
### Descriptor

Create unique BLE descriptors by inheriting ``blepy.Descriptor``:

```python
class ExampleDescriptor(blepy.Descriptor):
   def __init__(self):
      super().__init__(self, "UUID")
```
### Peripheral

Create a new peripheral with included services by either using the ``blepy.Peripheral`` as it is:

```python  
# Initialize and publish the peripheral
peripheral = blepy.Peripheral([ExampleService(True)], adapter_address, local_name='Peripheral', appearance=0)
peripheral.publish()
```

... or by inherit from the ``blepy.Peripheral`` and create an unique ``peripheral``:

```python  
class ExamplePeripheral(blepy.Peripheral):
    def __init__(self, adapter_address):
        services = [ExampleService(True)]
        super().__init__(services, adapter_address, local_name='Peripheral', appearance=0)

# Initialize and publish the peripheral
peripheral = ExamplePeripheral(adapter_address)
peripheral.publish()
```
## Examples

### (GATT Server) [cpu-temperature.py](https://github.com/TrinaryLabs/blepy/blob/main/examples/cpu_temperature.py) 
This example transmits (randomly generated) temperature values of the CPU over a single characteristic. 
Values are only updated when notification are switched on.

### (UART) [ble_uart.py](https://github.com/TrinaryLabs/blepy/blob/main/examples/ble_uart.py) 
This example simulates a basic UART connection over two lines, TXD and RXD.

It is based on a proprietary UART service specification by Nordic Semiconductors. 
Data sent to and from this service can be viewed using the nRF UART apps from Nordic Semiconductors for Android and iOS.
