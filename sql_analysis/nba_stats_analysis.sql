-- NBA Player Statistics Analysis (2023-24 Season)
-- SQL queries to analyze NBA player performance data

-- Create the database schema
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

-- Note: This assumes the data is already loaded into the table
-- In a real scenario, you would use an INSERT statement or a bulk import tool

-- 1. Data Exploration and Basic Statistics
-- Basic information about the dataset
SELECT COUNT(*) AS total_players,
       COUNT(DISTINCT Team) AS total_teams,
       COUNT(DISTINCT Pos) AS total_positions
FROM nba_player_stats;

-- Summary statistics for key metrics
SELECT 
    AVG(PTS) AS avg_points,
    MIN(PTS) AS min_points,
    MAX(PTS) AS max_points,
    AVG(TRB) AS avg_rebounds,
    AVG(AST) AS avg_assists,
    AVG(STL) AS avg_steals,
    AVG(BLK) AS avg_blocks,
    AVG(FG_PCT) AS avg_fg_pct,
    AVG(ThreeP_PCT) AS avg_3p_pct,
    AVG(FT_PCT) AS avg_ft_pct
FROM nba_player_stats;

-- Distribution of player positions
SELECT Pos, COUNT(*) AS count
FROM nba_player_stats
GROUP BY Pos
ORDER BY count DESC;

-- Distribution of player ages
SELECT Age, COUNT(*) AS count
FROM nba_player_stats
GROUP BY Age
ORDER BY Age;

-- Distribution of minutes played
SELECT 
    CASE 
        WHEN MP < 10 THEN '0-9'
        WHEN MP < 20 THEN '10-19'
        WHEN MP < 30 THEN '20-29'
        WHEN MP < 40 THEN '30-39'
        ELSE '40+'
    END AS minutes_range,
    COUNT(*) AS player_count
FROM nba_player_stats
GROUP BY minutes_range
ORDER BY 
    CASE minutes_range
        WHEN '0-9' THEN 1
        WHEN '10-19' THEN 2
        WHEN '20-29' THEN 3
        WHEN '30-39' THEN 4
        ELSE 5
    END;

-- 2. Filter for significant playing time
-- Create a view for players with significant minutes
CREATE VIEW significant_players AS
SELECT *
FROM nba_player_stats
WHERE MP >= 20 AND G >= 40;

-- Count of players with significant minutes
SELECT COUNT(*) AS significant_players_count
FROM significant_players;

-- 3. Top Performers Analysis

-- Top 10 scorers
SELECT Player, Team, Pos, PTS, FG_PCT, ThreeP_PCT, FT_PCT
FROM significant_players
ORDER BY PTS DESC
LIMIT 10;

-- Top 10 rebounders
SELECT Player, Team, Pos, TRB, ORB, DRB
FROM significant_players
ORDER BY TRB DESC
LIMIT 10;

-- Top 10 assist leaders
SELECT Player, Team, Pos, AST, TOV, 
       CASE WHEN TOV = 0 THEN AST ELSE AST/TOV END AS AST_TO_TOV_RATIO
FROM significant_players
ORDER BY AST DESC
LIMIT 10;

-- Top 10 steal leaders
SELECT Player, Team, Pos, STL
FROM significant_players
ORDER BY STL DESC
LIMIT 10;

-- Top 10 block leaders
SELECT Player, Team, Pos, BLK
FROM significant_players
ORDER BY BLK DESC
LIMIT 10;

-- Top 10 3-point shooters (minimum 100 3PA)
SELECT Player, Team, Pos, ThreeP_PCT, ThreeP, ThreePA
FROM nba_player_stats
WHERE ThreePA >= 100
ORDER BY ThreeP_PCT DESC
LIMIT 10;

-- 4. Player Efficiency Metrics

-- Calculate Player Efficiency Rating (PER) - simplified
SELECT 
    Player, 
    Team,
    Pos,
    (PTS + TRB + AST + STL*2 + BLK*2 - TOV - (FGA-FG) - (FTA-FT)*0.5) / MP AS PER,
    PTS,
    TRB,
    AST,
    MP
