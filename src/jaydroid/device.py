from .utils import adb
from .exceptions import DeviceNotFoundError, DeviceNotConnectedError, WifiNotConnectedError

class Device:
    """
    Manage connection state and display dimensions for an Android device.

    Create a ``Device`` instance before using gesture helpers, then call
    :meth:`connect` to verify that an ADB device is available and load its
    display dimensions.

    Device information helpers query the connected device through ADB and
    raise ``DeviceNotConnectedError`` when a connection is required but absent.
    """

    def __init__(self):
        self._width = None
        self._height = None

    def connect(self):
        """Connect to the first available ADB device and load its display size.

        Raises:
            DeviceNotFoundError: If no device or emulator is available through
                ADB.
        """
        result = adb('devices')
        devices = result.stdout.splitlines()
        _ = devices.pop(0)
        devices = [item for item in devices if item]
        if not devices:
            raise DeviceNotFoundError('Error: No device(s) connected')

        self.setup()


    @property
    def width(self):
        """The connected device's display width in pixels.

        Raises:
            DeviceNotConnectedError: If :meth:`connect` has not completed.
        """
        if self._width is not None:
            return self._width
        raise DeviceNotConnectedError('Error: No device/emulator connected. Did you forget to run connect()? See documentation')


    @property
    def height(self):
        """The connected device's display height in pixels.

        Raises:
            DeviceNotConnectedError: If :meth:`connect` has not completed.
        """
        if self._height is not None:
            return self._height
        raise DeviceNotConnectedError('Error: No device/emulator connected. Did you forget to run connect()? See documentation')



    def setup(self):
        """Refresh and store the device display width and height.

        Raises:
            RuntimeError: If the device does not return a recognized display
                resolution.
        """
        self._width, self._height = self.get_screen_size()

    def get_screen_size(self):
        """Return the physical display size as ``(width, height)``.

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


    def is_connected(self):
        """Return whether an Android device or emulator is connected through ADB.

        Returns:
            bool: ``True`` when at least one device is connected; otherwise,
                ``False``.
        """
        result = adb('devices')
        devices = result.stdout.splitlines()
        header = devices.pop(0)
        devices = [item for item in devices if item]
        return bool(devices)

    def get_android_version(self):
        """Return the Android release version of the connected device.

        Returns:
            str: The Android release version reported by ADB.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self.is_connected():
            result =  adb('shell', 'getprop', 'ro.build.version.release')
            android_version = result.stdout.strip()
            return android_version
        error = 'No device was detected. Connect an android device and try again.'
        raise DeviceNotConnectedError(error)

    def battery_info(self):
        """Return battery information reported by the connected device.

        Returns:
            dict: Battery properties parsed from ``adb shell dumpsys battery``.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self.is_connected():
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

    def wifi_status(self):
        """Return the Wi‑Fi state for the connected device.

        Queries Android settings via ADB and maps the numeric state to a human-
        readable string.

        Returns:
            str: One of ``'On'``, ``'Off'``, or ``'Unknown'`` when the setting
            cannot be interpreted.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self.is_connected():
            result = adb('shell', 'settings', 'get', 'global', 'wifi_on')
            values = {
                '0' : 'Off',
                '1' : 'On'
            }
            status_code = result.stdout.strip()

            return values.get(status_code, 'Unknown')
        raise DeviceNotConnectedError('No device was detected. Connect an android device and try again.')
        


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
        if self.is_connected():
            result = adb('shell', 'pm', 'list', 'packages', '-3')
            app_list = result.stdout
            packages = app_list.splitlines()

            installed_apps = []
            for package in packages:
                _, app_name = package.split(':')
                installed_apps.append(app_name)

            return installed_apps
        raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')


    def storage_space_info(self):
        """Return filesystem usage information for the device data partition.

        Calls ``df -h /data`` on the device and returns a dictionary mapping the
        reported header fields (e.g. ``Filesystem``, ``Size``, ``Used``,
        ``Available``, ``Use%``, ``Mounted on``) to their corresponding values.

        Returns:
            dict: A mapping of column name to value for the ``/data`` mount.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self.is_connected():
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

    def get_device_model(self):
        """Return the device model name reported by the connected device.

        Returns:
            str: The device model name reported by ADB.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self.is_connected():
            result = adb('shell', 'getprop', 'ro.product.model')
            device_model = result.stdout.strip()
            return device_model
        raise DeviceNotConnectedError('No device was detected. Connect an android and try again.')

    def get_device_ip(self):
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

    
