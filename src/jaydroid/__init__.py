"""
jaydroid — a beginner-friendly Python wrapper for simulating Android actions via ADB.

Provides helpers for connecting to an Android device, reading display dimensions and
device info, sending button input, capturing the screen, and performing swipe and tap
gestures.

Example:
    >>> import jaydroid
    >>> jaydroid.device.connect()
    >>> jaydroid.tap.tap(500, 800)
    >>> jaydroid.button.power()
"""

from .core import device, button, swipe, tap, Device, Button, Screen, Gesture
from .exceptions import DeviceNotFoundError, DeviceNotConnectedError

__version__ = "0.2.0"

__all__ = [
    "device", "button", "swipe", "tap",
    "Device", "Button", "Screen", "Gesture",
    "DeviceNotFoundError", "DeviceNotConnectedError",
]