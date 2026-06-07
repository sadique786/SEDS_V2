import yaml
from pathlib import Path


class ConfigManager:

    def __init__(self,
                 config_path="config/config.yaml"):

        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self):

        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def get(self, *keys):

        value = self.config

        for key in keys:
            value = value[key]

        return value
