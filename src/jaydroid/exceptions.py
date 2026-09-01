class JaydroidError(Exception): pass


class DeviceNotFoundError(JaydroidError):
    """Raised when no Android device or emulator is found via ADB."""
    pass

class DeviceNotConnectedError(JaydroidError):
    """Raised when an operation requires a connected device but none is available."""
    pass

class AdbCommandError(JaydroidError):
    """Raised when an ADB command execution fails."""
    pass

class WifiNotConnectedError(JaydroidError):
    """Raised when an operation requires Wi-Fi connectivity but it is unavailable."""
    pass