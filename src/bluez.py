import dbus
import dbus.exceptions

from utils.recursivenamespace import RecursiveNamespace

constants = RecursiveNamespace()
constants.BLUEZ_SERVICE_NAME  = 'org.bluez'
constants.GATT_MANAGER_IFACE  = 'org.bluez.GattManager1'
constants.DBUS_OM_IFACE       = 'org.freedesktop.DBus.ObjectManager'
constants.DBUS_PROP_IFACE     = 'org.freedesktop.DBus.Properties'
constants.GATT_SERVICE_IFACE  = 'org.bluez.GattService1'
constants.GATT_CHRC_IFACE     = 'org.bluez.GattCharacteristic1'
constants.GATT_DESC_IFACE     = 'org.bluez.GattDescriptor1'


class _InvalidArgsException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.freedesktop.DBus.Error.InvalidArgs'

class _NotSupportedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotSupported'

class _NotPermittedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.NotPermitted'

class _InvalidValueLengthException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.InvalidValueLength'

class _FailedException(dbus.exceptions.DBusException):
    _dbus_error_name = 'org.bluez.Error.Failed'


exceptions = RecursiveNamespace()
exceptions.InvalidArgsException         = _InvalidArgsException
exceptions._NotSupportedException       = _NotSupportedException
exceptions._NotPermittedException       = _NotPermittedException
exceptions._InvalidValueLengthException = _InvalidValueLengthException
exceptions._FailedException             = _FailedException