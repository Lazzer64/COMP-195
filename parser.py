"""Tools to parse Twitch chat."""

import yaml
from tmi import TwitchIrcBot

LAST_MESSAGE = {}

class TwitchChatParser(TwitchIrcBot):
    """Twitch Chat parser that reads data from IRC."""

    def on_message(self, message):
        LAST_MESSAGE[message.user_id] = message

    def on_timeout(self, timeout):
        if timeout.user_id in LAST_MESSAGE:
            message = LAST_MESSAGE[timeout.user_id]
            print(f"{timeout.username} TIMED OUT for {timeout.duration} "
                  f"from {timeout.channel} last message: '{message.message}'")

    def on_ban(self, ban):
        if ban.user_id in LAST_MESSAGE:
            message = LAST_MESSAGE[ban.user_id]
            print(f"{ban.username} BANNED from {ban.channel} last message: '{message.message}'")

if __name__ == "__main__":
    CONFIG = yaml.load(open("config.yaml").read())
    TwitchChatParser(CONFIG["username"], CONFIG["token"], CONFIG["channels"]).start()
