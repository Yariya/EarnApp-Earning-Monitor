import json
import sys
import time
from config import *
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
from dp.baljson import *
from datetime import datetime
import colorama


class Headers:
    params = (
        ('appid', 'earnapp_dashboard'),
    )


def main():
    infos = ""
    now = datetime.now()
    curr = now.strftime("%H")

    print(f"{colorama.Fore.GREEN}[+] EarnApp Earnings Watcher started!{colorama.Fore.RESET}")

    devs = requests.get('https://earnapp.com/dashboard/api/devices',
                        headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                        params=Headers.params)

    devlen = 0
    devgnu = 0
    devwin = 0
    totalbw = 0

    x = json.loads(devs.text)

    for y in x:
        devlen += 1
        if str(y["uuid"]).startswith("sdk-win"):
            devwin += 1
        else:
            devgnu += 1
        totalbw += int(y["total_bw"])

    try:
        infos = requests.get("https://earnapp.com/dashboard/api/user_data",
                             headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                             params=Headers.params)
        y = json.loads(infos.text)
    except:
        print(f"{colorama.Fore.RED}Can't parse json from api/user_data")
        print(f"Send this to an admin{colorama.Fore.RESET}")
        print(infos.text)
        input("")
        sys.exit(0)

    response = requests.get('https://earnapp.com/dashboard/api/money',
                            headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                            params=Headers.params)

    devices = requests.get('https://earnapp.com/dashboard/api/devices',
                           headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                           params=Headers.params)

    # Short fix of payment needed problem
    xbackup = []
    try:
        xbackup = welcome7_from_dict(json.loads(response.text))
    except:
        xbackup = "nil"
    x = json.loads(response.text)
    history = x["balance"]

    print(f"{colorama.Fore.GREEN}[+] Successfully loaded profile!{colorama.Fore.RESET}")
    print(f"    {colorama.Fore.RED}Username: {y['name']}")
    print(f"    Multiplier: {x['multiplier']}x")
    print(f"    Current Balance: {x['balance']}$")
    print(f"    Lifetime Balance: {x['earnings_total']}$")
    print(f"    Devices: {devlen} (Windows: {int(devwin)} Linux: {int(devgnu)})\n{colorama.Fore.RESET}")

    while 1:
        n = datetime.now().strftime("%H")
        if curr == n:
            time.sleep(1)
        else:
            curr = n
            time.sleep(DELAY)

            response = requests.get('https://earnapp.com/dashboard/api/money',
                                    headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                                    params=Headers.params)

            devs = requests.get('https://earnapp.com/dashboard/api/devices',
                                headers={'cookie': f'auth=1; auth-method=google; oauth-refresh-token={AUTH}'},
                                params=Headers.params)

            x = json.loads(response.text)
            y = json.loads(devs.text)
            totalbw2 = 0
            devlen = 0
            for n in y:
                totalbw2 += int(n["total_bw"])
                devlen += 1
            if x['balance'] > history:

                webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
                embed = DiscordEmbed(title="Balance Updated!", description="Your EarnApp Balance has been updated!",
                                     color="03b2f8")
                embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                embed.add_embed_field(name="Earned", value=f"+{round((x['balance'] - history), 2)}$")
                embed.add_embed_field(name="Traffic", value=f"+{round(((totalbw2-totalbw)/pow(10,6)), 2)} mb")
                embed.add_embed_field(name="Balance", value=f"{x['balance']}$")
                embed.add_embed_field(name="Multiplier", value=f"{x['multiplier']}")
                embed.add_embed_field(name="Total Earnings", value=f"{x['earnings_total']}$")
                embed.set_footer(text=f"You are earning with {devlen} Devices",
                                 icon_url="https://img.icons8.com/color/64/000000/paypal.png")
                webhook.add_embed(embed)
                webhook.execute()

                print(f"{colorama.Fore.GREEN}[+] Balance Updated!")
                print(f"    +{round((x['balance'] - history), 2)}${colorama.Fore.RESET}\n")

                history = float(x['balance'])
                totalbw = totalbw2



            elif x['balance'] < history:
                webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
                embed = DiscordEmbed(title="New Transactions", description="New Transactions Detected!",
                                     color="02ECC71")
                embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                embed.add_embed_field(name="Redeemed", value=f"+{round((history - x['balance']), 2)}$")
                embed.add_embed_field(name="Email", value=f"{xbackup.redeem_details.email}")
                embed.set_footer(text=f"Payment Method: {xbackup.redeem_details.payment_method}",
                                 icon_url="https://img.icons8.com/color/64/000000/paypal.png")
                webhook.add_embed(embed)
                webhook.execute()
                print(f"{colorama.Fore.MAGENTA}[+] New payout detected!")
                print(f"    Payout: {round((history - x['balance']), 2)}")
                print(f"    Payment method: {xbackup.redeem_details.payment_method}{colorama.Fore.RESET}\n")
                history = float(x['balance'])

            else:
                webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
                embed = DiscordEmbed(title="Balance Status!", description="Your EarnApp balance has not changed!",
                                     color="E67E22")
                embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
                embed.add_embed_field(name="Earned", value=f"+{round((x['balance'] - history), 2)}$")
                embed.add_embed_field(name="Multiplier", value=f"{x['multiplier']}")
                embed.add_embed_field(name="Total Earnings", value=f"{x['total_earnings']}$")
                embed.set_footer(text=f"You are earning with {devlen} Devices",
                                 icon_url="https://img.icons8.com/nolan/64/paypal.png")
                webhook.add_embed(embed)
                webhook.execute()
                print(f"{colorama.Fore.YELLOW}[~] Balance did not Change!")
                print(f"    +{round((x['balance'] - history), 2)}${colorama.Fore.RESET}\n")
                history = float(x['balance'])


if __name__ == '__main__':
    main()
