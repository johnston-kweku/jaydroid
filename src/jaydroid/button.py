import subprocess
from .utils import adb

class Button:
    """
    Methods for simulating common Android hardware and navigation buttons.

    Provides methods to send key events for hardware and navigation buttons
    (power, volume, home, back, etc.). ADB must be installed and available
    on ``PATH``, and a device or emulator must be connected before calling
    these methods.

    All methods accept an optional ``delay`` parameter (in seconds) that
    waits after the ADB action completes. The default delay is ``0``.

    All methods return :class:`subprocess.CompletedProcess` to allow inspection
    of command output and return codes.
    """
    def power(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Toggle the device's screen with a power-button press.

        The screen is turned on when it is off and turned off when it is on.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """

        return adb('shell', 'input', 'keyevent', '26', delay=delay)

    def volume_up(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Increase the device's system volume by one default increment.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '24', delay=delay)

    def volume_down(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Decrease the device's system volume by one default increment.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '25', delay=delay)

    def home(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Navigate to the device home screen.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '3', delay=delay)

    def back(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Navigate back one step in the current Android interface.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '4', delay=delay)
    
    def recent_apps(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Open the Android recent-apps view.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '187', delay=delay)

    def menu(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Send the Android menu-button key event.

        The effect depends on the active application and Android version.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '82', delay=delay)

    def wake(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Wake the device's screen if it is off.

        This has no effect when the device is already awake.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '224', delay=delay)

    def sleep(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
        """
        Put the device's screen to sleep.

        Args:
            delay: Seconds to wait after the key event completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess[str]: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '223', delay=delay)


