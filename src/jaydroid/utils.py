import time, subprocess
from .exceptions import AdbCommandError


def adb(*args, **kwargs):
    """Run an ADB command and return its completed-process result.

    Args:
        *args (str): Arguments passed to the ``adb`` executable.
        **kwargs: Additional keyword arguments passed to
            :func:`subprocess.run`. Output is captured and decoded as text by
            default.
        delay (int | float): Seconds to wait after the command completes.
            Defaults to ``0``.

    Returns:
        subprocess.CompletedProcess: The result of the ADB command.
    """
    kwargs.setdefault('capture_output', True)
    kwargs.setdefault('text', True)
    delay_value = kwargs.pop('delay', 0)
    
    result =  subprocess.run(
        ['adb', *args],
        **kwargs
    )

    if result.returncode != 0:
        raise AdbCommandError(result.stderr)
    time.sleep(delay_value)
    return result

