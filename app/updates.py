import requests
import json
from graphics import Graphics, VERSION

graphics = Graphics()

github_api_endpoint = 'https://api.github.com/repos/Yariya/EarnApp-Earning-Monitor/releases'


def check_for_updates():
    try:
        response = requests.get(github_api_endpoint)
        if response.status_code == 200:
            releases = json.loads(response.content)
            latest_version = releases[0]['tag_name']
            if latest_version > f'v{VERSION}':
                graphics.info("Update Available.")
                graphics.info(
                    "Please download the latest version from below link.")
                graphics.info(
                    f"https://github.com/Yariya/EarnApp-Earning-Monitor/releases/download/{latest_version}/EarnApp-Earning-Monitor.exe")
            else:
                graphics.success("You are on the latest version.")
    except:
        graphics.error("Error checking for updates.")


if __name__ == "__main__":
    check_for_updates()
