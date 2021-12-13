import os
import io
import json


class Configuration:
    def __init__(self) -> None:
        self.check_for_existing_config()
        # if config doesn't exist
        if self.config_file_exists:
            self.__want_to_reset_config()
            if self.__reuse_config == True:
                self.load_config()
            else:
                self.ask_config()
        else:
            self.ask_config()

    def ask_config(self):
        self.AUTH = (input("Enter the oauth-refresh-token from EarnApp dashboard\n\t: ")
                     if os.environ.get("AUTH") is None else os.environ.get("AUTH"))

        # time to wait in seconds after the UTC time at which EarnApp Updates
        self.DELAY = (60 if os.environ.get("DELAY")
                      is None else int(os.environ.get("DELAY")))

        self.WEBHOOK_URL = (input("Enter the Discord WebHook URL\n\t: ") if os.environ.get(
            "WEBHOOK_URL") is None else os.environ.get("WEBHOOK_URL"))
        self.create_config()

    def __want_to_reset_config(self):
        got_response = False
        while(not got_response):
            response = input("Want to use existing configuration? (y/n): ")
            if response.lower() == "yes" or response.lower() == "y" or response.lower() == "Y":
                got_response = True
                self.__reuse_config = True
            elif response.lower() == "no" or response.lower() == "n" or response.lower() == "N":
                got_response = True
                self.__reuse_config = False
            else:
                print("Didn't quiet understand, try again!")

    def check_for_existing_config(self):
        self.home_directory = os.path.expanduser("~")
        self.program_data_folder = ".earnapp-earning-monitor"
        self.config_file_name = "config.json"

        self.program_directory = os.path.join(
            self.home_directory, self.program_data_folder)
        self.config_file_path = os.path.join(
            self.program_directory, self.config_file_name)

        self.config_file_exists = os.path.exists(self.config_file_path)

    def create_config(self):
        # If config file doesn't exist
        if not self.config_file_exists:
            # If direcotry doesn't exist, create dir
            if not os.path.exists(self.program_directory):
                os.mkdir(self.program_directory)
        config = {
            "AUTH": self.AUTH,
            "DELAY": self.DELAY,
            "WEBHOOK_URL": self.WEBHOOK_URL
        }
        with io.open(self.config_file_path, "w", encoding="utf-8") as stream:
            json.dump(config, stream, indent=0)

    def load_config(self):
        with io.open(self.config_file_path, "r", encoding="utf-8") as stream:
            config_data = json.load(stream)
            self.AUTH = config_data["AUTH"]
            self.DELAY = config_data["DELAY"]
            self.WEBHOOK_URL = config_data["WEBHOOK_URL"]


if __name__ == "__main__":
    config = Configuration()
