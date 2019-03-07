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
    def emotes(self):
        """Dict where keys are emote ids and values are occurance counts."""
        if not self.tags["emotes"]:
            return []

        emotes = {}
        for emote in self.tags["emotes"].split("/"):
            emote_id, indexes = emote.split(":")
            count = len(indexes.split(","))
            emotes[emote_id] = count

        return emotes

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
    def user_id(self):
        """User id of banned user."""
        return self.tags["target-user-id"]

class TimeoutEvent(BanEvent):
    """Class representing a single timeout event."""

    @property
    def duration(self):
        """Duration of timeout."""
        return self.tags["ban-duration"]
