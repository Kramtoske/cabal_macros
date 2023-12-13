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


def stop_all(event=None):
    print("STOPPING...")
    global run_combat_thread
    global run_main_loop
    global pause_event
    global internal_pause_event
    run_combat_thread = False
    run_main_loop = False
    pause_event.set()
    internal_pause_event.set()
    os._exit(0)


def pause_all(event=None):
    if pause_event.is_set():
        print("PAUSING...")
        pause_event.clear()
    else:
        pause_event.set()
        print("UNPAUSING...")


def init():
    global internal_pause_event
    internal_pause_event.wait()
    print("init...")
    pydirectinput.press("f4")


def start():
    global internal_pause_event
    internal_pause_event.wait()
    print("start...")

    start_time = time.time()
    while not controller.image_on_screen(
        "pics/enter_button.png", 0.9
    ) and not controller.image_on_screen("pics/cannot_enter.png", 0.9):
        if time.time() - start_time >= 15:
            stop_all()
            print("cannot find enter button")
            os._exit(-1)
        pyautogui.click(button="left", x=1065, y=583)

    time.sleep(0.5)

    if controller.image_on_screen("pics/cannot_enter.png", 0.9):
        stop_all()
        print("found cannot enter button")
        os._exit(-2)
    time.sleep(0.5)

    if not controller.image_click("pics/enter_button.png", 0.9):
        stop_all()
        print("failed to find enter button")
        os._exit(-3)
    time.sleep(0.5)

    pyautogui.moveTo(1, 1)

    if not controller.image_on_screen("pics/challenge_screen.png", 0.9):
        stop_all()
        print("failed to find challenge screen")
        os._exit(-4)
    time.sleep(0.5)

    if not controller.image_click("pics/challenge_button.png", 0.9):
        stop_all()
        print("failed to find challenge button")
        os._exit(-5)
    time.sleep(0.5)


def run_to_gate():
    global internal_pause_event
    internal_pause_event.wait()
    print("run to gate...")
    pyautogui.moveTo(x=41, y=876)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pyautogui.dragTo(x=800, y=864, button="right", duration=0.5)
    time.sleep(0.5)
    pyautogui.moveTo(x=1250, y=60)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)
    pydirectinput.press("2", interval=0.4)
    pydirectinput.press("1", interval=0.6)


def kill_gate() -> bool:
    global internal_pause_event
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
        controller.send_key("3")
        controller.send_key("4")
        controller.send_key("5")
        controller.send_key("6")
        time.sleep(0.1)

    return True


def run_to_center():
    global internal_pause_event
    internal_pause_event.wait()
    print("run to center...")
    pyautogui.moveTo(x=1200, y=51)
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


def protection_thread_func(
    main_pause: threading.Event, internal_pause: threading.Event
):
    print("starting protection thread")
    global run_combat_thread
    global run_main_loop
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
            print(f"cleared!")
            exit_after_clear()

        if failed():
            run_combat_thread = False
            print(f"failed!")
            dungeon_failed()

        if dead():
            run_combat_thread = False
            print(f"dead!")
            resurrect()
            time.sleep(0.5)
            if failed():
                print(f"failed!")
                dungeon_failed()
            else:
                exit_dungeon()
        time.sleep(0.1)


def mercenary_thread(main_pause: threading.Event, internal_pause: threading.Event):
    print("starting mercenary thread")
    global run_combat_thread
    mercs = ["alt_1", "alt_2"]
    print("calling mercs")
    for merc in mercs:
        controller.send_key(merc)
        time.sleep(12)

    start_time = time.time()

    while run_combat_thread:
        internal_pause.wait()
        main_pause.wait()
        if (time.time() - start_time) > 920:
            print("calling mercs")
            for merc in mercs:
                controller.send_key(merc)
                time.sleep(12)
            break
        time.sleep(0.1)


def combat_thread(main_pause: threading.Event, internal_pause: threading.Event):
    print("starting combat thread")
    global run_combat_thread
    global run_main_loop
    start_time = time.time()
    counter = 0
    run_combat_thread = True
    one_shot_trigger = False
    while run_combat_thread and run_main_loop:
        internal_pause.wait()
        main_pause.wait()
        diff = time.time() - start_time

        controller.send_key("3")
        controller.send_key("4")
        controller.send_key("5")
        controller.send_key("6")

        controller.send_key("8")
        controller.send_key("9")

        controller.send_key("alt_3")
        controller.send_key("alt_4")
        controller.send_key("alt_5")
        controller.send_key("alt_6")
        controller.send_key("alt_7")

        if diff > 300:
            controller.send_key("7")

        if diff % 240 == 0 and diff > 300 or not one_shot_trigger:
            controller.send_key("ctrl_8")
            one_shot_trigger = True

        if counter % 10 == 0:
            pyautogui.click(button="middle")

        counter = counter + 1
        time.sleep(0.1)


def main():
    print("starting...")
    global run_main_loop
    global pause_event
    global internal_pause_event

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
            stop_all()

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
        for thread in [combat_thread, mercenary_thread]:
            t = threading.Thread(
                target=thread, args=(pause_event, internal_pause_event)
            )
            t.start()
            combat_thread_joins.append(t)

        for thread_join in combat_thread_joins:
            thread_join.join()

        print("after threads...")

        time.sleep(1)
        print("refilling sp...")
        counter = 0
        while run_main_loop and counter < 6:
            controller.send_key("ctrl_8")
            time.sleep(6)
            counter = counter + 1

    protection_thread.join()


main()
