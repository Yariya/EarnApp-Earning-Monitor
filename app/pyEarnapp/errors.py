class AuthenticationError(Exception):
    def __init__(self) -> None:
        message = "Error authenticating. Enter a proper oauth-refresh-token"
        super().__init__(message)

class DeviceAddError(Exception):
    pass

class DeviceNotFoundError(DeviceAddError):
    def __init__(self, error_message) -> None:
        super().__init__(error_message)

class DeviceAlreadyAddedError(DeviceAddError):
    def __init__(self, error_message) -> None:
        super().__init__(error_message)

class UnKnownDeviceAddError(DeviceAddError):
    def __init__(self, error_message) -> None:
        super().__init__(error_message)

class TooManyRequestsError(DeviceAddError):
    def __init__(self) -> None:
        super().__init__("EarnApp doesn't allow you to add many devices at time. Try adding delay in sending requests")