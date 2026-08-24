# jaydroid

`jaydroid` is a small Python wrapper around [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb). It provides helpers for common device buttons, screenshots, screen recordings, and swipe gestures.

## Requirements

- Python 3.8 or newer
- ADB installed and available on your `PATH`
- An Android device or emulator connected to ADB
- USB debugging enabled when using a physical device

Check the connection with:

```bash
adb devices
```

## Installation

From the project directory, install the package in editable mode:

```bash
python -m pip install -e .
```

## Usage

```python
from jaydroid.core import Button, Device, Screen

device = Device()
width, height = device.get_screen_size()
print(f'Display: {width}x{height}')

buttons = Button()
buttons.wake()
buttons.home()

screen = Screen()
screen.screenshot(filename='screen.png', pull=True)
screen.screenrecord(filename='recording.mp4', pull=True, duration=10)
```

ADB command results are returned as `subprocess.CompletedProcess` objects. Inspect `returncode`, `stdout`, and `stderr` to check the result. Pull operations use `check=True` and raise `subprocess.CalledProcessError` when ADB reports an error.

## Gestures

Use `Swipe.swipe()` for custom coordinates, or use the built-in directional helpers:

```python
from jaydroid.core import Gesture

swipe = Gesture.Swipe()
swipe.swipe_left()
swipe.swipe_right()
swipe.swipe_up()
swipe.swipe_down()
```

Coordinates are pixels. The built-in directional helpers use fixed coordinates, so custom coordinates may be needed for devices with different display sizes:

```python
swipe.swipe(600, 640, 100, 640)
```

## Available button helpers

`Button` provides `power()`, `volume_up()`, `volume_down()`, `home()`, `back()`, `recent_apps()`, `menu()`, `wake()`, and `sleep()`.

## Screen helpers

- `Screen.capture()` sends the Android screenshot key event.
- `Screen.screenshot()` saves a PNG under `/sdcard/` and can optionally pull it locally.
- `Screen.screenrecord()` records an MP4 under `/sdcard/` and can optionally pull it locally.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
