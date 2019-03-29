import chart

from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",
                           moderation={"enabled": True},
                           stream={"name": "foobar"},
                           logs=[("2019-03-24 16:36:59.568000", "foo timed out for 10 seconds"),
                                 ("2019-03-22 18:36:59.568000", "foo timed out for 30 seconds"),
                                 ("2019-03-21 19:36:59.568000", "foo banned")])

@app.route("/insights")
def insights():
    emotes = {"Kappa": 10,
              "FrankerZ": 20,
              "Pogchamp": 5,
              "BibleThump": 7}

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
