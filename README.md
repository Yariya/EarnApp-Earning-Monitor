# EarnApp-Earning-Monitor
Watches your earnings on EarnApp and notifies you when you earned balance or received an payout.

![zmX0s0RozyN5IjdcDMrw3sfTy](https://user-images.githubusercontent.com/65712074/140638993-09a3645e-3c4b-48b1-b139-ee2c1387c79e.png)
![wueUME2JVYzlP4iyfXFtJiaAH](https://user-images.githubusercontent.com/65712074/140639093-7925bb31-52b7-42c1-81a5-0a3ce755438b.png)


## Installation

- Install [Python3](https://www.python.org/downloads/)
- Download this repo.
- Unzip and put in directory
- Install Dependencies
  * `pip3 install requests`
  * `pip3 install discord_webhook`
- Open `config.py`
  ```py
  AUTH = '' # Google Auth Cookie
  Delay = 300 # Interval to check balance in seconds
  WebhookURL = '' # Discord Webhook URL
  ```
- Run `python3 main.py`

### How to get Google Auth
1) Go to the EarnApp [Dashboard](https://earnapp.com/dashboard/)
2) Login with Google
3) Open Developer tools with `CTR+SHIFT+I`
   * Goto Network TAB
   
   ![qATMniDchDUWiR9Y1LQGimLOQ](https://user-images.githubusercontent.com/65712074/140639251-a6be881d-b394-4fc3-a7e5-2543e80320bb.png)
   
   * Refresh Page
   * After you refreshed the Page you will see something like this
   
   ![Q0VrgDlLf14kM4v59WmKFoUZq](https://user-images.githubusercontent.com/65712074/140639334-c5f7dfe1-0600-4e01-99f0-f08db0d1489c.png)

   * Click where the name is `money?appid=earnapp_dashboard&version[version number]`
   * Scroll down a bit until you see `cookies`
   * Copy the AUTH after `oauth-refresh-token=`
   
   ![bpR8BPGRpf3cqRkT004Ejywmj](https://user-images.githubusercontent.com/65712074/140639500-01b4aa40-91bf-48eb-a4af-a45a4b615d4d.png)
4) You're done :)

### Remember
  * This does not use an official API from earnapp so bugs may occur

## Credits
- [EarnApp](https://earnapp.com/)
- [LockBlock](https://github.com/LockBlock-dev/) For giving me the Idea :)
- [ItzDatMC](https://github.com/ItzDatMC) helping Pull Requests :)
- [Woodie-07](https://github.com/Woodie-07) helping typo :)
- [merwie](https://github.com/merwie) helping typo :)
