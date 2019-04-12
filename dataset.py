"""Classes and tools for building datasets."""
from dataclasses import dataclass, InitVar, fields
from difflib import SequenceMatcher
from pathlib import Path


@dataclass
class Datapoint:
    """Class to represent a single datapoint."""
    # pylint: disable=R0902

    subscriber: int = 0
    turbo: int = 0
    similarity: int = 0
    word_count: int = 0
    word_variety: float = 1.0
    emote_count: float = 1.0
    emote_variety: float = 1.0
    ban: int = 0

    message: InitVar = None
    prev_message: InitVar = None

    @classmethod
    def headers(cls):
        """Get a list of coulumn headers for this class."""
        return [field.name for field in fields(cls)]

    def save(self, dataset):
        """Save this datapoint to some file."""
        with dataset.open(mode="a") as f:
            f.write(f"{self}\n")

    def __post_init__(self, message, prev_message):
        if message is not None:
            self.subscriber = int(message.subscriber)
            self.turbo = int(message.turbo)
            self.word_count = self._word_count(message.message)
            self.word_variety = self._word_variety(message.message)
            self.emote_count = self._emote_count(message.emotes)
            self.emote_variety = self._emote_variety(message.emotes)

        if prev_message is not None:
            self.similarity = self._similarity(message.message, prev_message)

        self.ban = int(self.ban)

    @classmethod
    def _emote_count(cls, emotes):
        total = 0
        for count in emotes.values():
            total += count
        return total

    @classmethod
    def _emote_variety(cls, emotes):
        count = cls._emote_count(emotes)

        if count == 0:
            return 1.0

        emotes = len(emotes.keys())
        return emotes / count

    @classmethod
    def _word_count(cls, text):
        return len(text.split())

    @classmethod
    def _word_variety(cls, text):
        words = text.split()
        return len(set(words)) / len(words)

    @classmethod
    def _similarity(cls, first, second):
        if not second:
            return 0.0
        return SequenceMatcher(None, first, second).ratio()

    def __str__(self):
        return ",".join([str(self.__dict__[header]) for header in self.headers()])


def open_dataset(path):
    dataset = Path(path)

    if not dataset.exists():
        dataset.parent.mkdir(parents=True, exist_ok=True)
        dataset.write_text(",".join(Datapoint.headers()) + "\n")

    return dataset
