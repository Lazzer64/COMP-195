import sqlite3
from collections import defaultdict
from datetime import timedelta, datetime

import yaml

from .tmi import TwitchIrcBot
from .database_storage import db_path

LAST_MESSAGE = {}

class TwitchChatModerator(TwitchIrcBot):
    """Twitch Chat parser that reads data from IRC."""

    db = sqlite3.connect(db_path)
    channel_id = "spambot"

    def __init__(self, classifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classifier = classifier
        self.seen_users = set()
        self.last_seen = datetime.now()
        self.subscribers = set()
        self.non_subscribers = set()

    def moderation_enabled(self):
        row = self.db.execute("SELECT enabled FROM moderation WHERE channel_id = ?", (self.channel_id,)).fetchone()
        if row:
            return bool(row[0])
        return False

    def observe_user(self, message):
        self.seen_users.add(message.user_id)

        if message.subscriber:
            self.subscribers.add(message.user_id)
        else:
            self.non_subscribers.add(message.user_id)

        now = datetime.now()
        self.db.execute("INSERT OR REPLACE INTO subscribers (channel_id, subscribers, nonsubscribers) VALUES (?, ?, ?)",
                        (self.channel_id, len(self.subscribers), len(self.non_subscribers)))
        self.db.commit()

        if now - self.last_seen > timedelta(minutes=10):
            self.last_seen = now
            query = self.db.execute("INSERT INTO chatters (channel_id, timestamp, chatters) VALUES (?, ?, ?)",
                                    (self.channel_id, datetime.now(), len(self.seen_users)))
            self.seen_users = set()
            self.db.commit()

    def on_message(self, message):
        if message.user_id in LAST_MESSAGE:
            last_message = LAST_MESSAGE[message.user_id]

        self.observe_user(message)

        if message.emotes:
            query = self.db.execute("SELECT emote, count FROM emotes WHERE channel_id = ? AND emote IN (?)",
                                    (self.channel_id, ", ".join(message.emotes.keys())))

            emote_counts = message.emotes.copy()
            for emote, count in query.fetchall():
                emote_counts[emote] += count

            self.db.executemany("INSERT OR REPLACE INTO emotes (channel_id, emote, count) VALUES (?, ?, ?)",
                                 [(self.channel_id, emote, count) for emote, count in emote_counts.items()])
            self.db.commit()

        LAST_MESSAGE[message.user_id] = message

        if not self.moderation_enabled():
            return

        if self.classifier.predict([message.message])[0]:
            print("[PREDICTED BAN]", message)

            self.db.execute("INSERT INTO log_message (channel_id, timestamp, message) VALUES (?, ?, ?)",
                            (self.channel_id, str(datetime.now()), f"{message.username} banned."))
            self.db.commit()

    def on_ban(self, ban):
        if ban.user_id in LAST_MESSAGE:
            message = LAST_MESSAGE[ban.user_id]
            print("[ACTUAL BAN]", message)
        else:
            print("[ACTUAL BAN BUT NO MESSAGE FOUND]")

    def on_timeout(self, timeout):
        self.on_ban(timeout)

if __name__ == "__main__":
    from .learn import Classifier

    classifier = Classifier.load('./models/my_classifier.pkl')

    CONFIG = yaml.load(open("config.yaml").read())
    TwitchChatModerator(classifier, CONFIG["username"], CONFIG["token"], CONFIG["channels"]).start()
