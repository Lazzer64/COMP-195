"""Tools and objects representing Twitch chat."""

from dataclasses import dataclass

@dataclass
class ChatMessage:
    """Class to represent a single Twitch chat message."""

    channel: str
    message: str
    tags: dict

    @classmethod
    def from_event(cls, event):
        """Create a ChatMessage object from an event."""
        return cls(
            channel=event.target,
            message=event.arguments[0],
            tags={tag["key"]: tag["value"] for tag in event.tags})

    @property
    def username(self):
        """Username of the message owner."""
        return self.tags["display-name"]

    @property
    def user_id(self):
        """Id of the user."""
        return self.tags["user-id"]

    @property
    def badges(self):
        """Badges string of message."""
        return self.tags["badges"] or ""

    @property
    def admin(self):
        """True if this message was sent by an admin."""
        return "admin" in self.badges

    @property
    def bits(self):
        """True if this message contains bits."""
        return "bits" in self.badges

    @property
    def broadcaster(self):
        """True if this message was sent by the broadcaster."""
        return "broadcaster" in self.badges

    @property
    def global_mod(self):
        """True if this message was sent by a global mod."""
        return "global_mod" in self.badges

    @property
    def moderator(self):
        """True if this message was sent by a moderator."""
        return "moderator" in self.badges

    @property
    def subscriber(self):
        """True if this message was sent by a subscriber."""
        return "subscriber" in self.badges

    @property
    def staff(self):
        """True if this message was sent by Twitch staff."""
        return "staff" in self.badges

    @property
    def turbo(self):
        """True if this message was sent by a turbo user."""
        return "turbo" in self.badges

    @property
    def emotes(self):
        """Dict where keys are emote ids and values are occurance counts."""
        if not self.tags["emotes"]:
            return {}

        emotes = {}
        for emote in self.tags["emotes"].split("/"):
            _, indexes = emote.split(":")
            uses = indexes.split(",")
            start, stop = uses[0].split("-")
            emote_name = self.message[int(start):int(stop) + 1]

            count = len(uses)
            emotes[emote_name] = count

        return emotes

    def __str__(self):
        return self.message

@dataclass
class BanEvent:
    """Class representing a single ban event."""

    username: str
    channel: str
    tags: dict

    @classmethod
    def from_event(cls, event):
        """Create a BanEvent object from an event."""
        return cls(
            username=event.arguments[0],
            channel=event.target,
            tags={tag["key"]: tag["value"] for tag in event.tags})


    @property
    def ban_reason(self):
        """The ban reason if one was given."""
        return self.tags["ban-reason"] if "ban-reason" in self.tags else ""


    @property
    def user_id(self):
        """User id of banned user."""
        return self.tags["target-user-id"]

class TimeoutEvent(BanEvent):
    """Class representing a single timeout event."""

    @property
    def duration(self):
        """Duration of timeout."""
        return self.tags["ban-duration"]
