import os


class Configuration:
    def __init__(self) -> None:
        self.AUTH = (input("Enter the oauth-refresh-token from EarnApp dashboard\n\t: ")
                     if os.environ.get("AUTH") is None else os.environ.get("AUTH"))

        # time to wait in seconds after the UTC time at which EarnApp Updates
        self.DELAY = (60 if os.environ.get("DELAY")
                      is None else int(os.environ.get("DELAY")))

        self.WEBHOOK_URL = (input("Enter the Discord WebHook URL\n\t: ") if os.environ.get(
            "WEBHOOK_URL") is None else os.environ.get("WEBHOOK_URL"))

if __name__ == "__main__":
    config = Configuration()