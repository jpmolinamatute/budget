#!/usr/bin/env python
import logging
import sys
import uuid
from os import path

from dotenv import load_dotenv

from src import create_app
from src.controller.complete_budget_controler import CompleteBudgetControler


def run() -> None:
    load_dotenv()
    app = create_app()
    # app.run(debug=True)
    with app.app_context():
        budget = CompleteBudgetControler(3, 2023, uuid.UUID("4849cb99-b084-4024-b613-8f3e0cd1079c"))
        budget.process_bills()
        biweek_plan = budget.process_salaries()
        budget.process_payment_plan(biweek_plan)


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
