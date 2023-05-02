import datetime as dt

# Static contract info
last_day = dt.date(2023, 5, 23)
shift_start_time = dt.time(9, 0, 0)
shift_end_time = dt.time(16, 0, 0)
shift_len = shift_end_time.hour - shift_start_time.hour


# Functions 🧠
def is_weekend(date: dt.date) -> bool:
    return date.weekday() in [5, 6]


def hours_worked_today(now: dt.datetime) -> int:
    # if checked before the workday has started, then no hours and have been worked
    # same logic for checking over the weekend
    if now.time() < shift_start_time or is_weekend(now.date()):
        return 0

    shift_start_dt = dt.datetime.combine(now.date(), shift_start_time)
    hours_since_shift_start = (now - shift_start_dt).seconds / 60 / 60

    # bc the tool might be used *after* work hours, this value caps at 7
    hours_worked_today = round(hours_since_shift_start) if hours_since_shift_start < shift_len else shift_len
    return hours_worked_today


def contract_workdays_remaining(now: dt.datetime) -> int:
    """Calculate workdays left in contract. Today & last workday inclusive"""
    days_left = (last_day - now.date()).days + 1
    days = [now.date() + dt.timedelta(n) for n in range(days_left)]
    days = [day for day in days if not is_weekend(day)]  # No weekends!
    workdays_remaining = len(days)
    return workdays_remaining


def contract_workhours_remaining(now: dt.datetime) -> int:
    """Workhours remaining in contract. Today & last day inclusive"""
    return (contract_workdays_remaining(now.now()) * shift_len) - hours_worked_today(now.now())


def workday_completed(now: dt.datetime) -> float:
    """Calculates the percentage of a workday that has been completed.
    If the current date is a weekend, or if called before workhours, the function returns 0.

    Note:
    - This code was copied in from another script, too lazy to refactor it right now
    - hours_worked_today() always returns an int, but a float is more appropriate for here
    """
    now = now.now()
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
    now = dt.datetime.now()
    print(f"{contract_workdays_remaining(now)=}")
    print(f"{hours_worked_today(now)=}")
    print(f"{contract_workhours_remaining(now)=}")
    print(f"{workday_completed(now)=}")
