# Twitch Statistic Parsing And Moderation Bot

### Installation
```bash
pip install -r requirements.txt
```
**Note**: if you are using `python3` to use `pip3` as well.

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
```bash
python spam.py
```
For usage information use
```bash
python spam.py --help
```
