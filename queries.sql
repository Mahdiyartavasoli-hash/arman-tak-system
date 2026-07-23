-- name: create-table-factory-managers!
CREATE TABLE IF NOT EXISTS factory_managers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- name: create-table-machines!
CREATE TABLE IF NOT EXISTS machines (
    id SERIAL PRIMARY KEY,
    machine_name VARCHAR(100) NOT NULL,
    model_year INTEGER
);

-- name: create-table-production!
CREATE TABLE IF NOT EXISTS production (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER REFERENCES machines(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    date VARCHAR(50) NOT NULL
);

-- name: create-table-users!
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- name: create-machine$
INSERT INTO machines (machine_name, model_year) 
VALUES (:machine_name, :model_year) 
RETURNING id;

-- name: check-machine-exists^
SELECT id FROM machines WHERE id = :machine_id;

-- name: insert-production$
INSERT INTO production (machine_id, amount, date) 
VALUES (:machine_id, :amount, :date) 
RETURNING id;

-- name: update-production$
UPDATE production 
SET amount = :new_amount 
WHERE id = :record_id 
RETURNING id;

-- name: delete-production$
DELETE FROM production 
WHERE id = :record_id 
RETURNING id;

-- name: get-analytics^
SELECT SUM(amount) as total_production, AVG(amount) as average_production 
FROM production 
WHERE machine_id = :machine_id;

-- name: register-user$
INSERT INTO users (username, password) 
VALUES (:username, :password) 
RETURNING id;