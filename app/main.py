from pyEarnapp import EarnApp
from pyEarnapp.errors import *
from config import Configuration
from colorama import init
from graphics import Graphics
from discord_webhook import DiscordWebhook
from webhooks import WebhookTemplate
from time import sleep
from datetime import datetime, timezone

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


def test_discord_webhook():
    graphics.info("Testing Discord Webhook.")
    webhook = DiscordWebhook(url=config.WEBHOOK_URL,
                             content='Testing Discord Webhook.')
    response = webhook.execute()
    if response.status_code == 401:
        graphics.error("Looks like a wrong webhook URL.")
        exit()
    elif response.status_code == 200:
        graphics.success("Webhook test successful.")
    webhook.delete(response)


def main():
    try:
        # Earnapp
        user_info = api.get_user_data()
        earnings_info = api.get_earning_info()
        devices_info = api.get_devices_info()
        transaction_info = api.get_transaction_info()

        # Discord Webhook
        test_discord_webhook()

    except AuthenticationError:
        graphics.error("Looks like a wrong oauth-refresh-token.")
        exit()

    graphics.info(f"Username: {user_info.name}")
    graphics.info(f"Multiplier: {earnings_info.multiplier}")
    graphics.info(f"Balance: {earnings_info.balance}")
    graphics.info(f"Lifetime Balance: {earnings_info.earnings_total}")
    graphics.info(f"Referral Balance: {earnings_info.bonuses}")
    graphics.info(f"Lifetime Referral Balance: {earnings_info.bonuses_total}")
    graphics.info(f"Total Devices: {devices_info.total_devices}")
    graphics.info(f"\tWindows: {devices_info.windows_devices}")
    graphics.info(f"\tLinux: {devices_info.linux_devices}")
    graphics.info(f"\tOther: {devices_info.other_devices}")
    webhook_templates.send_first_message(
        config.WEBHOOK_URL, user_info, earnings_info, devices_info)

    previous_balance = earnings_info.balance
    previous_number_of_transactions = transaction_info.total_transactions

    while(True):
        # run every hour at *:02 UTC
        if datetime.now(timezone.utc).strftime("%M") == "02":
            user_info = api.get_user_data()
            earnings_info = api.get_earning_info()
            devices_info = api.get_devices_info()
            transaction_info = api.get_transaction_info()

            # Balance changed
            if round(earnings_info.balance - previous_balance, 2) != 0:
                # After a redeem request, the initial balance is assumed to be 0.
                if earnings_info.balance < previous_balance:
                    previous_balance = 0
                
                graphics.balance_increased("Balance Updated.")
                graphics.balance_increased(
                    f"+{round((earnings_info.balance - previous_balance),2)}$"
                )
            else:
                graphics.balance_unchanged("Balance not changed.")
                graphics.balance_unchanged(
                    f"Your balance has not changed. Current balance: {earnings_info.balance}"
                )

            webhook_templates.balance_update(
                config.WEBHOOK_URL,
                user_info,
                earnings_info,
                devices_info,
                previous_balance
            )

            # new redeem request
            graphics.info(f"Number of transactions: {transaction_info.total_transactions}")
            if transaction_info.total_transactions == previous_number_of_transactions:
                graphics.info("No new transactions found.")
            elif transaction_info.total_transactions > previous_number_of_transactions:
                graphics.new_transaction("New redeem request detected.")
                graphics.new_transaction(
                    f"Redeemed {transaction_info.transactions[0].amount}$ via {transaction_info.transactions[0].payment_method}"
                )
                webhook_templates.new_transaction(
                    config.WEBHOOK_URL,
                    user_info,
                    earnings_info,
                    devices_info,
                    transaction_info.transactions[0]
                )

            # update historical data
            previous_balance = earnings_info.balance
            previous_number_of_transactions = transaction_info.total_transactions

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