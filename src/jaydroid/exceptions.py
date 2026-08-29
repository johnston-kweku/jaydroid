class DeviceNotFoundError(Exception):
    pass

class DeviceNotConnectedError(Exception):
    pass

class AdbCommandError(Exception):
    pass

class WifiNotConnectedError(Exception):
    pass