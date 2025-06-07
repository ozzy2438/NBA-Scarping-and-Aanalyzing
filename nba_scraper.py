#!/usr/bin/env python3
"""
NBA Player Performance Scraper
------------------------------
This script scrapes NBA player performance data from Basketball-Reference.com
for NBA seasons. It respects the site's rate limit of 20 requests per minute.

Usage:
    python3 nba_scraper.py [season_end_year] [stat_type]
    python3 nba_scraper.py --multi --start START_YEAR --end END_YEAR [stat_type]

Arguments:
    season_end_year: The ending year of the NBA season (default: 2024 for 2023-24 season)
    stat_type: The type of statistics to scrape (default: per_game)
               Options: per_game, totals, per_36min, per_100poss, advanced
    --multi: Flag to activate multi-season scraping mode
    --start: Starting season end year (inclusive) for multi-season mode
    --end: Ending season end year (inclusive) for multi-season mode

Examples:
    python3 nba_scraper.py                    # Scrapes 2023-24 per game stats
    python3 nba_scraper.py 2023               # Scrapes 2022-23 per game stats
    python3 nba_scraper.py 2025               # Scrapes 2024-25 per game stats
    python3 nba_scraper.py 2024 totals        # Scrapes 2023-24 total stats
    python3 nba_scraper.py 2024 advanced      # Scrapes 2023-24 advanced stats
    
    # Multi-season mode examples
    python3 nba_scraper.py --multi --start 2022 --end 2025             # Scrapes per game stats for 2021-22 through 2024-25 seasons
    python3 nba_scraper.py --multi --start 2022 --end 2025 advanced    # Scrapes advanced stats for 2021-22 through 2024-25 seasons

Output:
    Creates a CSV file with NBA player statistics for the specified season(s) and stat type.
"""

import os
import ssl
# Fix SSL certificate issue
os.environ['SSL_CERT_FILE'] = '/opt/homebrew/etc/openssl@3/cert.pem'
os.environ['SSL_CERT_DIR'] = '/opt/homebrew/etc/openssl@3/certs'

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import sys
import argparse
import random

def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Scrape NBA player statistics from Basketball-Reference.com')
    
    # Create a mutually exclusive group for single season vs multi-season mode
    group = parser.add_mutually_exclusive_group()
    
    # Single season mode arguments
    group.add_argument('season_end_year', nargs='?', type=int, default=2024,
                      help='The ending year of the NBA season (default: 2024 for 2023-24 season)')
    
    # Multi-season mode arguments
    group.add_argument('--multi', action='store_true', help='Flag to activate multi-season scraping mode')
    
    # Common arguments
    parser.add_argument('stat_type', nargs='?', type=str, default='per_game',
                        choices=['per_game', 'totals', 'per_36min', 'per_100poss', 'advanced'],
                        help='The type of statistics to scrape (default: per_game)')
    
    # These are only used in multi-season mode, but we need to define them here
    parser.add_argument('--start', type=int, dest='start_year',
                       help='Starting season end year (inclusive) for multi-season mode')
    parser.add_argument('--end', type=int, dest='end_year',
                       help='Ending season end year (inclusive) for multi-season mode')
    
    return parser.parse_args()

def get_stat_url(season_end_year, stat_type):
    """
    Generate the URL for the specified season and stat type.
    
    Args:
        season_end_year (int): The ending year of the NBA season.
        stat_type (str): The type of statistics to scrape.
    
    Returns:
        str: The URL for the specified season and stat type.
    """
    # Map stat_type to the corresponding URL segment
    stat_type_map = {
        'per_game': 'per_game',
        'totals': 'totals',
        'per_36min': 'per_minute',
        'per_100poss': 'per_poss',
        'advanced': 'advanced'
    }
    
    url_segment = stat_type_map.get(stat_type, 'per_game')
    return f"https://www.basketball-reference.com/leagues/NBA_{season_end_year}_{url_segment}.html"

