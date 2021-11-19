from discord_webhook import DiscordEmbed, DiscordWebhook
from pyEarnapp.earnapp import DevicesInfo, Transaction, EarningInfo, UserData


class WebhookTemplate:
    def __init__(self) -> None:
        pass

    def send_first_message(
        self,
        webhook_url: str,
        user_info: UserData,
        earnings_info: EarningInfo,
        devices_info: DevicesInfo
    ):

        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)

        embed = DiscordEmbed(
            title="Bot Started 🤖",
            description="Earnapp Earning Monitor has been started.",
            color="FFFFFF"
        )

        embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Username", value=f"{user_info.name}")
        embed.add_embed_field(name="Multiplier", value=f"{earnings_info.multiplier}")
        embed.add_embed_field(name="Balance", value=f"{earnings_info.balance}")
        embed.add_embed_field(name="Lifetime Balance", value=f"{earnings_info.earnings_total}")
        embed.add_embed_field(name="Total Devices", value=f"{devices_info.total_devices}")
        embed.add_embed_field(name="Devices", value=f"Windows: {devices_info.windows_devices}\nLinux: {devices_info.linux_devices}\nOther: {devices_info.other_devices}", inline=False)
        embed.set_footer(text=f"Version 2.1.2 by toothyraider201", icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    def balance_update(
        self,
        webhook_url:str,
        user_info:UserData,
        earnings_info:EarningInfo,
        devices_info:DevicesInfo,
        previous_balance:float
    ):
        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        change = round(earnings_info.balance - previous_balance, 2)
        
        if change > 0:
            description = "Your EarnApp Balance has been updated!"
            color = "03F8C4"
        else:
            description = "Your EarnApp Balance has not changed."
            color = "E67E22"
        
        embed = DiscordEmbed(
            title="Balance Updated!",
            description=description,
            color=color
        )
        embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Earned", value=f"+{change}$")
        embed.add_embed_field(name="Balance", value=f"{earnings_info.balance}$")
        embed.add_embed_field(name="Total Earnings", value=f"{earnings_info.earnings_total}$")
        embed.add_embed_field(name="Referral Balance", value=f"{earnings_info.bonuses}$")
        embed.add_embed_field(name="Total Referral Earning", value=f"{earnings_info.bonuses_total}$")
        embed.add_embed_field(name="Multiplier", value=f"{earnings_info.multiplier}")
        embed.set_footer(text=f"You are earning with {devices_info.total_devices} Devices",icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    def new_transaction(
        self,
        webhook_url: str,
        user_info: UserData,
        earnings_info: EarningInfo,
        devices_info: DevicesInfo,
        transaction_info: Transaction
    ):
        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        
        embed = DiscordEmbed(
            title="New Redeem Request",
            description="New redeem request has been submitted",
            color="07FF70"
        )
        embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="UUID", value=f"+{transaction_info.uuid}$")
        embed.add_embed_field(name="Amount", value=f"+{transaction_info.amount}$")
        embed.add_embed_field(name="Method", value=f"{transaction_info.payment_method}")
        embed.add_embed_field(name="Status", value=f"{transaction_info.status}")
        embed.add_embed_field(name="Redeem Date", value=f"{transaction_info.redeem_date.strftime('%Y-%m-%d')}")
        # embed.set_footer(text=f"You are earning with {devices_info.total_devices} Devices",icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        if transaction_info.is_paid:
            footer_text = f"Paid on {transaction_info.payment_date.strftime('%Y-%m-%d')} via {transaction_info.payment_method}"
        else:
            footer_text = f"Payment expected on {transaction_info.payment_date.strftime('%Y-%m-%d')} via {transaction_info.payment_method}"
        
        embed.set_footer(text=footer_text,icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

