from .utils import adb

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

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '24', delay=delay)

    def volume_down(self, delay=0):
        """
        Decrease the device's system volume by one default increment.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '25', delay=delay)

    def home(self, delay=0):
        """
        Navigate to the device home screen.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '3', delay=delay)

    def back(self, delay=0):
        """
        Navigate back one step in the current Android interface.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '4', delay=delay)
    
    def recent_apps(self, delay=0):
        """
        Open the Android recent-apps view.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '187', delay=delay)

    def menu(self, delay=0):
        """
        Send the Android menu-button key event.

        The effect depends on the active application and Android version.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '82', delay=delay)

    def wake(self, delay=0):
        """
        Wake the device's screen if it is off.

        This has no effect when the device is already awake.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '224', delay=delay)

    def sleep(self, delay=0):
        """
        Put the device's screen to sleep.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.

        Args:
            delay (int | float): Seconds to wait after the key event completes.
                Defaults to ``0``.
        """
        return adb('shell', 'input', 'keyevent', '223', delay=delay)


