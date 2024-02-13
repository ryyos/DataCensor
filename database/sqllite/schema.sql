CREATE TABLE IF NOT EXISTS path(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path VARCHAR(500) NOT NULL,
    domain VARCHAR(255),
    timestamp_column TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now'))
);

