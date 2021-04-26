===============
Blepy
===============

.. _python-bluezero: https://github.com/ukBaz/python-bluezero
.. _BlueZ: http://www.bluez.org/

.. image:: https://img.shields.io/pypi/l/bluezero.svg
   :target: https://github.com/TrinaryLabs/blepy/blob/main/LICENSE
   :alt: MIT License
   
A class-based wrapper for `python-bluezero`_ peripheral functionalities.

About
====

The primary goal for this library is to make it easier and more clearer about how to implement Bluetooth low energy ``Peripherals``, including the associated ``Services``, ``Characteristics`` and ``Descriptors``. This is done by using a class-based wrapper for the `BlueZ`_ based `python-bluezero`_ package.

As seen in the figure below, a ``Service`` has one to many ``Characteristics`` and a ``Characteristic`` has (often) one to many ``Descriptors``, which is what this library is built to follow.

.. raw:: html

   <embed>
      <img src="https://github.com/TrinaryLabs/blepy/blob/development/docs/ble-overview.png?raw=true" width=500 alt="ble overview"/>
   </embed>

Getting Started
====

Usage
====

To use ``blepy`` in your project, simply import the whole package:

.. code-block:: python

   import blepy
|

Create unique BLE services by inheriting ``blepy.Service``, including associated ``characteristics``:

.. code-block:: python

   class ExampleService(blepy.Service):
      def __init__(self, primary):
         super().__init__(self, "UUID", primary)
         self.characteristics = [ExampleCharacteristic()]
|

Create unique BLE characteristics by inheriting ``blepy.Characteristic``, including associated ``descriptors``:

.. code-block:: python

   class ExampleCharacteristic(blepy.Characteristic):
      def __init__(self):
         super().__init__(self, "UUID")
         self.descriptors = [ExampleDescriptor()]
|

Create unique BLE descriptors by inheriting ``blepy.Descriptor``:

.. code-block:: python

   class ExampleDescriptor(blepy.Descriptor):
      def __init__(self):
         super().__init__(self, "UUID")

|

Create a new peripheral with included services by either using the ``blepy.Peripheral`` as it is:

.. code-block:: python
   
   # Initialize and publish the peripheral
   peripheral = blepy.Peripheral([ExampleService(True)], adapter_address, local_name='Peripheral', appearance=0)
   peripheral.publish()

... or by inherit from the ``blepy.Peripheral`` and create an unique ``peripheral``:

.. code-block:: python
   
   class ExamplePeripheral(blepy.Peripheral):
       def __init__(self, adapter_address):
           services = [ExampleService(True)]
           super().__init__(services, adapter_address, local_name='Peripheral', appearance=0)
   
   # Initialize and publish the peripheral
   peripheral = ExamplePeripheral(adapter_address)
   peripheral.publish()
           
Examples
====

GATT Server: `cpu-temperature.py`_
----------------------------------

.. _cpu-temperature.py: https://github.com/TrinaryLabs/blepy/blob/development/examples/cpu_temperature.py

