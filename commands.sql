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
SELECT p.id, m.machine_name, p.amount, p.date
FROM production p
INNER JOIN machines m ON p.machine_id = m.id
WHERE m.machine_name = ? AND p.amount > ?;

-- [SELECT_ORDERED_PRODUCTION]
SELECT p.id, m.machine_name, p.amount, p.date
FROM production p
INNER JOIN machines m ON p.machine_id = m.id
WHERE m.machine_name = ? 
ORDER BY p.amount DESC;

-- [get_analytics]
SELECT SUM(p.amount), AVG(p.amount) 
FROM production p
INNER JOIN machines m ON p.machine_id = m.id
WHERE m.machine_name = ?;

-- [get_max_min]
SELECT MAX(p.amount), MIN(p.amount) 
FROM production p
INNER JOIN machines m ON p.machine_id = m.id
WHERE m.machine_name = ?;

-- [get_production_count]
SELECT COUNT(p.amount) 
FROM production p
INNER JOIN machines m ON p.machine_id = m.id
WHERE m.machine_name = ?;


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


