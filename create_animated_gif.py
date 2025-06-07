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
    
    ax.text(5, 5.5, '2023-24 Season Statistical Analysis', 
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
    
    # Minutes vs Points
    if 'MP' in df.columns and 'PTS' in df.columns:
        valid_data = df[['MP', 'PTS']].dropna()
        ax3.scatter(valid_data['MP'], valid_data['PTS'], alpha=0.6, s=30)
        ax3.set_title('Minutes vs Points', fontweight='bold', fontsize=12)
        ax3.set_xlabel('Minutes per Game')
        ax3.set_ylabel('Points per Game')
    else:
        ax3.text(0.5, 0.5, 'Minutes/Points\ndata not available', ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Minutes vs Points', fontweight='bold', fontsize=12)
    
    # Dataset stats
    ax4.text(0.5, 0.7, f'Total Players: {len(df)}', fontsize=16, ha='center', va='center', 
             transform=ax4.transAxes, fontweight='bold')
    ax4.text(0.5, 0.5, f'Features: {len(df.columns)}', fontsize=14, ha='center', va='center', 
             transform=ax4.transAxes)
    ax4.text(0.5, 0.3, '2023-24 NBA Season', fontsize=12, ha='center', va='center', 
             transform=ax4.transAxes, style='italic')
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
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Top scorers
    if 'PTS' in df.columns and 'Player' in df.columns:
        top_scorers = df.nlargest(8, 'PTS')
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
    if 'TRB' in df.columns and 'Player' in df.columns:
        top_rebounders = df.nlargest(8, 'TRB')
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
    if 'AST' in df.columns and 'Player' in df.columns:
        top_assisters = df.nlargest(8, 'AST')
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
    if all(col in df.columns for col in ['FGA', 'PTS', 'FG%', 'MP']):
        qualified = df[df['MP'] >= 15].dropna(subset=['FGA', 'PTS', 'FG%'])
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
    
    plt.suptitle('🌟 2023-24 Season Top Performers', fontsize=16, fontweight='bold')
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
        "📊 Comprehensive analysis of NBA player statistics",
        "🏆 Advanced performance metrics and efficiency ratings",
        "📈 Statistical correlations and relationship analysis",
        "🎯 Position-based performance breakdowns",
        "📍 Team comparison and ranking analysis",
        "🏀 Professional data science portfolio project"
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
    print("Loading NBA data...")
    df = pd.read_csv('data/nba_player_stats_2023_24_per_game.csv')
    
    # Convert numeric columns safely
    numeric_cols = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 
                    'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    percentage_cols = ['FG%', '3P%', '2P%', 'eFG%', 'FT%']
    
    for col in numeric_cols + percentage_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"Data loaded: {len(df)} players, {len(df.columns)} features")
    
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
        print("🎬 Ready for portfolio presentation!")
        
    except Exception as e:
        print(f"Error creating GIF: {e}")
        print("Please check your data file and try again.")

if __name__ == "__main__":
    create_animated_gif()