CREATE TABLE ADVENTURE_TRIP(
    TRIP_ID DECIMAL(3,0) PRIMARY KEY,
    TRIP_NAME NVARCHAR(75),
    START_LOCATION CHAR(50),
    STATE CHAR(2),
    DISTANCE NUMBER(4,0),
    MAX_GRP_SIZE NUMBER(4,0),
    TYPE CHAR(20),
    SEASON CHAR(20)
);

INSERT INTO ADVENTURE_TRIP VALUES (45, 'Jay Peak', 'Jay', 'VT', 8, 8, 'Hiking', 'Summer');

DROP TABLE ADVENTURE_TRIP