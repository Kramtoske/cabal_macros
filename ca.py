import keyboard
import os
import pyautogui
import pydirectinput
import threading
import time
from controller import image_click, image_on_screen, send_key, focus_cabal

pyautogui.FAILSAFE = False
run_combat_thread = False


def stop_all(_event=None):
    print("STOPPING...")
    os._exit(0)


def init():
    print("init...")
    pydirectinput.press("f4")


def start():
    print("start...")

    start_time = time.time()
    while (
        image_on_screen("pics/ca/enter_button.png", 0.9) is False
        and image_on_screen("pics/ca/cannot_enter.png", 0.9) is False
    ):
        if time.time() - start_time >= 20:
            stop_all()
            print("cannot find enter button")
            os._exit(-1)
        pyautogui.click(button="left", x=1096, y=483)
        time.sleep(3)

    time.sleep(0.5)

    if image_on_screen("pics/ca/cannot_enter.png", 0.9) is True:
        stop_all()
        print("found cannot enter button")
        os._exit(-2)
    time.sleep(0.5)

    if image_click("pics/ca/enter_button.png", 0.9) is False:
        stop_all()
        print("failed to find enter button")
        os._exit(-3)
    time.sleep(0.5)

    pyautogui.moveTo(1, 1)

    if image_on_screen("pics/ca/challenge_screen.png", 0.9) is False:
        stop_all()
        print("failed to find challenge screen")
        os._exit(-4)
    time.sleep(0.5)

    if image_click("pics/ca/challenge_button.png", 0.9) is False:
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


def kill_gate() -> bool:
    print("kill gate...")

    start_time = time.time()
    while image_on_screen("pics/ca/gate_hp_bar.png", 0.9) is False:
        if time.time() - start_time > 15:
            print("failed to find gates")
            return False
        pyautogui.click(button="middle")
        time.sleep(0.1)

    start_time = time.time()
    while image_on_screen("pics/ca/gate_hp_bar.png", 0.9) is True:
        if time.time() - start_time > 30:
            print("failed to kill gates")
            return False
        send_key("3")
        send_key("4")
        send_key("5")
        send_key("6")
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
    return image_on_screen("pics/ca/death_window.png", confidence=0.9)


def resurrect() -> bool:
    if not image_click("pics/ca/normal_resurrect.png", 0.9):
        return False
    return image_click("pics/ca/confirmation.png", 0.9)


def exit_dungeon() -> bool:
    if not image_click("pics/ca/exit_button.png", 0.9):
        return False
    if not image_click("pics/ca/exit_confirmation_button.png", 0.9):
        return False
    return True


def failed() -> bool:
    return image_on_screen("pics/ca/dungeon_failed.png", 0.9)


def dungeon_failed() -> bool:
    return image_click("pics/ca/ok_button.png", 0.9)


def cleared() -> bool:
    return image_on_screen("pics/ca/cleared.png", 0.9)


def exit_after_clear() -> bool:
    if not image_click("pics/ca/clear_confirmation.png", 0.9):
        return False
    if not image_click("pics/ca/roll_dice.png", 0.9):
        return False
    if not image_click("pics/ca/exit_after_clear.png", 0.9):
        return False
    return True


def disconnected() -> bool:
    return image_on_screen("pics/ca/disconnected.png", 0.9) or image_on_screen(
        "pics/ca/account_login.png", 0.9
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
