import json

import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
from pyEarnapp.earnapp import DevicesInfo, Transaction, EarningInfo, UserData
from functions import AllInformation


# Very inefficient to make this like this but I leave it for now

def offlineDevices(header):
    try:
        params = (
            ('appid', 'earnapp_dashboard'),
            ('version', '1.284.850'),
        )
        dev = requests.get("https://earnapp.com/dashboard/api/devices?appid=earnapp_dashboard&version=1.284.850", headers=header)
        json_data = {
            'list': [],
        }
        g = json.loads(dev.text)
        for e in g:
            json_data['list'].append({
                "uuid": e["uuid"],
                "appid": e["appid"]
            })
        response = requests.post('https://earnapp.com/dashboard/api/device_statuses', headers=header, params=params, json=json_data)
        statuses = json.loads(response.text)
        offlineDevs = 0
        for i in statuses["statuses"]:
            if not statuses["statuses"][i]["online"]:
                offlineDevs+=1
        return offlineDevs
    except Exception as e:
        print(f"Erreur est survenue! Vous pouvez ignorer cela si vous ne souhaitez pas utiliser la fonction d'état de l'appareil. Essayez de redémarrer le moniteur et si cela se produit toujours, contactez les développeurs !\n{e}")
        return 0

def onlineDevices(header):
    try:
        params = (
            ('appid', 'earnapp_dashboard'),
            ('version', '1.284.850'),
        )
        dev = requests.get("https://earnapp.com/dashboard/api/devices?appid=earnapp_dashboard&version=1.284.850", headers=header)
        json_data = {
            'list': [],
        }
        g = json.loads(dev.text)
        for e in g:
            json_data['list'].append({
                "uuid": e["uuid"],
                "appid": e["appid"]
            })
        response = requests.post('https://earnapp.com/dashboard/api/device_statuses', headers=header, params=params, json=json_data)
        statuses = json.loads(response.text)
        offlineDevs = 0
        for i in statuses["statuses"]:
            if statuses["statuses"][i]["online"]:
                offlineDevs+=1
        return offlineDevs
    except Exception as e:
        print(f"Erreur est survenue! Vous pouvez ignorer cela si vous ne souhaitez pas utiliser la fonction d'état de l'appareil. Essayez de redémarrer le moniteur et si cela se produit toujours, contactez les développeurs !\n{e}")
        return 0

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


lastUpdateBalanceChange = 0
lastUpdateTrafficChange = 0

