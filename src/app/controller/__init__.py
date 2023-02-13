from datetime import datetime, timedelta


def get_biweekly_dates(start_date: datetime) -> list[datetime]:
    first_date = start_date + timedelta(days=14)
    last_date = first_date + timedelta(days=14)
    extra_date = last_date + timedelta(days=14)

    dates = [first_date, last_date]
    print(extra_date.month, last_date.month)
    if extra_date.month == last_date.month:
        dates.append(extra_date)
    return dates
