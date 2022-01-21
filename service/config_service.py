import yaml


class ConfigService:

    def __init__(self):
        self.configs = self.__get_configs()

    def get_configs(self):
        """
        Returns a dict of config values loaded from a file.
        """
        return self.configs

    @staticmethod
    def __get_configs():
        try:
            with open("config/config.yaml", "r") as f:
                return yaml.safe_load(f)
        finally:
            f.close()
