# EarnApp-Earning-Monitor
Watches your earnings on EarnApp and notifies you when you earned balance or received an payout.

Containerised by [https://github.com/fazalfarhan01](https://github.com/fazalfarhan01)

![unknown (7)](https://user-images.githubusercontent.com/65712074/140953429-4049d955-f99e-461b-b03e-94d78ce2d98d.png)
![Ohjijq6M7nlCczQVWxH5zf7uZ](https://user-images.githubusercontent.com/65712074/140953604-72e84743-d294-40cf-b4a2-7591df34c088.png)


![I3BX998HBWdqAuMa81oJhhlWe](https://user-images.githubusercontent.com/65712074/140958375-282ef443-ab8d-4304-86ed-b334e68377ce.png)


# Installation

## Docker-Compose
```BASH
version: "3.3"
services:
  app:
    image: fazalfarhan01/earnapp-earning-monitor
    restart: always
    environment:
      AUTH: YOUR_AUTH_COOKIE_HERE
      DELAY: 60
      WEBHOOK_URL: YOUR_WEBHOOK_URL_HERE

```

### Windows/Linux

- Install [Python3](https://www.python.org/downloads/)
- Download or clone this repo.
- Unzip and put in directory
- Install Dependencies
  * `pip3 install requests`
  * `pip3 install discord_webhook`
  * `pip3 install colorama`
- Open `app/config.py`
  ```py
  auth = '' # Google Auth Cookie
  delay = 120 # Time to wait after server update (60-120)
  webhook_url = '' # Discord Webhook URL
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
   
   ![ZcXmT1zW3otc1Fu0QHTMOcQHO](https://user-images.githubusercontent.com/65712074/140956237-0ba63c31-94b7-4d67-a80b-dc8438fdb010.gif)

   * Click where the name is `money?appid=earnapp_dashboard&version[version number]`
   * Scroll down a bit until you see `cookies`
   * Copy the AUTH after `oauth-refresh-token=`
   
   ![bpR8BPGRpf3cqRkT004Ejywmj](https://user-images.githubusercontent.com/65712074/140639500-01b4aa40-91bf-48eb-a4af-a45a4b615d4d.png)
4) You're done :)

### Remember
  * This does not use an official API from earnapp so bugs may occur

## Credits
- [EarnApp](https://earnapp.com/)
- [LockBlock](https://github.com/LockBlock-dev/) [ItzDatMC](https://github.com/ItzDatMC) [Woodie-07](https://github.com/Woodie-07) [merwie](https://github.com/merwie) 

## Version
- 1.1
