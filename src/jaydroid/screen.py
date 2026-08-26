from .utils import adb

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

