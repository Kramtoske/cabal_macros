import controller
import keyboard
import os
import pyautogui
import threading
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.001


def stop(reason: str, code: int):
    print(f"Exiting with code {code}. Reason {reason}")
    os._exit(code)


def stop_all(_event=None):
    stop("Stop button pressed", 0)


def dead() -> bool:
    return controller.image_on_screen("pics/death_window.png", confidence=0.9)


def click_every_pixel(coords):
    left, top, width, height = coords
    for x in range(left, left + width):
        for y in range(top, top + height):
            pyautogui.click(x, y)
            time.sleep(0.01)


def resurrect() -> bool:
    if not controller.image_click("pics/normal_resurrect.png", 0.9):
        return False
    time.sleep(0.5)
    if not controller.image_click("pics/confirmation.png", 0.9):
        return False
    pyautogui.click(button="left", x=1443, y=694)
    pyautogui.click(button="left", x=1447, y=717)
    click_every_pixel((1202,584,300,300))
    return True


def protection_thread_func():
    while True:
        if dead():
            resurrect()
        time.sleep(0.1)


def combat_thread():
    while True:
        controller.press_skillbar("3")
        controller.press_skillbar("4")
        controller.press_skillbar("5")
        controller.press_skillbar("alt_3")
        controller.press_skillbar("alt_4")
        controller.press_skillbar("alt_5")
        controller.press_skillbar("alt_6")
        controller.press_skillbar("alt_7")
        pyautogui.click(button="middle")
        time.sleep(0.1)


def main():
    keyboard.on_press_key("f12", stop_all)
    controller.focus_cabal()
    combat_thread_joins = []
    for thread in [combat_thread, protection_thread_func]:
        t = threading.Thread(target=thread)
        t.start()
        combat_thread_joins.append(t)

    for thread_join in combat_thread_joins:
        thread_join.join()


main()
