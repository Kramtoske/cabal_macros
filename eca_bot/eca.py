import os
import threading
import time

import keyboard
import pyautogui as pygui
import pydirectinput as pyd
import pygetwindow as pyw

import util.controller as controller
from util.controller import send_key

run_combat_thread = True
run_main_loop = True
eca_started = False
pause_event = threading.Event()
internal_pause_event = threading.Event()
pygui.FAILSAFE = False


def stop_all(event=None):
    print("STOPPING...")
    global run_combat_thread
    global run_main_loop
    global eca_started
    global pause_event
    global internal_pause_event
    run_combat_thread = False
    run_main_loop = False
    eca_started = False
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
    pyd.press("f4")


def start():
    global internal_pause_event
    internal_pause_event.wait()
    print("start...")

    start_time = time.time()
    while (
        controller.image_on_screen("pics/enter_button.png", 0.9) is False
        and controller.image_on_screen("pics/cannot_enter.png", 0.9) is False
    ):
        if time.time() - start_time >= 15:
            stop_all()
            print("cannot find enter button")
            os._exit(-1)
        pygui.click(button="left", x=1065, y=583)

    time.sleep(0.2)

    if controller.image_on_screen("pics/cannot_enter.png", 0.9) is True:
        stop_all()
        print("found cannot enter button")
        os._exit(-2)
    time.sleep(0.2)

    if controller.image_click("pics/enter_button.png", 0.9) is False:
        stop_all()
        print("failed to find enter button")
        os._exit(-3)
    time.sleep(0.2)

    pygui.moveTo(1, 1)

    if controller.image_on_screen("pics/challenge_screen.png", 0.9) is False:
        stop_all()
        print("failed to find challenge screen")
        os._exit(-4)
    time.sleep(0.2)

    if controller.image_click("pics/challenge_button.png", 0.9) is False:
        stop_all()
        print("failed to find challenge button")
        os._exit(-5)
    time.sleep(0.2)


def run_to_gate():
    global internal_pause_event
    internal_pause_event.wait()
    print("run to gate...")
    pygui.moveTo(x=41, y=876)
    pyd.press("1", interval=0.6)
    pyd.press("2", interval=0.4)
    pyd.press("1", interval=0.6)
    pyd.press("2", interval=0.4)
    pyd.press("1", interval=0.6)
    pygui.dragTo(x=800, y=864, button="right", duration=0.5)
    time.sleep(0.2)
    pygui.moveTo(x=1250, y=60)
    pyd.press("1", interval=0.6)
    pyd.press("2", interval=0.4)
    pyd.press("1", interval=0.6)
    pyd.press("2", interval=0.4)
    pyd.press("1", interval=0.6)


def kill_gate():
    global internal_pause_event
    internal_pause_event.wait()
    print("kill gate...")

    start_time = time.time()
    while controller.image_on_screen("pics/gate_hp_bar.png", 0.9) is False:
        if time.time() - start_time > 15:
            stop_all()
            print("failed to find gates")
            os._exit(-6)
        pygui.click(button="middle")
        time.sleep(0.1)

    start_time = time.time()
    while controller.image_on_screen("pics/gate_hp_bar.png", 0.9) is True:
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
    global internal_pause_event
    internal_pause_event.wait()
    print("run to center...")
    pygui.moveTo(x=1200, y=51)
    pyd.press("1", interval=0.6)
    pyd.press("2", interval=0.4)
    pyd.press("1", interval=0.6)
    pyd.press("2", interval=0.4)
    pyd.press("1", interval=0.6)


def dead() -> bool:
    return controller.image_on_screen("pics/death_window.png", confidence=0.9)


def resurrect() -> bool:
    if controller.image_click("pics/normal_resurrect.png", 0.9) == False:
        return False
    return controller.image_click("pics/confirmation.png", 0.9)


