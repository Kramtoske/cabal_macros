import controller
import keyboard
import os
import pyautogui
import pydirectinput
import threading
import time

run_combat_thread = True
run_main_loop = True
pause_event = threading.Event()
internal_pause_event = threading.Event()
pyautogui.FAILSAFE = False


def stop(reason: str, code: int):
    print(f"Exiting with code {code}. Reason {reason}")
    os._exit(code)


def stop_all(_event=None):
    stop("Stop button pressed", 0)


def pause_all(_event=None):
    if pause_event.is_set():
        print("PAUSING...")
        pause_event.clear()
    else:
        pause_event.set()
        print("UNPAUSING...")


def init():
    internal_pause_event.wait()
    print("init...")
    pydirectinput.press("f4")


def start():
    internal_pause_event.wait()
    print("start...")

    start_time = time.time()
    while not controller.image_on_screen("pics/dungeon_window.png", 0.9):
        if time.time() - start_time >= 15:
            stop("cannot find dungeon entry", -1)
        pyautogui.click(button="left", x=1065, y=583)

    time.sleep(0.5)

    if not controller.image_click("pics/enter_button.png", 0.9):
        stop("failed to find enter button", -3)
    time.sleep(0.5)

    pyautogui.moveTo(1, 1)

    if not controller.image_on_screen("pics/challenge_screen.png", 0.9):
        stop("failed to find challenge screen", -4)
    time.sleep(0.5)

    if not controller.image_click("pics/challenge_button.png", 0.9):
        stop("failed to find challenge button", -5)
    time.sleep(0.5)


def run_to_gate():
    internal_pause_event.wait()
    print("run to gate...")
    pyautogui.moveTo(x=41, y=876)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pyautogui.dragTo(x=190, y=864, button="right", duration=0.5)
    time.sleep(0.5)
    pyautogui.moveTo(x=1300, y=160)
    time.sleep(1)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)


def kill_gate() -> bool:
    internal_pause_event.wait()
    print("kill gate...")

    start_time = time.time()
    while not controller.image_on_screen("pics/gate_hp_bar.png", 0.9):
        if time.time() - start_time > 15:
            print("failed to find gates")
            return False
        pyautogui.click(button="middle")
        time.sleep(0.1)

    start_time = time.time()
    while controller.image_on_screen("pics/gate_hp_bar.png", 0.9):
        if time.time() - start_time > 30:
            print("failed to kill gates")
            return False
        controller.press_skillbar("3")
        controller.press_skillbar("4")
        controller.press_skillbar("5")
        controller.press_skillbar("6")
        time.sleep(0.1)

    return True


def run_to_center():
    internal_pause_event.wait()
    print("run to center...")
    pyautogui.moveTo(x=1280, y=200)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)


def dead() -> bool:
    return controller.image_on_screen("pics/death_window.png", confidence=0.9)


def resurrect() -> bool:
    if not controller.image_click("pics/normal_resurrect.png", 0.9):
        return False
    time.sleep(0.5)
    return controller.image_click("pics/confirmation.png", 0.9)


def exit_dungeon() -> bool:
    if not controller.image_click("pics/exit_button.png", 0.9):
        return False
    time.sleep(0.5)
    return controller.image_click("pics/exit_confirmation_button.png", 0.9)


def failed() -> bool:
    return controller.image_on_screen("pics/dungeon_failed.png", 0.9)


def dungeon_failed() -> bool:
    return controller.image_click("pics/ok_button.png", 0.9)


def cleared() -> bool:
    return controller.image_on_screen("pics/cleared.png", 0.9)


def exit_after_clear() -> bool:
    if not controller.image_click("pics/clear_confirmation.png", 0.9):
        return False
    time.sleep(0.5)
    if not controller.image_click("pics/roll_dice.png", 0.9):
        return False
    time.sleep(0.5)
    return controller.image_click("pics/exit_after_clear.png", 0.9)


def disconnected() -> bool:
    return controller.image_on_screen(
        "pics/disconnected.png", 0.9
    ) or controller.image_on_screen("pics/account_login.png", 0.9)


def cancel_bm():
    print("canceling bm")
    time.sleep(0.1)
    pyautogui.click(button="right", x=196, y=122)
    time.sleep(0.1)
    pyautogui.click(button="right", x=196, y=122)
    time.sleep(0.1)
    pyautogui.click(button="right", x=196, y=122)
    time.sleep(0.1)


