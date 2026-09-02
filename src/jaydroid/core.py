r"""
Core module for Android Debug Bridge (ADB) interaction.

Provides ready-to-use instances for device connection, button input, gestures,
and screen operations. The connected Android device must have developer options
and USB debugging enabled.

Most operations return :class:`subprocess.CompletedProcess` instances from
:func:`subprocess.run`, allowing callers to inspect command output and return codes.
"""


from .device.device import Device
from .gesture import Gesture
from .button import Button
from .screen import Screen
from .files import FileTransfer






device = Device()
button = Button()
swipe = Gesture.Swipe(device=device)
tap = Gesture.Tap(device=device)
screen = Screen()
files = FileTransfer(device=device)



