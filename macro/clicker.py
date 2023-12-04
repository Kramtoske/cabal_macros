import time

import keyboard
import pyautogui

pyautogui.PAUSE = 0.01

while keyboard.is_pressed("f12") is not True:
    pyautogui.click(button="left")
    time.sleep(0.001)
