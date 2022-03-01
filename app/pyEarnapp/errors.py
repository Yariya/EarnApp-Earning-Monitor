class UnKnownError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AuthenticationError(Exception):
    def __init__(self) -> None:
        message = "Error authenticating. Enter a proper oauth-refresh-token"
        super().__init__(message)


class DeviceAddError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DeviceNotFoundError(DeviceAddError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DeviceAlreadyAddedError(DeviceAddError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnKnownDeviceAddError(DeviceAddError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class TooManyRequestsError(DeviceAddError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IPCheckError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnKnownIPCheckError(IPCheckError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InValidIPAddressError(IPCheckError):
    def __init__(self, *args: object) -> None:
        super().__init__("The IP Address is not valid.", *args)


class RedeemError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnKnownRedeemError(RedeemError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MinimumRedeemBalanceError(RedeemError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
