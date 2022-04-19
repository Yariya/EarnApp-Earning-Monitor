import os
from sys import exit
from config import Configuration
from colorama import init
from graphics import Graphics
from webhooks import WebhookTemplate
from time import sleep
from datetime import datetime, timezone
from functions import *
from pyEarnapp import EarnApp
from pyEarnapp.errors import *
from updates import check_for_updates
import matplotlib.pyplot as plt
import pause

# initiallise colorama
init(autoreset=True)
automatic_redeem_local = False
redeem_email = ""
try:
    # Initiallise graphics
    graphics = Graphics()
    graphics.print_app_title()

    # get configurations
    config = Configuration()
    graphics.success("Configurations Loaded.")

    try:
        config.AUTOMATIC_REDEEM = abs(float(config.AUTOMATIC_REDEEM))
        if int(config.AUTOMATIC_REDEEM) != 0 or int(config.AUTOMATIC_REDEEM) > 2.5:
            automatic_redeem_local = True
            redeem_email = input("PayPal Email: ")
            if redeem_email == "" or "@" not in redeem_email:
                raise Exception
    except Exception as e:
        graphics.warn("Check automatic redeem value. Reconfigure or edit config from ~user/.earnapp-earnings-monitor")
        exit()
    # initiallise earnapp
    api = EarnApp(config.AUTH)
    graphics.success("Earnapp Earning Monitor Started.")

    webhook_templates = WebhookTemplate()
except (KeyboardInterrupt, SystemExit):
    graphics.warn("Received exit signal!")
    exit()



def payoutBalance(header):
    try:
        params = (
            ('appid', 'earnapp_dashboard'),
            ('version', '1.285.887'),
        )
        json_data = {
            'to': redeem_email,
            'payment_method': 'paypal.com',
        }
        requests.post('https://earnapp.com/dashboard/api/redeem', headers=header, params=params, json=json_data)
    except Exception as e:
        pass # Handling later

