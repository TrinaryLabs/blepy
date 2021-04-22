from runner import Runner
from application import Application
from service import Service
from characteristic import Characteristic



class ExampleService(Service):
    UUID = '0000180d-0000-1000-8000-00805f9b34fb'
    
    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(ExampleCharacteristic(bus, 0, self))
        

class ExampleCharacteristic(Characteristic):
    UUID = '00002a37-0000-1000-8000-00805f9b34fb'
    
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, self.UUID, ['notify'], service)
    
    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True

    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False

class ExampleApplication(Application):
    
    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(ExampleService(bus, 0))
              
              
                        
def main():
    runner = Runner(ExampleApplication)
    runner.start();

if __name__ == '__main__':
    main()