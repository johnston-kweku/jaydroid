from .utils import adb

class Screen:
    """Methods for capturing screenshots and recording the device screen.

    Provides methods to take screenshots and record screen video. All methods
    accept an optional ``delay`` parameter (in seconds) that waits after each
    ADB action completes. The default delay is ``0``.
    """

    def capture(self, delay=0):
        """
        Send the Android screenshot key event.

        This method does not save or pull an image file. Use :meth:`screenshot`
        to capture the screen to a file.

        Note:
            This key event may be less universally reliable across OEM Android
            skins than calling :meth:`screenshot` directly.

        Args:
            delay (int | float): Seconds to wait after the capture completes.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess: The result of the ADB command.
        """

        return adb('shell', 'input', 'keyevent', '120', delay=delay)


    def screenshot(self, filename=None, pull=False, delay=0):
        """
        Save a screenshot on the connected device.

        Optionally copies the screenshot to the current local directory after
        capturing it.

        Args:
            filename (str | None): Name of the image file on the device.
                Defaults to ``'screenshot.png'``. The file is saved under ``/sdcard/``.
            pull (bool): If ``True``, copy the screenshot to the current local
                directory after capturing. Defaults to ``False``.
            delay (int | float): Seconds to wait after each ADB command.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess: The result of ``adb pull`` when ``pull``
                is ``True``; otherwise, the result of the capture command.
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

        Optionally copies the recording to the current local directory after
        recording it.

        Args:
            filename (str | None): Name of the video file on the device.
                Defaults to ``'recording.mp4'``. The file is saved under ``/sdcard/``.
            pull (bool): If ``True``, copy the recording to the current local
                directory after recording. Defaults to ``False``.
            duration (int | float): Maximum recording duration in seconds.
                Defaults to ``10``.
            delay (int | float): Seconds to wait after each ADB command.
                Defaults to ``0``.

        Returns:
            subprocess.CompletedProcess: The result of ``adb pull`` when ``pull``
                is ``True``; otherwise, the result of the recording command.
            str: ``'File format unsupported.'`` when ``filename`` does not use
                the ``.mp4`` extension.
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

