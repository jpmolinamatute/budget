#!/usr/bin/env python
import logging
import sys
from os import path
import uuid
from datetime import datetime
import psycopg2


def connect_to_db() -> psycopg2.connect:
    return psycopg2.connect(dbname="finance", user="juanpa")


def create_budget(conn: psycopg2.connect, month: int, year: int) -> str:
    cur = conn.cursor()
    sql_stmt = """
        INSERT INTO budget (id, month, year, is_current)
        VALUES (%s, %s, %s, %s)
    """
    budget_id = str(uuid.uuid4())
    stmt = cur.mogrify(sql_stmt, (budget_id, month, year, True))
    cur.execute(stmt)
    conn.commit()
    cur.close()
    return budget_id


def create_budget_detail(
    conn: psycopg2.connect,
    expenses_list: list[tuple],
) -> None:
    with conn.cursor() as curs:
        sql_stmt = """
            INSERT INTO budget_detail (id, budget_id, provider, amount, due_date, payment_type)
            VALUES (%s, %s, %s, %s)
        """
        for expense in expenses_list:
            stmt = curs.mogrify(sql_stmt, expense)
            curs.execute(stmt)
        conn.commit()


def get_expenses_from_template(conn: psycopg2.connect) -> list[tuple]:
    return [("",)]


def process_expenses(
    expenses_list: list[tuple],
    budget_id: str,
    month: int,
    year: int,
) -> list[tuple]:
    process_expenses_list = []
    for expense in expenses_list:
        # check if biweekly is True and if it is, create two or three expenses based on month
        # and year
        pass
    return process_expenses_list


def write_to_db() -> None:
    conn = connect_to_db()
    now = datetime.now()
    budget_id = create_budget(conn, now.month, now.year)
    expenses_list = get_expenses_from_template(conn)
    process_expenses_list = process_expenses(expenses_list, budget_id, now.month, now.year)
    logging.info(f"Budget {budget_id} created")
    conn.close()


def main() -> None:
    exit_status = 0
    logging.basicConfig(level=logging.DEBUG)
    try:
        logging.info(f"Script {path.basename(__file__)} has started")
        write_to_db()
        logging.info("Bye!")
    except Exception as err:
        logging.exception(err)
        exit_status = 1
    finally:
        sys.exit(exit_status)


if __name__ == "__main__":
    main()
