
class Referee:
    def __init__(self, json_referee_info: dict) -> None:
        self.id = json_referee_info.get("id")
        self.bonuses = json_referee_info.get("bonuses")
        self.bonuses_total = json_referee_info.get("bonuses_total")
        self.email = json_referee_info.get("email")


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
