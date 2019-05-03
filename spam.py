#!/usr/bin/env python
import argparse
import os
from time import sleep

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-web', help='Do not start web application.', action='store_true')
    parser.add_argument('--no-learn', help='Do not start data gathering.', action='store_true')
    parser.add_argument('--no-moderation', help='Do not start channel moderation.', action='store_true')
    parser.add_argument('--create-db', help='Create new database (deletes any existing databse)', action='store_true')
    parser.add_argument('--config', help='Specify config file (default config.yaml)', default='config.yaml', type=argparse.FileType('r'))
    return parser.parse_args()

def webserver():
    from spam.web.server import app

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()

def learn(config):
    import yaml

    from spam.chat_parser import TwitchChatParser

    TwitchChatParser(config["username"], config["token"], config["channels"]).start()

def moderator(config):
    import yaml

    from spam.chat_moderator import TwitchChatModerator
    from spam.learn import Classifier

    while not os.path.isfile("models/my_classifier.pkl"):
        sleep(1)

    classifier = Classifier.load("models/my_classifier.pkl")
    print("Ban accuracy:", classifier.ban_accuracy)

    TwitchChatModerator(classifier, config["username"], config["token"], config["channels"]).start()

def create_db():
    from spam.database_storage import create_db
    create_db()

if __name__ == "__main__":
    args = args()

    import yaml
    from multiprocessing import Process

    config = yaml.load(args.config.read())

    if args.create_db:
        create_db()

    if not args.no_moderation:
        Process(target=moderator, args=(config,)).start()

    if not args.no_learn:
        Process(target=learn, args=(config,)).start()

    if not args.no_web:
        Process(target=webserver).start()