class WebhookTemplate:
    def __init__(self) -> None:
        pass

    def trafficGraph(self, graphPath, info: AllInformation):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)

        embed = DiscordEmbed(
            title="Nouvelles informations sur le trafic disponibles !",
            color="00ff00"
        )
        with open(graphPath, "rb") as f:
            webhook.add_file(file=f.read(), filename="graph.png")
        embed.set_image(url="attachment://graph.png")
        embed.set_footer(text="")
        webhook.add_embed(embed)
        webhook.execute()

    def device_gone_offline(self, info: AllInformation, count: int, devices):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)
        embed = DiscordEmbed(
            title=f"[WARNING] [{count}] DISPOSITIF(S) HORS-LIGNE ",
            description=f"{count} Le ou les appareils viennent de se déconnecter !  {info.devices_info.total_devices-info.devices_info.banned_devices-offlineDevices(info.auth)} appareil(s) restent ...",
            color="ff0000"
        )
        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Device List", value=f"\n".join(devices))

        embed.set_footer(
            text=f"{info.devices_info.total_devices - offlineDevices(info.auth)}/{info.devices_info.total_devices - hiddenDevices(info.auth)} Appareil(s)",
            icon_url="https://img.icons8.com/external-becris-lineal-color-becris/64/000000/external-iot-fintech-becris-lineal-color-becris.png")
        webhook.add_embed(embed)
        webhook.execute()

    def send_first_message(self, info: AllInformation):

        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)

        embed = DiscordEmbed(
            title="Bot démarré 🤖",
            description="Earnapp Earning Monitor a été lancé.",
            color="FFFFFF"
        )

        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Pseudo", value=f"{info.user_info.name}")
        embed.add_embed_field(
            name="Multiplicateur ", value=f"{info.earnings_info.multiplier}x")
        embed.add_embed_field(
            name="Solde", value=f"{info.earnings_info.balance}$")
        embed.add_embed_field(name="Solde à vie",
                              value=f"{info.earnings_info.earnings_total}$")
        embed.add_embed_field(name="Solde du Référencement", value=f"{info.earnings_info.bonuses}$")
        embed.add_embed_field(name="Nombre total d'appareils",
                              value=f"{info.devices_info.total_devices}")
        embed.add_embed_field(name="Statut du périphérique",
                              value=f"En ligne: {onlineDevices(info.auth)}\nHors ligne: {offlineDevices(info.auth)}\nCaché: {hiddenDevices(info.auth)}")
        embed.add_embed_field(
            name="Nombre total d'appareils",
            value=f"{info.devices_info.windows_devices} Windows\n{info.devices_info.linux_devices} Linux\n{info.devices_info.other_devices} Autres",
            inline=True)
        embed.add_embed_field(name="Bugs?",
                              value=f"[Contact Devs.](https://github.com/Yariya/EarnApp-Earning-Monitor/issues)")
        embed.set_footer(text=f"Version: 2.2.0.2",
                         icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    # def device_status_change(self, info: AllInformation, ):

    def balance_update(self, info: AllInformation, delay: int):
        global lastUpdateBalanceChange, lastUpdateTrafficChange
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)
        change = round(info.earnings_info.balance - info.previous_balance, 2)

        if change > 0:
            title = f"Soldes augmenté [+{change}]"
            color = "03F8C4"
        else:
            title = "Solde inchangé !"
            color = "E67E22"
        traffic_change = round(
            (info.devices_info.total_bandwidth_usage -
             info.previous_bandwidth_usage) / (1024 ** 2), 2)

        if change == 0 or traffic_change == 0:
            value = "Aucun changement dans le trafic ."
        else:
            value = f'{round(change / (traffic_change / 1024), 2)} $/GB'

        embed = DiscordEmbed(
            title=title,
            color=color
        )

        try:
            moneyPercentage = "{0:+.2f}%".format((change / lastUpdateBalanceChange) * 100.0 - 100)
            trafficPercentage = "{0:+.2f}%".format(
                (traffic_change / lastUpdateTrafficChange) * 100.0 - 100)
        except ZeroDivisionError:
            moneyPercentage = ':|'
            trafficPercentage = ':|'

        lastUpdateBalanceChange = change
        lastUpdateTrafficChange = traffic_change

        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="Gagné ", value=f"+{change}$ ({moneyPercentage})")
        embed.add_embed_field(name="Trafic", value=f"+{traffic_change} MB ({trafficPercentage})")
        embed.add_embed_field(name="Prix Moyen/GB", value=value)
        embed.add_embed_field(name="Solde",
                              value=f"{info.earnings_info.balance}$")
        embed.add_embed_field(name="Solde de parrainage ",
                              value=f"{info.earnings_info.bonuses}$")
        embed.add_embed_field(name="Solde à vie",
                              value=f"{info.earnings_info.earnings_total}$")
        embed.add_embed_field(
            name="Multiplicateur", value=f"{info.earnings_info.multiplier}")
        if delay < 5:
            embed.add_embed_field(
                name="[Warning]", value=f"Votre retard est peut-être trop faible ! Essayez de définir un délai plus élevé.")
        embed.set_footer(
            text=f"Vous gagnez avec {info.devices_info.total_devices - offlineDevices(info.auth)}/{info.devices_info.total_devices-hiddenDevices(info.auth)} appareils",
            icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()

    def new_transaction(self, info: AllInformation):
        webhook = DiscordWebhook(url=info.webhook_url, rate_limit_retry=True)
        transaction = info.transaction_info.transactions[0]
        embed = DiscordEmbed(
            title="Nouvelle demande de payement ",
            description="Une nouvelle demande de payement a été soumise ",
            color="07FF70"
        )
        embed.set_thumbnail(
            url="https://www.androidfreeware.net/img2/com-earnapp.jpg")
        embed.add_embed_field(name="UUID", value=f"{transaction.uuid}")
        embed.add_embed_field(name="PPrix", value=f"+{transaction.amount}$")
        embed.add_embed_field(
            name="Via", value=f"{transaction.payment_method}")
        embed.add_embed_field(name="Statut", value=f"{transaction.status}")
        embed.add_embed_field(name="Email", value=f"{transaction.email}")
        embed.add_embed_field(
            name="Date", value=f"{transaction.redeem_date.strftime('%Y-%m-%d')}")
        footer_text = f"Paiement {transaction.status} le {transaction.payment_date.strftime('%Y-%m-%d')} via {transaction.payment_method}"

        embed.set_footer(
            text=footer_text, icon_url="https://img.icons8.com/color/64/000000/paypal.png")
        webhook.add_embed(embed)
        webhook.execute()



    def update_available(self, webhook_url, params):
        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        embed = DiscordEmbed(
            title="Nouvelle version disponible!",
            color="0002ff"
        )
        embed.set_thumbnail(
            url="https://img.icons8.com/nolan/96/downloading-updates.png")
        embed.add_embed_field(name="Changelog", value=f"```{params['body']}```", inline=True)
        embed.add_embed_field(
            name="Update", value=f"[Download](https://github.com/Yariya/EarnApp-Earning-Monitor/releases/{params['tag_name']}/)", inline=False)
        footer_text = f"Mettez à jour vers la dernière version maintenant."

        embed.set_footer(
            text=footer_text, icon_url="https://img.icons8.com/fluency/256/000000/update-left-rotation.png")
        webhook.add_embed(embed)
        webhook.execute()
