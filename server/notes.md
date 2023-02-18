# Ideas #

A budget consist of:

1. Bill
2. Salary
3. Payment plan

## enums ##

```sql
DO $$ BEGIN
    CREATE TYPE payment_type AS ENUM ('visa', 'mastercard', 'rbc', 'tangerine', 'saving');
    CREATE TYPE provider_type AS ENUM ('city_of_ottawa', 'enbridge', 'bell', 'hiydro_ottawa', 'netflix', 'copilot', 'disney+', 'google_one', 'spotify', 'cc', 'mortgage', 'condominio', 'fit4less', 'tia', 'seguro', 'line_of_credit', 'everyday', 'saving');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
```

## Tables ##

### template ###

```sql
CREATE TABLE template (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    provider provider_type NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    due_date INT DEFAULT NULL,
    payment payment_type NOT NULL,
    biweekly BOOLEAN NOT NULL DEFAULT FALSE
);
```

### budget ###

```sql
CREATE TABLE budget (
    id UUID PRIMARY KEY,
    month INT NOT NULL,
    year INT NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (month, year)
);
```

### bill ###

```sql
CREATE TABLE bill (
    id UUID PRIMARY KEY,
    budget_id UUID NOT NULL,
    provider provider_type NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    due_date DATE DEFAULT NULL,
    payment payment_type NOT NULL,
    is_paid BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY(budget_id) REFERENCES budget(id)
);
```

### salary ###

```sql
CREATE TABLE salary (
    id UUID PRIMARY KEY,
    date DATE NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    extra NUMERIC(8, 2) NOT NULL DEFAULT 0,
    budget_id UUID NOT NULL,
    FOREIGN KEY(budget_id) REFERENCES budget(id)
);
```

### payment_plan ###

```sql
CREATE TABLE payment_plan (
    id UUID PRIMARY KEY,
    payment payment_type NOT NULL,
    budget_id UUID NOT NULL,
    salary_id UUID NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY(budget_id) REFERENCES budget(id),
    FOREIGN KEY(salary_id) REFERENCES salary(id),
    UNIQUE (payment, budget_id, salary_id)
);
```

## Views ##

```sql
CREATE VIEW total_per_payment_type AS
SELECT payment, SUM(amount)
FROM bill
WHERE budget_id = (
    SELECT id
    FROM budget
    WHERE is_current = TRUE
)
GROUP BY payment
HAVING SUM(amount) > 0
```

## Models ##

1. Budget
2. Bill
3. Payment plan
4. Salary

## Generating a new budget ##

1. Close current budget. Set is_current = false. Closing is only posible if all expenses are paid. return True if it was closed
2. Only Open a new current budget if a previous budget was closed successfully. Set is_current = true
3. Copy template rows into bill table, generate real duedates and process biweekly bills
4. We need to edit the current budget a this point so that the generated payment plan (in next step) make senses. Ex there is not point to plan to pay a $0 payment type.
5. Generate rows into the salary table. This means dates and how many rows per month are based on latest date from previous salaries. Get salary base from last salary row.
6. Generate rows into payment plan, get basic cost from total_per_payment_type and divide them by the number of pay checks

### Features ###

1. create new budget, get budget id
2. close previous budget
3. update/add/remove bill. get list of bills
4. update/add/remove payment. get list of payments
5. update salary. get list of salaries

### Endpoints ###

1. /budget: [POST, GET, UPDATE]
2. /bill: [GET, POST]
3. /bill/<bill_id>: [UPDATE, DELETE]
4. /payment: [GET, POST]
5. /payment/<payment_id>: [UPDATE]
6. /salary: [GET]
7. /salary/<salary_id>: [UPDATE]
