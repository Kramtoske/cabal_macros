import time

import keyboard
import pygetwindow

cabal_window = pygetwindow.getWindowsWithTitle("CABAL")[0]
cabal_window.activate()

counter = 0

while not keyboard.is_pressed("f12"):
    if cabal_window.isActive:
        keyboard.send("4")
        keyboard.send("5")
        keyboard.send("6")
        keyboard.send("7")
        if counter % 3 == 0:
            keyboard.send("z")
        keyboard.send("space")
        counter = counter + 1
    time.sleep(0.5)
