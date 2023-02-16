#!/usr/bin/env python
import logging
import sys
import uuid
from os import path

from dotenv import load_dotenv

from src import create_app
from src.controller.bill_controler import BillControler
from src.controller.budget_controler import BudgetController
from src.controller.salary_controler import SalaryControler
from src.controller.payment_plan_controler import PaymentPlanControler, Plan


def run() -> None:
    load_dotenv()
    app = create_app()
    # app.run(debug=True)
    with app.app_context():
        budget_controler = BudgetController()
        bill_controler = BillControler()
        salary_controler = SalaryControler()
        payment_plan_controler = PaymentPlanControler()
        budget_controler.close_budget(uuid.UUID("4849cb99-b084-4024-b613-8f3e0cd1079c"))
        budget_id = budget_controler.get_current_budget()

        if not budget_id:
            budget_id = budget_controler.create_budget(3, 2023)

        bills = bill_controler.process_bills(budget_id, 3, 2023)
        bill_controler.save_bulk(bills)

        salaries = salary_controler.process_salaries(budget_id)
        salary_controler.save_bulk(salaries)
        month_plan = bill_controler.get_total_per_payment(budget_id)
        number_of_biweeks = len(salaries)
        biweek_list = []
        item = bill_controler.get_total_per_provider_biweekly(month_plan, number_of_biweeks)
        for salary in salaries:
            biweek_plan1: Plan = {
                "budget_id": budget_id,
                "salary_id": salary.id_,
                "item": item,
            }
            biweek_list.append(biweek_plan1)

        payment_plan_list = payment_plan_controler.process_payment_plan(biweek_list)
        payment_plan_controler.save_bulk(payment_plan_list)


def main() -> None:
    exit_status = 0
    logging.basicConfig(level=logging.DEBUG)
    try:
        logging.info(f"Script {path.basename(__file__)} has started")
        run()
        logging.info("Bye!")
    except Exception as err:
        logging.exception(err)
        exit_status = 1
    finally:
        sys.exit(exit_status)


if __name__ == "__main__":
    main()
