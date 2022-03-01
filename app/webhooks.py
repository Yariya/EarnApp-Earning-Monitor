import json

import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
from pyEarnapp.earnapp import DevicesInfo, Transaction, EarningInfo, UserData
from functions import AllInformation


def offlineDevices(info: AllInformation):
    x = 0
    all = info.device_status
    for i in all:
        if not all[i]["online"]:
            x += 1
    return x


def onlineDevices(info: AllInformation):
    x = 0
    all = info.device_status
    for i in all:
        if all[i]["online"]:
            x += 1
    return x

def hiddenDevices(header):
    r = requests.get("https://earnapp.com/dashboard/api/devices?appid=earnapp_dashboard&version=1.284.850", headers=header)
    devices = json.loads(r.text)
    hidden = 0
    on = 0
    for device in devices:
        try:
            tmp = device["hide_ts"]
            hidden+=1
        except:
          on+=1
    return hidden




class WebhookTemplate:
    def __init__(self) -> None:
        pass

    def trafficGraph(self, graphPath, info: AllInformation):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)

        embed = DiscordEmbed(
            title="New Traffic insights available!",
            color="00ff00"
        )
        with open(graphPath, "rb") as f:
            webhook.add_file(file=f.read(), filename="graph.png")
        embed.set_image(url="attachment://graph.png")

        embed.set_footer(text="Build by Yariya")
        webhook.add_embed(embed)
        webhook.execute()

    def device_gone_offline(self, info: AllInformation, count: int, devices):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)

        embed = DiscordEmbed(
            title="[WARNING] DEVICES OFFLINE",
            description=f"{count} Device(s) just went offline! {info.devices_info.total_devices-info.devices_info.banned_devices-offlineDevices(info)} Devices remain...",
            color="ff0000"
        )
        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Device List", value=f"\n".join(devices))

        embed.set_footer(
            text=f"{info.devices_info.total_devices - offlineDevices(info)}/{info.devices_info.total_devices - hiddenDevices(info.auth)} Devices",
            icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    def send_first_message(self, info: AllInformation):

        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)

        embed = DiscordEmbed(
            title="Bot Started 🤖",
            description="Earnapp Earning Monitor has been started.",
            color="FFFFFF"
        )

        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Username", value=f"{info.user_info.name}")
        embed.add_embed_field(
            name="Multiplier", value=f"{info.earnings_info.multiplier}x")
        embed.add_embed_field(
            name="Balance", value=f"{info.earnings_info.balance}$")
        embed.add_embed_field(name="Lifetime Balance",
                              value=f"{info.earnings_info.earnings_total}$")
        embed.add_embed_field(name="Lifetime Referral", value=f"{info.earnings_info.bonuses}$")
        embed.add_embed_field(name="Total Devices",
                              value=f"{info.devices_info.total_devices}")
        embed.add_embed_field(name="Device Status",
                              value=f"Online: {onlineDevices(info)}\nOffline: {offlineDevices(info)}\nHidden: {hiddenDevices(info.auth)}")
        embed.add_embed_field(
            name="Total Devices",
            value=f"{info.devices_info.windows_devices} Windows\n{info.devices_info.linux_devices} Linux\n{info.devices_info.other_devices} Others",
            inline=True)
        embed.add_embed_field(name="Bugs?",
                              value=f"[Contact Devs.](https://github.com/Yariya/EarnApp-Earning-Monitor/issues)")
        embed.set_footer(text=f"Version: 2.2.0.0",
                         icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    # def device_status_change(self, info: AllInformation, ):

    def balance_update(self, info: AllInformation):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)
        change = round(info.earnings_info.balance - info.previous_balance, 2)

        if change > 0:
            title = f"Balance Increased [+{change}]"
            color = "03F8C4"
        else:
            title = "Balance Unchanged!"
            color = "E67E22"
        traffic_change = round(
            (info.devices_info.total_bandwidth_usage -
             info.previous_bandwidth_usage) / (1024 ** 2), 2)

        if change == 0 or traffic_change == 0:
            value = "No change in traffic."
        else:
            value = f'{round(change / (traffic_change / 1024), 2)} $/GB'

        embed = DiscordEmbed(
            title=title,
            color=color
        )
        moneyPercentage = "{0:+.2f}%".format((info.earnings_info.balance/info.previous_balance)*100.0 - 100)
        trafficPercentage = "{0:+.2f}%".format((info.devices_info.total_bandwidth_usage/info.previous_bandwidth_usage)*100.0 - 100)
        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Earned", value=f"+{change}$ ({moneyPercentage})")
        embed.add_embed_field(name="Traffic", value=f"+{traffic_change} MB ({trafficPercentage})")
        embed.add_embed_field(name="Avg. Price/GB", value=value)
        embed.add_embed_field(name="Balance",
                              value=f"{info.earnings_info.balance}$")
        embed.add_embed_field(name="Referral Balance",
                              value=f"{info.earnings_info.bonuses}$")
        embed.add_embed_field(name="Lifetime Balance",
                              value=f"{info.earnings_info.earnings_total}$")
        embed.add_embed_field(
            name="Multiplier", value=f"{info.earnings_info.multiplier}")
        embed.set_footer(
            text=f"You are earning with {info.devices_info.total_devices - offlineDevices(info)}/{info.devices_info.total_devices-hiddenDevices(info.auth)} Devices",
            icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    def new_transaction(self, info: AllInformation):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)
        transaction = info.transaction_info.transactions[0]
        embed = DiscordEmbed(
            title="New Redeem Request",
            description="New redeem request has been submitted",
            color="07FF70"
        )
        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="UUID", value=f"{transaction.uuid}")
        embed.add_embed_field(name="Amount", value=f"+{transaction.amount}$")
        embed.add_embed_field(
            name="Method", value=f"{transaction.payment_method}")
        embed.add_embed_field(name="Status", value=f"{transaction.status}")
        embed.add_embed_field(name="Email", value=f"{transaction.email}")
        embed.add_embed_field(
            name="Redeem Date", value=f"{transaction.redeem_date.strftime('%Y-%m-%d')}")
        footer_text = f"Payment {transaction.status} as on {transaction.payment_date.strftime('%Y-%m-%d')} via {transaction.payment_method}"

        embed.set_footer(
            text=footer_text, icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()



    def update_available(self, webhook_url, params):
        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        embed = DiscordEmbed(
            title="New Version available!",
            color="0002ff"
        )
        embed.set_thumbnail(
            url="https://img.icons8.com/nolan/96/downloading-updates.png")
        embed.add_embed_field(name="Changelog", value=f"```{params['body']}```", inline=True)
        embed.add_embed_field(
            name="Update", value=f"[Download](https://github.com/Yariya/EarnApp-Earning-Monitor/releases/{params['tag_name']}/)", inline=False)
        footer_text = f"Update to the latest version now."

        embed.set_footer(
            text=footer_text, icon_url="https://img.icons8.com/fluency/256/000000/update-left-rotation.png")
        webhook.add_embed(embed)
        webhook.execute()
