CREATE TABLE disk_use_rate (
    mount_point CHAR(50) NOT NULL,
    use_rate FLOAT NOT NULL,
    timestamp INTEGER NOT NULL,
    total_space Float NOT NULL
);
