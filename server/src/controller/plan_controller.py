import logging
import uuid

from datetime import datetime, timedelta
from typing import TypedDict

from src.controller.budget_controller import BudgetController
from src.model import db
from src.model.bill_model import BillModel
from src.model.plan_item_model import PlanItemModel
from src.model.plan_model import PlanModel


class primitivePlan(TypedDict):
    id_: uuid.UUID
    plan_id: uuid.UUID
    payment: str
    amount: float
    is_closed: bool


class PlanController:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.budget_id = BudgetController.get_current_budget_id()

    def create(self, old_budget_id: uuid.UUID) -> None:
        self.logger.info("Creating new plan")
        cut_dates = self.get_dates(old_budget_id)
        plan_ids = []
        for start_date, end_date in cut_dates:
            plan_id = uuid.uuid4()
            plan = PlanModel(
                id_=plan_id,
                budget_id=self.budget_id,
                start_date=start_date,
                end_date=end_date,
            )
            db.session.add(plan)
            db.session.commit()
            plan_ids.append(plan_id)
        bulk = self.get_processed_plan_item(plan_ids, len(cut_dates))
        self.save_bulk(bulk)

    def get_start_date(self, old_budget_id: uuid.UUID) -> datetime:
        self.logger.info("Getting start date")
        plan_filtered = db.session.query(PlanModel.end_date).filter_by(budget_id=old_budget_id)
        previous_plan = plan_filtered.order_by(PlanModel.end_date.desc()).first()
        if not previous_plan:
            raise Exception("No previous plan")
        return previous_plan.end_date

    def get_dates(self, old_budget_id: uuid.UUID) -> list[tuple[datetime, datetime]]:
        self.logger.info("Getting biweekly range dates")
        start_date = self.get_start_date(old_budget_id)
        end_date1 = start_date + timedelta(days=14)
        end_date2 = end_date1 + timedelta(days=14)
        dates = [
            (start_date, end_date1),
            (end_date1, end_date2),
        ]

        extra_date = end_date2 + timedelta(days=14)

        if extra_date.month == end_date2.month:
            dates.append((end_date2, extra_date))
        return dates

    def get_bills_in_budget(self, number_of_biweeks: int) -> dict[str, float]:
        self.logger.info("Getting bills for month plan")
        total_per_payment: dict[str, float] = {}
        bills = BillModel.query.filter_by(budget_id=self.budget_id).all()
        for bill in bills:
            if bill.payment in total_per_payment:
                total_per_payment[bill.payment] += bill.amount
            else:
                total_per_payment[bill.payment] = bill.amount
        for total in total_per_payment:
            total_per_payment[total] = total_per_payment[total] / number_of_biweeks
        return total_per_payment

    def get_processed_plan_item(
        self, plan_ids: list[uuid.UUID], number_of_biweeks: int
    ) -> list[PlanItemModel]:
        self.logger.info("Getting processed payment plan")
        plan_item_list: list[PlanItemModel] = []
        item = self.get_bills_in_budget(number_of_biweeks)
        for plan_id in plan_ids:
            for payment, amount in item.items():
                payment_plan = PlanItemModel(
                    id_=uuid.uuid4(),
                    budget_id=self.budget_id,
                    plan_id=plan_id,
                    amount=amount,
                    payment=payment,
                )
                plan_item_list.append(payment_plan)
        return plan_item_list

    def save_bulk(self, bulk: list[PlanItemModel]) -> None:
        self.logger.info("Saving bulk plan items data to database")
        db.session.bulk_save_objects(bulk)
        db.session.commit()

    @staticmethod
    def update__plan_item_amount(amount: float, payment_plan_id: uuid.UUID) -> None:
        payment_plan = PlanItemModel.query.filter_by(id_=payment_plan_id).first()
        payment_plan.amount = amount
        db.session.commit()

    @staticmethod
    def mark_plan_item_closed(payment_plan_id: uuid.UUID) -> None:
        payment_plan = PlanItemModel.query.filter_by(id_=payment_plan_id).first()
        payment_plan.is_closed = True
        db.session.commit()

    @staticmethod
    def get_plan_items() -> list[primitivePlan]:
        payment_plan_list: list[primitivePlan] = []
        budget_id = BudgetController.get_current_budget_id()
        payment_plans = PlanItemModel.query.filter_by(budget_id=budget_id).all()
        for payment_plan in payment_plans:
            payment_plan_list.append(
                {
                    "id_": payment_plan.id_,
                    "payment": payment_plan.payment,
                    "plan_id": payment_plan.plan_id,
                    "amount": payment_plan.amount,
                    "is_closed": payment_plan.is_closed,
                }
            )
        return payment_plan_list
