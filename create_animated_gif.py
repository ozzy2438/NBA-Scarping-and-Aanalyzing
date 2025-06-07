#!/usr/bin/env python3
"""
NBA Analysis Animated GIF Generator
Creates an animated GIF showcasing key visualizations for portfolio presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
import io
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_title_frame():
    """Create an opening title frame"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Remove axes
    ax.axis('off')
    
    # Add title and subtitle
    ax.text(5, 7, '🏀 NBA Analytics Dashboard', 
            fontsize=28, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="orange", alpha=0.8))
    
    ax.text(5, 5.5, '2015-2024 Seasons Statistical Analysis', 
            fontsize=18, ha='center', va='center')
    
    ax.text(5, 4.5, 'Data Science Portfolio Project', 
            fontsize=14, ha='center', va='center', style='italic')
    
    ax.text(5, 3, 'By Osman Orka', 
            fontsize=16, fontweight='bold', ha='center', va='center')
    
    # Add some basketball emojis around
    positions = [(1, 8), (9, 8), (1, 2), (9, 2), (2, 5), (8, 5)]
    for x, y in positions:
        ax.text(x, y, '🏀', fontsize=20, ha='center', va='center')
    
    plt.tight_layout()
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    return img

def create_data_overview_frame(df):
    """Create data overview frame"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Players by position - handle missing values
    if 'Pos' in df.columns:
        position_counts = df['Pos'].value_counts().head(8)  # Top 8 positions
        ax1.pie(position_counts.values, labels=position_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Players by Position', fontweight='bold', fontsize=12)
    else:
        ax1.text(0.5, 0.5, 'Position data\nnot available', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Players by Position', fontweight='bold', fontsize=12)
    
    # Age distribution
    if 'Age' in df.columns and df['Age'].notna().sum() > 0:
        ages = df['Age'].dropna()
        ax2.hist(ages, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(ages.mean(), color='red', linestyle='--', linewidth=2)
        ax2.set_title('Age Distribution', fontweight='bold', fontsize=12)
        ax2.set_xlabel('Age')
        ax2.set_ylabel('Count')
    else:
        ax2.text(0.5, 0.5, 'Age data\nnot available', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('Age Distribution', fontweight='bold', fontsize=12)
    
    # Season breakdown
    if 'Season' in df.columns:
        season_counts = df['Season'].value_counts().sort_index()
        ax3.bar(range(len(season_counts)), season_counts.values, color='purple', alpha=0.7)
        ax3.set_xticks(range(len(season_counts)))
        ax3.set_xticklabels(season_counts.index, rotation=45, fontsize=8)
        ax3.set_title('Records by Season', fontweight='bold', fontsize=12)
        ax3.set_ylabel('Number of Records')
    else:
        # Minutes vs Points as fallback
        if 'MP' in df.columns and 'PTS' in df.columns:
            valid_data = df[['MP', 'PTS']].dropna()
            ax3.scatter(valid_data['MP'], valid_data['PTS'], alpha=0.6, s=30)
            ax3.set_title('Minutes vs Points', fontweight='bold', fontsize=12)
            ax3.set_xlabel('Minutes per Game')
            ax3.set_ylabel('Points per Game')
        else:
            ax3.text(0.5, 0.5, 'Season data\nnot available', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Season Breakdown', fontweight='bold', fontsize=12)
    
    # Dataset stats
    ax4.text(0.5, 0.8, f'Total Records: {len(df)}', fontsize=16, ha='center', va='center', 
             transform=ax4.transAxes, fontweight='bold')
    
    if 'Season' in df.columns:
        seasons = df['Season'].nunique()
        ax4.text(0.5, 0.6, f'Seasons: {seasons}', fontsize=14, ha='center', va='center', 
                transform=ax4.transAxes)
        ax4.text(0.5, 0.4, f'Years: 2015-2024', fontsize=14, ha='center', va='center', 
                transform=ax4.transAxes)
    
    ax4.text(0.5, 0.2, f'Features: {len(df.columns)}', fontsize=14, ha='center', va='center', 
             transform=ax4.transAxes)
    ax4.set_title('Dataset Overview', fontweight='bold', fontsize=12)
    ax4.axis('off')
    
    plt.suptitle('📊 Dataset Overview', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    return img

def create_top_performers_frame(df):
    """Create top performers visualization"""
    # Get latest season
    if 'Season' in df.columns:
        latest_season = sorted(df['Season'].unique())[-1]
        df_latest = df[df['Season'] == latest_season]
        season_title = f"{latest_season} Season"
    else:
        df_latest = df
        season_title = "Latest Season"
        
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Top scorers
    if 'PTS' in df_latest.columns and 'Player' in df_latest.columns:
        top_scorers = df_latest.nlargest(8, 'PTS')
        bars1 = ax1.bar(range(len(top_scorers)), top_scorers['PTS'], color='red', alpha=0.7)
        ax1.set_title('🏆 Top Scorers', fontweight='bold', fontsize=12)
        ax1.set_xticks(range(len(top_scorers)))
        # Safely handle player names
        labels = []
        for name in top_scorers['Player']:
            if pd.notna(name):
                labels.append(str(name).split()[-1] if ' ' in str(name) else str(name)[:8])
            else:
                labels.append('Unknown')
        ax1.set_xticklabels(labels, rotation=45, fontsize=8)
        ax1.set_ylabel('Points per Game')
    else:
        ax1.text(0.5, 0.5, 'Scoring data\nnot available', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('🏆 Top Scorers', fontweight='bold', fontsize=12)
    
    # Top rebounders
    if 'TRB' in df_latest.columns and 'Player' in df_latest.columns:
        top_rebounders = df_latest.nlargest(8, 'TRB')
        bars2 = ax2.bar(range(len(top_rebounders)), top_rebounders['TRB'], color='green', alpha=0.7)
        ax2.set_title('🏀 Top Rebounders', fontweight='bold', fontsize=12)
        ax2.set_xticks(range(len(top_rebounders)))
        labels = []
        for name in top_rebounders['Player']:
            if pd.notna(name):
                labels.append(str(name).split()[-1] if ' ' in str(name) else str(name)[:8])
            else:
                labels.append('Unknown')
        ax2.set_xticklabels(labels, rotation=45, fontsize=8)
        ax2.set_ylabel('Rebounds per Game')
    else:
        ax2.text(0.5, 0.5, 'Rebounding data\nnot available', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('🏀 Top Rebounders', fontweight='bold', fontsize=12)
    
    # Top assist leaders
    if 'AST' in df_latest.columns and 'Player' in df_latest.columns:
        top_assisters = df_latest.nlargest(8, 'AST')
        bars3 = ax3.bar(range(len(top_assisters)), top_assisters['AST'], color='blue', alpha=0.7)
        ax3.set_title('🎯 Top Assist Leaders', fontweight='bold', fontsize=12)
        ax3.set_xticks(range(len(top_assisters)))
        labels = []
        for name in top_assisters['Player']:
            if pd.notna(name):
                labels.append(str(name).split()[-1] if ' ' in str(name) else str(name)[:8])
            else:
                labels.append('Unknown')
        ax3.set_xticklabels(labels, rotation=45, fontsize=8)
        ax3.set_ylabel('Assists per Game')
    else:
        ax3.text(0.5, 0.5, 'Assists data\nnot available', ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('🎯 Top Assist Leaders', fontweight='bold', fontsize=12)
    
    # Shooting efficiency
    if all(col in df_latest.columns for col in ['FGA', 'PTS', 'FG%', 'MP']):
        qualified = df_latest[df_latest['MP'] >= 15].dropna(subset=['FGA', 'PTS', 'FG%'])
        if len(qualified) > 0:
            scatter = ax4.scatter(qualified['FGA'], qualified['PTS'], c=qualified['FG%'], 
                                 cmap='viridis', alpha=0.7, s=40)
            ax4.set_title('📈 Scoring Efficiency', fontweight='bold', fontsize=12)
            ax4.set_xlabel('Field Goal Attempts')
            ax4.set_ylabel('Points per Game')
            plt.colorbar(scatter, ax=ax4, label='FG%')
        else:
            ax4.text(0.5, 0.5, 'Insufficient data\nfor efficiency plot', ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('📈 Scoring Efficiency', fontweight='bold', fontsize=12)
    else:
        ax4.text(0.5, 0.5, 'Efficiency data\nnot available', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('📈 Scoring Efficiency', fontweight='bold', fontsize=12)
    
    plt.suptitle(f'🌟 {season_title} Top Performers', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    return img

def create_position_evolution_frame(df):
    """Create position evolution visualization"""
    if 'Season' not in df.columns or 'Pos' not in df.columns:
        # Create placeholder if data isn't available
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Position evolution data not available', 
                ha='center', va='center', transform=ax.transAxes, fontsize=16)
        ax.axis('off')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()
        return img
    
    # Count positions by season
    position_data = df.groupby(['Season', 'Pos']).size().reset_index(name='Count')
    
    # Create a pivot table
    position_pivot = position_data.pivot(index='Season', columns='Pos', values='Count').fillna(0)
    
    # Calculate percentages
    position_pct = position_pivot.div(position_pivot.sum(axis=1), axis=0) * 100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
    
    # Raw counts
    position_pivot.plot(kind='bar', stacked=True, ax=ax1, colormap='viridis')
    ax1.set_title('Number of Players by Position', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Season', fontsize=10)
    ax1.set_ylabel('Number of Players', fontsize=10)
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(title='Position', fontsize=8, loc='upper right')
    
    # Percentages
    position_pct.plot(kind='bar', stacked=True, ax=ax2, colormap='viridis')
    ax2.set_title('Position Distribution (%)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Season', fontsize=10)
    ax2.set_ylabel('Percentage', fontsize=10)
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(title='Position', fontsize=8, loc='upper right')
    
    plt.suptitle('📊 Evolution of NBA Position Distribution (2015-2024)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    return img

def create_scoring_trends_frame(df):
    """Create scoring trends visualization"""
    if 'Season' not in df.columns:
        # Create placeholder if data isn't available
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Scoring trends data not available', 
                ha='center', va='center', transform=ax.transAxes, fontsize=16)
        ax.axis('off')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()
        return img
    
    # Group by season and calculate averages
    metrics = ['PTS', '3PA', 'AST', 'FG%']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if not available_metrics:
        # Create placeholder if no metrics are available
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Scoring metrics not available', 
                ha='center', va='center', transform=ax.transAxes, fontsize=16)
        ax.axis('off')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img = Image.open(buf)
        plt.close()
        return img
    
    season_stats = df.groupby('Season')[available_metrics].mean().reset_index()
    season_stats = season_stats.sort_values('Season')
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    
    titles = {
        'PTS': 'Points Per Game',
        '3PA': '3-Point Attempts',
        'AST': 'Assists Per Game',
        'FG%': 'Field Goal Percentage'
    }
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, metric in enumerate(available_metrics):
        if i < len(axes):
            ax = axes[i]
            ax.plot(season_stats['Season'], season_stats[metric], marker='o', 
                   linewidth=2, color=colors[i % len(colors)])
            ax.set_title(titles.get(metric, metric), fontsize=12, fontweight='bold')
            ax.set_xlabel('Season', fontsize=10)
            ax.set_ylabel(metric, fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Add value annotations
            for x, y in zip(season_stats['Season'], season_stats[metric]):
                ax.annotate(f'{y:.2f}', (x, y), textcoords="offset points", 
                          xytext=(0,10), ha='center', fontsize=8)
    
    # Hide unused subplots
    for j in range(len(available_metrics), len(axes)):
        axes[j].set_visible(False)
    
    plt.suptitle('📈 NBA Statistical Trends (2015-2024)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    return img

def create_insights_frame():
    """Create key insights summary frame"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9, '🎯 Key Insights & Findings', 
            fontsize=24, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    # Insights
    insights = [
        "📊 10-year analysis of NBA player statistics (2015-2024)",
        "🏆 Evolution of position distributions and player roles",
        "📈 Statistical trends showing the 3-point revolution",
        "🎯 Correlation patterns across different performance metrics",
        "📍 Comparative analysis of efficiency across seasons",
        "🏀 Multi-season performance metrics and visualizations"
    ]
    
    for i, insight in enumerate(insights):
        ax.text(5, 7.5 - i*0.8, insight, 
                fontsize=14, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
    
    # Footer
    ax.text(5, 1, 'Data Science Portfolio | github.com/ozzy2438', 
            fontsize=12, ha='center', va='center', style='italic')
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    return img

def create_animated_gif():
    """Create the animated GIF"""
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    print("Loading NBA data...")
    try:
        # Try loading the multi-season dataset
        df = pd.read_csv('datasets/all_nba_player_stats_2015_2024.csv')
        data_type = "multi-season"
        print(f"Multi-season data loaded: {len(df)} records across {df['Season'].nunique()} seasons")
    except (FileNotFoundError, KeyError):
        try:
            # Fall back to single-season dataset
            df = pd.read_csv('data/nba_player_stats_2023_24_per_game.csv')
            data_type = "single-season"
            print(f"Single-season data loaded: {len(df)} players")
        except FileNotFoundError:
            print("Error: No data file found. Please ensure either multi-season or single-season data exists.")
            return
    
    # Convert numeric columns safely
    numeric_cols = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 
                    'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    percentage_cols = ['FG%', '3P%', '2P%', 'eFG%', 'FT%']
    
    for col in numeric_cols + percentage_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print("Creating animation frames...")
    frames = []
    
    # Create frames
    try:
        frames.append(create_title_frame())
        print("✓ Title frame created")
        
        frames.append(create_data_overview_frame(df))
        print("✓ Data overview frame created")
        
        frames.append(create_top_performers_frame(df))
        print("✓ Top performers frame created")
        
        if data_type == "multi-season":
            frames.append(create_position_evolution_frame(df))
            print("✓ Position evolution frame created")
            
            frames.append(create_scoring_trends_frame(df))
            print("✓ Scoring trends frame created")
        
        frames.append(create_insights_frame())
        print("✓ Insights frame created")
        
        # Create GIF
        print("Generating animated GIF...")
        
        # Resize all frames to the same size
        target_size = (1200, 800)
        resized_frames = []
        for frame in frames:
            resized_frame = frame.resize(target_size, Image.Resampling.LANCZOS)
            resized_frames.append(resized_frame)
        
        # Save as GIF
        resized_frames[0].save(
            'images/nba_analysis_demo.gif',
            save_all=True,
            append_images=resized_frames[1:],
            duration=3000,  # 3 seconds per frame
            loop=0
        )
        
        print("✅ Animated GIF created: images/nba_analysis_demo.gif")
        print("🎬 Ready for GitHub upload and portfolio presentation!")
        
    except Exception as e:
        print(f"Error creating GIF: {e}")
        print("Please check your data file and try again.")

if __name__ == "__main__":
    create_animated_gif() 