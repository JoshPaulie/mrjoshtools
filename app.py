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
        # fyi - boomers get mad if you include the last day, so -1
        days_left=calc.calc_workdays_left_in_contract() - 1,
        hours_left=calc.calc_hours_left_in_contract(),
        workday_completed=calc.workday_completed(),
    )
