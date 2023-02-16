from datetime import datetime, timedelta


def get_biweekly_dates(start_date: datetime) -> list[datetime]:
    first_date = start_date + timedelta(days=14)
    last_date = first_date + timedelta(days=14)
    extra_date = last_date + timedelta(days=14)

    dates = [first_date, last_date]
    if extra_date.month == last_date.month:
        dates.append(extra_date)
    return dates


def get_number_of_weeks(start_date: datetime) -> int:
    weeks_list = get_biweekly_dates(start_date)
    return len(weeks_list)
