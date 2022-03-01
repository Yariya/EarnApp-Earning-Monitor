import requests
from urllib.parse import urljoin
import json

from .tools import *
from .errors import *
from .models.transactions import *
from .models.referral import *
from .models.endpoints import *
from .models.device import *
from .models.user import *
from .models.header import *
from .models.earnings import *


class EarnApp:
    def __init__(self, auth_refresh_token, report_ip_ban: bool = False) -> None:
        self.headers = Headers(auth_refresh_token)
        self.endpoints = EarnAppEndpoints()
        self.report_ip_ban = report_ip_ban
        self.minimum_redeem_balance = 5

    def get_user_data(self, *args, **kwargs) -> UserData:
        response = requests.get(
            self.endpoints.userData,
            headers=self.headers.header,
            params=self.headers.params,
            *args,
            **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return UserData(json.loads(response.content))

    def get_earning_info(self, *args, **kwargs) -> EarningInfo:
        response = requests.get(
            self.endpoints.money,
            headers=self.headers.header,
            params=self.headers.params,
            *args,
            **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return EarningInfo(json.loads(response.content))

    def get_devices_info(self, *args, **kwargs) -> DevicesInfo:
        response = requests.get(
            self.endpoints.devices,
            headers=self.headers.header,
            params=self.headers.params,
            *args,
            **kwargs
        )
        device_statuses = requests.post(
            self.endpoints.device_status,
            headers=self.headers.header,
            params=self.headers.params,
            *args,
            **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return DevicesInfo(json.loads(response.content), self.report_ip_ban, device_statuses)

    def get_transaction_info(self, *args, **kwargs) -> Transactions:
        response = requests.get(
            self.endpoints.transaction,
            headers=self.headers.header,
            params=self.headers.params, *args, **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return Transactions(json.loads(response.content))

    def get_referral_info(self, *args, **kwargs) -> Referrals:
        response = requests.get(
            self.endpoints.referrals,
            headers=self.headers.header,
            params=self.headers.params, *args, **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 200:
            return Referrals(json.loads(response.content))

    def add_new_device(self, new_device_id, *args, **kwargs):
        data = {"uuid": new_device_id}
        response = requests.post(
            self.endpoints.add_device,
            headers=self.headers.header,
            params=self.headers.params,
            json=data, *args, **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 429:
            raise TooManyRequestsError(
                "EarnApp doesn't allow you to add many devices at time. Try adding delay in sending requests")
        elif response.status_code == 200:
            content = json.loads(response.content)
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

    def delete_device(self, device_uuid: str, *args, **kwargs) -> bool:
        response = requests.delete(
            urljoin(self.endpoints.device, device_uuid),
            headers=self.headers.header,
            params=self.headers.params,
            *args,
            **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 429:
            raise TooManyRequestsError(
                f'Response: {response.content.decode()}')
        elif response.status_code == 200:
            content = json.loads(response.content)
            error_message = content.get("error", None)
            if error_message:
                raise UnKnownDeviceAddError(error_message)
            else:
                return (True if content.get("status", None) == 'ok' else False)
        else:
            raise UnKnownDeviceAddError(
                f"Failed to delete device. Status code: {response.status_code}")

    def is_ip_allowed(self, ip_address: str, *args, **kwargs) -> bool:
        if not is_a_valid_ip(ip_address):
            raise InValidIPAddressError()
        response = requests.get(
            urljoin(self.endpoints.check_ip, ip_address),
            *args,
            **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code in [429, 423]:
            raise TooManyRequestsError(
                f'Response: {response.content.decode()}')
        elif response.status_code == 200:
            content = json.loads(response.content)
            error_message = content.get("error", None)
            if error_message:
                raise UnKnownIPCheckError(error_message)
            else:
                return (True if content.get('ip_blocked') is False else False)
        else:
            raise UnKnownIPCheckError(
                f"Failed to check IP Address: {ip_address}. Status code: {response.status_code}")

    def redeem_to_paypal(self, paypal_email: str, *args, **kwargs) -> bool:
        current_balance = self.get_earning_info(*args, **kwargs).balance
        if not current_balance > self.minimum_redeem_balance:
            raise MinimumRedeemBalanceError(
                f"Minimum balance for redeeming is {self.minimum_redeem_balance}. Your balance is {current_balance}")
        data = {
            'to': paypal_email,
            'payment_method': "paypal.com"
        }
        response = requests.post(
            self.endpoints.redeem,
            headers=self.headers.header,
            params=self.headers.params,
            json=data, *args, **kwargs
        )
        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 429:
            raise TooManyRequestsError(
                f'Response: {response.content.decode()}')
        elif response.status_code == 200:
            content = json.loads(response.content)
            error_message = content.get("error", None)
            if 'ok' in content:
                return content.get('ok', False)
            if error_message:
                raise RedeemError(error_message)
            else:
                return content
        else:
            raise UnKnownRedeemError(
                f"Failed to redeem balance. Status code: {response.status_code} Response: {response.content}")

    def get_device_statuses(self) -> dict:
        devices = self.get_devices_info().get_devices()
        self.__status_payload = []

        for device in devices:
            self.__status_payload.append({
                "uuid": device.uuid,
                "appid": "node_earnapp.com"
            })

        response = requests.post(
            self.endpoints.device_status,
            headers=self.headers.header,
            params=self.headers.params,
            json={'list': self.__status_payload}
        )

        if response.status_code == 403:
            raise AuthenticationError()
        elif response.status_code == 429:
            raise TooManyRequestsError(
                f'Response: {response.content.decode()}')
        elif response.status_code == 200:
            content = json.loads(response.content)
            error_message = content.get("error", None)
            if error_message:
                raise UnKnownError(error_message)
            else:
                return content['statuses']
        else:
            raise UnKnownError(
                "Failed to get device statuses. Status code: {response.status_code} Response: {response.content}")
        
