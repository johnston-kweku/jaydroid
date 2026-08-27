from .utils import adb
import time


class Gesture:
    """Gesture helpers for a connected Android device.

    Args:
        device (Device): Device whose display dimensions are used for the
            built-in directional gestures.

    Gesture methods accept ``delay`` in seconds and wait after the ADB action
    completes. The default delay is ``0``.
    """

    def __init__(self, device):
        """Create gesture helpers associated with ``device``."""
        self.device = device
        self.swipe = Gesture.Swipe(device)
        self.tap = Gesture.Tap(device)

    class Swipe():
        """Helpers for sending coordinate-based swipe gestures.

        Built-in directional gestures calculate their coordinates as a
        percentage of the associated device's display dimensions.
        """
        def __init__(self, device):
            """Create a swipe helper associated with ``device``."""
            self.device = device

        def swipe(self, x1, y1, x2, y2, delay=0):
            """Swipe from ``(x1, y1)`` to ``(x2, y2)`` in screen pixels.

            Args:
                delay (int | float): Seconds to wait after the swipe completes.
                    Defaults to ``0``.
            """
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), delay=delay)


        def swipe_up(self, delay=0):
            """Swipe upward using the built-in screen coordinates.

            Args:
                delay (int | float): Seconds to wait after the swipe completes.
                    Defaults to ``0``.
            """
            x1 = int(self.device.width * 0.5)
            y1 = int(self.device.height * 0.60)
            y2 = int(self.device.height * 0.10)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x1), str(y2), delay=delay)

        def unlock(self, delay=0):
            """Attempt to unlock the device with an upward swipe.

            Args:
                delay (int | float): Seconds to wait after the swipe completes.
                    Defaults to ``0``.
            """
            return self.swipe_up(delay=delay)

        def swipe_down(self, delay=0):
            """Swipe downward using the built-in screen coordinates.

            Args:
                delay (int | float): Seconds to wait after the swipe completes.
                    Defaults to ``0``.
            """
            x1 = int(self.device.width * 0.5)
            y1 = int(self.device.height * 0.10)
            y2 = int(self.device.height * 0.80)

            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x1), str(y2), delay=delay)


        def swipe_right(self, delay=0):
            """Swipe right using the built-in screen coordinates.

            Args:
                delay (int | float): Seconds to wait after the swipe completes.
                    Defaults to ``0``.
            """
            x1 = int(self.device.width * 0.10)
            y1 = int(self.device.height * 0.50)
            x2 = int(self.device.width * 0.70)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y1), delay=delay)

        def swipe_left(self, delay=0):
            """Swipe left using the built-in screen coordinates.

            Args:
                delay (int | float): Seconds to wait after the swipe completes.
                    Defaults to ``0``.
            """
            x1 = int(self.device.width * 0.70)
            y1 = int(self.device.height * 0.50)
            x2 = int(self.device.width * 0.10)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y1), delay=delay)

    class Tap:
        """Helpers for sending coordinate-based tap gestures.

        Tap coordinates are expressed in screen pixels.
        """
        def __init__(self, device):
            """Create a tap helper associated with ``device``."""
            self.device = device

        def tap(self, x, y, delay=0):
            """Tap at ``(x, y)`` in screen pixels.

            Args:
                delay (int | float): Seconds to wait after the tap completes.
                    Defaults to ``0``.
            """
            return adb('shell', 'input', 'tap', str(x), str(y), delay=delay)

        def double_tap(self, x, y, delay=0):
            """Double-tap near ``(x, y)`` in screen pixels.

            Args:
                delay (int | float): Seconds to wait after each tap completes.
                    Defaults to ``0``.
            """
            self.tap(x, y, delay=delay)
            time.sleep(0.05)
            return self.tap(x, y, delay=delay)

        def longpress(self, x, y, duration=3000, delay=0):
            """Press at ``(x, y)`` for ``duration`` milliseconds.

            Args:
                delay (int | float): Seconds to wait after the long press
                    completes. Defaults to ``0``.
            """
            return adb('shell', 'input', 'swipe', str(x), str(y), str(x), str(y), str(duration), delay=delay)


