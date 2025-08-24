-- schema.sql
-- Defines the database structure for the API Monitoring Dashboard.

-- Drop existing tables to ensure a clean setup
DROP TABLE IF EXISTS endpoints;
DROP TABLE IF EXISTS history;

-- Table to store the API endpoints to be monitored
CREATE TABLE endpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    method TEXT NOT NULL CHECK(method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')),
    headers TEXT, -- Stored as a JSON string
    body TEXT, -- Stored as a JSON string
    expected_status INTEGER NOT NULL DEFAULT 200,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table to store the history of each API test run
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint_id INTEGER NOT NULL,
    status_code INTEGER,
    response_time INTEGER, -- in milliseconds
    response_body TEXT,
    is_success BOOLEAN NOT NULL,
    error_message TEXT,
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (endpoint_id) REFERENCES endpoints (id)
);
