import keyboard
import mouse
import pyautogui
import time
from configuration import MouseConfiguration
from controller import click, double_click, focus_cabal, log

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
cfg = MouseConfiguration(cfg_dict, "configs/reward_configuration.json")
cfg.load_configuration()
configuration = cfg.configuration

reward_configuration = {
    "FIRST_ROW": 1,
    "SECOND_ROW": 1,
    "THIRD_ROW": 1,
    "FOURTH_ROW": 1,
    "FIFTH_ROW": 1,
}


CH_CONFIRM_PATH = "pics/mission_reward/channel_change_confirm.png"
EQ_PATH = "pics/mission_reward/eq.png"
LAG_TIME = 7.0
channel = configuration["FIRST_CHANNEL"]


def indicate_relog_finish():
    try:
        while pyautogui.locateOnScreen(
            EQ_PATH, confidence=0.9
        ) is None and not keyboard.is_pressed("f12"):
            keyboard.send("i")
            time.sleep(0.2)
        keyboard.send("i")
        time.sleep(0.2)
    except pyautogui.ImageNotFoundException as ex:
        log(f"locate on screen - equipment path - exception: {ex}")


def select_channel():
    counter = 0
    while True:
        keyboard.send("o")
        time.sleep(0.2)
        click(
            configuration["SELECT_CHANNEL"]["X"], configuration["SELECT_CHANNEL"]["Y"]
        )
        time.sleep(0.2)

        decide_channel()
        double_click(channel["X"], channel["Y"])
        time.sleep(0.2)

        try:
            if pyautogui.locateOnScreen(CH_CONFIRM_PATH, confidence=0.9) is not None:
                break
            counter += 1
            if counter > 1:
                break
        except pyautogui.ImageNotFoundException as ex:
            log(f"locate on screen - confirm path - exception: {ex}")


def relog():
    select_channel()

    click(
        configuration["CHANGE_CHANNEL_ACCEPT"]["X"],
        configuration["CHANGE_CHANNEL_ACCEPT"]["Y"],
    )

    start = time.time()

    time.sleep(0.5)

    try:
        indicate_relog_finish()
    except pyautogui.ImageNotFoundException:
        return 0.0

    return time.time() - start


def decide_channel():
    global channel
    if channel == configuration["FIRST_CHANNEL"]:
        channel = configuration["SECOND_CHANNEL"]
    else:
        channel = configuration["FIRST_CHANNEL"]


def collect_rewards():
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

    click(
        configuration["CHALLENGE_MISSION"]["X"], configuration["CHALLENGE_MISSION"]["Y"]
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

    click(configuration["RECEIVE_REWARD"]["X"], configuration["RECEIVE_REWARD"]["Y"])
    click(
        configuration["CHANGE_CHANNEL_ACCEPT"]["X"],
        configuration["CHANGE_CHANNEL_ACCEPT"]["Y"],
    )

    start = time.time()

    time.sleep(0.5)

    try:
        indicate_relog_finish()
    except pyautogui.ImageNotFoundException:
        return 0.0

    return time.time() - start


def main():
    focus_cabal()

    time.sleep(0.5)

    relog_time = relog()

    while not keyboard.is_pressed("f12"):
        print(f"relog time {relog_time}")
        if relog_time < LAG_TIME:
            time.sleep(15)
            relog_time = relog()
        else:
            print("collecting rewards")
            relog_time = collect_rewards()


if __name__ == "__main__":
    main()
