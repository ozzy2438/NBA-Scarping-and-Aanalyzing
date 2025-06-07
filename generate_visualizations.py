#!/usr/bin/env python3
"""
NBA Statistics Visualization Generator
Generates professional visualizations for portfolio presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set style for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data():
    """Load NBA player statistics data"""
    return pd.read_csv('data/nba_player_stats_2023_24_per_game.csv')

def create_top_scorers_chart(df):
    """Create top 15 scorers visualization"""
    plt.figure(figsize=(12, 8))
    top_scorers = df.nlargest(15, 'PTS')
    
    bars = plt.bar(range(len(top_scorers)), top_scorers['PTS'], 
                   color=sns.color_palette("viridis", len(top_scorers)))
    
    plt.title('Top 15 NBA Scorers (2023-24 Season)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Players', fontsize=12, fontweight='bold')
    plt.ylabel('Points Per Game', fontsize=12, fontweight='bold')
    plt.xticks(range(len(top_scorers)), top_scorers['Player'], rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('images/top_scorers.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_efficiency_scatter(df):
    """Create scoring efficiency scatter plot"""
    plt.figure(figsize=(12, 8))
    
    # Filter players with significant playing time
    qualified_players = df[df['MP'] >= 20]
    
    scatter = plt.scatter(qualified_players['FGA'], qualified_players['PTS'], 
                         c=qualified_players['FG%'], cmap='RdYlGn', 
                         s=60, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    plt.colorbar(scatter, label='Field Goal Percentage')
    plt.title('NBA Player Scoring Efficiency (2023-24 Season)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Field Goal Attempts Per Game', fontsize=12, fontweight='bold')
    plt.ylabel('Points Per Game', fontsize=12, fontweight='bold')
    
    # Add trend line
    z = np.polyfit(qualified_players['FGA'], qualified_players['PTS'], 1)
    p = np.poly1d(z)
    plt.plot(qualified_players['FGA'], p(qualified_players['FGA']), "r--", alpha=0.8, linewidth=2)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('images/scoring_efficiency.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_team_performance_heatmap(df):
    """Create team performance heatmap"""
    plt.figure(figsize=(14, 10))
    
    # Group by team and calculate averages
    team_stats = df.groupby('Tm').agg({
        'PTS': 'mean',
        'AST': 'mean', 
        'TRB': 'mean',
        'STL': 'mean',
        'BLK': 'mean',
        'FG%': 'mean',
        '3P%': 'mean',
        'FT%': 'mean'
    }).round(2)
    
    # Remove 'TOT' if present (players who played for multiple teams)
    if 'TOT' in team_stats.index:
        team_stats = team_stats.drop('TOT')
    
    # Normalize data for better heatmap visualization
    team_stats_norm = (team_stats - team_stats.min()) / (team_stats.max() - team_stats.min())
    
    sns.heatmap(team_stats_norm.T, annot=team_stats.T, fmt='.2f', 
                cmap='RdYlGn', center=0.5, square=True, cbar_kws={'label': 'Performance Level'})
    
    plt.title('NBA Team Performance Comparison (2023-24 Season)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Teams', fontsize=12, fontweight='bold')
    plt.ylabel('Statistics', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('images/team_performance_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_position_analysis(df):
    """Create position-based analysis"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Points by position
    sns.boxplot(data=df, x='Pos', y='PTS', ax=ax1)
    ax1.set_title('Points Per Game by Position', fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    # Rebounds by position
    sns.boxplot(data=df, x='Pos', y='TRB', ax=ax2)
    ax2.set_title('Rebounds Per Game by Position', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # Assists by position
    sns.boxplot(data=df, x='Pos', y='AST', ax=ax3)
    ax3.set_title('Assists Per Game by Position', fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    
    # Field Goal Percentage by position
    sns.boxplot(data=df, x='Pos', y='FG%', ax=ax4)
    ax4.set_title('Field Goal Percentage by Position', fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.suptitle('NBA Player Performance Analysis by Position (2023-24 Season)', 
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('images/position_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_correlation_matrix(df):
    """Create correlation matrix of key statistics"""
    plt.figure(figsize=(12, 10))
    
    # Select key numeric columns
    numeric_cols = ['PTS', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'FG%', '3P%', 'FT%', 'MP']
    correlation_matrix = df[numeric_cols].corr()
    
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                center=0, square=True, cbar_kws={'label': 'Correlation Coefficient'})
    
    plt.title('NBA Statistics Correlation Matrix (2023-24 Season)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('images/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_age_performance_analysis(df):
    """Create age vs performance analysis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Age vs Points
    ax1.scatter(df['Age'], df['PTS'], alpha=0.6, s=50)
    z1 = np.polyfit(df['Age'], df['PTS'], 1)
    p1 = np.poly1d(z1)
    ax1.plot(df['Age'], p1(df['Age']), "r--", alpha=0.8, linewidth=2)
    ax1.set_xlabel('Age', fontweight='bold')
    ax1.set_ylabel('Points Per Game', fontweight='bold')
    ax1.set_title('Age vs Scoring Performance', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Age distribution
    ax2.hist(df['Age'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.axvline(df['Age'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Mean Age: {df["Age"].mean():.1f}')
    ax2.set_xlabel('Age', fontweight='bold')
    ax2.set_ylabel('Number of Players', fontweight='bold')
    ax2.set_title('NBA Player Age Distribution', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('NBA Player Age Analysis (2023-24 Season)', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('images/age_performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all visualizations"""
    print("Loading NBA data...")
    df = load_data()
    
    print("Generating visualizations...")
    create_top_scorers_chart(df)
    print("✓ Top scorers chart created")
    
    create_efficiency_scatter(df)
    print("✓ Scoring efficiency scatter plot created")
    
    create_team_performance_heatmap(df)
    print("✓ Team performance heatmap created")
    
    create_position_analysis(df)
    print("✓ Position analysis created")
    
    create_correlation_matrix(df)
    print("✓ Correlation matrix created")
    
    create_age_performance_analysis(df)
    print("✓ Age performance analysis created")
    
    print("\n🎉 All visualizations completed!")
    print("Generated files in 'images/' directory:")
    print("- top_scorers.png")
    print("- scoring_efficiency.png")
    print("- team_performance_heatmap.png")
    print("- position_analysis.png")
    print("- correlation_matrix.png")
    print("- age_performance_analysis.png")

if __name__ == "__main__":
    # Create images directory if it doesn't exist
    import os
    os.makedirs('images', exist_ok=True)
    main()