FROM significant_players
ORDER BY PER DESC
LIMIT 15;

-- Calculate True Shooting Percentage (TS%)
SELECT 
    Player,
    Team,
    Pos,
    PTS / (2 * (FGA + 0.44 * FTA)) AS TS_PCT,
    PTS,
    FGA,
    FTA
FROM significant_players
ORDER BY TS_PCT DESC
LIMIT 15;

-- 5. Position-Based Analysis

-- Average statistics by position
SELECT 
    Pos,
    COUNT(*) AS player_count,
    AVG(PTS) AS avg_points,
    AVG(TRB) AS avg_rebounds,
    AVG(AST) AS avg_assists,
    AVG(STL) AS avg_steals,
    AVG(BLK) AS avg_blocks,
    AVG(TOV) AS avg_turnovers,
    AVG(FG_PCT) AS avg_fg_pct,
    AVG(ThreeP_PCT) AS avg_3p_pct,
    AVG(FT_PCT) AS avg_ft_pct,
    AVG(MP) AS avg_minutes
FROM significant_players
GROUP BY Pos
ORDER BY Pos;

-- Position comparison for specific stats
SELECT 
    Pos,
    AVG(PTS) AS avg_points
FROM significant_players
GROUP BY Pos
ORDER BY avg_points DESC;

SELECT 
    Pos,
    AVG(TRB) AS avg_rebounds
FROM significant_players
GROUP BY Pos
ORDER BY avg_rebounds DESC;

SELECT 
    Pos,
    AVG(AST) AS avg_assists
FROM significant_players
GROUP BY Pos
ORDER BY avg_assists DESC;

SELECT 
    Pos,
    AVG(STL) AS avg_steals
FROM significant_players
GROUP BY Pos
ORDER BY avg_steals DESC;

SELECT 
    Pos,
    AVG(BLK) AS avg_blocks
FROM significant_players
GROUP BY Pos
ORDER BY avg_blocks DESC;

-- 6. Team Analysis

-- Average player statistics by team
SELECT 
    Team,
    COUNT(*) AS player_count,
    AVG(PTS) AS avg_points,
    AVG(TRB) AS avg_rebounds,
    AVG(AST) AS avg_assists,
    AVG(STL) AS avg_steals,
    AVG(BLK) AS avg_blocks,
    AVG(TOV) AS avg_turnovers,
    AVG(FG_PCT) AS avg_fg_pct,
    AVG(ThreeP_PCT) AS avg_3p_pct,
    AVG(FT_PCT) AS avg_ft_pct,
    AVG(PTS) / (2 * (AVG(FGA) + 0.44 * AVG(FTA))) AS avg_ts_pct
FROM significant_players
GROUP BY Team
ORDER BY avg_points DESC;

-- Best team in each category
WITH team_stats AS (
    SELECT
        Team,
        AVG(PTS) AS avg_points,
        AVG(TRB) AS avg_rebounds,
        AVG(AST) AS avg_assists,
        AVG(STL) AS avg_steals,
        AVG(BLK) AS avg_blocks,
        AVG(FG_PCT) AS avg_fg_pct,
        AVG(ThreeP_PCT) AS avg_3p_pct,
        AVG(FT_PCT) AS avg_ft_pct
    FROM significant_players
    GROUP BY Team
)

-- Best scoring team
SELECT Team, avg_points
FROM team_stats
ORDER BY avg_points DESC
LIMIT 1;

-- Best rebounding team
SELECT Team, avg_rebounds
FROM team_stats
ORDER BY avg_rebounds DESC
LIMIT 1;

-- Best assisting team
SELECT Team, avg_assists
FROM team_stats
ORDER BY avg_assists DESC
LIMIT 1;

-- Best shooting team (FG%)
SELECT Team, avg_fg_pct
FROM team_stats
ORDER BY avg_fg_pct DESC
LIMIT 1;

