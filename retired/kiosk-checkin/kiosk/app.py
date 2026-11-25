import configparser

import requests
from flask import Flask, render_template, request

from .printer import print_ticket

cfg = configparser.ConfigParser()
cfg.read("kiosk/config.ini")
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        ref = request.form["ref"].strip().upper()
        r = requests.post(cfg["kiosk"]["api_base"] + "/checkin", json={"ref": ref}, timeout=5)
        if r.ok:
            print_ticket(r.json()["queue"])
            return render_template("done.html", queue=r.json()["queue"])
        return render_template("error.html"), 400
    return render_template("index.html")
