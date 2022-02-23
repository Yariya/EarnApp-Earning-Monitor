from ..report import report_banned_ip
import re
import requests

class BanDetails:
    def __init__(self, ban_info) -> None:
        if ban_info is False:
            self.is_banned = False
            self.reason = None
            self.ip = None
            self.details = None
        else:
            self.is_banned = True
            self.reason = ban_info.get('reason')
            self.ip = ban_info.get('ip')
            self.details = ban_info.get('details')


class Device:
    def __init__(self, json_device_info: dict):
        self.uuid = json_device_info.get("uuid", "Error retrieving UUID")
        self.bandwidth_usage = json_device_info.get("bw", 0)
        self.total_bandwidth_usage = json_device_info.get(
            "total_bw", "Error retrieving total bandwidth")
        self.redeemed_bandwidth = json_device_info.get(
            "redeem_bw", "Error retrieving redeemed bandwidth")
        self.rate = json_device_info.get("rate", "Error retrieving rate")
        self.country = json_device_info.get("cn", "UnKnown")
        self.device_type = re.findall('sdk-([a-zA-Z0-9]*)-', self.uuid)[0]
        self.banned = BanDetails(json_device_info.get('banned', False))


class DevicesInfo:
    def __init__(self, json_devices_info: dict, report_ip_ban, device_statuses):
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

    def get_devices(self) -> list[Device]:
        return self.devices