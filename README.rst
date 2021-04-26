===============
Blepy
===============

.. image:: https://img.shields.io/pypi/l/bluezero.svg
   :target: https://github.com/TrinaryLabs/blepy/blob/main/LICENSE
   :alt: MIT License
   
A class-based wrapper for `python-bluezero`_ peripheral functionalities.

.. _python-bluezero: https://github.com/ukBaz/python-bluezero

About
====

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
           super().__init__(services, adapter_address, local_name='BLE UART', appearance=0)
   
   # Initialize and publish the peripheral
   peripheral = ExamplePeripheral(adapter_address)
   peripheral.publish()
           
Examples
====

GATT Server: `cpu-temperature.py`_
----------------------------------

.. _cpu-temperature.py: https://github.com/

