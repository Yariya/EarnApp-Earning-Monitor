from logging import info
from pyEarnapp import EarnApp
from pyEarnapp.errors import *
from config import Configuration
from colorama import init
from graphics import Graphics
from webhooks import WebhookTemplate
from time import sleep
from datetime import datetime, timezone
from functions import AllInformation, display_initial_info, test_discord_webhook, check_redeem_requests

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
    global info
    try:
        # Earnapp
        info = AllInformation(config.WEBHOOK_URL, api)
        # Discord Webhook
        test_discord_webhook(graphics, config.WEBHOOK_URL)
    except AuthenticationError:
        graphics.error("Looks like a wrong oauth-refresh-token.")
        exit()

    display_initial_info(graphics, info)
    webhook_templates.send_first_message(info)

    info.previous_balance = info.earnings_info.balance
    info.previous_number_of_transactions = info.transaction_info.total_transactions
    info.previous_bandwidth_usage = info.devices_info.total_bandwidth_usage

    while(True):
        # run every hour at *:02 UTC
        if datetime.now(timezone.utc).strftime("%M") == "02":
            info.get_info()

            # Balance changed
            if round(info.earnings_info.balance - info.previous_balance, 2) != 0:
                # After a redeem request, the initial balance is assumed to be 0.
                if info.earnings_info.balance < info.previous_balance:
                    info.previous_balance = 0
                graphics.balance_increased("Balance Updated.")
                graphics.balance_increased(
                    f"+{round((info.earnings_info.balance - info.previous_balance),2)}$"
                )
                graphics.balance_increased(
                    f"Traffic +{info.devices_info.total_bandwidth_usage-info.previous_bandwidth_usage}MB")
            else:
                graphics.balance_unchanged(
                    f"Your balance has not changed. Current balance: {info.earnings_info.balance}"
                )
                traffic_change = round(
                    (info.devices_info.total_bandwidth_usage - \
                        info.previous_bandwidth_usage)/(1024*1024), 2)
                graphics.balance_unchanged(
                    f"Traffic +{traffic_change}MB")
            webhook_templates.balance_update(info)

            # new redeem request
            graphics.info(
                f"Number of transactions: {info.transaction_info.total_transactions}")
            if check_redeem_requests(graphics, info, webhook_templates):
                webhook_templates.new_transaction(info)

            # update historical data
            info.previous_balance = info.earnings_info.balance
            info.previous_number_of_transactions = info.transaction_info.total_transactions

            # wait for the minute to end
            sleep(120)
        # Delay to check if it's time to ping earnapp
        sleep(10)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        graphics.warn("Received exit signal!")
        exit()
