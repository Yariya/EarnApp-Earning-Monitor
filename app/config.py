import os
import io
import json
from time import sleep


class Configuration:
    def __init__(self) -> None:
        self.check_for_existing_config()
        # Delay before checking env. Solves docker issues.
        sleep(2)
        # if config doesn't exist
        if self.config_file_exists:
            self.__want_to_reset_config()
            if self.__reuse_config == True:
                self.load_config()
            else:
                self.ask_config()
        else:
            self.ask_config()

        self.fix_bugs()

    def fix_bugs(self):
        self.__fix_delay_bug()

    def ask_config(self):
        self.AUTH = (input("Entrez le jeton oauth-refresh-token du tableau de bord EarnApp\n\t: ")
                     if os.environ.get("AUTH") is None else os.environ.get("AUTH"))
        # 10 Minutes recommended by Vita
        self.DELAY = (10 if os.environ.get("DELAY")
                      is None else int(os.environ.get("DELAY")))
        self.WEBHOOK_URL = (input("Entrez l'URL Discord WebHook \n\t: ") if os.environ.get(
            "WEBHOOK_URL") is None else os.environ.get("WEBHOOK_URL"))
        self.AUTOMATIC_REDEEM = (input("Voulez-vous utiliser le payement automatique ? \n\t[i] Cela aide à obtenir votre  "
                                             "argents plus rapidement.\n\t[i] Si vous ne voulez pas utiliser cette fonctionnalité, mettez simplement 0 ici, sinon mettez la balance qui doit être [>2.5]\n\t: ")) if os.environ.get("AUTOMATIC_REDEEM") is None \
            else os.environ.get("AUTOMATIC_REDEEM")
        self.create_config()

    def __want_to_reset_config(self):
        if os.environ.get('container', False) == 'docker':
            self.__reuse_config = True
            return
        got_response = False
        while(not got_response):
            response = input("Vous souhaitez utiliser la configuration existante? (yes/no): ")
            if response.lower() == "yes":
                got_response = True
                self.__reuse_config = True
            elif response.lower() == "no":
                got_response = True
                self.__reuse_config = False
            else:
                print("Je n'ai pas compris, réessayez!")

    def check_for_existing_config(self):
        self.home_directory = os.path.expanduser("~")
        self.program_data_folder = ".earnapp-earning-monitor"
        self.config_file_name = "config.json"

        self.program_directory = os.path.join(self.home_directory, self.program_data_folder)
        self.config_file_path = os.path.join(self.program_directory, self.config_file_name)

        self.config_file_exists = os.path.exists(self.config_file_path)

    def create_config(self):
        if os.environ.get('container', False) == 'docker':
            print("Temps d'exécution du conteneur détecté.")
        else:
            # If config file doesn't exist
            if not self.config_file_exists:
                # If direcotry doesn't exist, create dir
                if not os.path.exists(self.program_directory):
                    os.mkdir(self.program_directory)
            config = {
                "AUTH": self.AUTH,
                "DELAY": self.DELAY,
                "WEBHOOK_URL": self.WEBHOOK_URL,
                "AUTOMATIC_REDEEM": self.AUTOMATIC_REDEEM,
            }
            with io.open(self.config_file_path, "w", encoding="utf-8") as stream:
                json.dump(config, stream, indent=2)

    def load_config(self):
        with io.open(self.config_file_path, "r", encoding="utf-8") as stream:
            try:
                config_data = json.load(stream)
                self.AUTH = config_data["AUTH"]
                self.DELAY = config_data["DELAY"]
                self.WEBHOOK_URL = config_data["WEBHOOK_URL"]
                self.AUTOMATIC_REDEEM = config_data["AUTOMATIC_REDEEM"]
            except:
                print("Il semble qu'il manque des paramètres à votre fichier de configuration... Veuillez reconfigurer.")
                exit(1)

    def __fix_delay_bug(self):
        if self.DELAY < 0 or self.DELAY >= 60:
            print('Configuration de délai non valide détectée. Fix..!')
            self.DELAY = 10 # Standart
            self.create_config()

if __name__ == "__main__":
    config = Configuration()
