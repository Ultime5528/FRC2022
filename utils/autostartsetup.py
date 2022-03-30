import pygetwindow
import os
import time
import webbrowser
from colorama import Fore
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

os.system("cls")
print(Fore.GREEN)
os.startfile(r"C:\Program Files (x86)\FRC Driver Station\DriverStation.exe")
os.system(r"C:\Users\Admin\Desktop\FRC2022\.dashboard\pynetworktables2js.exe --team 5528")
print(Fore.BLUE + "Waiting" + Fore.RESET)
time.sleep(1)

try:
    DriverStation = pygetwindow.getWindowsWithTitle("FRC Driver Station")[0]
except IndexError:
    print(Fore.RED + 'FRC Driver Station not detected')

DriverStation.moveTo(0, 0)

time.sleep(1)
webbrowser.get(chrome_path).open(r"youtube.com")
print(Fore.RESET)
