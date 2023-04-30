import datetime as dt
import os
import time

from flask import Flask, render_template

from tools import calc

app = Flask(__name__)
if os.name == "posix":
    os.environ["TZ"] = "US/Central"
    time.tzset()


@app.route("/")
def index():
    return render_template(
        "index.html",
    )


@app.route("/summer/")
def summer():
    now = dt.datetime.now()
    return render_template(
        "summer.html",
        days_left=calc.schooldays_until_summer(now),
        hours_left=calc.contract_workhours_remaining(now),
        workday_completed=calc.workday_completed(now),
    )
