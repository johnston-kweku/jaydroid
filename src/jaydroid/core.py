r"""
Utilities for sending Android Debug Bridge (ADB) input commands.

The connected Android device must have developer options and USB debugging
enabled. Most operations return the :class:`subprocess.CompletedProcess`
instance produced by :func:`subprocess.run`, allowing callers to inspect the
command's output and return code.
"""


import subprocess, time
from .exceptions import DeviceNotFoundError, DeviceNotConnectedError, AdbCommandError


class Device:
    """
    Manage connection state and display dimensions for an Android device.

    Create a ``Device`` instance before using gesture helpers, then call
    :meth:`connect` to verify that an ADB device is available and load its
    display dimensions.
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
        header = devices.pop(0)
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
        """Refresh and store the device display width and height."""
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
        text, resolution = screen.split(':')
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
            info = [line.strip() for line in info]

            battery_information = {}
            for line in info:
                key, value = line.split(':')
                key, value = key.strip(), value.strip()

                battery_information[key] = value

            return battery_information
        error = 'No device was detected. Connect an android device and try again.'
        raise DeviceNotConnectedError(error)

def adb(*args, **kwargs):
    """Run an ADB command and return its completed-process result.

    Args:
        *args (str): Arguments passed to the ``adb`` executable.
        **kwargs: Additional keyword arguments passed to
            :func:`subprocess.run`. Output is captured and decoded as text by
            default.
        delay (int | float): Seconds to wait after the command completes.
            Defaults to ``0``.

    Returns:
        subprocess.CompletedProcess: The result of the ADB command.
    """
    kwargs.setdefault('capture_output', True)
    kwargs.setdefault('text', True)
    delay_value = kwargs.pop('delay', 0)
    
    result =  subprocess.run(
        ['adb', *args],
        **kwargs
    )

    if result.returncode != 0:
        raise AdbCommandError(result.stderr)
    time.sleep(delay_value)
    return result





class Button:
    """
    Methods for simulating common Android hardware and navigation buttons.

    ADB must be installed and available on ``PATH``, and a device or emulator
    must be connected before calling these methods.

    Each button method accepts ``delay`` in seconds and waits after its ADB
    action completes. The default delay is ``0``.
    """
    def power(self, delay=0):
        """
        Toggle the device's screen with a power-button press.

        The screen is turned on when it is off and turned off when it is on.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """

        return adb('shell', 'input', 'keyevent', '26', delay=delay)

    def volume_up(self, delay=0):
        """
        Increase the device's system volume by one default increment.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '24', delay=delay)

    def volume_down(self, delay=0):
        """
        Decrease the device's system volume by one default increment.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '25', delay=delay)

    def home(self, delay=0):
        """
        Navigate to the device home screen.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '3', delay=delay)

    def back(self, delay=0):
        """
        Navigate back one step in the current Android interface.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '4', delay=delay)
    
    def recent_apps(self, delay=0):
        """
        Open the Android recent-apps view.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '187', delay=delay)

    def menu(self, delay=0):
        """
        Send the Android menu-button key event.

        The effect depends on the active application and Android version.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '82', delay=delay)

    def wake(self, delay=0):
        """
        Wake the device's screen if it is off.

        This has no effect when the device is already awake.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '224', delay=delay)

    def sleep(self, delay=0):
        """
        Put the device's screen to sleep.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '223', delay=delay)


class Screen:
    """Methods for capturing screenshots and recording the device screen.

    Each method accepts ``delay`` in seconds and waits after its ADB action
    completes. For methods that run multiple commands, the delay is applied
    after each command. The default delay is ``0``.
    """

    def capture(self, delay=0):
        """
        Send the Android screenshot key event.

        This method does not save or pull an image file. Use :meth:`screenshot`
        to capture the screen to a file.

        Note:
            This key event is less universally reliable across OEM skins than
            calling :meth:`screenshot` directly.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the capture completes.
                Defaults to ``0``.
        """

        return adb('shell', 'input', 'keyevent', '120', delay=delay)


    def screenshot(self, filename=None, pull=False, delay=0):
        """
        Save a screenshot on the connected device.

        Args:
            filename (str | None): Name of the image file on the device.
                Defaults to ``'screenshot.png'``. The file is saved under
                ``/sdcard/``.
            pull (bool): If ``True``, copy the screenshot to the current local
                directory after capturing it. Defaults to ``False``.
            delay (int | float): Seconds to wait after each ADB command.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess: The result of ``adb pull`` when
                ``pull`` is ``True``; otherwise, the result of the capture
                command.
        """
        if not filename:
            filename = 'screenshot.png'
        remote_path = f'/sdcard/{filename}'

        res_capture = adb('shell', 'screencap', '-p', remote_path, delay=delay)

        if pull:
            res_pull = adb('pull', remote_path, check=True, delay=delay)
            return res_pull

        return res_capture


    def screenrecord(self, filename=None, pull=False, duration=10, delay=0):
        """
        Record the device screen to an MP4 file.

        Args:
            filename (str | None): Name of the video file on the device.
                Defaults to ``'recording.mp4'``. The file is saved under
                ``/sdcard/``.
            pull (bool): If ``True``, copy the recording to the current local
                directory after recording it. Defaults to ``False``.
            duration (int | float): Maximum recording duration in seconds.
                Defaults to ``10``.
            delay (int | float): Seconds to wait after each ADB command.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess: The result of ``adb pull`` when
                ``pull`` is ``True``; otherwise, the result of the recording
                command.
            str: ``'File format unsupported.'`` when ``filename`` does not
                use the ``.mp4`` extension.
        """
        if not filename:
            filename = 'recording.mp4'

        name, file_format = filename.rsplit('.', 1)
        if file_format != 'mp4':
            return "File format unsupported."


        remote_path = f'/sdcard/{filename}'

        res_record = adb(
            'shell', 'screenrecord', '--time-limit', str(duration), remote_path,
            delay=delay
        )

        if pull:
            res_pull = adb('pull', remote_path, check=True, delay=delay)
            return res_pull

        return res_record


class Gesture:
    """Gesture helpers for a connected Android device.

    Args:
        device (Device): Device whose display dimensions are used for the
            built-in directional gestures.

    Gesture methods accept ``delay`` in seconds and wait after the ADB action
    completes. The default delay is ``0``.
    """

    def __init__(self, device):
        """Create gesture helpers associated with ``device``."""
        self.device = device
        self.swipe = Gesture.Swipe(device)
        self.tap = Gesture.Tap(device)

    class Swipe():
        """Helpers for sending coordinate-based swipe gestures.

        Built-in directional gestures calculate their coordinates as a
        percentage of the associated device's display dimensions.
        """
        def __init__(self, device):
            """Create a swipe helper associated with ``device``."""
            self.device = device

        def swipe(self, x1, y1, x2, y2, delay=0):
            """Swipe from ``(x1, y1)`` to ``(x2, y2)`` in screen pixels.

            Args:
                delay (int | float): Seconds to wait after the swipe completes.
                    Defaults to ``0``.
            """
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), delay=delay)


        def swipe_up(self, delay=0):
            """Swipe upward using the built-in screen coordinates."""
            x1 = int(self.device.width * 0.5)
            y1 = int(self.device.height * 0.80)
            y2 = int(self.device.height * 0.10)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x1), str(y2), delay=delay)

        def unlock(self, delay=0):
            """Attempt to unlock the device with an upward swipe."""
            return self.swipe_up(delay=delay)

        def swipe_down(self, delay=0):
            """Swipe downward using the built-in screen coordinates."""
            x1 = int(self.device.width * 0.5)
            y1 = int(self.device.height * 0.10)
            y2 = int(self.device.height * 0.80)

            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x1), str(y2), delay=delay)


        def swipe_right(self, delay=0):
            """Swipe right using the built-in screen coordinates."""
            x1 = int(self.device.width * 0.10)
            y1 = int(self.device.height * 0.50)
            x2 = int(self.device.width * 0.90)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y1), delay=delay)

        def swipe_left(self, delay=0):
            """Swipe left using the built-in screen coordinates."""
            x1 = int(self.device.width * 0.90)
            y1 = int(self.device.height * 0.50)
            x2 = int(self.device.width * 0.10)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y1), delay=delay)

    class Tap:
        """Helpers for sending coordinate-based tap gestures.

        Tap coordinates are expressed in screen pixels.
        """
        def __init__(self, device):
            """Create a tap helper associated with ``device``."""
            self.device = device

        def tap(self, x, y, delay=0):
            """Tap at ``(x, y)`` in screen pixels.

            Args:
                delay (int | float): Seconds to wait after the tap completes.
                    Defaults to ``0``.
            """
            return adb('shell', 'input', 'tap', str(x), str(y), delay=delay)

        def double_tap(self, x, y, delay=0):
            """Double-tap near ``(x, y)`` in screen pixels.

            Args:
                delay (int | float): Seconds to wait after each tap completes.
                    Defaults to ``0``.
            """
            self.tap(x, y, delay=delay)
            time.sleep(0.05)
            return self.tap(x, y, delay=delay)

        def longpress(self, x, y, duration=3000, delay=0):
            """Press at ``(x, y)`` for ``duration`` milliseconds.

            Args:
                delay (int | float): Seconds to wait after the long press
                    completes. Defaults to ``0``.
            """
            return adb('shell', 'input', 'swipe', str(x), str(y), str(x), str(y), str(duration), delay=delay)


device = Device()
button = Button()
swipe = Gesture.Swipe(device=device)
tap = Gesture.Tap(device=device)



