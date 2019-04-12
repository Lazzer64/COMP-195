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
    channel_id = 0

    if request.method == 'POST':
        enabled = True if request.form["moderation"] == "True" else False
        data.moderation_enabled(channel_id, enabled)

    return render_template("dashboard.html",
                           moderation={"enabled": data.moderation_enabled(channel_id)},
                           stream={"name": "foobar"},
                           logs=data.logs(channel_id))

@app.route("/insights")
def insights():
    emotes = data.emotes(0)

    viewers = {"Sunday (1/1)": 1237,
               "Monday (1/2)": 5238,
               "Tuesday (1/2)": 2927,
               "Wednesday (1/3)": 8389,
               "Thursday (1/4)": 1783,
               "Friday (1/5)": 8427,
               "Saturday (1/6)": 4483}

    return render_template("insights.html",
                           emotes=chart.bar(" # of uses", list(emotes.keys()), list(emotes.values())),
                           viewers=chart.line("viewers", list(viewers.keys()), list(viewers.values())))

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
