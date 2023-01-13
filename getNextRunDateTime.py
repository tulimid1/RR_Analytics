from datetime import datetime, timedelta


def getNextRunDateTime(interval_seconds):
    current_date_time = datetime.now()
    next_run_date_time = current_date_time + timedelta(0, interval_seconds)
    print(
        f"The next run attempt will occur on {next_run_date_time.month:d}/{next_run_date_time.day:d}/{next_run_date_time.year:d} at {next_run_date_time.hour:d}:{next_run_date_time.minute}:{next_run_date_time.second}\n"
    )