def protection_thread_func(
    main_pause: threading.Event, internal_pause: threading.Event
):
    print("starting protection thread")
    global run_combat_thread
    while run_main_loop:
        internal_pause.wait()
        main_pause.wait()

        if cleared():
            run_combat_thread = False
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            pydirectinput.press("space")
            print("cleared!")
            cancel_bm()
            exit_after_clear()

        if failed():
            run_combat_thread = False
            print("failed!")
            dungeon_failed()

        if dead():
            run_combat_thread = False
            print("dead!")
            resurrect()
            time.sleep(0.5)
            if failed():
                print("failed!")
                dungeon_failed()
            else:
                exit_dungeon()
        time.sleep(0.1)


def mercenary_thread(main_pause: threading.Event, internal_pause: threading.Event):
    print("starting mercenary thread")
    mercs = ["alt_1", "alt_2"]
    print("calling mercs")
    for merc in mercs:
        controller.press_skillbar(merc)
        time.sleep(15)

    start_time = time.time()
    while run_combat_thread:
        internal_pause.wait()
        main_pause.wait()
        if (time.time() - start_time) > 940:
            print("calling mercs")
            for merc in mercs:
                controller.press_skillbar(merc)
                time.sleep(15)
            break
        time.sleep(0.1)

def buff_thread(main_pause: threading.Event, internal_pause: threading.Event):
    print("starting buff thread")
    buffs = ["alt_6", "alt_7", "alt_8", "alt_9"]
    print("buff ")
    for buff in buffs:
        controller.press_skillbar(buff)
        time.sleep(2)

    start_time = time.time()
    while run_combat_thread:
        internal_pause.wait()
        main_pause.wait()
        if (time.time() - start_time) > 1800:
            print("buffing")
            for buff in buffs:
                controller.press_skillbar(buff)
                time.sleep(2)
            break
        time.sleep(0.1)

def combat_thread(main_pause: threading.Event, internal_pause: threading.Event):
    print("starting combat thread")
    global run_combat_thread
    start_time = time.time()
    counter = 0
    run_combat_thread = True
    while run_combat_thread and run_main_loop:
        internal_pause.wait()
        main_pause.wait()
        diff = time.time() - start_time

        controller.press_skillbar("3")
        controller.press_skillbar("4")
        controller.press_skillbar("5")
        controller.press_skillbar("6")

        controller.press_skillbar("8")
        controller.press_skillbar("9")

        controller.press_skillbar("alt_3")
        controller.press_skillbar("alt_4")
        controller.press_skillbar("alt_5")

        if diff > 600:
            controller.press_skillbar("7")

        if counter % 10 == 0:
            if diff > 1080:
                if not controller.image_on_screen("pics/boss_icon.png", 0.9):
                    pyautogui.click(button="middle")
            else:
                pyautogui.click(button="middle")

        counter = counter + 1
        time.sleep(0.1)


def main():
    print("starting...")

    keyboard.on_press_key("f10", pause_all)
    keyboard.on_press_key("f12", stop_all)

    controller.focus_cabal()

    pause_event.set()
    internal_pause_event.set()

    protection_thread = threading.Thread(
        target=protection_thread_func, args=(pause_event, internal_pause_event)
    )
    protection_thread.start()

    while run_main_loop:
        pause_event.wait()
        internal_pause_event.wait()
        pyautogui.PAUSE = 0.1
        pyautogui.click(button="right", x=1065, y=583)

        if disconnected():
            internal_pause_event.clear()
            stop("Disconnected!", -6)

        init()
        start()
        run_to_gate()

        if not kill_gate():
            exit_dungeon()
            continue

        run_to_center()
        pyautogui.PAUSE = 0.001

        print("start threads...")

        combat_thread_joins = []
        for thread in [combat_thread, mercenary_thread , buff_thread]:
            t = threading.Thread(
                target=thread, args=(pause_event, internal_pause_event)
            )
            t.start()
            combat_thread_joins.append(t)

        for thread_join in combat_thread_joins:
            thread_join.join()

        print("after threads...")
        time.sleep(5)
        print("refilling sp...")
        counter = 0
        while run_main_loop and counter < 6:
            controller.press_skillbar("alt_10")
            time.sleep(6)
            counter = counter + 1

        time.sleep(3)
        cancel_bm()
        time.sleep(3)

    protection_thread.join()


main()
