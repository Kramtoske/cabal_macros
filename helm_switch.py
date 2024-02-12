import keyboard
import pyautogui
import pygetwindow as pyw
import time
from configuration import MouseConfiguration

pyautogui.PAUSE = 0.01
cabal_window = pyw.getWindowsWithTitle("CABAL")[0]

cfg = {
    "first_inventory": {"X": 0, "Y": 0},
    "helm_inventory": {"X": 0, "Y": 0},
    "helm_location": {"X": 0, "Y": 0}
}
config = MouseConfiguration(cfg, "configs/helm_switch.json")
config.load_configuration()
cfg = config.configuration


def switch_helm(event=None):
    if not cabal_window.isActive:
        return

    # open inv
    keyboard.send("i")
    time.sleep(0.2)
    x,y = (0,0)
    pos = pyautogui.position()
    if pos:
        x,y = pos

    # open helm inventory
    pyautogui.click(
        cfg["helm_inventory"]["X"], cfg["helm_inventory"]["Y"], button="left"
    )

    # right click on time reducer
    pyautogui.click(cfg["helm_location"]["X"], cfg["helm_location"]["Y"], button="right")

    # open 1st page of inventory
    pyautogui.click(
        cfg["first_inventory"]["X"], cfg["first_inventory"]["Y"], button="left"
    )
    pyautogui.moveTo(x,y)
    keyboard.send("esc")

keyboard.on_press_key("f5", switch_helm)

while not keyboard.is_pressed("f11"):
    time.sleep(1)