def main():
    graphics.info("Checking for updates.")
    updateCheck = check_for_updates()
    if updateCheck != "":
        webhook_templates.update_available(config.WEBHOOK_URL, updateCheck)
    global info, device_status_change
    try:
        # Earnapp
        info = AllInformation(config.WEBHOOK_URL, api, graphics)
        # Discord Webhook
        test_discord_webhook(graphics, config.WEBHOOK_URL)
    except AuthenticationError:
        graphics.error("Looks like a wrong oauth-refresh-token.")
        exit()

    display_initial_info(graphics, info)
    webhook_templates.send_first_message(info)

    info.previous_balance = info.earnings_info.balance
    info.previous_number_of_transactions = info.transaction_info.total_transactions
    info.previous_bandwidth_usage = info.devices_info.total_bandwidth_usage


    # Offline devices
    offline_change = 0
    device_status_change = []

    # Too many duplicates of offline/online functions cleaning up soon
    def offline_device_len(header):
        try:
            params = (
                ('appid', 'earnapp_dashboard'),
                ('version', '1.284.850'),
            )
            dev = requests.get("https://earnapp.com/dashboard/api/devices?appid=earnapp_dashboard&version=1.284.850",
                               headers=header)
            json_data = {
                'list': [],
            }
            g = json.loads(dev.text)
            for e in g:
                json_data['list'].append({
                    "uuid": e["uuid"],
                    "appid": e["appid"]
                })
            response = requests.post('https://earnapp.com/dashboard/api/device_statuses', headers=header, params=params,
                                     json=json_data)
            statuses = json.loads(response.text)
            offlineDevs = 0
            for i in statuses["statuses"]:
                if not statuses["statuses"][i]["online"]:
                    offlineDevs += 1
            return offlineDevs
        except Exception as e:
            print(
                f"Error occurred! You can ignore this if you don't want to use device status function. Try restarting the monitor and if it still occurs contact devs!\n{e}")
            return 0

    def device_changes():
        nonlocal offline_change
        global device_status_change
        offline_change = offline_device_len(info.auth)
        device_status_change = info.device_status

    device_changes()

     #trafficGraph = [0 for x in range(24)]
    #c = 0
    #startTime = datetime.now(timezone.utc).strftime("%H")

    while 1:
        info.get_info()
        # initialise locals
        balance_change = 0
        traffic_change = 0

        bandwidth = round(info.devices_info.total_bandwidth_usage / (1024 ** 2), 2)

        def calculate_changes():
            nonlocal balance_change, traffic_change
            # calculate changes
            balance_change = round(info.earnings_info.balance - info.previous_balance, 2)
            traffic_change = round((info.devices_info.total_bandwidth_usage - info.previous_bandwidth_usage) / (1024 ** 2), 2)
        calculate_changes()
        if automatic_redeem_local:
            if info.earnings_info.balance > config.AUTOMATIC_REDEEM:
                payoutBalance(info.auth)
        # Soon
        '''
        if c == int(config.TRAFFIC_GRAPH_INTERVAL):
            try:
                x = []
                i = startTime
                for _ in range(0, int(config.TRAFFIC_GRAPH_INTERVAL)):
                    if i >= 24:
                        i = 1
                    x.append(i)
                    i+=1
                print(x)
                y = trafficGraph

                # plot
                plt.title("Traffic")
                plt.xlabel("time (utc)")
                plt.ylabel("mb")

                plt.scatter(x, y)

                # beautify the x-labels
                plt.gcf().autofmt_xdate()
                myFmt = mdates.DateFormatter('%H')
                plt.gca().xaxis.set_major_formatter(myFmt)
                plt.savefig(os.path.expanduser('~')+"\\.earnapp-earning-monitor\\tmp.png")
                webhook_templates.trafficGraph(os.path.expanduser('~')+"\\.earnapp-earning-monitor\\tmp.png", info)
                c = 0
            except:
                graphics.error("Graph Error!")

        trafficGraph[c+1] = balance_change
        c += 1 # Number of updates
        '''


        # Still causing problems.
        if offline_device_len(info.auth) > offline_change:
            # x Devices just got offline
            try:
                off = []
                for token in info.device_status:
                    if device_status_change[token] != info.devices_info[token]:
                        off.append(str(token))
                graphics.warn(f"{offline_device_len() - offline_change} Device(s) just went offline!\n")
                print("\t (offline)\n".join(off))
                device_changes()
                webhook_templates.device_gone_offline(info, offline_device_len() - offline_change, off)
            except Exception as e:
                graphics.warn("Device(s) just got offline. Watch out. Failed to send message.")


        if balance_change != 0:
            # After a redeem request, the initial balance & initial traffic is assumed to be 0.
            if info.earnings_info.balance < info.previous_balance:
                info.previous_balance = 0
                info.previous_bandwidth_usage = 0
                calculate_changes()
            graphics.balance_increased("Balance Updated.")
            graphics.balance_increased(f"+{balance_change}$")
            graphics.balance_increased(f"Traffic +{traffic_change}MB")
        else:
            if config.DELAY < 5:
                graphics.warn(f"Delay is to low. There might be update issues.")

            graphics.balance_unchanged(
                f"Your balance has not changed. Current balance: {info.earnings_info.balance}")
            graphics.balance_unchanged(
                f"No traffic change detected. Current bandwidth usage: {bandwidth} MB")
        webhook_templates.balance_update(info, config.DELAY)


        # new redeem request
        graphics.info(
            f"Number of transactions: {info.transaction_info.total_transactions}")

        if check_redeem_requests(graphics, info, webhook_templates):
            webhook_templates.new_transaction(info)

        # update historical data
        info.previous_balance = info.earnings_info.balance
        info.previous_number_of_transactions = info.transaction_info.total_transactions
        info.previous_bandwidth_usage = info.devices_info.total_bandwidth_usage

        # wait for the minute to end
        if check_for_updates():
            webhook_templates.update_available(config.WEBHOOK_URL)

        next_update_time = datetime.now(timezone.utc).replace(minute=config.DELAY) + timedelta(minutes=config.INTERVAL)
        next_update_time = datetime.now(timezone.utc) + timedelta(minutes=config.INTERVAL+config.DELAY) \
            if next_update_time < datetime.now(timezone.utc) else None  # make sure time is in future
        next_update_in(next_update_time, graphics)
        pause.until(next_update_time)



if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        graphics.warn("Received exit signal!")
        exit()
