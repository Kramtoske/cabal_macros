import keyboard
import pyautogui
import pygetwindow as pyw
import time
from configuration import MouseConfiguration

pyautogui.PAUSE = 0.01
cabal_window = pyw.getWindowsWithTitle("CABAL")[0]

cfg = {
    "first_inventory": {"X": 0, "Y": 0},
    "time_reducer": {"X": 0, "Y": 0},
    "arrow_up": {"X": 0, "Y": 0},
    "walking_area": {"X": 0, "Y": 0},
    "use_time_reducer": {"X": 0, "Y": 0},
}
config = MouseConfiguration(cfg, "configs/bm2.json")
config.load_configuration()
cfg = config.configuration


def bm2(event=None):
    if not cabal_window.isActive:
        return
    # remove all windows
    keyboard.send("esc")
    keyboard.send("esc")
    keyboard.send("esc")
    time.sleep(0.2)

    # open inv
    keyboard.send("i")
    time.sleep(0.2)

    # open inventory 1
    pyautogui.click(
        cfg["first_inventory"]["X"], cfg["first_inventory"]["Y"], button="left"
    )

    # right click on time reducer
    pyautogui.click(cfg["time_reducer"]["X"], cfg["time_reducer"]["Y"], button="right")

    # delete inserted number
    keyboard.send("del")
    keyboard.send("del")
    keyboard.send("del")
    keyboard.send("backspace")
    keyboard.send("backspace")
    keyboard.send("backspace")
    time.sleep(0.2)

    # # insert 1
    pyautogui.click(cfg["arrow_up"]["X"], cfg["arrow_up"]["Y"], button="left")

    # press walk
    pyautogui.click(cfg["walking_area"]["X"], cfg["walking_area"]["Y"], button="left")
    pyautogui.click(cfg["walking_area"]["X"], cfg["walking_area"]["Y"], button="left")
    time.sleep(0.2)

    # bm
    keyboard.send("=")
    time.sleep(0.2)

    # press use time reducer
    pyautogui.click(
        cfg["use_time_reducer"]["X"], cfg["use_time_reducer"]["Y"], button="left"
    )


keyboard.on_press_key("f5", bm2)

while not keyboard.is_pressed("f11"):
    time.sleep(1)
