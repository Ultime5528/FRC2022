import win32gui
from win32api import GetSystemMetrics
import os
import time
import ctypes

driver_station_handle = None
driver_station_start_command = r'start "" "C:\Program Files (x86)\FRC Driver Station\DriverStation.exe" '
os.system(driver_station_start_command)
user32 = ctypes.windll
screensize = [GetSystemMetrics(0), GetSystemMetrics(1)]

def winEnumHandler(handle, ctx):
    global driver_station_handle
    if win32gui.IsWindowVisible(handle) and "FRC Driver Station" in win32gui.GetWindowText(handle):
        driver_station_handle = handle

while not driver_station_handle:
    win32gui.EnumWindows(winEnumHandler, None)
    time.sleep(1)

if driver_station_handle:
    print("Found DriverStation")
    print(screensize)
    driver_station_rect = win32gui.GetWindowRect(driver_station_handle)
    win32gui.MoveWindow(driver_station_handle, 0, 0, 500, 500, True)
