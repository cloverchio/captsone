CREATE TABLE IF NOT EXISTS candidates (
    id TEXT NOT NULL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    years_experience INT,
    salary INT,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);