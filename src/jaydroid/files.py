"""File operations for a connected Android device.

This module provides methods to manage files on the device, including
transferring files to and from the device via ADB.
"""

from .utils import adb
from .exceptions import DeviceNotConnectedError, PathDoesNotExistError
import os


class FileTransfer:
    def __init__(self, device):
        self._device = device


    def get_sdcard_contents(self) -> list[str]:
        """Return the contents of the device's /sdcard/ directory.

        Returns:
            list[str]: A list of file and directory names found in /sdcard/.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
        """
        if self._device.is_connected():
            result = adb('shell', 'ls', '/sdcard/')
            raw_output = result.stdout
            entries = raw_output.splitlines()
            return entries
        raise DeviceNotConnectedError('No device was detected. Please connect an android and try again.')

    
    def push_file(self, from_path: str, to_path: str) -> str:
        """Push a local file to the connected Android device.

        Copies a file from the local computer to the specified location on
        the device's filesystem via ADB.

        Args:
            from_path (str): Path to the file on the local computer.
            to_path (str): Destination path on the device (e.g. under /sdcard/).

        Returns:
            str: The raw transfer output reported by ADB.

        Raises:
            DeviceNotConnectedError: If no device or emulator is connected.
            PathDoesNotExistError: If ``from_path`` does not exist on the
                local computer.
        """
        if self._device.is_connected():
            if os.path.exists(from_path):
                result = adb('push', from_path, to_path)
                transfer_meta = result.stdout
                return transfer_meta
            raise PathDoesNotExistError('The path specified does not exists on this computer.')
        raise DeviceNotConnectedError('No device was detected. Please connect an android and try agian.')