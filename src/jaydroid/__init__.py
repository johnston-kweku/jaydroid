"""
jaydroid — a beginner-friendly Python wrapper for simulating Android actions via ADB.

Example:
    import jaydroid

    jaydroid.device.connect()
    jaydroid.tap.tap(500, 800)
"""

from .core import device, button, swipe, tap, Device, Button, Screen, Gesture
from .exceptions import DeviceNotFoundError, DeviceNotConnectedError

__version__ = "0.1.0"

__all__ = [
    "device", "button", "swipe", "tap",
    "Device", "Button", "Screen", "Gesture",
    "DeviceNotFoundError", "DeviceNotConnectedError",
]