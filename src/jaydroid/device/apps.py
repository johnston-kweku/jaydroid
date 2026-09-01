from jaydroid.utils import adb
from jaydroid.exceptions import DeviceNotConnectedError

class Apps:
    """App management operations for a connected Android device.

    Args:
        device (Device): The device instance.
    """

    def __init__(self, device):
        """Initialize the Apps manager with a device reference."""
        self._device = device

    def get_installed_apps(self):
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
                app_list = result.stdout
                packages = app_list.splitlines()
    
                installed_apps = []
                for package in packages:
                    _, app_name = package.split(':')
                    installed_apps.append(app_name)
    
                return installed_apps
            raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')
    