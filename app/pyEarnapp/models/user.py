
class UserData:
    def __init__(self, json_user_data: dict) -> None:
        self.first_name = json_user_data.get("first_name", None)
        self.last_name = json_user_data.get("last_name", None)
        self.name = json_user_data.get("name", None)
        self.email = json_user_data.get("email", None)
        self.referral_code = json_user_data.get("referral_code", None)
