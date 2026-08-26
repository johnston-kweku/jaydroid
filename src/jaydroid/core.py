r"""
Utilities for sending Android Debug Bridge (ADB) input commands.

The connected Android device must have developer options and USB debugging
enabled. Most operations return the :class:`subprocess.CompletedProcess`
instance produced by :func:`subprocess.run`, allowing callers to inspect the
command's output and return code.
"""


from .device import Device
from .gesture import Gesture
from .button import Button
from .screen import Screen






device = Device()
button = Button()
swipe = Gesture.Swipe(device=device)
tap = Gesture.Tap(device=device)



