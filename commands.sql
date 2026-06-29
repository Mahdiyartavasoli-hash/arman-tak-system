-- [CREATE_TABLE]
CREATE TABLE production (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_name TEXT,
    amount INTEGER,
    date TEXT
);

-- [INSERT_PRODUCTION]
INSERT INTO production (machine_name, amount, date)
VALUES (?, ?, ?);

-- [SELECT_ALL]
SELECT * FROM production;

-- [UPDATE_PRODUCTION]
UPDATE production SET amount = ? WHERE machine_name = ? AND date = ?;

-- [DELETE_PRODUCTION]
DELETE FROM production WHERE id = ?;

-- [SELECT_HIGH_PRODUCTION]
SELECT * FROM production WHERE machine_name = ? AND amount > ?;

-- [SELECT_ORDERED_PRODUCTION]
SELECT * FROM production WHERE machine_name = ? ORDER BY amount DESC;