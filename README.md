# jaydroid

`jaydroid` is a beginner-friendly Python wrapper around [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb). It simplifies Android device automation by providing intuitive helpers for connecting to devices, reading display dimensions, querying device information, sending button input, capturing screenshots/video, and performing swipe and tap gestures.

This project was created as a learning exercise in designing, structuring, and publishing a Python package from scratch. The development process is documented as a video series, and the package continues to evolve.

## Features

- **Device Connection**: Simple interface to connect to the first available ADB device and retrieve its display dimensions
- **Button Simulation**: Send hardware button events (power, volume, home, back, etc.)
- **Gestures**: Perform coordinate-based swipes and taps with optional directional helpers
- **Screen Capture**: Screenshot and screen recording with optional file transfer
- **Device Information**: Query Android version, device model, battery status, Wi-Fi connectivity, installed apps, and storage usage
- **Error Handling**: Specific exceptions for different failure modes
- **Delay Support**: Optional delays after each action to allow the device to catch up

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

```bash
pip install jaydroid
```

For local development, from the project directory:

```bash
python -m pip install -e .
```

## Quick start

`jaydroid` exposes ready-to-use module-level instances that require no explicit initialization beyond connecting your device:

```python
from jaydroid import device, button, swipe, tap

device.connect()  # Required first step — checks device is reachable and loads screen dimensions

button.wake(delay=1)
swipe.swipe_up()
tap.tap(360, 640)
```

### How it works

1. `device.connect()` verifies that at least one device or emulator is reachable over ADB and retrieves its display dimensions
2. All subsequent operations use the connected device
3. Most methods accept an optional `delay` parameter (in seconds) to wait after the action completes

## Delays

Every `Button`, `Screen`, `Swipe`, and `Tap` method accepts an optional `delay` parameter (in seconds, default `0`). The delay runs *after* the action completes successfully — "do this, then wait" — giving the device time to process the action:

```python
button.wake(delay=1)  # Wake device, then wait 1 second
swipe.swipe_up(delay=0.5)  # Swipe up, then wait 0.5 seconds
tap.tap(360, 640, delay=0.2)  # Tap, then wait 0.2 seconds
```

**Error handling**: If a command fails, the delay is skipped — you see the error immediately instead of waiting first.

## Gestures

### Swipe

Send swipe gestures to the connected device:

```python
from jaydroid import swipe

swipe.swipe_up(delay=0.5)    # Swipe upward
swipe.swipe_down()            # Swipe downward
swipe.swipe_left()            # Swipe left
swipe.swipe_right()           # Swipe right
swipe.unlock()                # Alias for swipe_up()
```

**Directional swipes** are calculated as percentages of the device's display dimensions, so they adapt across different screen sizes rather than using fixed pixel coordinates:

- **Left/Right**: from 10% to 90% (or vice versa) of display width, at 50% of height
- **Up/Down**: at 50% of display width, from 80% to 10% (or vice versa) of height

**Custom coordinates** — use `swipe.swipe(x1, y1, x2, y2)` for precise control:

```python
swipe.swipe(600, 640, 100, 640, delay=0.5)  # Swipe from (600, 640) to (100, 640)
```

### Tap

Send tap and long-press gestures to the connected device:

```python
from jaydroid import tap

tap.tap(360, 640)                           # Single tap at (360, 640)
tap.double_tap(360, 640, delay=0.2)        # Double-tap at (360, 640)
tap.longpress(360, 640, duration=1000)     # Long press for 1000ms (1 second)
```

## Buttons

Send hardware and navigation button events to the connected device:

```python
from jaydroid import button

button.power()           # Toggle power (turn screen on/off)
button.wake()            # Wake the device screen
button.sleep()           # Put the device to sleep
button.home()            # Navigate to home screen
button.back()            # Go back one step
button.recent_apps()     # Open recent apps view
button.menu()            # Send menu button event
button.volume_up()       # Increase volume
button.volume_down()     # Decrease volume
```

All methods accept optional `delay` parameter.

## Screen

Capture screenshots and record video from the connected device:

```python
from jaydroid.screen import Screen

screen = Screen()

screen.capture()                                          # Send screenshot key event
screen.screenshot(filename='screen.png', pull=True)      # Capture and optionally transfer
screen.screenrecord(filename='recording.mp4', pull=True, duration=10)  # Record video
```

**Details:**
- `capture()` sends the screenshot key event (less reliable than `screenshot()` on some devices)
- `screenshot()` and `screenrecord()` save to `/sdcard/` by default
- Use `pull=True` to transfer the file to your local working directory
- `screenrecord()` defaults to 10 seconds; set `duration` for different lengths

## Device information

Query and monitor device state and capabilities:

