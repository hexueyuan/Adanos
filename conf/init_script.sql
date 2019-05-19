CREATE TABLE IF NOT EXISTS cpuTable (
    TIMESTAMP       INTEGER     PRIMARY KEY     NOT NULL,
    LOGICALCNT      INTEGER                     NOT NULL,
    PHYSICSCNT      INTEGER                     NOT NULL,
    USERATE         FLOAT                       NOT NULL,
    USERTIME        FLOAT                       NOT NULL,
    SYSTEMTIME      FLOAT                       NOT NULL,
    IDLETIME        FLOAT                       NOT NULL,
    FREQUENCY       INTEGER                     NOT NULL
);
CREATE TABLE IF NOT EXISTS memoryTable (
    TIMESTAMP       INTEGER     PRIMARY KEY     NOT NULL,
    MEMORYTOTAL     INTEGER                     NOT NULL,
    MEMORYUSERATE   FLOAT                       NOT NULL,
    SWAPTOTAL       INTEGER                     NOT NULL,
    SWAPUSERATE     FLOAT                       NOT NULL,
    SWAPSIN         INTEGER                     NOT NULL,
    SWAPSOUT        INTEGER                     NOT NULL
);
CREATE TABLE IF NOT EXISTS diskTable (
    TIMESTAMP       INTEGER                     NOT NULL,
    DEVICENAME      TEXT                        NOT NULL,
    MOUNTPOINT      TEXT                        NOT NULL,
    FSTYPE          TEXT                        NOT NULL,
    TOTAL           INTEGER                     NOT NULL,
    USERATE         FLOAT                       NOT NULL,
    PRIMARY KEY(TIMESTAMP, DEVICENAME)
);
CREATE TABLE IF NOT EXISTS userTable (
    USERNAME        TEXT        PRIMARY KEY     NOT NULL,
    PASSWORD        TEXT                        NOT NULL
)