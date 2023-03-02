#!/usr/bin/env python
import logging
import sys
from os import path
import uuid

from dotenv import load_dotenv

from src import create_app
from src.controller import create_new_budget


def run() -> None:
    load_dotenv()
    app = create_app()
    # app.run(debug=True)
    with app.app_context():
        old_budget_id = uuid.UUID("4849cb99-b084-4024-b613-8f3e0cd1079c")
        create_new_budget(old_budget_id)


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
