import pygetwindow
import os
import time
import webbrowser
from colorama import Fore
from pathlib import Path
import subprocess
import mouse

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

os.system("cls")
os.startfile(r"C:\Program Files (x86)\FRC Driver Station\DriverStation.exe")

time.sleep(1)
DriverStation = None
while not DriverStation:
    try:
        DriverStation = pygetwindow.getWindowsWithTitle("FRC Driver Station")[0]
    except IndexError:
        print('FRC Driver Station not detected')
        time.sleep(0.1)

DriverStation.moveTo(0, 0)
time.sleep(0.75)
DriverStation.maximize()

subprocess.Popen(str(Path(r"dashboard\pynetworktables2js.exe").absolute()) + " --team 5528")
time.sleep(1)
webbrowser.get(chrome_path).open_new_tab(r"http://localhost:8888")
time.sleep(1)
print(pygetwindow.getAllTitles())

Browser = None
while Browser is None:
    try:
        Browser = pygetwindow.getWindowsWithTitle("My Robot Dashboard! - Google Chrome")[0]
        print(Browser)
    except IndexError:
        print('Chrome not detected')
        time.sleep(0.1)

print("Resizing Chrome")
time.sleep(1)
Browser.minimize()
Browser.resizeTo(1546, 603)