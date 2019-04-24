"""Tools to parse Twitch chat."""
from collections import defaultdict
from storage import create_storage, store_data

import yaml

from tmi import TwitchIrcBot
from dataset import Datapoint, open_dataset

DATASET = open_dataset("datasets/dataset.csv")
PREVIOUS_MESSAGE = defaultdict(str)
LAST_MESSAGE = {}

class TwitchChatParser(TwitchIrcBot):
    """Twitch Chat parser that reads data from IRC."""

    def on_message(self, message):
        if message.user_id in LAST_MESSAGE:
            last_message = LAST_MESSAGE[message.user_id]
            PREVIOUS_MESSAGE[message.user_id] = last_message

        LAST_MESSAGE[message.user_id] = message
        Datapoint(message=message, prev_message=str(PREVIOUS_MESSAGE[message.user_id]),
                  ban=False).save(DATASET)

    def on_timeout(self, timeout):
        if timeout.user_id in LAST_MESSAGE:
            message = LAST_MESSAGE[timeout.user_id]

            Datapoint(message=message, prev_message=str(PREVIOUS_MESSAGE[message.user_id]),
                      ban=True).save(DATASET)

    def on_ban(self, ban):
        if ban.user_id in LAST_MESSAGE:
            message = LAST_MESSAGE[ban.user_id]

            Datapoint(message=message, prev_message=str(PREVIOUS_MESSAGE[message.user_id]),
                      ban=True).save(DATASET)


if __name__ == "__main__":
    create_storage()

    # store_data("streams", [(1, '5pm', '6pm', 0), (2, '5am', '6am', 0)])

    CONFIG = yaml.load(open("config.yaml").read())
    TwitchChatParser(CONFIG["username"], CONFIG["token"], CONFIG["channels"]).start()

