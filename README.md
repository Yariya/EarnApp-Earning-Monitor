# EarnApp-Earning-Monitor
Watches your earnings on EarnApp and notifies you when you earned balance or received an payout.

Containerised by [https://github.com/fazalfarhan01](https://github.com/fazalfarhan01)
![Screenshot 2021-11-18 110427](https://user-images.githubusercontent.com/45929854/142373141-5f1dd484-4124-4bf3-a2b9-d731833725f1.png)


![TtB7FfrHSF1O7AxwnRUin9OHe](https://user-images.githubusercontent.com/65712074/142068590-cd6de535-0410-4451-af13-357543c35ace.png)



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
