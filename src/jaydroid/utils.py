import time
import subprocess
from typing import Any
from .exceptions import AdbCommandError


def adb(*args: str, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """Run an ADB command and return its completed-process result.

    Args:
        *args: Arguments passed to the ``adb`` executable.
        **kwargs: Additional keyword arguments passed to
            :func:`subprocess.run`. Output is captured and decoded as text by
            default.
        delay: Seconds to wait after the command completes (passed as a kwarg).
            Defaults to ``0``.

    Returns:
        subprocess.CompletedProcess[str]: The result of the ADB command.
    """
    kwargs.setdefault('capture_output', True)
    kwargs.setdefault('text', True)
    delay_value = kwargs.pop('delay', 0)
    
    result = subprocess.run(
        ['adb', *args],
        **kwargs
    )

    
    if result.returncode != 0:
        raise AdbCommandError(result.stderr)
    time.sleep(delay_value)
    return result

