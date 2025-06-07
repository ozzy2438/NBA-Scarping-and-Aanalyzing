# 🏀 NBA Player Statistics Analysis (2023-24 Season)

A comprehensive data analysis project examining NBA player performance metrics, statistical relationships, and team comparisons for the 2023-24 season.

## 🎯 Project Overview

This project provides in-depth statistical analysis of NBA player performance using data science techniques including data cleaning, exploratory data analysis, statistical correlation analysis, and advanced visualization. The analysis covers 736 NBA players and reveals key insights about player efficiency, team performance, and positional trends.

## 📊 Key Features

- **Comprehensive Data Analysis**: Analysis of 31 different statistical metrics
- **Advanced Visualizations**: Professional charts and heatmaps showing statistical relationships
- **Player Performance Metrics**: Custom efficiency ratings and advanced statistics
- **Team Comparisons**: Cross-team analysis of performance indicators
- **Position-Based Analysis**: Statistical breakdowns by player position
- **Interactive Jupyter Notebook**: Detailed step-by-step analysis with visualizations

## 🛠️ Technologies Used

- **Python 3.13**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical data visualization
- **Jupyter Notebook**: Interactive analysis environment
- **SQL**: Database queries and analysis
- **Beautiful Soup**: Web scraping capabilities

## 📈 Analysis Highlights

### Dataset Statistics
- **736 total players** analyzed
- **237 qualified players** (≥20 minutes per game, ≥40 games)
- **31 statistical categories** including points, rebounds, assists, shooting percentages
- **Custom metrics** including True Shooting %, Player Efficiency Rating (PER), and combined ratings

### Key Insights Discovered

#### 🏆 Top Performers (2023-24 Season)
- **Leading Scorer**: Comprehensive analysis of top scoring leaders
- **Most Efficient Players**: Advanced efficiency metrics beyond basic statistics
- **Position Excellence**: Identification of best performers by position

#### 📊 Statistical Correlations
- Strong correlation between minutes played and scoring output
- Relationship between age and playing time
- Shooting efficiency vs. attempt volume analysis
- Position-specific performance patterns

#### 🏀 Team Analysis
- Cross-team performance comparisons
- Offensive and defensive statistical leaders
- Team shooting efficiency rankings
- Balanced roster analysis

#### 📍 Position-Based Insights
- **Centers**: Excel in rebounds and blocks
- **Point Guards**: Lead in assists and playmaking
- **Shooting Guards**: High 3-point shooting volume
- **Forwards**: Balanced scoring and rebounding contributions

## 🗂️ Project Structure

```
nba_analysis/
├── data/
│   └── nba_player_stats_2023_24_per_game.csv
├── sql_analysis/
│   ├── load_nba_data.sql
│   └── nba_stats_analysis.sql
├── images/
│   ├── position_distribution.png
│   ├── correlation_matrix.png
│   ├── top_performers.png
│   ├── team_comparison.png
│   └── efficiency_analysis.png
├── nba_scraper.py
├── nba_stats_analysis.ipynb
├── generate_visualizations.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ozzy2438/NBA-Scarping-and-Aanalyzing.git
cd NBA-Scarping-and-Aanalyzing
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Launch Jupyter Notebook**
```bash
jupyter notebook nba_stats_analysis.ipynb
```

## 📊 Data Sources

- **Basketball-Reference.com**: Primary source for player statistics
- **NBA Official Statistics**: Verification and supplementary data
- **Custom Web Scraping**: Automated data collection pipeline

## 🔍 Analysis Methodology

### 1. Data Collection & Cleaning
- Web scraping of current season statistics
- Data validation and type conversion
- Missing value handling and outlier analysis
- Feature engineering for advanced metrics

### 2. Exploratory Data Analysis
- Statistical distribution analysis
- Correlation matrix generation
- Player and team performance ranking
- Position-based statistical breakdowns

### 3. Advanced Analytics
- True Shooting Percentage calculations
- Player Efficiency Rating (PER) computation
- Custom combined rating system
- Win Shares and Box Plus/Minus integration

### 4. Visualization & Insights
- Professional statistical visualizations
- Interactive charts and heatmaps
- Performance comparison dashboards
- Trend analysis and pattern identification

## 📱 Key Visualizations

The analysis includes several professional visualizations:

- **Player Performance Heatmaps**: Correlation analysis of key statistics
- **Team Comparison Charts**: Cross-team performance metrics
- **Position Analysis**: Statistical breakdowns by player position
- **Efficiency Scatter Plots**: Advanced metric relationships
- **Top Performer Rankings**: Comprehensive player rankings

## 🎯 Business Applications

This analysis provides valuable insights for:

- **NBA Teams**: Player evaluation and roster construction
- **Sports Analytics**: Advanced metric development
- **Fantasy Sports**: Player value assessment
- **Sports Media**: Data-driven storytelling
- **Betting Analysis**: Statistical trend identification

## 📊 SQL Analysis

The project includes comprehensive SQL analysis for:
- Database-driven statistical queries
- Complex joins and aggregations
- Performance metric calculations
- Trend analysis over time

## 🔮 Future Enhancements

- **Machine Learning Models**: Predictive analytics for player performance
- **Real-time Data Integration**: Live statistics updates
- **Interactive Dashboard**: Web-based visualization platform
- **Historical Trend Analysis**: Multi-season comparison
- **Advanced Metrics**: Custom efficiency calculations

## 📈 Skills Demonstrated

- **Data Science**: End-to-end data analysis pipeline
- **Python Programming**: Advanced data manipulation and analysis
- **Statistical Analysis**: Correlation analysis and hypothesis testing
- **Data Visualization**: Professional chart creation and design
- **SQL**: Complex database queries and analysis
- **Web Scraping**: Automated data collection
- **Documentation**: Professional project presentation

## 👤 Author

**Osman Orka**
- Data Scientist & Analytics Professional
- Specializing in Sports Analytics and Statistical Modeling
- [GitHub](https://github.com/ozzy2438) | [LinkedIn](https://linkedin.com/in/osmanorka)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Basketball-Reference.com for comprehensive NBA statistics
- NBA for official player and team data
- Python data science community for excellent libraries
- Sports analytics community for methodology inspiration

---

**⭐ If you found this analysis valuable, please star the repository!**

*This project demonstrates advanced data science capabilities including statistical analysis, data visualization, and insight generation from complex sports datasets.* 