-- Best 3-point shooting team
SELECT Team, avg_3p_pct
FROM team_stats
ORDER BY avg_3p_pct DESC
LIMIT 1;

-- 7. Age-Based Analysis

-- Performance by age
SELECT 
    Age,
    COUNT(*) AS player_count,
    AVG(PTS) AS avg_points,
    AVG(TRB) AS avg_rebounds,
    AVG(AST) AS avg_assists,
    AVG(STL) AS avg_steals,
    AVG(BLK) AS avg_blocks,
    AVG(FG_PCT) AS avg_fg_pct,
    AVG(ThreeP_PCT) AS avg_3p_pct,
    AVG(FT_PCT) AS avg_ft_pct,
    AVG((PTS + TRB + AST + STL*2 + BLK*2 - TOV - (FGA-FG) - (FTA-FT)*0.5) / MP) AS avg_per
FROM significant_players
GROUP BY Age
ORDER BY avg_per DESC;

-- 8. Advanced Statistical Analysis

-- Correlation approximation between minutes and points
-- In SQL, computing correlation directly is complex
-- This is a simple approximation of the relationship
SELECT
    SUM((MP - avg_mp) * (PTS - avg_pts)) / 
    (SQRT(SUM(POWER(MP - avg_mp, 2))) * SQRT(SUM(POWER(PTS - avg_pts, 2)))) AS mp_pts_correlation
FROM significant_players,
     (SELECT AVG(MP) AS avg_mp, AVG(PTS) AS avg_pts FROM significant_players) AS avgs;

-- 9. Summary Statistics for the League

-- League-wide statistics for the filtered players
SELECT 
    COUNT(*) AS player_count,
    AVG(PTS) AS avg_points,
    AVG(TRB) AS avg_rebounds,
    AVG(AST) AS avg_assists,
    AVG(FG_PCT) AS avg_fg_pct,
    AVG(ThreeP_PCT) AS avg_3p_pct,
    AVG(FT_PCT) AS avg_ft_pct,
    AVG(MP) AS avg_minutes,
    AVG(Age) AS avg_age
FROM significant_players;

-- 10. Combined Player Rating

-- Create a comprehensive player rating using multiple metrics
WITH player_metrics AS (
    SELECT 
        Player,
        Team,
        Pos,
        PTS,
        -- Calculate PER
        (PTS + TRB + AST + STL*2 + BLK*2 - TOV - (FGA-FG) - (FTA-FT)*0.5) / MP AS PER,
        -- Calculate TS%
        PTS / (2 * (FGA + 0.44 * FTA)) AS TS_PCT,
        -- Calculate simplified BPM (Box Plus/Minus)
        (PTS - 20)/20 + (TRB - 7)/7 + (AST - 5)/5 + STL + BLK*0.7 - TOV/2 AS BPM
    FROM significant_players
),
min_max_values AS (
    SELECT
        MIN(PER) AS min_per, MAX(PER) AS max_per,
        MIN(TS_PCT) AS min_ts, MAX(TS_PCT) AS max_ts,
        MIN(BPM) AS min_bpm, MAX(BPM) AS max_bpm
    FROM player_metrics
)

SELECT 
    pm.Player,
    pm.Team,
    pm.Pos,
    pm.PTS,
    pm.PER,
    pm.TS_PCT,
    pm.BPM,
    -- Calculate normalized combined rating (0-100 scale)
    (
        (pm.PER - mmv.min_per) / (mmv.max_per - mmv.min_per) +
        (pm.TS_PCT - mmv.min_ts) / (mmv.max_ts - mmv.min_ts) +
        (pm.BPM - mmv.min_bpm) / (mmv.max_bpm - mmv.min_bpm)
    ) / 3 * 100 AS Combined_Rating
FROM player_metrics pm, min_max_values mmv
ORDER BY Combined_Rating DESC
LIMIT 15; 