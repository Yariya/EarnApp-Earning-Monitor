# Dev: Yariya

import json
import time
from config import *
from dp.colors import *
from dp.accountjson import *
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
from dp.baljson import *
from datetime import datetime


class Headers:
    params = (
        ('appid', 'earnapp_dashboard'),
    )


def main():
    now = datetime.now()
    curr = now.strftime("%H")

    print(f"{colors.GREEN}[+] EarnApp Earnings Watcher started!{colors.RESET}")

    devs = requests.get('https://earnapp.com/dashboard/api/devices',
                        headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                        params=Headers.params)

    # Lazy... Will update next update :)
    x = str(devs.text).split(",")
    devlen = int(round(len(x) / 8.9, 0))
    devgnu = str(devs.text).count("sdk-node") / 2
    devwin = str(devs.text).count("sdk-win") / 2

    infos = requests.get("https://earnapp.com/dashboard/api/user_data",
                         headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                         params=Headers.params)
    y = welcome8_from_dict(json.loads(infos.text))

    response = requests.get('https://earnapp.com/dashboard/api/money',
                            headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                            params=Headers.params)
    x = welcome7_from_dict(json.loads(response.text))
    history = x.balance

    print(f"{colors.GREEN}[+] Successfully loaded profile!{colors.RESET}")
    print(f"    {colors.RED}Username: {y.name}")
    print(f"    Multiplier: {x.multiplier}x")
    print(f"    Current Balance: {x.balance}$")
    print(f"    Lifetime Balance: {x.total_earnings}$")
    print(f"    Devices: {devlen} (Windows: {int(devwin)} Linux: {int(devgnu)})\n{colors.RESET}")

    while 1:
        n = datetime.now().strftime("%H")
        if curr == n:
            time.sleep(1)
        else:
            curr = n
            time.sleep(Delay)
            try:
                response = requests.get('https://earnapp.com/dashboard/api/money',
                                        headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                                        params=Headers.params)
                x = welcome7_from_dict(json.loads(response.text))
                if x.balance > history:
                    webhook = DiscordWebhook(url=WebhookURL, rate_limit_retry=True)
                    embed = DiscordEmbed(title="Balance Updated!", description="Your EarnApp Balance has been updated!", color="03b2f8")
                    embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                    embed.add_embed_field(name="Earned", value=f"+{round((x.balance - history), 2)}$")
                    embed.add_embed_field(name="Balance", value=f"{x.balance}$")
                    embed.add_embed_field(name="Multiplier", value=f"{x.multiplier}")
                    embed.add_embed_field(name="Total Earnings", value=f"{x.total_earnings}$")
                    embed.set_footer(text=f"You are earning with {devlen} devices", icon_url="https://img.icons8.com/color/64/000000/paypal.png")
                    webhook.add_embed(embed)
                    webhook.execute()

                    print(f"{colors.GREEN}[+] Balance Updated!")
                    print(f"    +{round((x.balance - history), 2)}${colors.RESET}\n")

                    history = float(x.balance)



                elif x.balance < history:
                    webhook = DiscordWebhook(url=WebhookURL, rate_limit_retry=True)
                    embed = DiscordEmbed(title="New Transactions", description="New Transactions Detected!", color="02ECC71")
                    embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                    embed.add_embed_field(name="Redeemed", value=f"+{round((history - x.balance), 2)}$")
                    embed.add_embed_field(name="Email", value=f"{x.redeem_details.email}")
                    embed.set_footer(text=f"Payment Method: {x.redeem_details.payment_method}", icon_url="https://img.icons8.com/color/64/000000/paypal.png")
                    webhook.add_embed(embed)
                    webhook.execute()
                    print(f"{colors.MAGENTA}[+] New payout detected!")
                    print(f"    Payout: {round((history - x.balance), 2)}")
                    print(f"    Payment method: {x.redeem_details.payment_method}{colors.RESET}\n")
                    history = float(x.balance)

                else:
                    webhook = DiscordWebhook(url=WebhookURL, rate_limit_retry=True)
                    embed = DiscordEmbed(title="Balance Status!", description="Your EarnApp balance has not changed!", color="E67E22")
                    embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                    embed.add_embed_field(name="Earned", value=f"+{round((x.balance - history), 2)}$")
                    embed.add_embed_field(name="Muliplier", value=f"{x.multiplier}")
                    embed.add_embed_field(name="Total Earnings", value=f"{x.total_earnings}$")
                    embed.set_footer(text=f"You are earning with {devlen} devices", icon_url="https://img.icons8.com/nolan/64/paypal.png")
                    webhook.add_embed(embed)
                    webhook.execute()
                    print(f"{colors.YELLOW}[~] Balance did not Change!")
                    print(f"    +{round((x.balance - history), 2)}${colors.RESET}\n")
                    history = float(x.balance)

            except:
                print(f"{colors.RED}[-] EarnApp is currently down :/{colors.RESET}")


if __name__ == '__main__':
    main()
