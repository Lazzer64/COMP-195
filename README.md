# Twitch Statistic Parsing And Moderation Bot

## Table of Contents
* [Installation](#Installation)
* [Configuration](#Configuration)
* [Running the application](#Running-the-application)
* [Implementation Files](#Implementation-Files)

### Installation
```bash
pip install -r requirements.txt
```
**Note**: if you are using `python3` remember to use `pip3` as well.

### Configuration
* A [Twitch.tv](https://www.twitch.tv/signup) account is required to run this application.
* The application can be configured with `config.yaml`.
* OAuth token can be generated from [twitchapps](https://twitchapps.com/tmi).

Example:
```yaml
---
username: MyUsername
token: oauth:abc123
channels:
  - loltyler1
  - sodapoppin
  - nl_kripp
```

### Running the application
If this is the first time running the application or you wish to remake the database use the `--create-db` option
```bash
python spam.py --create-db
```
For additional usage information use
```bash
python spam.py --help
```

### Implementation Files 
1. [spam.learn](spam/learn.py) - Machine Learning training and classification
1. [spam.dataset](spam/dataset.py) - Dataset and datapoint building
1. [spam.tmi.chat](spam/tmi/chat.py) - Twitch IRC object parsing
