from jaydroid.utils import adb
from jaydroid.exceptions import DeviceNotConnectedError
from typing import Dict, List
class Apps:
    """App management operations for a connected Android device.

    Args:
        device (Device): The device instance.
    """

    def __init__(self, device):
        """Initialize the Apps manager with a device reference."""
        self._device = device

    def get_installed_apps(self) -> List[str]:
            """Return a list of third‑party packages installed on the device.
    
            Uses ``pm list packages -3`` to list installed packages and extracts the
            package names.
    
            Returns:
                list[str]: A list of package names installed by the user (third-
                party apps).
    
            Raises:
                DeviceNotConnectedError: If no device or emulator is connected.
            """
            if self._device.is_connected():
                result = adb('shell', 'pm', 'list', 'packages', '-3')
                app_list = result.stdout.splitlines()
    
                installed_apps = []
                for package in app_list:
                    _, app_name = package.split(':')
                    installed_apps.append(app_name)
    
                return installed_apps
            raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')


    def get_system_apps(self) -> List[str]:
        if self._device.is_connected():
            result = adb('shell', 'pm', 'list', 'packages', '-s')

            app_list = result.stdout.splitlines()
            system_apps = []

            for app in app_list:
                _, app_name = app.split(':')
                system_apps.append(app_name)

            return system_apps
        raise DeviceNotConnectedError('No device was detected, Connect to an android and try again.')



    def launch_app(self, package_name:str) -> Dict[str, str]:
        if self._device.is_connected():
            result = adb('shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1')
            lines = result.stdout.splitlines()

            response = {}
            for line in lines:
                key, value = line.split(': ')
                response[key] = value

            return response
        raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')


