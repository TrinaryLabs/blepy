import dbus
import dbus.service
import bluez


class Descriptor(dbus.service.Object):

    def __init__(self, bus, index, uuid, flags, characteristic):
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.chrc = characteristic
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
            bluez.constants.GATT_DESC_IFACE: {
                'Characteristic': self.chrc.get_path(),
                'UUID': self.uuid,
                'Flags': self.flags,
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(bluez.constants.DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != bluez.constants.GATT_DESC_IFACE:
            raise bluez.exceptions.InvalidArgsException()

        return self.get_properties()[bluez.constants.GATT_DESC_IFACE]

    @dbus.service.method(bluez.constants.GATT_DESC_IFACE,
                        in_signature='a{sv}',
                        out_signature='ay')
    def ReadValue(self, options):
        print ('Default ReadValue called, returning error')
        raise bluez.exceptions.NotSupportedException()

    @dbus.service.method(bluez.constants.GATT_DESC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        print('Default WriteValue called, returning error')
        raise bluez.exceptions.NotSupportedException()