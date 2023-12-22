import keyboard
import pyautogui
import pygetwindow
import time

cabal_window = pygetwindow.getWindowsWithTitle("CABAL")[0]
cabal_window.activate()

counter = 0

while not keyboard.is_pressed("f12"):
    if cabal_window.isActive:
        keyboard.send("3")
        keyboard.send("4")
        keyboard.send("5")
        if counter % 3 == 0:
            pyautogui.click(button="middle")
        keyboard.send("space")
        counter = counter + 1
    time.sleep(0.5)
