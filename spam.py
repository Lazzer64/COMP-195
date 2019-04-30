#!/usr/bin/env python
import argparse

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-web', help='Do not start web application.', action='store_true')
    parser.add_argument('--no-learn', help='Do not start data gathering.', action='store_true')
    parser.add_argument('--no-moderation', help='Do not start channel moderation.', action='store_true')
    return parser.parse_args()

def webserver():
    from spam.web.server import app

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()

def learn():
    import yaml

    from spam.chat_parser import TwitchChatParser

    CONFIG = yaml.load(open("config.yaml").read())
    TwitchChatParser(CONFIG["username"], CONFIG["token"], CONFIG["channels"]).start()

def moderator():
    import yaml

    from spam.chat_moderator import TwitchChatModerator
    from spam.learn import Classifier

    classifier = Classifier.load("models/my_classifier.pkl")
    print("Ban accuracy:", classifier.ban_accuracy)

    CONFIG = yaml.load(open("config.yaml").read())
    TwitchChatModerator(classifier, CONFIG["username"], CONFIG["token"], CONFIG["channels"]).start()

if __name__ == "__main__":
    args = args()

    from multiprocessing import Process

    if not args.no_moderation:
        Process(target=moderator).start()

    if not args.no_learn:
        Process(target=learn).start()

    if not args.no_web:
        Process(target=webserver).start()