def exit_dungeon() -> bool:
    if controller.image_click("pics/exit_button.png", 0.9) == False:
        return False
    if controller.image_click("pics/exit_confirmation_button.png", 0.9) == False:
        return False
    return True


def failed() -> bool:
    return controller.image_on_screen("pics/dungeon_failed.png", 0.9)


def dungeon_failed() -> bool:
    return controller.image_click("pics/ok_button.png", 0.9)


def cleared() -> bool:
    return controller.image_on_screen("pics/cleared.png", 0.9)


def exit_after_clear() -> bool:
    if controller.image_click("pics/clear_confirmation.png", 0.9) == False:
        return False
    if controller.image_click("pics/roll_dice.png", 0.9) == False:
        return False
    if controller.image_click("pics/exit_after_clear.png", 0.9) == False:
        return False
    return True


def disconnected() -> bool:
    return controller.image_on_screen(
        "pics/disconnected.png", 0.9
    ) or controller.image_on_screen("pics/account_login.png", 0.9)


def protection_thread(main_pause: threading.Event, internal_pause: threading.Event):
    print("starting protection thread")
    global run_combat_thread
    global run_main_loop
    while run_main_loop:
        internal_pause.wait()
        main_pause.wait()

        if cleared() is True:
            run_combat_thread = False
            pyd.press("space")
            pyd.press("space")
            pyd.press("space")
            pyd.press("space")
            pyd.press("space")
            print(f"cleared!")
            exit_after_clear()

        if failed() is True:
            run_combat_thread = False
            print(f"failed!")
            dungeon_failed()

        if dead() is True:
            run_combat_thread = False
            print(f"dead!")
            resurrect()
            if failed() is True:
                run_combat_thread = False
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
        send_key(merc)
        time.sleep(11)

    start_time = time.time()

    while run_combat_thread:
        internal_pause.wait()
        main_pause.wait()
        if (time.time() - start_time) > 920:
            print("calling mercs")
            for merc in mercs:
                send_key(merc)
                time.sleep(11)
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

        if diff % 240 == 0 and diff > 300 or one_shot_trigger is False:
            send_key("ctrl_8")
            one_shot_trigger = True

        if counter % 10 == 0:
            pygui.click(button="middle")

        counter = counter + 1
        time.sleep(0.1)


def main():
    print("starting...")
    global run_main_loop
    global pause_event
    global internal_pause_event
    global eca_started

    keyboard.on_press_key("f10", pause_all)
    keyboard.on_press_key("f12", stop_all)

    cabal_window = pyw.getWindowsWithTitle("CABAL")[0]
    cabal_window.activate()
    cabal_window.maximize()

    pause_event.set()
    internal_pause_event.set()

    main_threads = [protection_thread]
    main_thread_joins = []
    for thread in main_threads:
        t = threading.Thread(target=thread, args=(pause_event, internal_pause_event))
        t.start()
        main_thread_joins.append(t)

    while run_main_loop:
        pause_event.wait()
        internal_pause_event.wait()
        pygui.PAUSE = 0.1
        pygui.click(button="right", x=1065, y=583)

        if disconnected():
            internal_pause_event.clear()

        init()
        start()

        eca_started = True

        run_to_gate()
        kill_gate()
        run_to_center()
        pygui.PAUSE = 0.001

        print("start threads...")

        combat_threads = [combat_thread, mercenary_thread]
        combat_thread_joins = []
        for thread in combat_threads:
            t = threading.Thread(
                target=thread, args=(pause_event, internal_pause_event)
            )
            t.start()
            combat_thread_joins.append(t)

        for thread_join in combat_thread_joins:
            thread_join.join()

        print("after threads...")

        eca_started = False
        time.sleep(1)
        print("refilling sp...")
        counter = 0
        while run_main_loop and counter < 6:
            send_key("ctrl_8")
            time.sleep(6)
            counter = counter + 1

    for thread_join in main_thread_joins:
        thread_join.join()


main()
