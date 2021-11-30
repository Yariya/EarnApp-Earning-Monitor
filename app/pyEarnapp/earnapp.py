import requests
from urllib.parse import urljoin
from .tools import *
from .errors import *
import json
import re
from datetime import datetime, timedelta, timezone
from .report import report_banned_ip


class Headers:
    def __init__(self, auth_refresh_token) -> None:
        self.params = (
            ('appid', 'earnapp_dashboard'),
        )
        self.header = {
            'cookie': f'auth=1; auth-method=google; oauth-refresh-token={auth_refresh_token}'
        }


class EarnAppEndpoints:
    def __init__(self) -> None:
        self.baseURL = "https://earnapp.com/dashboard/api/"
        self.userData = urljoin(self.baseURL, "user_data")
        self.money = urljoin(self.baseURL, "money")
        self.devices = urljoin(self.baseURL, "devices")
        self.transaction = urljoin(self.baseURL, "transactions")
        self.add_device = urljoin(self.baseURL, "link_device")
        self.referrals = urljoin(self.baseURL, "referees")
        self.counters = urljoin(self.baseURL, "counters")


class UserData:
    def __init__(self, json_user_data: dict) -> None:
        self.first_name = json_user_data["first_name"]
        self.last_name = json_user_data["last_name"]
        self.name = json_user_data["name"]
        self.email = json_user_data["email"]
        self.referral_code = json_user_data["referral_code"]


class EarningInfo:
    def __init__(self, json_earning_info: dict) -> None:
        self.balance = json_earning_info.get(
            "balance", "Error retrieving balance")
        self.earnings_total = json_earning_info.get(
            "earnings_total", "Error retrieving total earnings")
        self.multiplier = json_earning_info.get(
            "multiplier", "Error retrieving multiplier")
        self.tokens = json_earning_info.get(
            "tokens", "Error retrieving tokens")
        self.redeem_details = RedeemDetails(
            json_earning_info.get("redeem_details", dict()))
        self.bonuses = json_earning_info["ref_bonuses"]
        self.bonuses_total = json_earning_info["ref_bonuses_total"]
        self.referral_part = json_earning_info["referral_part"]



class RedeemDetails:
    def __init__(self, json_redeem_details: dict) -> None:
        if json_redeem_details is not None:
            self.email = json_redeem_details.get(
                "email", "Error retrieving payment email")
            self.payment_method = json_redeem_details.get(
                "payment_method", "Error retrieving payment method")
        else:
            self.email = "No email detected"
            self.payment_method = "No payment method found"


class BanDetails:
    def __init__(self, ban_info) -> None:
        if ban_info is False:
            self.is_banned = False
            self.reason = None
            self.ip = None
            self.details = None
        else:
            self.is_banned = True
            self.reason = ban_info['reason']
            self.ip = ban_info['ip']
            self.details = ban_info['details']


class Device:
    def __init__(self, json_device_info: dict):
        self.uuid = json_device_info.get("uuid", "Error retrieving UUID")
        self.bandwidth_usage = json_device_info.get(
            "bw", 0)
        self.total_bandwidth_usage = json_device_info.get(
            "total_bw", "Error retrieving total bandwidth")
        self.redeemed_bandwidth = json_device_info.get(
            "redeem_bw", "Error retrieving redeemed bandwidth")
        self.rate = json_device_info.get("rate", "Error retrieving rate")
        self.country = json_device_info.get("cn", "UnKnown")
        self.device_type = re.findall('sdk-([a-zA-Z0-9]*)-', self.uuid)[0]
        self.banned = BanDetails(json_device_info.get('banned', False))


class DevicesInfo:
    def __init__(self, json_devices_info: dict, report_ip_ban):
        self.devices = []
        self.windows_devices = 0
        self.linux_devices = 0
        self.other_devices = 0
        self.banned_devices = 0
        self.total_bandwidth_usage = 0

        for device in json_devices_info:
            self.devices.append(Device(device))

        self.total_devices = len(self.devices)

        self.banned_ip_addresses = []
        for device in self.devices:
            if device.device_type == "win":
                self.windows_devices += 1
            elif device.device_type == "node":
                self.linux_devices += 1
            else:
                self.other_devices += 1
            self.total_bandwidth_usage += device.bandwidth_usage
            if device.banned.is_banned:
                self.banned_devices += 1
                self.banned_ip_addresses.append(device.banned.ip)
        if report_ip_ban:
            report_banned_ip(self.banned_ip_addresses)


