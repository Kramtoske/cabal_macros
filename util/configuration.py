import json

import mouse


class MouseConfiguration:
    def __init__(self, cfg, path):
        self.configuration = cfg
        self.path = path
        self.load_configuration()

    def load_configuration(self):
        try:
            print("Loading configuration...")
            with open(self.path, "r", encoding="utf-8") as f:
                self.configuration.update(json.load(f))
            print("Configuration loaded!")
        except:
            print("No configuration file found - creating one")
            self.save_configuration()

    def save_configuration(self):
        for key in self.configuration:
            print(f"Right click on {key}")
            mouse.wait(button=mouse.RIGHT, target_types=(mouse.DOWN))
            self.configuration[key]["X"] = mouse.get_position()[0]
            self.configuration[key]["Y"] = mouse.get_position()[1]

        print("Saving configuration...")
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.configuration, f)
        print("Configuration saved!")
