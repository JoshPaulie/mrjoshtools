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
    now = now.replace(month=5, day=1, hour=10, minute=0)
    return render_template(
        "summer.html",
        # My coworkers don't include the current day when counting down
        # I like to look at it as:
        #   - We have X number of days after today until summer break
        #   - This means that on the last day of the year, they would say "0 days left"
        # This is very hard for me to wrap my head around, for whatever reason
        days_left=calc.contract_workdays_remaining(now) - 1,
        hours_left=calc.contract_workhours_remaining(now),
        workday_completed=calc.workday_completed(now),
    )
