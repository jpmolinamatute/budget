import uuid
from datetime import datetime

from sqlalchemy import desc

from src.app.controller import get_biweekly_dates
from src.app.model import db
from src.app.model.salary_model import SalaryModel


class SalaryControler:
    @staticmethod
    def get_dates() -> list[datetime]:
        salary = db.session.query(SalaryModel.date).order_by(desc(SalaryModel.date)).first()
        if not salary:
            raise Exception("No salary found")
        return get_biweekly_dates(salary[0])

    @staticmethod
    def save_bulk(salaries: list[SalaryModel]) -> None:
        db.session.bulk_save_objects(salaries)
        db.session.commit()

    def process_salaries(self, budget_id: uuid.UUID) -> list[SalaryModel]:
        salaries = []
        for a_date in self.get_dates():
            salaries.append(
                SalaryModel(
                    id_=uuid.uuid4(),
                    date=a_date,
                    amount=2920.92,
                    budget_id=budget_id,
                )
            )
        return salaries

    @staticmethod
    def update_salary(salary_id: uuid.UUID, amount_type: tuple[str, float]) -> None:
        salary = SalaryModel.query.get(salary_id)
        if amount_type[0] == "amount":
            salary.amount = amount_type[1]
        elif amount_type[0] == "extra":
            salary.extra = amount_type[1]
        else:
            raise Exception("Invalid amount type")
        db.session.commit()


# Path: src/app/controller/salary_controler.p
