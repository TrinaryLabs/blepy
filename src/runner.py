import dbus
import dbus.mainloop.glib
import bluez
from application import Application

try:
  from gi.repository import GLib
except ImportError:
  import lib as GLib

class Runner():

    def __init__(self, application):
        self.main = None
        self.application = application

    def _register_app_cb(self):
        print('GATT application registered')

    def _register_app_error_cb(self, error):
        print('Failed to register application: ' + str(error))
        self.main.quit()

    def _find_adapter(self, bus):
        remote_om = dbus.Interface(
            bus.get_object(bluez.constants.BLUEZ_SERVICE_NAME, '/'),
            bluez.constants.DBUS_OM_IFACE)

        objects = remote_om.GetManagedObjects()

        for o, props in objects.items():
            if bluez.constants.GATT_MANAGER_IFACE in props.keys():
                return o

        return None

    def start(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()

        adapter = self._find_adapter(bus)
        if not adapter:
            print('GattManager1 interface not found')
            return

        service_manager = dbus.Interface(
            bus.get_object(bluez.constants.BLUEZ_SERVICE_NAME, adapter),
            bluez.constants.GATT_MANAGER_IFACE)

        app = self.application(bus)

        self.main = GLib.MainLoop();

        print('Registering GATT application...')

        service_manager.RegisterApplication(app.get_path(), {},
                                            reply_handler=self._register_app_cb,
                                            error_handler=self._register_app_error_cb)

        self.main.run()

