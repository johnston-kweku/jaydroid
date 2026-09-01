import subprocess
import time
from typing import TYPE_CHECKING

from .utils import adb

if TYPE_CHECKING:
    from .device.device import Device


class Gesture:
    """Gesture helpers for a connected Android device.

    Provides access to swipe and tap gestures. Built-in directional gestures
    calculate coordinates as percentages of the device's display dimensions.

    Args:
        device: Device whose display dimensions are used for
            built-in directional gestures.

    All gesture methods accept an optional ``delay`` parameter (in seconds)
    that waits after the ADB action completes. The default delay is ``0``.
    """

    def __init__(self, device: 'Device') -> None:
        """Create gesture helpers associated with ``device``."""
        self.device = device
        self.swipe = Gesture.Swipe(device)
        self.tap = Gesture.Tap(device)

    class Swipe:
        """Helpers for sending coordinate-based swipe gestures.

        Supports arbitrary coordinate-based swipes and built-in directional
        swipes that automatically calculate coordinates based on the device's
        display dimensions.
        """
        def __init__(self, device: 'Device') -> None:
            """Create a swipe helper associated with ``device``."""
            self.device = device

        def swipe(self, x1: int, y1: int, x2: int, y2: int, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Swipe from ``(x1, y1)`` to ``(x2, y2)`` in screen pixels.

            Args:
                x1: Starting x-coordinate in pixels.
                y1: Starting y-coordinate in pixels.
                x2: Ending x-coordinate in pixels.
                y2: Ending y-coordinate in pixels.
                delay: Seconds to wait after the swipe completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), delay=delay)


        def swipe_up(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Swipe upward using the built-in screen coordinates.

            Swipes from 60% to 10% of the device's height at 50% of the width.

            Args:
                delay: Seconds to wait after the swipe completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            x1 = int(self.device.width * 0.5)
            y1 = int(self.device.height * 0.60)
            y2 = int(self.device.height * 0.10)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x1), str(y2), delay=delay)

        def unlock(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Attempt to unlock the device with an upward swipe.

            Equivalent to :meth:`swipe_up`.

            Args:
                delay: Seconds to wait after the swipe completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            return self.swipe_up(delay=delay)

        def swipe_down(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Swipe downward using the built-in screen coordinates.

            Swipes from 10% to 80% of the device's height at 50% of the width.

            Args:
                delay: Seconds to wait after the swipe completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            x1 = int(self.device.width * 0.5)
            y1 = int(self.device.height * 0.10)
            y2 = int(self.device.height * 0.80)

            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x1), str(y2), delay=delay)


        def swipe_right(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Swipe right using the built-in screen coordinates.

            Swipes from 10% to 70% of the device's width at 50% of the height.

            Args:
                delay: Seconds to wait after the swipe completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            x1 = int(self.device.width * 0.10)
            y1 = int(self.device.height * 0.50)
            x2 = int(self.device.width * 0.70)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y1), delay=delay)

        def swipe_left(self, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Swipe left using the built-in screen coordinates.

            Swipes from 70% to 10% of the device's width at 50% of the height.

            Args:
                delay: Seconds to wait after the swipe completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            x1 = int(self.device.width * 0.70)
            y1 = int(self.device.height * 0.50)
            x2 = int(self.device.width * 0.10)
            return adb('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y1), delay=delay)

    class Tap:
        """Helpers for sending coordinate-based tap gestures.

        Supports single taps, double-taps, and long-presses at specified
        screen coordinates.
        """
        def __init__(self, device: 'Device') -> None:
            """Create a tap helper associated with ``device``."""
            self.device = device

        def tap(self, x: int, y: int, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Tap at ``(x, y)`` in screen pixels.

            Args:
                x: X-coordinate in pixels.
                y: Y-coordinate in pixels.
                delay: Seconds to wait after the tap completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            return adb('shell', 'input', 'tap', str(x), str(y), delay=delay)

        def double_tap(self, x: int, y: int, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Double-tap near ``(x, y)`` in screen pixels.

            Performs two taps in quick succession with a 50ms interval between them.

            Args:
                x: X-coordinate in pixels.
                y: Y-coordinate in pixels.
                delay: Seconds to wait after each tap completes.
                    Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the second tap's ADB command.
            """
            self.tap(x, y, delay=delay)
            time.sleep(0.05)
            return self.tap(x, y, delay=delay)

        def longpress(self, x: int, y: int, duration: int = 3000, delay: int | float = 0) -> subprocess.CompletedProcess[str]:
            """Press at ``(x, y)`` for ``duration`` milliseconds.

            Uses a zero-distance swipe to simulate a long press.

            Args:
                x: X-coordinate in pixels.
                y: Y-coordinate in pixels.
                duration: Press duration in milliseconds. Defaults to ``3000`` (3 seconds).
                delay: Seconds to wait after the long press
                    completes. Defaults to ``0``.

            Returns:
                subprocess.CompletedProcess[str]: The result of the ADB command.
            """
            return adb('shell', 'input', 'swipe', str(x), str(y), str(x), str(y), str(duration), delay=delay)


