import logging
import uuid

from datetime import datetime, timedelta
from typing import TypedDict

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from src.controller.budget_controller import BudgetController
from src.model.bill_model import BillModel
from src.model.plan_item_model import PlanItemModel
from src.model.plan_model import PlanModel


class primitivePlanItem(TypedDict):
    id_: uuid.UUID
    amount: float
    payment: str
    is_locked: bool


class primitivePlan(TypedDict):
    id_: uuid.UUID
    start_date: datetime
    end_date: datetime
    budget_id: uuid.UUID
    plan_items: list[primitivePlanItem]


class PlanController:
    def __init__(self, logger: logging.Logger, session: Session, budget: BudgetController) -> None:
        self.logger = logger
        self.session = session
        self.budget = budget

    def create(self, old_budget_id: uuid.UUID) -> None:
        self.logger.info("Creating new plan")
        cut_dates = self.get_dates(old_budget_id)
        plan_ids = []

        for start_date, end_date in cut_dates:
            plan_id = uuid.uuid4()
            plan = PlanModel(
                id_=plan_id,
                budget_id=self.budget.budget_id,
                start_date=start_date,
                end_date=end_date,
            )
            self.session.add(plan)
            self.session.commit()
            plan_ids.append(plan_id)
        bulk = self.get_processed_plan_item(plan_ids, len(cut_dates))
        self.save_bulk(bulk)

    def get_start_date(self, old_budget_id: uuid.UUID) -> datetime:
        self.logger.info("Getting start date")
        plan_filtered = self.session.query(PlanModel.end_date).filter_by(budget_id=old_budget_id)
        previous_plan = plan_filtered.order_by(PlanModel.end_date.desc()).first()
        if previous_plan is None:
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
        bills = self.session.query(BillModel).filter_by(budget_id=self.budget.budget_id).all()
        for bill in bills:
            if bill.payment in total_per_payment:
                total_per_payment[bill.payment_type] += bill.amount
            else:
                total_per_payment[bill.payment_type] = bill.amount
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
            for payment_type, amount in item.items():
                payment_plan = PlanItemModel(
                    id_=uuid.uuid4(),
                    plan_id=plan_id,
                    amount=amount,
                    payment_type=payment_type,
                )
                plan_item_list.append(payment_plan)
        return plan_item_list

    def save_bulk(self, bulk: list[PlanItemModel]) -> None:
        self.logger.info("Saving bulk plan items data to database")
        self.session.bulk_save_objects(bulk)
        self.session.commit()

    def update_plan_item_amount(self, plan_item_id: uuid.UUID, amount: float) -> None:
        plan_item = self.session.query(PlanItemModel).filter_by(id_=plan_item_id).first()
        if plan_item is None:
            raise Exception("Plan item not found")
        plan_item.amount = amount
        self.session.commit()

    def mark_plan_closed(self, plan_id: uuid.UUID) -> None:
        plan = self.session.query(PlanModel).filter_by(id_=plan_id).first()
        if plan is None:
            raise Exception("Plan not found")
        plan.is_locked = True
        self.session.commit()

    def mark_plan_opened(self, plan_id: uuid.UUID) -> None:
        plan = self.session.query(PlanModel).filter_by(id_=plan_id).first()
        if plan is None:
            raise Exception("Plan not found")
        plan.is_locked = False
        self.session.commit()

    def get_plan(self) -> list[primitivePlan]:
        plan_list: list[primitivePlan] = []
        plans = (
            self.session.query(PlanModel)
            .filter_by(budget_id=self.budget.budget_id)
            .order_by(PlanModel.start_date)
            .all()
        )
        if plans is None:
            raise Exception("Plan not found")
        stm = select(PlanItemModel).where(PlanItemModel.plan_id.in_([plan.id_ for plan in plans]))
        result = self.session.execute(stm)
        items = result.fetchall()
        for plan in plans:
            single_plan: primitivePlan = {
                "id_": plan.id_,
                "start_date": plan.start_date,
                "end_date": plan.end_date,
                "budget_id": plan.budget_id,
                "plan_items": [],
            }
            for item in items:
                if item[0].plan_id == plan.id_:
                    single_plan["plan_items"].append(
                        {
                            "id_": item[0].id_,
                            "payment": item[0].payment,
                            "amount": item[0].amount,
                            "is_locked": item[0].is_locked,
                        }
                    )
            plan_list.append(single_plan)
        return plan_list

    def is_plan_item_locked(self, plan_id: uuid.UUID) -> bool:
        plan = self.session.query(PlanModel).filter_by(id_=plan_id).first()
        if plan is None:
            raise Exception("Plan not found")
        return plan.is_locked
