from discord_webhook import DiscordEmbed, DiscordWebhook
from pyEarnapp.earnapp import DevicesInfo, Transaction, EarningInfo, UserData
from functions import AllInformation


class WebhookTemplate:
    def __init__(self) -> None:
        pass

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
            name="Multiplier", value=f"{info.earnings_info.multiplier}")
        embed.add_embed_field(
            name="Balance", value=f"{info.earnings_info.balance}")
        embed.add_embed_field(name="Lifetime Balance",
                              value=f"{info.earnings_info.earnings_total}")
        embed.add_embed_field(name="Total Devices",
                              value=f"{info.devices_info.total_devices}")
        embed.add_embed_field(
            name="Devices", value=f"{info.devices_info.windows_devices} Windows | {info.devices_info.linux_devices} Linux | {info.devices_info.other_devices} Others", inline=False)
        embed.add_embed_field(name="Bugs?",
                              value=f"[Contact Devs.](https://github.com/Yariya/EarnApp-Earning-Monitor/issues)")
        embed.set_footer(text=f"Version: 2.1.4",
                         icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    def balance_update(self, info: AllInformation):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)
        change = round(info.earnings_info.balance - info.previous_balance, 2)

        if change > 0:
            title = "Balance Updated!"
            color = "03F8C4"
        else:
            title = "Balance Unchanged!"
            color = "E67E22"
        traffic_change = round(
            (info.devices_info.total_bandwidth_usage -
             info.previous_bandwidth_usage)/(1024**2), 2)

        if change == 0 or traffic_change == 0:
            value = "No change in traffic."
        else:
            value = f'{round(change/(traffic_change/1024) ,2)} $/GB'

        total_earnings = info.earnings_info.earnings_total + \
            info.earnings_info.bonuses_total

        embed = DiscordEmbed(
            title=title,
            color=color
        )
        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Earned", value=f"+{change}$")
        embed.add_embed_field(name="Traffic", value=f"+{traffic_change} MB")
        embed.add_embed_field(name="Avg. Price/GB", value=value)
        embed.add_embed_field(name="Balance",
                              value=f"{info.earnings_info.balance}$")
        embed.add_embed_field(name="Referral Balance",
                              value=f"{info.earnings_info.bonuses}$")
        embed.add_embed_field(name="Total Earnings",
                              value=f"{total_earnings}$")
        embed.add_embed_field(
            name="Multiplier", value=f"{info.earnings_info.multiplier}")
        embed.set_footer(text=f"You are earning with {info.devices_info.total_devices} Devices",
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
        embed.add_embed_field(
            name="Redeem Date", value=f"{transaction.redeem_date.strftime('%Y-%m-%d')}")
        footer_text = f"Payment {transaction.status} as on {transaction.payment_date.strftime('%Y-%m-%d')} via {transaction.payment_method}"
        
        embed.set_footer(
            text=footer_text, icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()
