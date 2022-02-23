from .transactions import RedeemDetails
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
        self.bonuses = json_earning_info.get("ref_bonuses", 0)
        self.bonuses_total = json_earning_info.get("ref_bonuses_total", 0)
        self.referral_part = json_earning_info.get("referral_part", 0)
