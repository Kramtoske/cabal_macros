import keyboard
import os
import pyautogui
import pydirectinput
import threading
import time
from controller import (
    image_click,
    image_on_screen,
    press_skillbar,
    focus_cabal,
    mouse_move,
)

pyautogui.FAILSAFE = False
run_combat_thread = False

ca_list = [
    {"X": 1023, "Y": 209},  # ca1
    {"X": 1023, "Y": 231},  # ca2
    {"X": 1023, "Y": 249},  # ca3
    {"X": 1023, "Y": 271},  # ca4
    {"X": 1023, "Y": 288},  # ca5
    {"X": 1023, "Y": 307},  # ca6
    {"X": 1023, "Y": 328},  # ca7
]


def stop(reason: str, code: int):
    print(f"Exiting with code {code}. Reason {reason}")
    os._exit(code)


def stop_all(_event=None):
    stop("Stop button pressed", 0)


def init():
    print("init...")
    pydirectinput.press("f4")


def start():
    print("start...")

    start_time = time.time()
    while not image_on_screen("pics/dungeon_window.png", 0.9):
        if time.time() - start_time >= 20:
            stop("cannot find dungeon entry", -1)
        pyautogui.click(button="left", x=1096, y=483)
        time.sleep(3)

    found_enter_button = False
    for ca in reversed(ca_list):
        pyautogui.click(button="left", x=ca["X"], y=ca["Y"])
        time.sleep(0.5)
        if image_on_screen("pics/enter_button.png", 0.9):
            found_enter_button = True
            break
        else:
            ca_list.remove(ca)
            continue

    if not found_enter_button:
        stop("failed to find enter button", -2)

    if image_click("pics/enter_button.png", 0.9) is False:
        stop("failed to find enter button", -3)
    time.sleep(0.5)

    pyautogui.moveTo(1, 1)

    if image_on_screen("pics/challenge_screen.png", 0.9) is False:
        stop("failed to find challenge screen", -4)
    time.sleep(0.5)

    if image_click("pics/challenge_button.png", 0.9) is False:
        stop("failed to find challenge button", -5)
    time.sleep(0.5)


def run_to_gate():
    print("run to gate...")
    pyautogui.moveTo(x=1833, y=109)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pyautogui.moveTo(x=370, y=148)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)


def kill_gate() -> bool:
    print("kill gate...")

    start_time = time.time()
    while image_on_screen("pics/gate_hp_bar.png", 0.9) is False:
        if time.time() - start_time > 15:
            print("failed to find gates")
            return False
        pyautogui.click(button="middle")
        time.sleep(0.1)

    start_time = time.time()
    while image_on_screen("pics/gate_hp_bar.png", 0.9) is True:
        if time.time() - start_time > 30:
            print("failed to kill gates")
            return False
        press_skillbar("3")
        press_skillbar("4")
        press_skillbar("5")
        press_skillbar("6")
        time.sleep(0.1)
    return True


def run_to_center():
    print("run to center...")
    pyautogui.moveTo(x=450, y=450)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)


def dead() -> bool:
    return image_on_screen("pics/death_window.png", confidence=0.9)


def resurrect() -> bool:
    if not image_click("pics/normal_resurrect.png", 0.9):
        return False
    return image_click("pics/confirmation.png", 0.9)


def exit_dungeon() -> bool:
    if not image_click("pics/exit_button.png", 0.9):
        return False
    if not image_click("pics/exit_confirmation_button.png", 0.9):
        return False
    return True


def failed() -> bool:
    return image_on_screen("pics/dungeon_failed.png", 0.9)


def dungeon_failed() -> bool:
    return image_click("pics/ok_button.png", 0.9)


def cleared() -> bool:
    return image_on_screen("pics/cleared.png", 0.9)


def exit_after_clear() -> bool:
    if not image_click("pics/clear_confirmation.png", 0.9):
        return False
    if not image_click("pics/roll_dice.png", 0.9):
        return False
    if not image_click("pics/exit_after_clear.png", 0.9):
        return False
    return True


def disconnected() -> bool:
    return image_on_screen("pics/disconnected.png", 0.9) or image_on_screen(
        "pics/account_login.png", 0.9
    )


def protection_thread():
    print("starting protection thread")
    global run_combat_thread
    while True:
        if cleared():
            run_combat_thread = False
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            print("cleared!")
            exit_after_clear()

        if failed():
            run_combat_thread = False
            print("failed!")
            dungeon_failed()

        if dead():
            run_combat_thread = False
            print("dead!")
            resurrect()
            if failed():
                run_combat_thread = False
                print("failed!")
                dungeon_failed()
            else:
                exit_dungeon()

        if disconnected():
            run_combat_thread = False
            stop("Disconnected!", -6)

        time.sleep(0.1)


def combat_thread():
    print("starting combat thread")
    global run_combat_thread
    start_time = time.time()
    counter = 0
    run_combat_thread = True
    while run_combat_thread:
        diff = time.time() - start_time

        press_skillbar("3")
        press_skillbar("4")
        press_skillbar("5")
        press_skillbar("6")

        press_skillbar("8")
        press_skillbar("9")

        press_skillbar("alt_3")
        press_skillbar("alt_4")
        press_skillbar("alt_5")
        press_skillbar("alt_6")
        press_skillbar("alt_7")

        if diff > 300:
            press_skillbar("7")

        if counter % 10 == 0:
            pyautogui.click(button="middle")

        counter = counter + 1
        time.sleep(0.1)


def main():
    print("starting...")

    keyboard.on_press_key("f12", stop_all)

    focus_cabal()

    threading.Thread(target=protection_thread).start()

    while True:
        pyautogui.PAUSE = 0.1
        # cancel bm if any
        time.sleep(2)
        pyautogui.click(button="right", x=196, y=122)
        time.sleep(2)
        pyautogui.click(button="right", x=1096, y=483)

        init()
        start()
        run_to_gate()

        if not kill_gate():
            exit_dungeon()
            continue

        run_to_center()

        pyautogui.PAUSE = 0.001

        print("start threads...")
        t = threading.Thread(target=combat_thread)
        t.start()
        t.join()

        time.sleep(5)


main()
