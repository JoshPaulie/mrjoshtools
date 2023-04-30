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


def days_until_summerbreak() -> int:
    """Find days between today -> last day in the contract. Today & weekends inclusive"""
    return (last_day - today).days + 1


def workdays_remaining() -> int:
    """Calculate workdays left in contract. Today & last workday inclusive"""
    days_left = days_until_summerbreak()
    days = [today + dt.timedelta(n) for n in range(days_left)]
    days = [day for day in days if not is_weekend(day)]  # No weekends!
    workdays_remaining = len(days)
    return workdays_remaining


def workdays_until_summer() -> int:
    """Similar to workdays_remaining() but with logic that would make more sense to my coworkers"""
    workdays_until_summer = workdays_remaining()
    workdays_until_summer -= 1  # 'Take off' the last day
    # If the work day is over, and it's not a weekend, take 1 off
    # Gives cute effect of a day going down after 4
    if now.time() > shift_end_time and not is_weekend(now.date()):
        return workdays_until_summer - 1
    return workdays_until_summer


def workhours_remaining() -> int:
    """Workhours remaining in contract. Today & last day inclusive"""
    # if used, say on a Sunday afternoon, then again the following monday,
    # the user would be surprised to see 7 hours added on. this covers that
    if is_weekend(now.date()):
        return workdays_remaining() * shift_len
    return (workdays_remaining() * shift_len) - hours_worked_today()


def workday_completed() -> float:
    """Calculates the percentage of a workday that has been completed.
    If the current date is a weekend, or if called before workhours, the function returns 0."""
    # We need to make another for this scope, as to not change the global
    now = dt.datetime.now()

    if is_weekend(now.date()):
        return 0

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
