#!/usr/bin/env python
import logging
import sys
from os import path, environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.controller import create_new_budget


def run(logger: logging.Logger) -> None:
    load_dotenv()
    database = environ["POSTGRES_DATABASE"]
    user = environ["POSTGRES_USER"]
    password = environ["POSTGRES_PASSWORD"]
    host = environ["POSTGRES_HOST"]
    port = environ["POSTGRES_PORT"]
    database_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(database_uri, future=True)
    Session = sessionmaker(engine, future=True)
    with Session() as session:
        create_new_budget(logger, session)


def main() -> None:
    exit_status = 0
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    try:
        logging.info(f"Script {path.basename(__file__)} has started")
        run(logger)
        logging.info("Bye!")
    except Exception as err:
        logging.exception(err)
        exit_status = 1
    finally:
        sys.exit(exit_status)


if __name__ == "__main__":
    main()
