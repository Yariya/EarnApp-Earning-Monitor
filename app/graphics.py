from colorama import Fore

VERSION = "2.1.7.1"

class Graphics:
    def print_app_title(self):
        print(self.app_title_gradient_new)  # self.app_title

    def success(self, message):
        print(f"\t{Fore.LIGHTGREEN_EX}[✓] {message}")

    def error(self, message):
        print(f"\t{Fore.LIGHTRED_EX}[X] {message}")

    def warn(self, message):
        print(f"\t{Fore.LIGHTYELLOW_EX}[!] {message}")

    def info(self, message):
        print(f"\t{Fore.LIGHTBLUE_EX}[i] {message}")

    def balance_increased(self, message):
        print(f"\t{Fore.GREEN}[💰] {message}")

    def new_transaction(self, message):
        print(f"\t{Fore.GREEN}[🤑] {message}")

    def balance_unchanged(self, message):
        print(f"\t{Fore.YELLOW}[💱] {message}")

    def __init__(self) -> None:
        self.app_title_gradient_new = f"""{Fore.CYAN}
 /$$$$$$$$                                /$$$$$$                     
| $$_____/                               /$$__  $$                    
| $$        /$$$$$$   /$$$$$$  /$$$$$$$ | $$  \ $$  /$$$$$$   /$$$$$$ 
| $$$$$    |____  $$ /$$__  $$| $$__  $$| $$$$$$$$ /$$__  $$ /$$__  $$
| $$__/     /$$$$$$$| $$  \__/| $$  \ $$| $$__  $$| $$  \ $$| $$  \ $$
| $$       /$$__  $$| $$      | $$  | $$| $$  | $$| $$  | $$| $$  | $$
| $$$$$$$$|  $$$$$$$| $$      | $$  | $$| $$  | $$| $$$$$$$/| $$$$$$$/
|________/ \_______/|__/      |__/  |__/|__/  |__/| $$____/ | $$____/ 
            Earnings Monitor                      | $$      | $$      
by:                                               | $$      | $$      
   github.com/Yariya & github.com/fazalfarhan01   |__/      |__/

App Version: {VERSION}
"""
