import dbus
import dbus.service
import bluez


class Characteristic(dbus.service.Object):

    def __init__(self, bus, index, uuid, flags, service):
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
            bluez.bluez.GATT_CHRC_IFACE: {
                'Service': self.service.get_path(),
                'UUID': self.uuid,
                'Flags': self.flags,
                'Descriptors': dbus.Array(
                        self.get_descriptor_paths(),
                        signature='o')
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_descriptor(self, descriptor):
        self.descriptors.append(descriptor)

    def get_descriptor_paths(self):
        result = []
        for desc in self.descriptors:
            result.append(desc.get_path())
        return result

    def get_descriptors(self):
        return self.descriptors

    @dbus.service.method(bluez.constants.DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != bluez.constants.GATT_CHRC_IFACE:
            raise bluez.exceptions.InvalidArgsException()

        return self.get_properties()[bluez.constants.GATT_CHRC_IFACE]

    @dbus.service.method(bluez.constants.GATT_CHRC_IFACE,
                        in_signature='a{sv}',
                        out_signature='ay')
    def ReadValue(self, options):
        print('Default ReadValue called, returning error')
        raise bluez.exceptions.NotSupportedException()

    @dbus.service.method(bluez.constants.GATT_CHRC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        print('Default WriteValue called, returning error')
        raise bluez.exceptions.NotSupportedException()

    @dbus.service.method(bluez.constants.GATT_CHRC_IFACE)
    def StartNotify(self):
        print('Default StartNotify called, returning error')
        raise bluez.exceptions.NotSupportedException()

    @dbus.service.method(bluez.constants.GATT_CHRC_IFACE)
    def StopNotify(self):
        print('Default StopNotify called, returning error')
        raise bluez.exceptions.NotSupportedException()

    @dbus.service.signal(bluez.constants.DBUS_PROP_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed, invalidated):
        pass