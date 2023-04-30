import datetime as dt

# Now && today
now = dt.datetime.now()
today = now.date().today()

# Static contract info
last_day = dt.date(2023, 5, 23)
shift_start_time = dt.time(9, 0, 0)
shift_end_time = dt.time(16, 0, 0)
shift_len = shift_end_time.hour - shift_start_time.hour


# Functions 🧠
def hours_worked_today():
    # fyi - keeps tool from breaking if checked before work hours
    if now.time() < shift_start_time:
        return 0

    shift_start = dt.datetime.combine(today, shift_start_time)
    hours_since_shift_start = (now - shift_start).seconds / 60 / 60

    # fyi - bc the tool might be used *after* work hours, this value caps at 7
    hours_worked_today = round(hours_since_shift_start) if hours_since_shift_start < shift_len else shift_len

    return hours_worked_today


def is_weekend(date: dt.date) -> bool:
    return date.weekday() in [5, 6]


def calc_workdays_left_in_contract() -> int:
    """Calculate workdays left in contract, today & last day inclusive"""
    days_left = calc_days()
    days = [today + dt.timedelta(n) for n in range(days_left)]
    days = [day for day in days if not is_weekend(day)]  # No weekends!
    workdays_remaining = len(days)
    if now.time() > shift_start_time:
        workdays_remaining -= 1
    return workdays_remaining


def calc_hours_left_in_contract() -> int:
    """Calculate "workhours" left in contract, today & last day inclusive"""
    # if used, say on a Sunday afternoon, then again the following monday,
    # the user would be surprised to see 7 hours added on. this covers that
    if is_weekend(now.date()):
        return calc_workdays_left_in_contract() * shift_len
    return (calc_workdays_left_in_contract() * shift_len) - hours_worked_today


def workday_completed() -> float:
    now = dt.datetime.now()
    start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
    shift_duration = end_time - start_time

    time_left = end_time - now
    shift_completed = shift_duration - time_left
    shift_completed_percent = (shift_completed / shift_duration) * 100
    # Because the tool can be used before & after work hours, the returned value must be clamped between 1 - 100
    return sorted([0, shift_completed_percent, 100])[1]


if __name__ == "__main__":
    hr_left = calc_hours_left_in_contract()
    print(f"Hours left in '22-'23 contract: {hr_left}")
    print(workday_completed())
