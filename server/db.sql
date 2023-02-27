DROP VIEW IF EXISTS total_per_payment_type;
DROP TABLE IF EXISTS template;
DROP TABLE IF EXISTS bill;
DROP TABLE IF EXISTS payment_plan;
DROP TABLE IF EXISTS income;
DROP TABLE IF EXISTS budget;


DO $$ BEGIN
    CREATE TYPE payment_type AS ENUM ('visa', 'mastercard', 'rbc', 'tangerine', 'saving');
    CREATE TYPE provider_type AS ENUM ('city_of_ottawa', 'enbridge', 'bell', 'hiydro_ottawa', 'netflix', 'copilot', 'disney+', 'google_one', 'spotify', 'cc', 'mortgage', 'condominio', 'fit4less', 'tia', 'seguro', 'line_of_credit', 'everyday', 'saving');
    CREATE TYPE income_type AS ENUM ('salary', 'bonus', 'other');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE template (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    provider provider_type NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    due_date INT DEFAULT NULL,
    payment payment_type NOT NULL,
    biweekly BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE budget (
    id UUID PRIMARY KEY,
    month INT NOT NULL,
    year INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (month, year)
);

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

CREATE TABLE income (
    id UUID PRIMARY KEY,
    date DATE NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    income_type income_type NOT NULL,
    budget_id UUID NOT NULL,
    FOREIGN KEY(budget_id) REFERENCES budget(id)
);

CREATE TABLE payment_plan (
    id UUID PRIMARY KEY,
    payment payment_type NOT NULL,
    budget_id UUID NOT NULL,
    income_id UUID NOT NULL,
    amount NUMERIC(8, 2) NOT NULL DEFAULT 0,
    is_closed BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY(budget_id) REFERENCES budget(id),
    FOREIGN KEY(income_id) REFERENCES income(id),
    UNIQUE (payment, budget_id, income_id)
);

CREATE VIEW total_per_payment_type AS
SELECT payment, SUM(amount)
FROM bill
WHERE budget_id = (
    SELECT id
    FROM budget
    WHERE is_current = TRUE
)
GROUP BY payment
HAVING SUM(amount) > 0;

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
('cc', 0, NULL, 'visa', FALSE),
('mortgage', 1195.16, 0, 'tangerine', TRUE),
('condominio', 296.83, 1, 'tangerine', FALSE),
('fit4less', 27.10, 0, 'tangerine', TRUE),
('tia', 500.00, 1, 'tangerine', FALSE),
('seguro', 42.86, 24, 'tangerine', FALSE),
('line_of_credit', 232.08, 23, 'rbc', FALSE),
('line_of_credit', 500.00, NULL, 'rbc', FALSE),
('everyday', 300.00, 0, 'mastercard', TRUE),
('saving', 0.00, NULL, 'saving', FALSE);

INSERT INTO budget(id, month, year, start_date, end_date, is_current)
VALUES ('4849cb99-b084-4024-b613-8f3e0cd1079c', 2, 2023, '2023-01-20', '2023-02-17', true);

INSERT INTO bill(id, budget_id, provider, amount, due_date, payment, is_paid) VALUES
('0fd33167-39ce-4d6c-9f23-77364b5b3bd7', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'city_of_ottawa', 200.57, '2023-02-03', 'visa', TRUE),
('4bb043a3-d888-4073-a94b-7f8e1de19b78', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'enbridge', 169.82, '2023-02-06', 'visa', TRUE),
('cd0c2726-1622-4c6d-b15c-94a99bd839b8', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'bell', 74.46, '2023-02-28', 'visa', TRUE),
('7691a2f9-048e-40d6-9849-08dddc2d5fb3', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'hiydro_ottawa', 65.23, '2023-02-12', 'visa', TRUE),
('99bb5015-3562-4488-aa53-2bd947887348', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'netflix', 26.95, '2023-02-14', 'visa', TRUE),
('9e21cf69-1a2a-411a-b0da-ca016c28e603', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'copilot', 14.25, '2023-02-15', 'visa', TRUE),
('8ac8c744-7884-484d-92bf-747eb432e073', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'disney+', 13.55, '2023-02-20', 'visa', TRUE),
('3ad412de-84b6-4306-9cf1-2363fdb45d04', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'google_one', 11.29, '2023-02-20', 'visa', TRUE),
('35e0c842-9eff-4b8b-852a-627c33a3a18b', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'google_one', 2.93, '2023-02-23', 'visa', TRUE),
('79f48d3b-773e-43ae-854d-da3dbb7c40b2', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'spotify', 11.49, '2023-02-25', 'visa', TRUE),
('65a6e7a3-b41b-47c6-a7ad-8e7c24b41bc2', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'cc', 88.60, NULL, 'visa', TRUE),
('463e3f21-f2b5-4075-afc8-40046265d0a0', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'mortgage', 1195.16, '2023-02-07', 'tangerine', TRUE),
('178dfaf4-0d94-459f-8cbf-e6f40618de11', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'mortgage', 1195.16, '2023-02-21', 'tangerine', TRUE),
('4715095e-ba07-430e-81e3-b0b733ce1c7b', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'condominio', 296.83, '2023-02-01', 'tangerine', TRUE),
('59f3b96f-1f29-432f-be8f-5453d627602a', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'fit4less', 27.10, '2023-02-07', 'tangerine', TRUE),
('31d651a3-1f6b-4268-a109-95fc066ca67c', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'fit4less', 27.10, '2023-02-21', 'tangerine', TRUE),
('7fcb9047-f030-45a4-b613-74acfb62e4ea', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'tia', 550.00, '2023-02-01', 'tangerine', TRUE),
('2605de87-178d-4e60-9b69-09edeab64cbb', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'seguro', 42.86, '2023-02-24', 'tangerine', TRUE),
('0212a941-ee21-418f-8096-cd78efaf9802', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'line_of_credit', 232.08, '2023-02-23', 'rbc', TRUE),
('486f536c-eb05-419c-b023-050acb4bc144', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'line_of_credit', 600.00, NULL, 'rbc', TRUE),
('43906de8-9020-44e8-a64f-ae9fbaa6a0e2', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'everyday', 795.81, '2023-02-17', 'mastercard', TRUE),
('f3559b54-fd50-4d23-8789-7d1052f7d9c4', '4849cb99-b084-4024-b613-8f3e0cd1079c', 'saving', 205.75, NULL, 'saving', TRUE);


INSERT INTO income(id, date, amount, budget_id, income_type) VALUES
('35b93c12-47cf-4219-8f40-c05ddba9a665', '2023-02-01', 5.18, '4849cb99-b084-4024-b613-8f3e0cd1079c', 'other'),
('02c19a7f-ad0d-4e49-a8b6-2cf0e0fabe06', '2023-02-03', 2920.92, '4849cb99-b084-4024-b613-8f3e0cd1079c', 'salary'),
('6ac073f2-e40d-4ef7-8fd2-0178c0f48d53', '2023-02-17', 2920.92, '4849cb99-b084-4024-b613-8f3e0cd1079c', 'salary');


INSERT INTO payment_plan(id, payment, budget_id, income_id, amount) VALUES
('a9497995-8dd3-4274-8c6f-8acdd30a90fc', 'rbc', '4849cb99-b084-4024-b613-8f3e0cd1079c', '02c19a7f-ad0d-4e49-a8b6-2cf0e0fabe06', 416.04),
('5942f84c-8323-4315-87b6-0b32ec2b7bea', 'tangerine', '4849cb99-b084-4024-b613-8f3e0cd1079c', '02c19a7f-ad0d-4e49-a8b6-2cf0e0fabe06', 1586.25),
('5354beb3-123d-48a0-992f-1b40cbb737b2', 'visa', '4849cb99-b084-4024-b613-8f3e0cd1079c', '02c19a7f-ad0d-4e49-a8b6-2cf0e0fabe06', 351.60),
('b5a8c948-ac9c-4d59-9ee1-fe3bdbb89ef2', 'mastercard', '4849cb99-b084-4024-b613-8f3e0cd1079c', '02c19a7f-ad0d-4e49-a8b6-2cf0e0fabe06', 495.81),
('d55c0984-f778-4062-a881-89a4b382701c', 'saving', '4849cb99-b084-4024-b613-8f3e0cd1079c', '02c19a7f-ad0d-4e49-a8b6-2cf0e0fabe06', 76.40),
 
('23176157-f1c7-4904-8cb1-13a1ecb2423e', 'rbc', '4849cb99-b084-4024-b613-8f3e0cd1079c', '6ac073f2-e40d-4ef7-8fd2-0178c0f48d53', 416.04),
('2759399c-2443-42ed-a936-1f3b02c09f6e', 'tangerine', '4849cb99-b084-4024-b613-8f3e0cd1079c', '6ac073f2-e40d-4ef7-8fd2-0178c0f48d53', 1747.99),
('4f7346c5-caaf-4836-b04a-45c309b92713', 'visa', '4849cb99-b084-4024-b613-8f3e0cd1079c', '6ac073f2-e40d-4ef7-8fd2-0178c0f48d53', 327.54),
('85c21f2f-c34b-40a1-907e-fd15111cfa82', 'mastercard', '4849cb99-b084-4024-b613-8f3e0cd1079c', '6ac073f2-e40d-4ef7-8fd2-0178c0f48d53', 300),
('38a02514-a4da-4183-8db8-3b1390fee932', 'saving', '4849cb99-b084-4024-b613-8f3e0cd1079c', '6ac073f2-e40d-4ef7-8fd2-0178c0f48d53', 129.35);
