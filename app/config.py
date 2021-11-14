import os

auth = '' # Google Auth Cookie
delay = 120 # Time to wait after server update (60-120)
webhook_url = '' # Discord Webhook URL

# Docker

AUTH = (auth if os.environ.get("AUTH") is None else os.environ.get("AUTH"))
DELAY = (delay if os.environ.get("DELAY") is None else int(os.environ.get("DELAY")))
WEBHOOK_URL = (webhook_url if os.environ.get("WEBHOOK_URL") is None else os.environ.get("WEBHOOK_URL"))
