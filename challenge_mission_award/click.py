import time

import keyboard
import pyautogui

from util.configuration import MouseConfiguration
from util.controller import *

cfg_dict = {
    "CHALLENGE_MISSION": {"X": 0, "Y": 0},
    "REWARD": {"X": 0, "Y": 0},
    "RECEIVE_REWARD": {"X": 0, "Y": 0},
    "FIRST_ROW_1": {"X": 0, "Y": 0},
    "FIRST_ROW_2": {"X": 0, "Y": 0},
    "FIRST_ROW_3": {"X": 0, "Y": 0},
    "FIRST_ROW_4": {"X": 0, "Y": 0},
    "SECOND_ROW_1": {"X": 0, "Y": 0},
    "SECOND_ROW_2": {"X": 0, "Y": 0},
    "SECOND_ROW_3": {"X": 0, "Y": 0},
    "SECOND_ROW_4": {"X": 0, "Y": 0},
    "THIRD_ROW_1": {"X": 0, "Y": 0},
    "THIRD_ROW_2": {"X": 0, "Y": 0},
    "THIRD_ROW_3": {"X": 0, "Y": 0},
    "THIRD_ROW_4": {"X": 0, "Y": 0},
    "SELECT_CHANNEL": {"X": 0, "Y": 0},
    "FIRST_CHANNEL": {"X": 0, "Y": 0},
    "SECOND_CHANNEL": {"X": 0, "Y": 0},
    "CHANGE_CHANNEL_ACCEPT": {"X": 0, "Y": 0},
}
cfg = MouseConfiguration(cfg_dict, "reward_configuration.json")
cfg.load_configuration()
configuration = cfg.configuration

reward_configuration = {
    "FIRST_ROW": 1,
    "SECOND_ROW": 1,
    "THIRD_ROW": 1,
    "FOURTH_ROW": 1,
    "FIFTH_ROW": 1,
}

CH_CONFIRM_PATH = "pics/channel_change_confirm.png"

F5_KEY = 0x3F

channel = configuration["FIRST_CHANNEL"]


def select_channel():
    counter = 0
    while True:
        keyboard.send("o")
        time.sleep(0.3)
        click(
            configuration["SELECT_CHANNEL"]["X"], configuration["SELECT_CHANNEL"]["Y"]
        )
        time.sleep(0.3)

        decide_channel()
        double_click(channel["X"], channel["Y"])
        time.sleep(0.3)

        try:
            if pyautogui.locateOnScreen(CH_CONFIRM_PATH, confidence=0.9) is not None:
                break
            else:
                counter += 1
                if counter > 1:
                    break
        except Exception as ex:
            print(f"locate on screen - confirm path - exception: {ex}")


def decide_channel():
    global channel
    if channel == configuration["FIRST_CHANNEL"]:
        channel = configuration["SECOND_CHANNEL"]
    else:
        channel = configuration["FIRST_CHANNEL"]


def collect_rewards(e):
    row_1 = configuration[
        list(reward_configuration.keys())[0]
        + "_"
        + str(reward_configuration["FIRST_ROW"])
    ]
    row_2 = configuration[
        list(reward_configuration.keys())[1]
        + "_"
        + str(reward_configuration["SECOND_ROW"])
    ]
    row_3 = configuration[
        list(reward_configuration.keys())[2]
        + "_"
        + str(reward_configuration["THIRD_ROW"])
    ]
    row_4 = configuration[
        list(reward_configuration.keys())[2]
        + "_"
        + str(reward_configuration["FOURTH_ROW"])
    ]
    row_5 = configuration[
        list(reward_configuration.keys())[2]
        + "_"
        + str(reward_configuration["FIFTH_ROW"])
    ]

    if e.event_type == "down":
        click(
            configuration["CHALLENGE_MISSION"]["X"],
            configuration["CHALLENGE_MISSION"]["Y"],
        )
        click(configuration["REWARD"]["X"], configuration["REWARD"]["Y"])
        click(row_1["X"], row_1["Y"])
        click(row_2["X"], row_2["Y"])
        click(row_3["X"], row_3["Y"])
        mouse.wheel(-1)
        time.sleep(0.1)
        double_click(row_4["X"], row_4["Y"])
        time.sleep(0.1)
        mouse.wheel(-1)
        double_click(row_5["X"], row_5["Y"])

        select_channel()

        click(
            configuration["RECEIVE_REWARD"]["X"], configuration["RECEIVE_REWARD"]["Y"]
        )
        click(
            configuration["CHANGE_CHANNEL_ACCEPT"]["X"],
            configuration["CHANGE_CHANNEL_ACCEPT"]["Y"],
        )


def main():
    focus_cabal()

    keyboard.hook_key(F5_KEY, collect_rewards, suppress=True)

    while not keyboard.is_pressed("f12"):
        time.sleep(0.5)


if __name__ == "__main__":
    main()
