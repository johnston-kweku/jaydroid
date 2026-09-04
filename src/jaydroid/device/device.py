from typing import Optional

from ..utils import adb
from ..exceptions import DeviceNotFoundError, DeviceNotConnectedError
from .apps import Apps
from .system import System
from .info import Info

class Device:
    """
    Manage connection state and display dimensions for an Android device.

    Provides a connection interface to Android devices via ADB and aggregates
    device information, app management, and system operations.

    Create a ``Device`` instance before using gesture helpers, then call
    :meth:`connect` to verify that an ADB device is available and load its
    display dimensions.

    Attributes:
        apps (Apps): App management operations.
        system (System): System status and control operations.
        info (Info): Device information queries.

    All methods raise ``DeviceNotConnectedError`` when a connected device is
    required but none is available.
    """

    def __init__(self) -> None:
        self._width: Optional[int] = None
        self._height: Optional[int] = None
        self.apps = Apps(self)
        self.system = System(self)
        self.info = Info(self)

    def connect(self) -> None:
        """Connect to the first available ADB device and load its display size.

        Queries ADB for connected devices and retrieves the screen dimensions
        of the first connected device.

        Raises:
            DeviceNotFoundError: If no device or emulator is available through ADB.
        """
        result = adb('devices')
        devices = result.stdout.splitlines()
        _ = devices.pop(0)
        devices = [item for item in devices if item]
        if not devices:
            raise DeviceNotFoundError('Error: No device(s) connected')

        self.setup()


    @property
    def width(self) -> int:
        """The connected device's display width in pixels.

        Returns:
            int: Display width in pixels.

        Raises:
            DeviceNotConnectedError: If :meth:`connect` has not completed.
        """
        if self._width is not None:
            return self._width
        raise DeviceNotConnectedError('Error: No device/emulator connected. Did you forget to run connect()? See documentation')


    @property
    def height(self) -> int:
        """The connected device's display height in pixels.

        Returns:
            int: Display height in pixels.

        Raises:
            DeviceNotConnectedError: If :meth:`connect` has not completed.
        """
        if self._height is not None:
            return self._height
        raise DeviceNotConnectedError('Error: No device/emulator connected. Did you forget to run connect()? See documentation')



    def setup(self) -> None:
        """Refresh and store the device display width and height.

        Queries the device's current screen dimensions and updates internal
        width and height attributes.

        Raises:
            RuntimeError: If the device does not return a recognized display
                resolution.
        """
        self._width, self._height = self.get_screen_size()

    def get_screen_size(self) -> tuple[int, int]:
        """Return the physical display size as ``(width, height)``.

        Queries the device via ADB to get the current physical display
        dimensions.

        Returns:
            tuple[int, int]: A tuple of (width, height) in pixels.

        Raises:
            RuntimeError: If ADB does not return a ``Physical size: WIDTHxHEIGHT``
                line.
        """
        result = adb('shell', 'wm', 'size')
        screen_info = result.stdout.splitlines()
        for info in screen_info:
            if info.startswith('Physical'):
                screen = info
                break
        else:
            raise RuntimeError('Connected device did not return a recognized resolution format.\
                                You can use swipe() to enter custom coordinates')
        _, resolution = screen.split(':')
        resolution = resolution.strip()
        width, height = resolution.split('x')
        return int(width), int(height)


    def is_connected(self) -> bool:
        """Return whether an Android device or emulator is connected through ADB.

        Returns:
            bool: ``True`` when at least one device is connected; otherwise,
                ``False``.
        """
        result = adb('devices')
        devices = result.stdout.splitlines()
        _ = devices.pop(0)
        devices = [item for item in devices if item]
        return bool(devices)

    
    
    def get_installed_apps(self):
        """Return a list of third-party packages installed on the device.

        Delegates to :meth:`Apps.get_installed_apps`.

        Returns:
            list[str]: A list of installed third-party app package names.

        Raises:
            DeviceNotConnectedError: If no device is connected.
        """
        return self.apps.get_installed_apps()


    def get_system_apps(self):
        return self.apps.get_system_apps()

    def battery_info(self):
        """Return battery information reported by the connected device.

        Delegates to :meth:`System.battery_info`.

        Returns:
            dict: Battery properties from the device.

        Raises:
            DeviceNotConnectedError: If no device is connected.
        """
        return self.system.battery_info()

    def wifi_status(self):
        """Return the Wi-Fi state for the connected device.

        Delegates to :meth:`System.wifi_status`.

        Returns:
            str: One of ``'On'``, ``'Off'``, or ``'Unknown'``.

        Raises:
            DeviceNotConnectedError: If no device is connected.
        """
        return self.system.wifi_status()

    def storage_space_info(self):
        """Return filesystem usage information for the device data partition.

        Delegates to :meth:`System.storage_space_info`.

        Returns:
            dict: A mapping of column name to value for the ``/data`` mount.

        Raises:
            DeviceNotConnectedError: If no device is connected.
        """
        return self.system.storage_space_info()

    def get_device_ip(self):
        """Return the device's local Wi-Fi IP address.

        Delegates to :meth:`System.get_device_ip`.

        Returns:
            str: The device's local Wi-Fi IP address.

        Raises:
            DeviceNotConnectedError: If no device is connected.
            WifiNotConnectedError: If Wi-Fi is not enabled.
        """
        return self.system.get_device_ip()

    def reboot(self):
        """Reboot the connected device.

        Delegates to :meth:`System.reboot`.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Raises:
            DeviceNotConnectedError: If no device is connected.
        """
        return self.system.reboot()

    def get_android_version(self):
        """Return the Android release version of the connected device.

        Delegates to :meth:`Info.get_android_version`.

        Returns:
            str: The Android release version.

        Raises:
            DeviceNotConnectedError: If no device is connected.
        """
        return self.info.get_android_version()

    def get_device_model(self):
        """Return the device model name reported by the connected device.

        Delegates to :meth:`Info.get_device_model`.

        Returns:
            str: The device model name.

        Raises:
            DeviceNotConnectedError: If no device is connected.
        """
        return self.info.get_device_model()


    def launch_app(self, package_name):
        return self.apps.launch_app(package_name)

    def force_stop_app(self, package_name):
        return self.apps.force_stop_app(package_name)
