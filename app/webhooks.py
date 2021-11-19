from discord_webhook import DiscordEmbed, DiscordWebhook
from pyEarnapp import EarnApp


class WebhookTemplate:
    def __init__(self) -> None:
        pass

    def send_first_message(self, webhook_url: str, user_info, earnings_info, devices_info):
        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)

        embed = DiscordEmbed(
            title="Bot Started 🤖",
            description="Earnapp Earning Monitor has been started.",
            color="03b2f8")

        embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Username", value=f"{user_info.name}")
        embed.add_embed_field(name="Multiplier", value=f"{earnings_info.multiplier}")
        embed.add_embed_field(name="Balance", value=f"{earnings_info.balance}")
        embed.add_embed_field(name="Lifetime Balance", value=f"{earnings_info.earnings_total}")
        embed.add_embed_field(name="Total Devices", value=f"{devices_info.total_devices}")
        embed.add_embed_field(name="Devices", value=f"Windows: {devices_info.windows_devices}\nLinux: {devices_info.linux_devices}\nOther: {devices_info.other_devices}", inline=False)
        embed.set_footer(text=f"by toothyraider201", icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    def balance_changed(self, webhook_url, user_info, earnings_info, devices_info, previous_balance):
        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        change = round(earnings_info.balance - previous_balance, 2)
        if change > 0:
            description = "Your EarnApp Balance has been updated!"
            color = "03B2F8"
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

    def new_transaction(self, webhook_url, user_info, earnings_info, devices_info, transaction_info):
        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        embed = DiscordEmbed(
            title="New Redeem Request",
            description="New redeem request has been submitted",
            color="02ECC71"
        )
        embed.set_thumbnail(url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Amount", value=f"+{transaction_info[0].amount}$")
        embed.add_embed_field(name="Method", value=f"{transaction_info[0].payment_method}")
        embed.add_embed_field(name="Status", value=f"{transaction_info[0].status}")
        embed.set_footer(text=f"You are earning with {devices_info.total_devices} Devices",icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

