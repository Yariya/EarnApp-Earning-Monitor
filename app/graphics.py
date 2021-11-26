from colorama import Fore


class Graphics:
    def print_app_title(self):
        print(self.app_title)

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
        self.app_title = f"""{Fore.LIGHTBLUE_EX}
███████╗ █████╗ ██████╗ ███╗   ██╗ █████╗ ██████╗ ██████╗ 
██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔══██╗
█████╗  ███████║██████╔╝██╔██╗ ██║███████║██████╔╝██████╔╝
██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║██╔══██║██╔═══╝ ██╔═══╝ 
███████╗██║  ██║██║  ██║██║ ╚████║██║  ██║██║     ██║     
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝     
 ███████╗ █████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗ 
 ██╔════╝██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝ 
 █████╗  ███████║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗
 ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║
 ███████╗██║  ██║██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝
 ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
███╗   ███╗ ██████╗ ███╗   ██╗██╗████████╗ ██████╗ ██████╗ 
████╗ ████║██╔═══██╗████╗  ██║██║╚══██╔══╝██╔═══██╗██╔══██╗
██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║   ██║   ██║██████╔╝
██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║   ██║   ██║██╔══██╗
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║   ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
by fazalfarhan01 (https://github.com/fazalfarhan01)
Version: 2.1.6"""
