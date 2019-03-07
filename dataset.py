from difflib import SequenceMatcher

dataset = open("dataset.csv", "w+")
dataset.write(",".join(["subscriber",
                        "turbo",
                        "word count",
                        "word variety",
                        "message similarity",
                        "emote count",
                        "emote variety",
                        "ban"]) + "\n")


def datapoint(message, prev_message, ban):
    data = [int(message.subscriber),
            int(message.turbo),
            word_count(message.message),
            word_variety(message.message),
            similarity(message.message, prev_message),
            emote_count(message.emotes),
            emote_variety(message.emotes),
            int(ban)]
    line = ",".join([str(item) for item in data])
    dataset.write(f"{line}\n")

def emote_count(emotes):
    total = 0
    for count in emotes.values():
        total += count
    return total

def emote_variety(emotes):
    count = emote_count(emotes)

    if count is 0:
        return 1.0

    emotes = len(emotes.keys())
    return emotes / count

def word_count(text):
    return len(text.split())

def word_variety(text):
    words = text.split()
    return len(set(words)) / len(words)

def similarity(first, second):
    if not second:
        return 0.0
    return SequenceMatcher(None, first, second).ratio()