def scrape_nba_stats(season_end_year=2022, stat_type='per_game'):
    """
    Scrape NBA player statistics from Basketball-Reference.com.
    
    Args:
        season_end_year (int): The ending year of the NBA season.
        stat_type (str): The type of statistics to scrape.
    
    Returns:
        DataFrame: A pandas DataFrame containing the player statistics.
    """
    print(f"Starting: Retrieving {season_end_year-1}-{str(season_end_year)[-2:]} season {stat_type} statistics...")
    
    # Get the URL for the specified season and stat type
    url = get_stat_url(season_end_year, stat_type)
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.basketball-reference.com/',
        'Connection': 'keep-alive',
    }
    
    try:
        # Implement rate limiting - random delay between 1-3 seconds
        # This ensures we stay well below the 20 requests per minute limit
        delay = 1 + 2 * random.random()
        print(f"Rate limiting: Waiting {delay:.2f} seconds...")
        time.sleep(delay)
        
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f"Connection successful: {url}")
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table with player statistics
            table_id = f"{stat_type.replace('per_36min', 'per_minute').replace('per_100poss', 'per_poss')}_stats"
            table = soup.find('table', {'id': table_id})
            
            if table:
                # Extract table headers
                headers = []
                header_row = table.find('thead').find_all('th')
                for th in header_row:
                    # Get the column name from the th element
                    col_name = th.get_text().strip()
                    if col_name:
                        headers.append(col_name)
                
                # Extract table rows
                rows = []
                tbody = table.find('tbody')
                player_rows = tbody.find_all('tr', class_=lambda x: x != 'thead')
                
                for row in player_rows:
                    # Skip header rows that might be interspersed in the tbody
                    if 'class' in row.attrs and 'thead' in row.attrs['class']:
                        continue
                    
                    # Extract data from each cell
                    cells = row.find_all(['th', 'td'])
                    player_data = []
                    
                    for cell in cells:
                        # Get the text content of the cell
                        value = cell.get_text().strip()
                        player_data.append(value)
                    
                    # Only add rows that have data
                    if player_data and len(player_data) > 1:
                        rows.append(player_data)
                
                # Create a DataFrame
                df = pd.DataFrame(rows, columns=headers)
                print(f"Total {len(df)} player data retrieved.")
                return df
            else:
                print(f"Error: Statistics table not found. Table ID: {table_id}")
                return None
        else:
            print(f"Error: Page could not be loaded. Status code: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def save_to_csv(df, season_end_year=2022, stat_type='per_game'):
    """
    Save the DataFrame to a CSV file.
    
    Args:
        df (DataFrame): The DataFrame to save.
        season_end_year (int): The ending year of the NBA season.
        stat_type (str): The type of statistics scraped.
    
    Returns:
        str: The filename if successful, None otherwise.
    """
    try:
        # Create filename based on season and stat type
        filename = f"nba_player_stats_{season_end_year-1}_{str(season_end_year)[-2:]}_{stat_type}.csv"
        
        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data successfully saved: {filename}")
        return filename
    except Exception as e:
        print(f"CSV saving error: {str(e)}")
        return None

def display_data_info(df, filename):
    """
    Display information about the scraped data.
    
    Args:
        df (DataFrame): The DataFrame containing the scraped data.
        filename (str): The name of the CSV file.
    """
    print("\nData Summary:")
    print(f"- File: {filename}")
    print(f"- Total number of players: {len(df)}")
    print(f"- Number of columns: {len(df.columns)}")
    
    # Display the first few rows of the DataFrame
    print("\nFirst 5 rows:")
    print(df.head().to_string())
    
    # Display column names
    print("\nColumn names:")
    print(df.columns.tolist())
    
    # Display some basic statistics if numeric columns exist
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        print("\nBasic statistics for numeric columns:")
        print(df[numeric_cols].describe().to_string())

def scrape_multiple_seasons(start_year, end_year, stat_type='per_game'):
    """
    Scrape NBA player statistics for multiple seasons.
    
    Args:
        start_year (int): The starting season end year (inclusive).
        end_year (int): The ending season end year (inclusive).
        stat_type (str): The type of statistics to scrape.
    
    Returns:
        dict: A dictionary mapping season years to filenames of saved data.
    """
    results = {}
    
    for year in range(start_year, end_year + 1):
        print(f"\n{'='*50}")
        print(f"Processing: {year-1}-{str(year)[-2:]} Season")
        print(f"{'='*50}")
        
        # Scrape data for the current season
        df = scrape_nba_stats(year, stat_type)
        
        if df is not None:
            # Save the data to a CSV file
            filename = save_to_csv(df, year, stat_type)
            
            if filename:
                results[year] = filename
                print(f"{year-1}-{str(year)[-2:]} season data successfully saved.")
            else:
                print(f"{year-1}-{str(year)[-2:]} season data could not be saved.")
        else:
            print(f"{year-1}-{str(year)[-2:]} season data could not be retrieved.")
        
        # Add a longer delay between seasons to be extra respectful of the server
        delay = 3 + 2 * random.random()
        print(f"Waiting {delay:.2f} seconds before proceeding to the next season...")
        time.sleep(delay)
    
    return results

def main():
    """
    Main function to execute the scraping process.
    """
    # Parse command line arguments
    args = parse_arguments()
    stat_type = args.stat_type
    
    # Check if running in multi-season mode
    if args.multi:
        if args.start_year and args.end_year:
            start_year = args.start_year
            end_year = args.end_year
            
            # Validate the year range
            if start_year < 1950 or end_year > 2025 or start_year > end_year:
                print("Error: Invalid year range. Start year should be greater than 1950, end year should be less than 2025, and start year should be less than end year.")
                return
            
            print(f"Running in multi-season mode: {start_year} - {end_year}, Statistic type: {stat_type}")
            results = scrape_multiple_seasons(start_year, end_year, stat_type)
            
            print("\nMulti-season process completed:")
            for year, filename in results.items():
                print(f"- {year-1}-{str(year)[-2:]}: {filename}")
        else:
            print("Error: For --multi usage, specify --start and --end parameters.")
            print("Example: python nba_scraper.py --multi --start 2022 --end 2025 [stat_type]")
        return
    
    # Normal single-season mode
    season_end_year = args.season_end_year
    
    # Validate season year
    if season_end_year < 1950 or season_end_year > 2025:
        print("Error: Invalid season year. Enter a year between 1950 and 2025.")
        return
    
    # Scrape NBA player statistics
    df = scrape_nba_stats(season_end_year, stat_type)
    
    if df is not None:
        # Save the data to a CSV file
        filename = save_to_csv(df, season_end_year, stat_type)
        
        if filename:
            # Display information about the scraped data
            display_data_info(df, filename)
            
            print(f"\nProcess completed. {filename} file created.")
    else:
        print("Data retrieval process failed.")

if __name__ == "__main__":
    main()