```python
from jaydroid import device

device.connect()  # Required to access width/height

# Display dimensions (available after connect())
print(device.width, device.height)

# Connection and live queries (no prior connect() required)
print(device.is_connected())              # bool: Is a device connected?
print(device.get_android_version())       # str: Android version (e.g., '14')
print(device.get_device_model())          # str: Device model name
print(device.get_device_ip())             # str: Wi-Fi IP address
print(device.wifi_status())               # str: 'On', 'Off', or 'Unknown'
print(device.battery_info())              # dict: Battery status and health
print(device.get_installed_apps())        # list: Third-party package names
print(device.storage_space_info())        # dict: /data partition usage

device.reboot()  # Reboot the connected device
```

### Display dimensions

- `width` and `height` are **only available after** `connect()` — accessing them before raises `DeviceNotConnectedError`
- Used automatically by directional swipe helpers to scale gestures across screen sizes

### Connection and live queries

The following methods check the connection **every time** they're called and don't require `connect()` to be run first:
- `is_connected()`, `get_android_version()`, `battery_info()`, `get_device_model()`, `get_device_ip()`, `wifi_status()`, `get_installed_apps()`, `storage_space_info()`

### Method details

**`battery_info()`**: Returns a dictionary parsed from `adb shell dumpsys battery`
- Consistently includes: `level`, `status`, `health`, `voltage`, `temperature`, `technology`, and `*_powered` flags
- May include additional OEM-specific fields depending on manufacturer

**`get_device_model()`**: Returns the device model name (e.g., `"SM-G950F"` for Samsung Galaxy S8)

**`get_device_ip()`**: Returns the device's local Wi-Fi IP address
- Raises `WifiNotConnectedError` if Wi-Fi is not currently enabled

**`wifi_status()`**: Returns `'On'`, `'Off'`, or `'Unknown'` for unknown states

**`get_installed_apps()`**: Returns a list of third-party package names (system apps excluded)

**`storage_space_info()`**: Returns a dictionary with keys: `Filesystem`, `Size`, `Used`, `Available`, `Use%`, `Mounted on`
- Queries the device's `/data` partition

**`reboot()`**: Reboots the connected device

## Error handling

`jaydroid` raises specific exceptions for different failure modes, allowing you to handle errors precisely:

```python
from jaydroid import device
from jaydroid.exceptions import DeviceNotFoundError, DeviceNotConnectedError, AdbCommandError

try:
    device.connect()
except DeviceNotFoundError:
    print("No device connected — plug one in and try again.")
except AdbCommandError as e:
    print(f"ADB command failed: {e}")

try:
    width = device.width
except DeviceNotConnectedError:
    print("Device not connected. Call device.connect() first.")
```

### Exception types

- **`DeviceNotFoundError`**: Raised by `connect()` when no device or emulator is reachable
- **`DeviceNotConnectedError`**: Raised when accessing `width`/`height` before `connect()` has been called, or when a device query is performed without an active connection
- **`AdbCommandError`**: Raised when an ADB command fails (e.g., device disconnects mid-operation); includes ADB's error output for debugging

## Module structure

The package is organized into logical modules:

- **`jaydroid.core`**: Main entry point with module-level instances (`device`, `button`, `swipe`, `tap`, `screen`)
- **`jaydroid.device.Device`**: Device connection and information queries
  - `Device.apps` → `Apps` class: App management
  - `Device.system` → `System` class: System status and control
  - `Device.info` → `Info` class: Device information
- **`jaydroid.button.Button`**: Hardware and navigation button simulation
- **`jaydroid.gesture.Gesture`**: Swipe and tap gestures
  - `Gesture.Swipe`: Directional and custom swipes
  - `Gesture.Tap`: Tap, double-tap, and long-press
- **`jaydroid.screen.Screen`**: Screenshot and video recording
- **`jaydroid.utils`**: ADB command execution utilities

## Roadmap

This package is under active development. Planned future enhancements include:

- **Input methods**: Text input and keyboard event simulation
- **Clipboard operations**: Read/write device clipboard content
- **File management**: Transfer files to/from the device
- **Logcat integration**: Capture and filter Android system logs
- **Performance profiling**: Device performance and CPU usage monitoring
- **Expanded gesture support**: Pinch, rotate, and other multi-touch gestures

## Contributing

Contributions are welcome! If you encounter bugs or have feature suggestions, please open an issue on [GitHub](https://github.com/johnston-kweku/jaydroid/issues).

## Related projects

- [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb) — Official ADB documentation
- [Appium](http://appium.io/) — A more comprehensive automation framework for mobile apps

## Author

Built by Johnston Kweku Abubakar ([@johnston-kweku](https://github.com/johnston-kweku)) — this is my first Python package, built while learning to design, structure, and publish one from scratch.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
