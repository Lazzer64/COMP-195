import sqlite3
from flask import Flask, g, render_template, request

from . import chart, data

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    channel_id = "spambot"

    if request.method == 'POST':
        enabled = True if request.form["moderation"] == "True" else False
        data.moderation_enabled(channel_id, enabled=enabled)
        data.logs(channel_id, message=f"Moderation {'En' if enabled else 'Dis'}abled")

    return render_template("dashboard.html",
                           moderation={"enabled": data.moderation_enabled(channel_id)},
                           stream={"name": channel_id},
                           logs=data.logs(channel_id))

@app.route("/insights")
def insights():
    channel_id = "spambot"

    emotes = dict(sorted(data.emotes(channel_id).items(), key=lambda e: e[1], reverse=True)[:7])
    viewers = data.viewers(channel_id)

    return render_template("insights.html",
                           emotes=chart.bar(" # of uses", list(emotes.keys()), list(emotes.values())),
                           viewers=chart.line("viewers", list(viewers.keys()), list(viewers.values())))

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
