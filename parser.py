"""Tools to parse Twitch chat."""
from collections import defaultdict

import yaml
from tmi import TwitchIrcBot
from dataset import datapoint

PREVIOUS_MESSAGE = defaultdict(str)
LAST_MESSAGE = {}

class TwitchChatParser(TwitchIrcBot):
    """Twitch Chat parser that reads data from IRC."""

    def on_message(self, message):
        if message.user_id in LAST_MESSAGE:
            last_message = LAST_MESSAGE[message.user_id]
            PREVIOUS_MESSAGE[message.user_id] = last_message

        LAST_MESSAGE[message.user_id] = message
        datapoint(message, str(PREVIOUS_MESSAGE[message.user_id]), ban=False)

    def on_timeout(self, timeout):
        if timeout.user_id in LAST_MESSAGE:
            message = LAST_MESSAGE[timeout.user_id]

            datapoint(message, str(PREVIOUS_MESSAGE[message.user_id]), ban=True)

    def on_ban(self, ban):
        if ban.user_id in LAST_MESSAGE:
            message = LAST_MESSAGE[ban.user_id]

            datapoint(message, str(PREVIOUS_MESSAGE[message.user_id]), ban=True)

if __name__ == "__main__":
    CONFIG = yaml.load(open("config.yaml").read())
    TwitchChatParser(CONFIG["username"], CONFIG["token"], CONFIG["channels"]).start()
