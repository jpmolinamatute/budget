DROP VIEW IF EXISTS total_per_payment_type;
DROP TABLE IF EXISTS template;
DROP TABLE IF EXISTS bill;
DROP TABLE IF EXISTS payment_plan;
DROP TABLE IF EXISTS salary;
DROP TABLE IF EXISTS budget;


DO $$ BEGIN
    CREATE TYPE payment_type AS ENUM ('visa', 'mastercard', 'rbc', 'tangerine', 'saving');
    CREATE TYPE provider_type AS ENUM ('city_of_ottawa', 'enbridge', 'bell', 'hiydro_ottawa', 'netflix', 'copilot', 'disney+', 'google_one', 'spotify', 'cc', 'mortgage', 'condominio', 'fit4less', 'tia', 'seguro', 'line_of_credit', 'everyday', 'saving');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE template (
    provider provider_type NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    due_date INT NOT NULL DEFAULT 0,
    payment payment_type NOT NULL,
    biweekly BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE budget (
    id UUID PRIMARY KEY,
    month INT NOT NULL,
    year INT NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (month, year)
);

CREATE TABLE bill (
    id UUID PRIMARY KEY,
    budget_id UUID NOT NULL,
    provider provider_type NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    due_date DATE NOT NULL,
    payment payment_type NOT NULL,
    is_paid BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY(budget_id) REFERENCES budget(id)
);

CREATE TABLE salary (
    id UUID PRIMARY KEY,
    date DATE NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    extra NUMERIC(8, 2) NOT NULL DEFAULT 0,
    budget_id UUID NOT NULL,
    FOREIGN KEY(budget_id) REFERENCES budget(id)
);

CREATE TABLE payment_plan (
    id UUID PRIMARY KEY,
    payment payment_type NOT NULL,
    budget_id UUID NOT NULL,
    salary_id UUID NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY(budget_id) REFERENCES budget(id),
    FOREIGN KEY(salary_id) REFERENCES salary(id)
);


INSERT INTO template (provider, amount, due_date, payment, biweekly) VALUES 
('city_of_ottawa', 0.0, 3, 'visa', FALSE),
('enbridge', 0.0, 6, 'visa', FALSE),
('bell', 160.67, 28, 'visa', FALSE),
('hiydro_ottawa', 0.0, 12, 'visa', FALSE),
('netflix', 26.95, 14, 'visa', FALSE),
('copilot', 14.25, 15, 'visa', FALSE),
('disney+', 13.55, 20, 'visa', FALSE),
('google_one', 11.29, 20, 'visa', FALSE),
('google_one', 2.93, 23, 'visa', FALSE),
('spotify', 11.49, 25, 'visa', FALSE),
('cc', 0, 0, 'visa', FALSE),
('mortgage', 1196.16, 0, 'tangerine', TRUE),
('condominio', 296.83, 1, 'tangerine', FALSE),
('fit4less', 27.10, 0, 'tangerine', TRUE),
('tia', 500, 1, 'tangerine', FALSE),
('seguro', 42.86, 24, 'tangerine', FALSE),
('line_of_credit', 232.08, 23, 'rbc', FALSE),
('line_of_credit', 250, 0, 'rbc', TRUE),
('everyday', 600.00, 0, 'mastercard', FALSE),
('saving', 0.00, 0, 'saving', TRUE);


CREATE VIEW total_per_payment_type AS
SELECT payment, SUM(amount)
FROM bill
WHERE budget_id = (
    SELECT id
    FROM budget
    WHERE is_current = TRUE
)
GROUP BY payment;
