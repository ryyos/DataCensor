CREATE TABLE IF NOT EXISTS path(
    id INT NOT NULL AUTO_INCREMENT,
    path VARCHAR(500) NOT NULL,
    domain VARCHAR(255),
    dates TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);


INSERT INTO path (path, domain) VALUES ('data/data_raw/hehe', 'archive');

SELECT path from path WHERE domain='archive';


INSERT INTO path( id, path, domain ) 
VALUES (1, 'data/data_raw', 'hehe');