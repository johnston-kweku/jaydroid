class DeviceNotFoundError(Exception):
    """Raised when no Android device or emulator is found via ADB."""
    pass

class DeviceNotConnectedError(Exception):
    """Raised when an operation requires a connected device but none is available."""
    pass

class AdbCommandError(Exception):
    """Raised when an ADB command execution fails."""
    pass

class WifiNotConnectedError(Exception):
    """Raised when an operation requires Wi-Fi connectivity but it is unavailable."""
    pass