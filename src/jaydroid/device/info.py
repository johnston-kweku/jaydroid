from ..utils import adb
from ..exceptions import DeviceNotConnectedError


class Info:
    """Device information queries for a connected Android device.

    Args:
        device (Device): The device instance.
    """

    def __init__(self, device):
        """Initialize the Info manager with a device reference."""
        self._device = device

    def get_device_model(self):
        """Return the device model name reported by the connected device.

        Returns:
            str: The device model name reported by ADB.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self._device.is_connected():
            result = adb('shell', 'getprop', 'ro.product.model')
            device_model = result.stdout.strip()
            return device_model
        raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')


    def get_android_version(self):
            """Return the Android release version of the connected device.
    
            Returns:
                str: The Android release version reported by ADB.
    
            Raises:
                DeviceNotConnectedError: If no device or emulator is connected.
            """
            if self._device.is_connected():
                result =  adb('shell', 'getprop', 'ro.build.version.release')
                android_version = result.stdout.strip()
                return android_version
            error = 'No device was detected. Connect an android device and try again.'
            raise DeviceNotConnectedError(error)
    