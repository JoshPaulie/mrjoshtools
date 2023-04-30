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
    return render_template(
        "summer.html",
        days_left=calc.workdays_until_summer(),
        hours_left=calc.workhours_remaining(),
        workday_completed=calc.workday_completed(),
    )
