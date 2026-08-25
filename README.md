# jaydroid

`jaydroid` is a small Python wrapper around [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb). It provides helpers for common device buttons, screenshots, screen recordings, display-size detection, and swipe gestures.

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

Create a `Device` first. It queries the display size, which the built-in directional helpers use to calculate valid coordinates for that device.

```python
from jaydroid.core import Device, Gesture

device = Device()
swipe = Gesture.Swipe(device)
swipe.swipe_left()
swipe.swipe_right()
swipe.swipe_up()
swipe.swipe_down()
```

You can also create the top-level `Gesture` wrapper. Its `swipe` attribute is a `Swipe` helper:

```python
from jaydroid.core import Device, Gesture

gestures = Gesture(Device())
gestures.swipe.swipe_left()
```

Use `Swipe.swipe()` for custom coordinates. Coordinates are pixel values, with `(0, 0)` at the top-left of the display:

```python
from jaydroid.core import Device, Gesture

swipe = Gesture.Swipe(Device())
swipe.swipe(600, 640, 100, 640)
```

The built-in helpers use these relative positions:

- Left and right: 10% to 90% of the display width at 50% of its height
- Up and down: 50% of the display width, from 80% to 10% of its height
- `unlock()`: an upward swipe

## Available button helpers

`Button` provides `power()`, `volume_up()`, `volume_down()`, `home()`, `back()`, `recent_apps()`, `menu()`, `wake()`, and `sleep()`.

## Screen helpers

- `Screen.capture()` sends the Android screenshot key event.
- `Screen.screenshot()` saves a PNG under `/sdcard/` and can optionally pull it locally.
- `Screen.screenrecord()` records an MP4 under `/sdcard/` and can optionally pull it locally.

## Device information

`Device()` queries `adb shell wm size` during initialization. Its `width` and `height` attributes contain the physical display dimensions. `get_screen_size()` can be called again to refresh the values through `setup()`.

If the connected device does not return a line beginning with `Physical size:`, initialization raises `RuntimeError`. For unusual device output, use `Swipe.swipe()` with explicit coordinates.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
