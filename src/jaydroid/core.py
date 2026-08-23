r"""
Utilities for sending Android Debug Bridge (ADB) input commands.

The connected Android device must have developer options and USB debugging
enabled. Each operation returns the :class:`subprocess.CompletedProcess`
instance produced by :func:`subprocess.run`, allowing callers to inspect the
command's output and return code.
"""


import subprocess


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

        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '26'],
            capture_output=True,
            text=True
        )

    def volume_up(self):
        """
        Increase the device's system volume by one default increment.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '24'],
            capture_output=True,
            text=True
        )

    def volume_down(self):
        """
        Decrease the device's system volume by one default increment.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '25'],
            capture_output=True,
            text=True
        )

    def home(self):
        """
        Navigate to the device home screen.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '3'],
            capture_output=True,
            text=True
        )   

    def back(self):
        """
        Navigate back one step in the current Android interface.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '4'],
            capture_output=True,
            text=True
        )
    
    def recent_apps(self):
        """
        Open the Android recent-apps view.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '187'],
            capture_output=True,
            text=True
        )

    def menu(self):
        """
        Send the Android menu-button key event.

        The effect depends on the active application and Android version.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '82'],
            capture_output=True,
            text=True
        )

    def wake(self):
        """
        Wake the device's screen if it is off.

        This has no effect when the device is already awake.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '224'],
            capture_output=True,
            text=True
        )

    def sleep(self):
        """
        Put the device's screen to sleep.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """
        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '223'],
            capture_output=True,
            text=True
        )


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

        return subprocess.run(
            ['adb', 'shell', 'input', 'keyevent', '120'],
            capture_output=True,
            text=True
        )


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

        res_capture = subprocess.run(
            ['adb', 'shell', 'screencap', '-p', remote_path],
            capture_output=True,
            text=True
        )

        if pull:
            res_pull = subprocess.run(
                ['adb', 'pull', remote_path],
                capture_output=True,
                text=True,
                check=True
            )
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

        res_record = subprocess.run(
            ['adb', 'shell', 'screenrecord', '--time-limit', str(duration), remote_path],
            capture_output=True,
            text=True,
        )

        if pull:
            res_pull = subprocess.run(
                ['adb', 'pull', remote_path],
                capture_output=True,
                text=True,
                check=True
            )
            return res_pull

        return res_record


