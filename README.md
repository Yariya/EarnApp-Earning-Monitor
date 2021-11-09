# EarnApp-Earning-Monitor
Watches your earnings on EarnApp and notifies you when you earned balance or received an payout.


![unknown (7)](https://user-images.githubusercontent.com/65712074/140953429-4049d955-f99e-461b-b03e-94d78ce2d98d.png)
![Ohjijq6M7nlCczQVWxH5zf7uZ](https://user-images.githubusercontent.com/65712074/140953604-72e84743-d294-40cf-b4a2-7591df34c088.png)

![rpcVV21JL6H8O6MebHe3xINXo](https://user-images.githubusercontent.com/65712074/140954872-61be8ab7-6881-4142-be20-8b395aa3df46.png)


## Installation

- Install [Python3](https://www.python.org/downloads/)
- Download or clone this repo.
- Unzip and put in directory
- Install Dependencies
  * `pip3 install requests`
  * `pip3 install discord_webhook`
- Open `config.py`
  ```py
  AUTH = '' # Google Auth Cookie
  Delay = 120 # Time to wait after server update (60-120)
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
- [LockBlock](https://github.com/LockBlock-dev/) For giving me the Idea :)
- [ItzDatMC](https://github.com/ItzDatMC) helping Pull Requests :)
- [Woodie-07](https://github.com/Woodie-07) helping typo :)
- [merwie](https://github.com/merwie) helping typo :)

## Version
- 1.1
