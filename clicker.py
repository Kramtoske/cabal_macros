import keyboard
import pyautogui
import time

pyautogui.PAUSE = 0.01

while keyboard.is_pressed("f12") is not True:
    pyautogui.click(button="left")
    time.sleep(0.001)
