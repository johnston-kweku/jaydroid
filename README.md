# jaydroid

`jaydroid` is a small Python wrapper around [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb). It provides helpers for connecting to an Android device, reading display dimensions, sending button input, capturing the screen, and performing swipe and tap gestures.

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
device.connect()
width, height = device.get_screen_size()
print(f'Display: {width}x{height}')

buttons = Button()
buttons.wake(delay=1)
buttons.home(delay=0.5)

screen = Screen()
screen.screenshot(filename='screen.png', pull=True, delay=1)
screen.screenrecord(filename='recording.mp4', pull=True, duration=10, delay=1)
```

ADB command results are returned as `subprocess.CompletedProcess` objects. Inspect `returncode`, `stdout`, and `stderr` to check the result. Pull operations use `check=True` and raise `subprocess.CalledProcessError` when ADB reports an error.

## Delays

All `Button`, `Screen`, and `Gesture` methods accept an optional `delay` argument in seconds. The default is `0`, so commands run without an additional pause. The delay is applied after the ADB action completes:

```python
from jaydroid.core import Button, Gesture

buttons = Button()
buttons.wake(delay=1)

gestures = Gesture(device)
gestures.tap.double_tap(360, 640, delay=0.5)
```

For compound methods, such as `double_tap()` and screen capture methods with `pull=True`, the delay is applied after each underlying ADB command. `delay` may be an integer or floating-point number.

## Gestures

Create a `Device`, connect it to an available ADB device, and pass it to the gesture helpers. The directional helpers calculate coordinates from the connected display size.

```python
from jaydroid.core import Device, Gesture

device = Device()
device.connect()
swipe = Gesture.Swipe(device)
swipe.swipe_left()
swipe.swipe_right()
swipe.swipe_up(delay=0.5)
swipe.swipe_down(delay=0.5)
```

You can also create the top-level `Gesture` wrapper. Its `swipe` attribute is a `Swipe` helper:

```python
from jaydroid.core import Device, Gesture

device = Device()
device.connect()
gestures = Gesture(device)
gestures.swipe.swipe_left(delay=0.5)
```

Use `Swipe.swipe()` for custom coordinates. Coordinates are pixel values, with `(0, 0)` at the top-left of the display:

```python
from jaydroid.core import Device, Gesture

device = Device()
device.connect()
swipe = Gesture.Swipe(device)
swipe.swipe(600, 640, 100, 640, delay=0.5)
```

The built-in helpers use these relative positions:

- Left and right: 10% to 90% of the display width at 50% of its height
- Up and down: 50% of the display width, from 80% to 10% of its height
- `unlock()`: an upward swipe

Tap gestures are available through `Gesture.Tap(device)`:

```python
from jaydroid.core import Device, Gesture

device = Device()
device.connect()
tap = Gesture.Tap(device)
tap.tap(360, 640, delay=0.5)
tap.double_tap(360, 640, delay=0.5)
tap.longpress(360, 640, duration=1000, delay=0.5)
```

## Available button helpers

`Button` provides `power()`, `volume_up()`, `volume_down()`, `home()`, `back()`, `recent_apps()`, `menu()`, `wake()`, and `sleep()`. Each accepts `delay=0`.

## Screen helpers

- `Screen.capture(delay=0)` sends the Android screenshot key event.
- `Screen.screenshot(filename=None, pull=False, delay=0)` saves a PNG under `/sdcard/` and can optionally pull it locally.
- `Screen.screenrecord(filename=None, pull=False, duration=10, delay=0)` records an MP4 under `/sdcard/` and can optionally pull it locally.

## Device information

`Device()` starts disconnected. Call `connect()` to verify that an ADB device or emulator is available and load its display dimensions. Its `width` and `height` attributes contain the physical display dimensions. Call `setup()` to refresh those values.

Accessing `width` or `height` before connecting raises `DeviceNotConnectedError`. If no device is available, `connect()` raises `DeviceNotFoundError`. If the device returns an unrecognized resolution format, `get_screen_size()` raises `RuntimeError`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
