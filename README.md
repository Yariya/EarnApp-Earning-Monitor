# EarnApp-Earning-Monitor
Watches your earnings on EarnApp and notifies you when you earned balance or received an payout.

Containerised by [https://github.com/fazalfarhan01](https://github.com/fazalfarhan01)

![rsz_pycharm64_iunja2sz3v](https://user-images.githubusercontent.com/65712074/156200038-0a928e35-e03b-4e3a-a8ba-b472cbf4e92f.png)  ![rsz_1discord_b6nzsvxaid](https://user-images.githubusercontent.com/65712074/156201782-4c2d05c2-723f-43ad-b4b8-c9b7a1ef54a9.png)
![Discord_NSorrCkHs2](https://user-images.githubusercontent.com/65712074/156205217-f5ab3e09-091e-4ca5-8069-463356a87bf0.png)


NOTE: `This is not a trojan! This is completely open source and you can check the source for yourself. Nothing is obfuscated.`



# Installation

## Docker
### Compose
```YML
version: "3.3"
services:
  app:
    image: fazalfarhan01/earnapp-earning-monitor
    restart: always
    environment:
      DELAY: 2 # MINUTES TO WAIT AFTER UTC *:00 TO CHECK FOR UPDATE | DEFAULT 2 MINUTES
      AUTH: YOUR_AUTH_COOKIE_HERE
      WEBHOOK_URL: YOUR_WEBHOOK_URL_HERE
```
### Non Compose
```BASH
docker run -d --restart always --name earnapp-monitor \
-e AUTH=YOUR_AUTH_COOKIE_HERE \
-e WEBHOOK_URL=YOUR_WEBHOOK_URL_HERE \
-e DELAY=2 \
fazalfarhan01/earnapp-earning-monitor:python-latest
```
  - Example
  ```BASH
docker run -d --restart always --name earnapp-monitor 
-e AUTH=1%2%adfbg-afvbfab-asfdbadbf -e WEBHOOK_URL=https://discord.com/api/webhooks/akjsdvasdvjafvb -e DELAY=2 fazalfarhan01/earnapp-earning-monitor:python-latest
```

## Windows
- Download the executable file from [releases](https://github.com/Yariya/EarnApp-Earning-Monitor/releases)
- Double click and run. (`Windows Defender might detect it as a trojan. Nothing to worry, it's a false positive. You will have to allow it from windows defender's protection history.`)
### Need more help?
Check out this video.

[![image](https://user-images.githubusercontent.com/45929854/142722065-6d765156-87f0-4c58-b4c3-2a21ea83ebc7.png)](https://www.youtube.com/watch?v=KBGQSFEdIsc)

## Windows Installation From Source

- Install [Python3](https://www.python.org/downloads/)
- Download or clone this repo.
- Unzip and put in directory
- Install Dependencies
  * `pip3 install discord_webhook pyEarnapp colorama`
  - On Windows, run `install.bat`
- Run `start.bat`

## Linux Installation
 - Install [Python3](https://www.python.org/downloads/)
 - Install python3-pip
        `apt install -y python3-pip`
 - Download or clone this repo.
 - Unzip and put in directory
 - Install Dependencies
   - `pip3 install discord_webhook pyEarnapp colorama`
   - On Linux, run `install.sh`
 - Run `start.sh`

### How to get Google Auth
1) Go to the EarnApp [Dashboard](https://earnapp.com/dashboard/)
2) Login with Google
3) Open Developer tools with `CTR+SHIFT+I`
   * Go to **Application** TAB
   
   ![image](https://user-images.githubusercontent.com/45929854/142379296-dc321d08-7f1b-4eb5-bc3d-cf2fde9c0e01.png)

   * Go to `Storage` > `Cookies` > `https://earnapp.com`

   ![image](https://user-images.githubusercontent.com/33323458/142406885-451e0d2e-5c33-42a0-a1b1-967ea63ec511.png)

   * Click on `oauth-refresh-token`
   
   ![image](https://user-images.githubusercontent.com/45929854/142379619-4f9c15a3-8710-4e11-bded-18ea1e4898d8.png)

   * Copy the entire thing as is.
   
   ![image](https://user-images.githubusercontent.com/45929854/142380234-5cb16cc8-4bce-49c0-8e82-706c9c156496.png)
4) You're done :)

### Remember
  * This does not use an official API from EarnApp so bugs may occur.

## Credits
- [EarnApp](https://earnapp.com/)
- Thanks to [fazalfarhan01](https://github.com/fazalfarhan01) for completely reworking this project :)
## Version
- 2.2.0.1
