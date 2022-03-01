from urllib.parse import urljoin


class EarnAppEndpoints:
    def __init__(self) -> None:
        self.baseURL = "https://earnapp.com/dashboard/api/"
        self.userData = urljoin(self.baseURL, "user_data/")
        self.money = urljoin(self.baseURL, "money/")
        self.devices = urljoin(self.baseURL, "devices/")
        self.transaction = urljoin(self.baseURL, "transactions/")
        self.add_device = urljoin(self.baseURL, "link_device/")
        self.referrals = urljoin(self.baseURL, "referees/")
        self.counters = urljoin(self.baseURL, "counters/")
        self.device = urljoin(self.baseURL, "device/")
        self.check_ip = urljoin(self.baseURL, "check_ip/")
        self.redeem = urljoin(self.baseURL, "redeem/")
        self.device_status = urljoin(self.baseURL, 'device_statuses')
