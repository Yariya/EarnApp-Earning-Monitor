from sys import exit
from config import Configuration
from colorama import init
from graphics import Graphics
from webhooks import WebhookTemplate
from time import sleep
from datetime import datetime, timezone
from functions import *
from pyEarnapp import EarnApp
from pyEarnapp.errors import *
from updates import check_for_updates

# initiallise colorama
init(autoreset=True)

try:
    # Initiallise graphics
    graphics = Graphics()
    graphics.print_app_title()

    # get configurations
    config = Configuration()
    graphics.success("Configurations Loaded.")

    # initiallise earnapp
    api = EarnApp(config.AUTH)
    graphics.success("Earnapp Earning Monitor Started.")

    webhook_templates = WebhookTemplate()
except (KeyboardInterrupt, SystemExit):
    graphics.warn("Received exit signal!")
    exit()


def main():
    graphics.info("Checking for updates.")
    if check_for_updates():
        webhook_templates.update_available(config.WEBHOOK_URL)
    global info, device_status_change
    try:
        # Earnapp
        info = AllInformation(config.WEBHOOK_URL, api, graphics)
        # Discord Webhook
        test_discord_webhook(graphics, config.WEBHOOK_URL)
    except AuthenticationError:
        graphics.error("Looks like a wrong oauth-refresh-token.")
        exit()
    try:
        config.AUTO_REDEEM = float(config.AUTO_REDEEM)
        if config.AUTO_REDEEM > 0 and config.AUTO_REDEEM < 2.5:
            raise ValueError()

    except:
        graphics.error("Value must be positive an integer and at least 2.5!")
        exit()

    display_initial_info(graphics, info)
    webhook_templates.send_first_message(info)

    info.previous_balance = info.earnings_info.balance
    info.previous_number_of_transactions = info.transaction_info.total_transactions
    info.previous_bandwidth_usage = info.devices_info.total_bandwidth_usage

    next_update_in(config.DELAY, graphics)



    # Offline devices
    offline_change = 0
    device_status_change = []

    def offline_device_len() -> int:
        x = 0
        all = info.device_status
        for i in all:
            if not all[i]["online"]:
                x += 1
        return x

    def device_changes():
        nonlocal offline_change
        global device_status_change
        offline_change = offline_device_len()
        device_status_change = info.device_status

    device_changes()

    while 1:
        # run every hour at *:05 UTC
        if datetime.now(timezone.utc).strftime("%M") == str(f"{config.DELAY+3:02}"):
            info.get_info()

            # initialise locals
            balance_change = 0
            traffic_change = 0

            bandwidth = round(info.devices_info.total_bandwidth_usage / (1024 ** 2), 2)

            def calculate_changes():
                nonlocal balance_change, traffic_change
                # calculate changes
                balance_change = round(info.earnings_info.balance - info.previous_balance, 2)
                traffic_change = round((info.devices_info.total_bandwidth_usage - info.previous_bandwidth_usage) / (1024 ** 2), 2)
                print(balance_change, traffic_change)
            calculate_changes()



            if offline_device_len() > offline_change:
                # x Devices just got offline
                off = []
                for token in info.device_status:
                    if device_status_change[token] is not info.devices_info[token]:
                        off.append(token)
                graphics.warn(f"{offline_device_len() - offline_change} Device(s) just went offline!\n")
                print("\t (offline)\n".join(off))
                device_changes()
                webhook_templates.device_gone_offline(info, offline_device_len() - offline_change, off)


            if balance_change != 0:
                # After a redeem request, the initial balance & initial traffic is assumed to be 0.
                if info.earnings_info.balance < info.previous_balance:
                    info.previous_balance = 0
                    info.previous_bandwidth_usage = 0
                    calculate_changes()
                graphics.balance_increased("Balance Updated.")
                graphics.balance_increased(f"+{balance_change}$")
                graphics.balance_increased(f"Traffic +{traffic_change}MB")
            else:
                graphics.balance_unchanged(
                    f"Your balance has not changed. Current balance: {info.earnings_info.balance}")
                graphics.balance_unchanged(
                    f"No traffic change detected. Current bandwidth usage: {bandwidth} MB")
            webhook_templates.balance_update(info)


            # new redeem request
            graphics.info(
                f"Number of transactions: {info.transaction_info.total_transactions}")

            if check_redeem_requests(graphics, info, webhook_templates):
                webhook_templates.new_transaction(info)

            # update historical data
            info.previous_balance = info.earnings_info.balance
            info.previous_number_of_transactions = info.transaction_info.total_transactions
            info.previous_bandwidth_usage = info.devices_info.total_bandwidth_usage

            # wait for the minute to end
            if check_for_updates():
                webhook_templates.update_available(config.WEBHOOK_URL)
            sleep(120)
        # Delay to check if it's time to ping earnapp
        sleep(10)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        graphics.warn("Received exit signal!")
        exit()
