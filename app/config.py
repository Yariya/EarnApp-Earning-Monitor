import os
AUTH = os.environ.get("AUTH")
DELAY = int(os.environ.get("DELAY"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")


# AUTH = '' # Google Auth Cookie
# DELAY = 120 # Time to wait after server update (60-120)
# WEBHOOK_URL = '' # Discord Webhook URL
