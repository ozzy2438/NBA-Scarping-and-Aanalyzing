# NBA Player Statistics Analysis (SQL)

This directory contains SQL scripts for analyzing NBA player statistics for the 2023-24 season. The scripts demonstrate how to perform similar analysis as the Jupyter notebook, but using SQL queries.

## Files

- `nba_stats_analysis.sql`: Contains SQL queries for analyzing the NBA player statistics
- `load_nba_data.sql`: Contains SQL commands for loading the CSV data into a database

## Prerequisites

- A SQL database system (PostgreSQL, MySQL, SQLite, etc.)
- The NBA player statistics CSV file (`nba_player_stats_2023_24_per_game.csv`) 

## Database Setup

1. Create a database for the NBA analysis
2. Use the appropriate commands in `load_nba_data.sql` to load the data into your database
   - The file contains examples for PostgreSQL, MySQL, and SQLite
   - Uncomment and modify the appropriate commands for your database system

## Analysis Overview

The `nba_stats_analysis.sql` file contains queries for:

1. **Basic Data Exploration**
   - Player counts, team counts, position distribution
   - Summary statistics for key metrics
   - Distribution of player ages and minutes played

2. **Top Performers Analysis**
   - Top scorers, rebounders, assist leaders, etc.
   - Best shooters in different categories

3. **Player Efficiency Metrics**
   - Calculation of Player Efficiency Rating (PER)
   - True Shooting Percentage (TS%)
   - Box Plus/Minus (BPM)

4. **Position-Based Analysis**
   - Average statistics by position
   - Comparative analysis of positions

5. **Team Analysis**
   - Team performance in different statistical categories
   - Identifying top teams in various metrics

6. **Age Analysis**
   - Performance metrics by player age

7. **Advanced Statistical Analysis**
   - Correlation approximation between different metrics

8. **Combined Player Rating**
   - Creation of a comprehensive player rating using multiple metrics

## Usage

1. Set up your database and load the data using `load_nba_data.sql`
2. Execute the queries in `nba_stats_analysis.sql` one by one to analyze the data
3. Modify the queries as needed for your specific analysis requirements

## Notes

- The SQL queries are designed to be educational and may need to be modified for specific database systems
- Some advanced statistical concepts (like correlation) are approximated in SQL
- The queries assume the data is loaded into a table named `nba_player_stats` 