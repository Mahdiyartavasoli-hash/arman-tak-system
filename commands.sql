-- [CREATE_TABLE]
CREATE TABLE production (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_name TEXT,
    amount INTEGER,
    date TEXT
);

-- [INSERT_PRODUCTION]
INSERT INTO production (machine_id, amount, date)
VALUES (?, ?, ?);


-- [SELECT_ALL]
SELECT * FROM production;


-- [UPDATE_PRODUCTION]
UPDATE production SET amount = ? WHERE id = ?;


-- [DELETE_PRODUCTION]
DELETE FROM production WHERE id = ?;


-- [SELECT_HIGH_PRODUCTION]
SELECT * FROM production WHERE machine_name = ? AND amount > ?;


-- [SELECT_ORDERED_PRODUCTION]
SELECT * FROM production WHERE machine_name = ? ORDER BY amount DESC;


-- [get_analytics]
SELECT SUM(amount), AVG(amount) FROM production WHERE machine_name = ?


-- [get_max_min]
SELECT MAX(amount), MIN(amount) FROM production WHERE machine_name = ?


-- [get_production_count]
SELECT COUNT(amount) FROM production WHERE machine_name = ?


-- [CREATE_MACHINES_TABLE]
CREATE TABLE IF NOT EXISTS machines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_name TEXT NOT NULL,
    model_year INTEGER
);


-- [ADD_MACHINE_ID_COLUMN]
ALTER TABLE production ADD COLUMN machine_id INTEGER;


-- [SELECT_PRODUCTION_WITH_JOIN]
SELECT production.id, machines.machine_name, production.amount, production.date
FROM production
INNER JOIN machines ON production.machine_id = machines.id;


