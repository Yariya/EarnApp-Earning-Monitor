import json
import time
from config import *
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
from typing import Any, TypeVar, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class RedeemDetails:
    email: str
    payment_method: str

    def __init__(self, email: str, payment_method: str) -> None:
        self.email = email
        self.payment_method = payment_method

    @staticmethod
    def from_dict(obj: Any) -> 'RedeemDetails':
        assert isinstance(obj, dict)
        email = from_str(obj.get("email"))
        payment_method = from_str(obj.get("payment_method"))
        return RedeemDetails(email, payment_method)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_str(self.email)
        result["payment_method"] = from_str(self.payment_method)
        return result


class Welcome7:
    balance: float
    tokens: int
    total_earnings: float
    multiplier: float
    redeem_details: RedeemDetails

    def __init__(self, balance: float, tokens: int, total_earnings: float, multiplier: float,
                 redeem_details: RedeemDetails) -> None:
        self.balance = balance
        self.tokens = tokens
        self.total_earnings = total_earnings
        self.multiplier = multiplier
        self.redeem_details = redeem_details

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome7':
        assert isinstance(obj, dict)
        balance = from_float(obj.get("balance"))
        tokens = from_int(obj.get("tokens"))
        total_earnings = from_float(obj.get("total_earnings"))
        multiplier = from_float(obj.get("multiplier"))
        redeem_details = RedeemDetails.from_dict(obj.get("redeem_details"))
        return Welcome7(balance, tokens, total_earnings, multiplier, redeem_details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["balance"] = to_float(self.balance)
        result["tokens"] = from_int(self.tokens)
        result["total_earnings"] = to_float(self.total_earnings)
        result["multiplier"] = to_float(self.multiplier)
        result["redeem_details"] = to_class(RedeemDetails, self.redeem_details)
        return result


def welcome7_from_dict(s: Any) -> Welcome7:
    return Welcome7.from_dict(s)


def welcome7_to_dict(x: Welcome7) -> Any:
    return to_class(Welcome7, x)


class Headers:
    params = (
        ('appid', 'earnapp_dashboard'),
    )


def main():
    print("[+] EarnApp Monitor started!")
    response = requests.get('https://earnapp.com/dashboard/api/money', headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'}, params=Headers.params)
    x = welcome7_from_dict(json.loads(response.text))
    history = x.balance
    time.sleep(60)
    while 1:
        try:
            response = requests.get('https://earnapp.com/dashboard/api/money', headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'}, params=Headers.params)
            x = welcome7_from_dict(json.loads(response.text))
            print(response.text)
            if x.balance > history:

                webhook = DiscordWebhook(url=WebhookURL, rate_limit_retry=True)
                embed = DiscordEmbed(title="Balance Updated!", description="Your EarnApp Balance has been updated!",
                                     color="03b2f8")
                embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                embed.add_embed_field(name="Earned", value=f"+{round((x.balance - history), 2)}$")
                embed.add_embed_field(name="Balance", value=f"{x.balance}$")
                embed.add_embed_field(name="Multiplier", value=f"{x.multiplier}")
                embed.add_embed_field(name="Total Earnings", value=f"{x.total_earnings}$")
                embed.set_footer(text=f"Payment Method: {x.redeem_details.payment_method}",
                                 icon_url="https://img.icons8.com/nolan/64/paypal.png")
                webhook.add_embed(embed)
                webhook.execute()
                history = float(x.balance)

            elif x.balance < history:
                webhook = DiscordWebhook(url=WebhookURL, rate_limit_retry=True)
                embed = DiscordEmbed(title="New Transactions", description="New Transactions Detected!",
                                     color="03b2f8")
                embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                embed.add_embed_field(name="Redeemed", value=f"+{round((history - x.balance), 2)}$")
                embed.add_embed_field(name="Email", value=f"{x.redeem_details.email}")
                embed.set_footer(text=f"Payment Method: {x.redeem_details.payment_method}",
                                 icon_url="https://img.icons8.com/nolan/64/paypal.png")
                webhook.add_embed(embed)
                webhook.execute()
                history = float(x.balance)
        except:
            print("[-] EarnApp is currently down /:")
        time.sleep(Delay)


if __name__ == '__main__':
    main()
