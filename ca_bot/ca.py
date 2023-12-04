import os
import threading
import time

import keyboard
import pyautogui
import pydirectinput
import pygetwindow

from util.controller import image_click, image_on_screen, send_key

pyautogui.FAILSAFE = False
run_combat_thread = False


def stop_all(_event=None):
    print("STOPPING...")
    os._exit(0)


def pause_all(_event=None):
    print("PAUSING...")


def init():
    print("init...")
    pydirectinput.press("f4")


def start():
    print("start...")

    start_time = time.time()
    while (
        image_on_screen("pics/enter_button.png", 0.9) is False
        and image_on_screen("pics/cannot_enter.png", 0.9) is False
    ):
        if time.time() - start_time >= 20:
            stop_all()
            print("cannot find enter button")
            os._exit(-1)
        pyautogui.click(button="left", x=1096, y=483)
        time.sleep(3)

    time.sleep(0.5)

    if image_on_screen("pics/cannot_enter.png", 0.9) is True:
        stop_all()
        print("found cannot enter button")
        os._exit(-2)
    time.sleep(0.5)

    if image_click("pics/enter_button.png", 0.9) is False:
        stop_all()
        print("failed to find enter button")
        os._exit(-3)
    time.sleep(0.5)

    pyautogui.moveTo(1, 1)

    if image_on_screen("pics/challenge_screen.png", 0.9) is False:
        stop_all()
        print("failed to find challenge screen")
        os._exit(-4)
    time.sleep(0.5)

    if image_click("pics/challenge_button.png", 0.9) is False:
        stop_all()
        print("failed to find challenge button")
        os._exit(-5)
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


def kill_gate():
    print("kill gate...")

    start_time = time.time()
    while image_on_screen("pics/gate_hp_bar.png", 0.9) is False:
        if time.time() - start_time > 15:
            stop_all()
            print("failed to find gates")
            os._exit(-6)
        pyautogui.click(button="middle")
        time.sleep(0.1)

    start_time = time.time()
    while image_on_screen("pics/gate_hp_bar.png", 0.9) is True:
        if time.time() - start_time > 30:
            stop_all()
            print("failed to kill gates")
            os._exit(-7)
        send_key("3")
        send_key("4")
        send_key("5")
        send_key("6")
        time.sleep(0.1)


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
            os._exit(-6)

        time.sleep(0.1)


def mercenary_thread():
    print("starting mercenary thread")
    mercs = ["alt_1", "alt_2"]
    print("calling mercs")
    for merc in mercs:
        send_key(merc)
        time.sleep(11)


def combat_thread():
    print("starting combat thread")
    global run_combat_thread
    start_time = time.time()
    counter = 0
    run_combat_thread = True
    while run_combat_thread:
        diff = time.time() - start_time

        send_key("3")
        send_key("4")
        send_key("5")
        send_key("6")

        send_key("8")
        send_key("9")

        send_key("alt_3")
        send_key("alt_4")
        send_key("alt_5")
        send_key("alt_6")
        send_key("alt_7")

        if diff > 300:
            send_key("7")

        if counter % 10 == 0:
            pyautogui.click(button="middle")

        counter = counter + 1
        time.sleep(0.1)


def main():
    print("starting...")

    keyboard.on_press_key("f10", pause_all)
    keyboard.on_press_key("f12", stop_all)

    cabal_window = pygetwindow.getWindowsWithTitle("CABAL")[0]
    cabal_window.activate()
    cabal_window.maximize()

    threading.Thread(target=protection_thread).start()

    while True:
        pyautogui.PAUSE = 0.1
        # cancel bm if any
        pyautogui.click(button="right", x=196, y=122)
        time.sleep(2)

        pyautogui.click(button="right", x=1096, y=483)

        init()
        start()
        run_to_gate()
        kill_gate()
        run_to_center()

        pyautogui.PAUSE = 0.001

        print("start threads...")

        combat_thread_joins = []
        for thread in [combat_thread, mercenary_thread]:
            t = threading.Thread(target=thread)
            t.start()
            combat_thread_joins.append(t)

        for thread_join in combat_thread_joins:
            thread_join.join()

        time.sleep(3)


main()
