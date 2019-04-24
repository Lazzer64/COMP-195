"""Tools to parse Twitch chat."""
from collections import defaultdict

import yaml

from tmi import TwitchIrcBot
from dataset import Datapoint, open_dataset
from learn import Classifier

MESSAGE_TRAIN_COUNT = 1000

class TwitchChatParser(TwitchIrcBot):
    """Twitch Chat parser that reads data from IRC."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dataset = open_dataset("datasets/dataset.csv")
        self.classifier = "models/my_classifier.pkl"

        self.messages_to_train = 0
        self.previous_message = defaultdict(str)
        self.last_message = {}

    def train_classifier(self):
        clf = Classifier()
        clf.train(self.dataset)
        clf.save(self.classifier)
        print("Trained with score:", clf.score)

    def on_message(self, message):
        if message.user_id in self.last_message:
            last_message = self.last_message[message.user_id]
            self.previous_message[message.user_id] = last_message

        self.last_message[message.user_id] = message
        Datapoint(message=message, prev_message=str(self.previous_message[message.user_id]),
                  ban=False).save(self.dataset)

        self.messages_to_train += 1

        if self.messages_to_train > MESSAGE_TRAIN_COUNT:
            self.train_classifier()
            self.messages_to_train = 0

    def on_timeout(self, timeout):
        if timeout.user_id in self.last_message:
            message = self.last_message[timeout.user_id]

            Datapoint(message=message, prev_message=str(self.previous_message[message.user_id]),
                      ban=True).save(self.dataset)

    def on_ban(self, ban):
        if ban.user_id in self.last_message:
            message = self.last_message[ban.user_id]

            Datapoint(message=message, prev_message=str(self.previous_message[message.user_id]),
                      ban=True).save(self.dataset)

if __name__ == "__main__":
    CONFIG = yaml.load(open("config.yaml").read())
    TwitchChatParser(CONFIG["username"], CONFIG["token"], CONFIG["channels"]).start()
