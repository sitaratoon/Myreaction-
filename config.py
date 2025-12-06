import os
from typing import List

API_ID = os.environ.get("API_ID", "")
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN = int(os.environ.get("ADMIN", "6692613520"))
PICS = (os.environ.get("PICS", "")).split()

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003455925059"))

DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")

IS_FSUB = os.environ.get("IS_FSUB", "True").lower() == "True"  # Set "True" For Enable Force Subscribe
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1003022855971").split())) # Add Multiple channel ids

EMOJIS = ["❤‍🔥", "🤗", "🔥", "🥰", "👏", "😁", "😘", "🥶", "🤩", "👍", "😎", "🙏", "😍", "💯"]
