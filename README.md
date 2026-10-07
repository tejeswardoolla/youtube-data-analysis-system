# YouTube Data Analysis System

## 1. Project Overview
The YouTube Data Analysis System is a comprehensive data analysis pipeline and interactive dashboard. It analyzes the YouTube Trending Videos dataset (India) to extract meaningful insights about video engagement, category trends, channel performance, and publishing patterns. The project consists of a Python/Pandas analysis pipeline and a React/Vite frontend dashboard.

## 2. Problem Statement
Analyzing raw, unstructured YouTube trending data using traditional spreadsheets is inefficient and prone to calculation errors. Content creators and analysts need an automated way to clean video records, calculate engagement metrics, and visualize performance trends across categories, channels, and publishing times to make data-driven decisions.

## 3. Objectives
- To analyze YouTube trending video data.
- To calculate engagement and engagement rates.
- To analyze publishing years, months, days, and hours.
- To analyze channel and category information.
- To compare videos across different categories.
- To identify views and engagement trends.
- To analyze relationships between views, likes, and comments.
- To represent the results using different visualization techniques.
- To develop an interactive React/Vite dashboard.
- To provide meaningful insights that support content creators.

## 4. Dataset
The original dataset used in this project is `INvideos.csv` (YouTube Trending Videos dataset for India). It contains video, channel, category, views, likes, dislikes, comments, trending date, and publish time information for videos that appeared on the YouTube trending page.

## 5. Project Workflow
```text
INvideos.csv
↓
Data Exploration
↓
Data Preprocessing
↓
Feature Engineering
↓
EDA
↓
Matplotlib Visualization
↓
youtube_dashboard_data.csv
↓
React/Vite Dashboard
```

## 6. Data Preprocessing
The preprocessing was performed using Pandas in Python:
1. Load `INvideos.csv` using Pandas.
2. Explore the dataset using `head()`, `tail()`, `shape`, `columns`, `info()`, and `describe()`.
3. Check missing values using `df.isnull().sum()`.
4. Check duplicate rows using `df.duplicated().sum()`.
5. Check repeated video IDs and invalid values (note: videos can legitimately appear multiple times as they remain trending across different dates).
6. Remove exact duplicate rows where appropriate.
7. Convert `trending_date` into the correct datetime format.
8. Convert `publish_time` into datetime format.
9. Select the useful columns into `youtube_df`.

## 7. Feature Engineering
The following derived features were created:
- `publish_year`
- `publish_month`
- `publish_day`
- `publish_hour`
- `engagement`
- `engagement_rate`

Calculations:
- **Engagement** = Likes + Comment Count
- **Engagement Rate** = (Engagement / Views) × 100

## 8. Exploratory Data Analysis
We performed Exploratory Data Analysis (EDA) using Pandas operations like `value_counts()`, `sort_values()`, `groupby()`, `mean()`, and `sum()`. The analyses included:
- Trending channels
- Top videos by views
- Top videos by likes
- Top videos by comments
- Category-wise video counts
- Category-wise views
- Channel performance
- Videos published by month
- Videos published by day
- Videos published by hour
- Views vs likes
- Views vs comments
- Engagement analysis
- Statistical summaries

## 9. Visualizations
The Matplotlib visualizations created during the analysis phase include:
1. Top 10 Channels by Trending Videos
2. Top Videos by Views
3. Category Counts
4. Category Views
5. Videos Published by Month
6. Videos Published by Day
7. Videos Published by Hour
8. Views vs Likes
9. Views vs Comments

## 10. Processed Dataset
The final processed dataset used for the dashboard is `youtube_dashboard_data.csv`.
- **Rows:** 33,089
- **Columns:** 16

Columns:
`video_id`, `trending_date`, `title`, `channel_title`, `category_id`, `publish_time`, `views`, `likes`, `dislikes`, `comment_count`, `publish_year`, `publish_month`, `publish_day`, `publish_hour`, `engagement`, `engagement_rate`

## 11. Interactive Dashboard
The frontend is a React + Vite interactive dashboard that presents the analyzed data via dynamic charts.
**Sections:**
- Overview
- Trending Videos
- Channels
- Engagement
- Publishing Insights

**Filters:**
- Year
- Channel
- Category
- Day

**KPI Cards:**
- Total Videos
- Total Views
- Total Likes
- Average Engagement Rate

## 12. Key Dataset Observations
- T-Series had the highest total channel views in the analyzed dataset.
- Amit Bhadana had the highest likes among the analyzed channel-level results.
- YouTube Rewind 2017 was the most viewed/viral record in the analyzed data.
- Friday had the highest publishing frequency in the analyzed dataset.
- 2 PM had the highest publishing frequency in the analyzed dataset.

## 13. How to Run

**Running the Python Analysis:**
1. Navigate to the `analysis` folder.
2. Run the script: `python youtube_data_analysis.py`

**Running the Dashboard:**
1. Navigate to the `dashboard` folder.
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`
4. Open the provided localhost link in your browser.

## 14. Project Structure
```text
YouTube-Data-Analysis/
│
├── README.md
│
├── data/
│   └── raw/
│       └── INvideos.csv
│
├── analysis/
│   └── youtube_data_analysis.py
│
└── dashboard/
    ├── package.json
    ├── src/
    ├── public/
    │   └── youtube_dashboard_data.csv
    └── ... (other React/Vite configuration files)
```

## 15. Conclusion
The YouTube Data Analysis System successfully transforms raw, unstructured YouTube trending data into clean, analyzed information. By combining robust Python data processing with a rich, interactive React dashboard, the project empowers users to seamlessly uncover deep insights into video performance, audience engagement, and publishing patterns.
