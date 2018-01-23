CREATE TABLE defs
(
    server  INT NOT NULL,
    command TEXT NOT NULL,
    def     TEXT NOT NULL,
    PRIMARY KEY (server, command)
);