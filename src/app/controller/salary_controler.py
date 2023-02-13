import calendar
from datetime import datetime, timedelta

from sqlalchemy import desc

from src.app.model import db
from src.app.model.salary_model import SalaryModel


class SalaryControler:
    @staticmethod
    def get_dates() -> list[datetime]:
        salary = db.session.query(SalaryModel).order_by(desc(SalaryModel.date)).first()
        if not salary:
            raise Exception("No salary found")
        first_date = salary.date + timedelta(days=14)
        last_date = first_date + timedelta(days=14)
        last_day_of_month = calendar.monthrange(last_date.year, last_date.month)[1]
        dates = [first_date, last_date]
        if last_date.day <= last_day_of_month:
            dates.append(last_date + timedelta(days=14))
        return dates

    @staticmethod
    def save_bulk(salaries: list[SalaryModel]) -> None:
        db.session.bulk_save_objects(salaries)
        db.session.commit()
