import json

from discord_webhook import DiscordWebhook
from sys import exit
import requests
from graphics import Graphics
from time import sleep
from datetime import datetime, timedelta, timezone

class AllInformation:
    def __init__(self, webhook_url: str, api, graphics:Graphics) -> None:
        self.api = api
        self.webhook_url = webhook_url
        self.previous_balance = 0
        self.previous_number_of_transactions = 0
        self.previous_bandwidth_usage = 0
        self.graphics = graphics
        self.get_info()

    def get_info(self):
        try:
            self.user_info = self.api.get_user_data()
            self.earnings_info = self.api.get_earning_info()
            self.devices_info = self.api.get_devices_info()
            self.transaction_info = self.api.get_transaction_info()
            self.device_status = self.api.get_device_statuses()
            self.auth = self.api.returnHeader()
        except requests.exceptions.ConnectionError:
            self.graphics.error("Connection closed by earnapp server. Retrying.")
            sleep(5)
            self.get_info()


def display_initial_info(graphics, info: AllInformation):

    graphics.info(f"Username: {info.user_info.name}")
    graphics.info(f"Multiplier: {info.earnings_info.multiplier}")
    graphics.info(f"Balance: {info.earnings_info.balance}")
    graphics.info(f"Lifetime Balance: {info.earnings_info.earnings_total}")
    graphics.info(f"Referral Balance: {info.earnings_info.bonuses}") #here
    graphics.info(
        f"Lifetime Referral Balance: {info.earnings_info.bonuses_total}") #here
    graphics.info(f"Total Devices: {info.devices_info.total_devices}")
    graphics.info(f"\tWindows: {info.devices_info.windows_devices}")
    graphics.info(f"\tLinux: {info.devices_info.linux_devices}")
    graphics.info(f"\tOther: {info.devices_info.other_devices}")


def test_discord_webhook(graphics, webhook_url: str):
    graphics.info("Testing Discord Webhook.")
    webhook = DiscordWebhook(url=webhook_url,
                             content='Testing Discord Webhook.')

    response = webhook.execute()
    if response.status_code == 401:
        graphics.error("Looks like a wrong webhook URL.")
        exit()
    elif response.status_code == 404:
        graphics.error(
            "Webhook URL doesn't exist. Try recreating it on discord.")
        exit()
    elif response.status_code == 200:
        graphics.success("Webhook test successful.")
        response = webhook.delete(response)
    else:
        graphics.error(
            f"Unknown Webhook Error, Error Code: {response.status_code}")
        exit()


def check_redeem_requests(graphics, info, webhook_templates):
    if info.transaction_info.total_transactions == info.previous_number_of_transactions:
        graphics.info("No new transactions found.")
        return False
    elif info.transaction_info.total_transactions > info.previous_number_of_transactions:
        transaction = info.transaction_info.transactions[0]
        graphics.new_transaction("New redeem request detected.")
        graphics.new_transaction(
            f"Redeemed {transaction.amount}$ via {transaction.payment_method}")
        return True


def next_update_in(minutes:int, graphics: Graphics):
    current_time = datetime.now(timezone.utc)
    next_hour = current_time + timedelta(hours=1)
    next_update_time = datetime.strptime(next_hour.strftime('%Y-%m-%dT%H+%Z'), "%Y-%m-%dT%H+%Z") + timedelta(minutes=minutes)
    current_time = datetime.strptime(current_time.strftime('%Y-%m-%dT%H:%M:%S+%Z'), '%Y-%m-%dT%H:%M:%S+%Z')
    next_update_in = divmod((next_update_time - current_time).total_seconds(), 60)
    
    graphics.info(f'Next update in {next_update_in[0]:02.00f} minutes {next_update_in[1]:02.00f} seconds')
