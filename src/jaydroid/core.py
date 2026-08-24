r"""
Utilities for sending Android Debug Bridge (ADB) input commands.

The connected Android device must have developer options and USB debugging
enabled. Most operations return the :class:`subprocess.CompletedProcess`
instance produced by :func:`subprocess.run`, allowing callers to inspect the
command's output and return code.
"""


import subprocess

def adb(*args, **kwargs):
    """Run an ADB command and return its completed-process result.

    Args:
        *args (str): Arguments passed to the ``adb`` executable.
        **kwargs: Additional keyword arguments passed to
            :func:`subprocess.run`. Output is captured and decoded as text by
            default.

    Returns:
        subprocess.CompletedProcess: The result of the ADB command.
    """
    kwargs.setdefault('capture_output', True)
    kwargs.setdefault('text', True)
    return subprocess.run(
        ['adb', *args],
        **kwargs
    )


class Button:
    """
    Methods for simulating common Android hardware and navigation buttons.

    ADB must be installed and available on ``PATH``, and a device or emulator
    must be connected before calling these methods.
    """
    def power(self):
        """
        Toggle the device's screen with a power-button press.

        The screen is turned on when it is off and turned off when it is on.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """

        return adb('shell', 'input', 'keyevent', '26')

    def volume_up(self):
        """
        Increase the device's system volume by one default increment.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '24')

    def volume_down(self):
        """
        Decrease the device's system volume by one default increment.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '25')

    def home(self):
        """
        Navigate to the device home screen.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '3')

    def back(self):
        """
        Navigate back one step in the current Android interface.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '4')
    
    def recent_apps(self):
        """
        Open the Android recent-apps view.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '187')

    def menu(self):
        """
        Send the Android menu-button key event.

        The effect depends on the active application and Android version.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '82')

    def wake(self):
        """
        Wake the device's screen if it is off.

        This has no effect when the device is already awake.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '224')

    def sleep(self):
        """
        Put the device's screen to sleep.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return adb('shell', 'input', 'keyevent', '223')


class Screen:
    """Methods for capturing screenshots and recording the device screen."""

    def capture(self):
        """
        Send the Android screenshot key event.

        This method does not save or pull an image file. Use :meth:`screenshot`
        to capture the screen to a file.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """

        return adb('shell', 'input', 'keyevent', '120')


    def screenshot(self, filename=None, pull=False):
        """
        Save a screenshot on the connected device.

        Args:
            filename (str | None): Name of the image file on the device.
                Defaults to ``'screenshot.png'``. The file is saved under
                ``/sdcard/``.
            pull (bool): If ``True``, copy the screenshot to the current local
                directory after capturing it. Defaults to ``False``.

        Returns:
            subprocess.CompletedProcess: The result of ``adb pull`` when
                ``pull`` is ``True``; otherwise, the result of the capture
                command.
        """
        if not filename:
            filename = 'screenshot.png'
        remote_path = f'/sdcard/{filename}'

        res_capture = adb('shell', 'screencap', '-p', remote_path)

        if pull:
            res_pull = adb('pull', remote_path, check=True)
            return res_pull

        return res_capture


    def screenrecord(self, filename=None, pull=False, duration=10):
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

        Returns:
            subprocess.CompletedProcess: The result of ``adb pull`` when
                ``pull`` is ``True``; otherwise, the result of the recording
                command.
            str: ``'File format unsupported.'`` when ``filename`` does not
                use the ``.mp4`` extension.
        """
        if not filename:
            filename = 'recording.mp4'

        name, file_format = filename.split('.') 
        if file_format != 'mp4':
            return "File format unsupported."


        remote_path = f'/sdcard/{filename}'

        res_record = adb(
            'shell', 'screenrecord', '--time-limit', str(duration), remote_path
        )

        if pull:
            res_pull = adb('pull', remote_path, check=True)
            return res_pull

        return res_record


