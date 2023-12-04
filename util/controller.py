from datetime import datetime
from typing import Optional

import mouse
import pyautogui as pygui
import pygetwindow
import pygetwindow as pyw
from pywinauto.application import Application

from util.configuration import MouseConfiguration

cabal_window = pyw.getWindowsWithTitle("CABAL")[0]
cabal_window_controller = (
    Application().connect(title_re="CABAL").window(title_re="CABAL")
)


skill_cfg_dict = {
    "1": {"X": 0, "Y": 0},
    "2": {"X": 0, "Y": 0},
    "3": {"X": 0, "Y": 0},
    "4": {"X": 0, "Y": 0},
    "5": {"X": 0, "Y": 0},
    "6": {"X": 0, "Y": 0},
    "7": {"X": 0, "Y": 0},
    "8": {"X": 0, "Y": 0},
    "9": {"X": 0, "Y": 0},
    "10": {"X": 0, "Y": 0},
    "11": {"X": 0, "Y": 0},
    "12": {"X": 0, "Y": 0},
    "alt_1": {"X": 0, "Y": 0},
    "alt_2": {"X": 0, "Y": 0},
    "alt_3": {"X": 0, "Y": 0},
    "alt_4": {"X": 0, "Y": 0},
    "alt_5": {"X": 0, "Y": 0},
    "alt_6": {"X": 0, "Y": 0},
    "alt_7": {"X": 0, "Y": 0},
    "alt_8": {"X": 0, "Y": 0},
    "alt_9": {"X": 0, "Y": 0},
    "alt_10": {"X": 0, "Y": 0},
    "alt_11": {"X": 0, "Y": 0},
    "alt_12": {"X": 0, "Y": 0},
    "ctrl_1": {"X": 0, "Y": 0},
    "ctrl_2": {"X": 0, "Y": 0},
    "ctrl_3": {"X": 0, "Y": 0},
    "ctrl_4": {"X": 0, "Y": 0},
    "ctrl_5": {"X": 0, "Y": 0},
    "ctrl_6": {"X": 0, "Y": 0},
    "ctrl_7": {"X": 0, "Y": 0},
    "ctrl_8": {"X": 0, "Y": 0},
}

cfg = MouseConfiguration(skill_cfg_dict, "skills.json")
cfg.load_configuration()


def send_key(key):
    if cabal_window.isActive:
        pygui.click(
            button="right",
            x=cfg.configuration[key]["X"],
            y=cfg.configuration[key]["Y"],
            duration=0,
        )


def send_key_background(key):
    cabal_window_controller.click(
        "right", coords=(cfg.configuration[key]["X"], cfg.configuration[key]["Y"] - 25)
    )


def image_on_screen(img: str, confidence: float) -> bool:
    for _ in range(3):
        item = pygui.locateOnScreen(img, confidence=confidence)
        if item is not None:
            return True
    return False


def image_locate(img: str, confidence: float) -> Optional[pygui.Point]:
    for _ in range(3):
        item = pygui.locateCenterOnScreen(image=img, confidence=confidence)
        if item is not None:
            return item
    return None


def image_click(img: str, confidence: float, off_x: int = 0, off_y: int = 0) -> bool:
    item = image_locate(img, confidence)
    if item is not None:
        (
            x,
            y,
        ) = item
        print(f"clicking on x: {x + off_x}, y: {y + off_y}")
        pygui.click(button="left", x=x + off_x, y=y + off_y)
        return True
    return False


def image_double_click(
    img: str, confidence: float, off_x: int = 0, off_y: int = 0
) -> bool:
    item = image_locate(img, confidence)
    if item is not None:
        (
            x,
            y,
        ) = item
        print(f"clicking on x: {x + off_x}, y: {y + off_y}")
        pygui.doubleClick(button="left", x=x + off_x, y=y + off_y)
        return True
    return False


def click(x, y):
    mouse.move(x, y)
    mouse.click(button=mouse.LEFT)


def double_click(x, y):
    mouse.move(x, y)
    mouse.double_click(button=mouse.LEFT)


def focus_cabal():
    cabal_window = pygetwindow.getWindowsWithTitle("CABAL")[0]
    cabal_window.activate()


def log(msg):
    time_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print_string = f"[{time_str}] {msg}"
    print(print_string)
    # log_file.write(print_string)
