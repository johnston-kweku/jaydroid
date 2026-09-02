from ..utils import adb
from ..exceptions import DeviceNotConnectedError, WifiNotConnectedError
from typing import Dict

class System:
    """System status and control operations for a connected Android device.

    Args:
        device (Device): The device instance.
    """

    def __init__(self, device):
        """Initialize the System manager with a device reference."""
        self._device = device

    def battery_info(self) -> Dict[str, str]:
            """Return battery information reported by the connected device.
    
            Returns:
                dict: Battery properties parsed from ``adb shell dumpsys battery``.
    
            Raises:
                DeviceNotConnectedError: If no device or emulator is connected.
            """
            if self._device.is_connected():
                result = adb('shell', 'dumpsys', 'battery')
                info = result.stdout
                info = info.splitlines()
                info.pop(0)
                info = [line.strip() for line in info if line.count(':') == 1]
    
                battery_information = {}
                for line in info:
                    key, value = line.split(':')
                    key, value = key.strip(), value.strip()
    
                    battery_information[key] = value
    
                return battery_information
            error = 'No device was detected. Connect an android device and try again.'
            raise DeviceNotConnectedError(error)


    def wifi_status(self) -> str:
            """Return the Wi‑Fi state for the connected device.
    
            Queries Android settings via ADB and maps the numeric state to a human-
            readable string.
    
            Returns:
                str: One of ``'On'``, ``'Off'``, or ``'Unknown'`` when the setting
                cannot be interpreted.
    
            Raises:
                DeviceNotConnectedError: If no device or emulator is connected.
            """
            if self._device.is_connected():
                result = adb('shell', 'settings', 'get', 'global', 'wifi_on')
                values = {
                    '0' : 'Off',
                    '1' : 'On'
                }
                status_code = result.stdout.strip()
    
                return values.get(status_code, 'Unknown')
            raise DeviceNotConnectedError('No device was detected. Connect an android device and try again.')
            

    def storage_space_info(self) -> Dict[str, str]:
            """Return filesystem usage information for the device data partition.
    
            Calls ``df -h /data`` on the device and returns a dictionary mapping the
            reported header fields (e.g. ``Filesystem``, ``Size``, ``Used``,
            ``Available``, ``Use%``, ``Mounted on``) to their corresponding values.
    
            Returns:
                dict: A mapping of column name to value for the ``/data`` mount.
    
            Raises:
                DeviceNotConnectedError: If no device or emulator is connected.
            """
            if self._device.is_connected():
                result = adb('shell', 'df', '-h', '/data')
                storage_info = result.stdout
                info = storage_info.splitlines()
                header = info[0]
                header = header.split()
                data = info[1]
                data = data.split()
                storage_dict = dict(zip(header, data))
                return storage_dict
            raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')


    
    def get_device_ip(self) -> str:
        """Return the device's local Wi-Fi IP address.

        Queries the device's routing table via ADB to extract the IP address
        assigned to the Wi-Fi interface (wlan0).

        Returns:
            str: The device's local Wi-Fi IP address.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
            WifiNotConnectedError: If Wi-Fi is not currently enabled on the
                device.
        """
        if self.is_connected():
            if self.wifi_status() == 'On':
                result = adb('shell', 'ip', 'route')

                lines = result.stdout
                lines = lines.splitlines()
                for line in lines:
                    if 'wlan' in line:
                        _, ip_addr = line.split(' src ')
                        return ip_addr.strip()
            raise WifiNotConnectedError('Wifi is not connected. Please connect wifi and try again.')
        raise DeviceNotConnectedError('No device was detected. Connect an android and try again')



    def reboot(self) -> None:
        """Reboot the connected device.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self.is_connected():
            adb('reboot')
            return
        raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')
