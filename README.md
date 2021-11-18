# EarnApp-Earning-Monitor
Watches your earnings on EarnApp and notifies you when you earned balance or received an payout.

Containerised by [https://github.com/fazalfarhan01](https://github.com/fazalfarhan01)

![Bot Started CLI](https://user-images.githubusercontent.com/45929854/142378521-13373e59-3657-4cb4-b89a-cde4890e7065.png)![Bot Started](https://user-images.githubusercontent.com/45929854/142378687-e31c454b-6662-4dc9-ac32-666c13fab3fe.png)![Balance Update](https://user-images.githubusercontent.com/45929854/142378692-47ff492f-370c-4e02-bfe1-7851959b9166.png)





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
      AUTH: YOUR_AUTH_COOKIE_HERE
      WEBHOOK_URL: YOUR_WEBHOOK_URL_HERE
```
### Non Compose
```BASH
docker run -d --restart always --name earnapp-monitor \
-e AUTH=YOUR_AUTH_COOKIE_HERE \
-e WEBHOOK_URL=YOUR_WEBHOOK_URL_HERE \
fazalfarhan01/earnapp-earning-monitor:python-latest
```
  - Example
  ```BASH
docker run -d --restart always --name earnapp-monitor 
-e AUTH=1%2%adfbg-afvbfab-asfdbadbf -e WEBHOOK_URL=https://discord.com/api/webhooks/akjsdvasdvjafvb fazalfarhan01/earnapp-earning-monitor:python-latest
```


## Windows/Linux

- Install [Python3](https://www.python.org/downloads/)
- Download or clone this repo.
- Unzip and put in directory
- Install Dependencies
  * `pip3 install discord_webhook pyEarnapp colorama`
  - On Windows, run `install.bat`
- Run `start.bat`

### How to get Google Auth
1) Go to the EarnApp [Dashboard](https://earnapp.com/dashboard/)
2) Login with Google
3) Open Developer tools with `CTR+SHIFT+I`
   * Go to **Application** TAB
   
   ![image](https://user-images.githubusercontent.com/45929854/142379296-dc321d08-7f1b-4eb5-bc3d-cf2fde9c0e01.png)

   * Go to `Storage` > `Cookies` > `https://earnapp.com`

  ![image](https://user-images.githubusercontent.com/33323458/142406676-410e8e4c-6030-4c0a-95f8-7f5ac6bb3191.png)

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
- 2.1