class Transaction:
    def __init__(self, json_transaction: dict) -> None:
        self.uuid = json_transaction.get(
            "uuid", "Error retrieving transaction UUID")
        self.status = json_transaction.get(
            "status", "Error retrieving transaction status")
        self.payment_method = json_transaction.get(
            "payment_method", "Payment method not found")

        self.amount = json_transaction.get(
            "money_amount", "Error retrieving payment amount")

        self.redeem_date = datetime.strptime(
            json_transaction.get("date").replace("Z", "UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")

        payment_date = json_transaction.get("payment_date")

        if payment_date is None:
            self.payment_date = self.redeem_date + timedelta(days=9)
        elif type(payment_date) is str:
            self.payment_date = datetime.strptime(
                payment_date.replace("Z", "UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        else:
            self.payment_date = datetime.now(timezone.utc)

        if self.status == "paid":
            self.is_paid = True
        else:
            self.is_paid = False


class Transactions:
    def __init__(self, json_transactions) -> None:
        self.transactions = []
        self.pending_payments = 0
        self.paid = 0
        for transaction in json_transactions:
            self.transactions.append(Transaction(transaction))

        self.total_transactions = len(self.transactions)
        for transaction in self.transactions:
            if transaction.is_paid:
                self.paid += 1
            else:
                self.pending_payments += 1


class Referee:
    def __init__(self, json_referee_info) -> None:
        self.id = json_referee_info["id"]
        self.bonuses = json_referee_info["bonuses"]
        self.bonuses_total = json_referee_info["bonuses_total"]
        self.email = json_referee_info["email"]


class Referrals:
    def __init__(self, json_referees_info) -> None:
        self.referrals = []
        self.referral_earnings = 0
        self.total_referral_earnings = 0

        for referee in json_referees_info:
            self.referrals.append(Referee(referee))

        self.number_of_referrals = len(self.referrals)
        for referee in self.referrals:
            self.referral_earnings += referee.bonuses
            self.total_referral_earnings += referee.bonuses_total


class EarnApp:
    def __init__(self, auth_refresh_token, report_ip_ban: bool = False) -> None:
        self.headers = Headers(auth_refresh_token)
        self.endpoints = EarnAppEndpoints()
        self.report_ip_ban = report_ip_ban

    def get_user_data(self):
        response = requests.get(
            self.endpoints.userData,
            headers=self.headers.header,
            params=self.headers.params
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return UserData(json.loads(response.content))

    def get_earning_info(self):
        response = requests.get(
            self.endpoints.money,
            headers=self.headers.header,
            params=self.headers.params
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return EarningInfo(json.loads(response.content))

    def get_devices_info(self):
        response = requests.get(
            self.endpoints.devices,
            headers=self.headers.header,
            params=self.headers.params
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return DevicesInfo(json.loads(response.content), self.report_ip_ban)

    def get_transaction_info(self):
        response = requests.get(
            self.endpoints.transaction,
            headers=self.headers.header,
            params=self.headers.params
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return Transactions(json.loads(response.content))

    def get_referral_info(self):
        response = requests.get(
            self.endpoints.referrals,
            headers=self.headers.header,
            params=self.headers.params
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return Referrals(json.loads(response.content))

    def add_new_device(self, new_device_id):
        data = {"uuid": new_device_id}
        response = requests.post(
            self.endpoints.add_device,
            headers=self.headers.header,
            params=self.headers.params,
            json=data
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 429:
            raise TooManyRequestsError()
        elif response.status_code == 200:
            content = json.loads(response.content)
            print(response.status_code, content)
            error_message = content.get("error", None)
            if error_message:
                if "already linked" in error_message:
                    raise DeviceAlreadyAddedError(error_message)
                elif "not found" in error_message:
                    raise DeviceNotFoundError(error_message)
                else:
                    raise UnKnownDeviceAddError(error_message)
            else:
                return content
        else:
            raise UnKnownDeviceAddError(
                f"Failed to add device. Status code: {response.status_code}")
