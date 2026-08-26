from jaydroid import button, device, tap, swipe
import time


device.connect()


battery_info = device.battery_info()

print(battery_info)


