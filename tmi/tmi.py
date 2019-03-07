"""Tools to interface with the Twitch Messaging Interface."""

import irc.bot

from .chat import ChatMessage, BanEvent, TimeoutEvent

class TwitchIrcBot(irc.bot.SingleServerIRCBot):
    """Class to interact with Twitch Messaging Interface."""
    # pylint: disable=unused-argument,no-self-use,missing-docstring

    HOST = "irc.chat.twitch.tv"
    PORT = 6667

    def __init__(self, username, token, channels):
        """
        Initialize a TwitchIrcBot instance.

        :param username: Username of the bot account
        :param token: OAuth token
        :param channels: List of channels to join
        """
        super().__init__([(self.HOST, self.PORT, token)], username, username)
        self.twitch_channels = [chnl if chnl[0] == "#" else f"#{chnl}" for chnl in channels]

    def _register_twitch_caps(self):
        self.connection.cap("REQ", "twitch.tv/membership")
        self.connection.cap("REQ", "twitch.tv/tags")
        self.connection.cap("REQ", "twitch.tv/commands")

    def on_welcome(self, conn, event):
        self._register_twitch_caps()

        for channel in self.twitch_channels:
            conn.join(channel)

    def on_join(self, conn, event):
        print(f"joined channel {event.target}")

    def on_pubmsg(self, conn, event):
        self.on_message(ChatMessage.from_event(event))

    def on_clearchat(self, conn, event):
        if "ban-duration" in event.tags:
            self.on_timeout(TimeoutEvent.from_event(event))
        else:
            self.on_ban(BanEvent.from_event(event))

    def on_error(self, conn, event):
        print(event)

    def on_message(self, message):
        pass

    def on_timeout(self, timeout):
        pass

    def on_ban(self, ban):
        pass
