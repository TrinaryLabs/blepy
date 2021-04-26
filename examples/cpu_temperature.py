"""Example of how to create a Peripheral device/GATT Server"""

# Standard modules
import random

# Blepy module
import blepy

# Helper from bluezero
from bluezero import async_tools

# For temperature characteristic and descriptor:
# https://www.bluetooth.com/specifications/assigned-numbers/

class CPUMonitorPeripheral(blepy.Peripheral):
    
    def __init__(self, adapter_address):
        services = [CPUMonitorService(True)]
        super().__init__(services, adapter_address, local_name='CPU Monitor', appearance=1344)


class CPUMonitorService(blepy.Service):
    
    # Custom service UUID
    CPU_TMP_SRVC = '12341000-1234-1234-1234-123456789abc'
    
    def __init__(self, primary):
        super().__init__(self.CPU_TMP_SRVC, primary)   
        self.characteristics = [CPUMonitorCharacteristics.Temperature()]


class CPUMonitorCharacteristics:
    
    class Temperature(blepy.Characteristic):
        
        # Bluetooth SIG adopted UUID for Temperature characteristic
        CPU_TMP_CHRC = '2A6E'
        
        def __init__(self):
            super().__init__(self.CPU_TMP_CHRC)
            self.flags = ['read', 'notify']
            self.read_callback = self.read
            self.notify_callback = self.notify
            self.descriptors = [CPUMonitorDescriptors.Temperature()]
            
        def read(self):
            """
            Example read callback. Value returned needs to a list of bytes/integers
            in little endian format.
            This one does a mock reading CPU temperature callback.
            Return list of integer values.
            Bluetooth expects the values to be in little endian format and the
            temperature characteristic to be an sint16 (signed & 2 octets) and that
            is what dictates the values to be used in the int.to_bytes method call.
            :return: list of uint8 values
            """
            cpu_value = random.randrange(3200, 5310, 10) / 100
            return list(int(cpu_value * 100).to_bytes(2, byteorder='little', signed=True))
        
        
        def notify(self, notifying, characteristic):
            """
            Noitificaton callback example. In this case used to start a timer event
            which calls the update callback ever 2 seconds

            :param notifying: boolean for start or stop of notifications
            :param characteristic: The python object for this characteristic
            """
            if notifying:
                async_tools.add_timer_seconds(2, self._update_value, characteristic)
        
        
        def _update_value(self, characteristic):
            """
            Example of callback to send notifications

            :param characteristic:
            :return: boolean to indicate if timer should continue
            """
            # read/calculate new value.
            new_value = read_value()
            # Causes characteristic to be updated and send notification
            characteristic.set_value(new_value)
            # Return True to continue notifying. Return a False will stop notifications
            # Getting the value from the characteristic of if it is notifying
            return characteristic.is_notifying


class CPUMonitorDescriptors:
    
    class Temperature(blepy.Descriptor):
        
        # Bluetooth SIG adopted UUID for Characteristic Presentation Format
        CPU_FMT_DSCP = '2904'
        
        def __init__(self):
            super().__init__(self.CPU_FMT_DSCP)
            self.value = [0x0E, 0xFE, 0x2F, 0x27, 0x01, 0x00, 0x00]
            self.flags = ['read']


def main(adapter_address):

    # Create peripheral
    cpu_monitor = CPUMonitorPeripheral(adapter_address)
    
    # Publish peripheral and start event loop
    cpu_monitor.publish()


if __name__ == '__main__':
    main(blepy.Adapter.get_available_address()) 