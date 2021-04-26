# Blepy module
import blepy


class UARTPeripheral(blepy.Peripheral):
    # Using single-element list to reference immutable object 'tx_obj':
    tx_obj = [None]
    
    def __init__(self, adapter_address):
        services = [UARTService(True, self.tx_obj)]
        super().__init__(services, adapter_address, local_name='BLE UART')


class UARTService(blepy.Service):
    UART_SERVICE = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
    
    def __init__(self, primary, tx_obj):
        super().__init__(self.UART_SERVICE, primary)   
        self.characteristics = [
            UARTCharacteristics.RX(tx_obj),
            UARTCharacteristics.TX(tx_obj)
        ]
        

class UARTCharacteristics:
    class RX(blepy.Characteristic):
        RX_CHARACTERISTIC = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        
        def __init__(self, tx_obj):
            super().__init__(self.RX_CHARACTERISTIC)
            self.flags = ['write', 'write-without-response']
            self.write_callback = self.write
            self.tx_obj = tx_obj
        
        def write(self, value, options):
            print('Raw bytes:', value)
            print('With options:', options)
            print('Text value:', bytes(value).decode('utf-8'))
            self._update_tx(value)
            
        def _update_tx(self, value):
            if self.tx_obj[0]:
                print("Sending")
                self.tx_obj[0].set_value(value)
            
    class TX(blepy.Characteristic):  
        TX_CHARACTERISTIC = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        
        def __init__(self, tx_obj):
            super().__init__(self.TX_CHARACTERISTIC)
            self.flags = ['notify']
            self.notify_callback = self.notify
            self.tx_obj = tx_obj
            
        def notify(self, notifying, characteristic):
            if notifying:
                self.tx_obj[0] = characteristic
            else:
                self.tx_obj[0] = None
            
            
def main(adapter_address):
    # Create peripheral
    uart = UARTPeripheral(adapter_address)
    
    # Publish peripheral and start event loop
    uart.publish()


if __name__ == '__main__':
    main(blepy.Adapter.get_available_address()) 
