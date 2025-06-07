-- Script to load NBA player statistics from CSV file into the database
-- This is written for PostgreSQL syntax; adjust for your specific database system

-- First create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS nba_player_stats (
    Rk INTEGER,
    Player VARCHAR(255),
    Age INTEGER,
    Team VARCHAR(3),
    Pos VARCHAR(5),
    G INTEGER,
    GS INTEGER,
    MP DECIMAL(4,1),
    FG DECIMAL(3,1),
    FGA DECIMAL(3,1),
    FG_PCT DECIMAL(4,3),
    ThreeP DECIMAL(3,1),
    ThreePA DECIMAL(3,1),
    ThreeP_PCT DECIMAL(4,3),
    TwoP DECIMAL(3,1),
    TwoPA DECIMAL(3,1),
    TwoP_PCT DECIMAL(4,3),
    eFG_PCT DECIMAL(4,3),
    FT DECIMAL(3,1),
    FTA DECIMAL(3,1),
    FT_PCT DECIMAL(4,3),
    ORB DECIMAL(3,1),
    DRB DECIMAL(3,1),
    TRB DECIMAL(3,1),
    AST DECIMAL(3,1),
    STL DECIMAL(3,1),
    BLK DECIMAL(3,1),
    TOV DECIMAL(3,1),
    PF DECIMAL(3,1),
    PTS DECIMAL(3,1),
    Awards VARCHAR(255)
);

-- For PostgreSQL, you can use the COPY command to load data
-- COPY nba_player_stats FROM '/path/to/nba_player_stats_2023_24_per_game.csv' DELIMITER ',' CSV HEADER;

-- For MySQL, you can use LOAD DATA INFILE
/*
LOAD DATA INFILE '/path/to/nba_player_stats_2023_24_per_game.csv'
INTO TABLE nba_player_stats
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
*/

-- For SQLite, you can use the .import command (from the SQLite CLI)
-- .mode csv
-- .headers on
-- .import '/path/to/nba_player_stats_2023_24_per_game.csv' nba_player_stats

-- Alternative: Insert the data row by row using INSERT statements
-- This is inefficient for large datasets but works on all SQL database systems
-- You would typically generate these INSERT statements programmatically

-- Example of inserting a single row (for illustration):
/*
INSERT INTO nba_player_stats (
    Rk, Player, Age, Team, Pos, G, GS, MP, FG, FGA, FG_PCT, 
    ThreeP, ThreePA, ThreeP_PCT, TwoP, TwoPA, TwoP_PCT, 
    eFG_PCT, FT, FTA, FT_PCT, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, Awards
) VALUES (
    1, 'Joel Embiid', 29, 'PHI', 'C', 39, 39, 33.6, 11.5, 21.8, 0.529,
    1.4, 3.6, 0.388, 10.2, 18.3, 0.556,
    0.561, 10.2, 11.6, 0.883, 2.4, 8.6, 11.0, 5.6, 1.2, 1.7, 3.8, 2.9, 34.7, 'AS'
);
*/

-- After loading the data, verify it was loaded correctly
SELECT COUNT(*) AS row_count FROM nba_player_stats;
SELECT * FROM nba_player_stats LIMIT 5; 