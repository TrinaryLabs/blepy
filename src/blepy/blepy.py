from queue import Queue

# Bluezero modules
from bluezero import peripheral
from bluezero import device
from bluezero import adapter


class Adapter(adapter.Adapter):
    
    @staticmethod
    def get_available_address():
        return list(adapter.Adapter.available())[0].address


class Service:

    def __init__(self, uuid, primary):
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        

class Characteristic:
    
    def __init__(self, uuid, event_queue=None):
        self.uuid = uuid
        self.event_queue = event_queue
        self.notifying = False
        self.value = []
        self.flags = []
        self.read_callback = None
        self.write_callback = None
        self.notify_callback = None
        self.descriptors = []
 
class Descriptor:
    
    def __init__(self, uuid):
        self.uuid = uuid
        self.value = []
        self.flags = []


class Peripheral(peripheral.Peripheral):
    
    def __init__(self, services, adapter_address, local_name=None, appearance=None):
        super().__init__(adapter_address, local_name, appearance)
        self.on_connect = self._on_connect_callback
        self.on_disconnect = self._on_disconnect_callback
        
        for srv_id, srv_item in enumerate(services, start = 1):
            self._add_service(srv_item, srv_id)
            for chr_id, chr_item in enumerate(srv_item.characteristics, start = 1):
                self._add_characteristic(chr_item, chr_id, srv_id)
                for dsc_id, dsc_item in enumerate(chr_item.descriptors, start = 1):
                    self._add_descriptor(dsc_item, dsc_id, srv_id, chr_id)
            
            
    def _on_connect_callback(self, device):
        print("Connected to " + str(device.address))
        
        
    def _on_disconnect_callback(self, adapter_address, device_address):
        print("Disconnected from " + device_address)                  
        
        
    def _add_service(self, service, index):
        self.add_service(
            srv_id  = index,
            uuid    = service.uuid,
            primary = True
        )
    
    
    def _add_characteristic(self, characteristic, index, srv_id):
        self.add_characteristic(
            srv_id          = srv_id,
            chr_id          = index,
            uuid            = characteristic.uuid,
            value           = characteristic.value,
            notifying       = characteristic.notifying,
            flags           = characteristic.flags,
            read_callback   = characteristic.read_callback,
            write_callback  = characteristic.write_callback,
            notify_callback = characteristic.notify_callback
        )
    
    
    def _add_descriptor(self, descriptor, index, srv_id, chr_id):
        self.add_descriptor(
            srv_id = srv_id,
            chr_id = chr_id,
            dsc_id = index,
            uuid   = descriptor.uuid,
            value  = descriptor.value,
            flags  = descriptor.flags
        )