import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Load INvideos.csv using Pandas
dataset_path = os.path.join("..", "data", "raw", "INvideos.csv")
df = pd.read_csv(dataset_path)

# 2. Explore the dataset
print(df.head())
print(df.tail())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe())

# 3. Check missing values
print(df.isnull().sum())

# 4. Check duplicate rows
print(df.duplicated().sum())

# 5. Check repeated video IDs (videos can legitimately appear multiple times as they remain trending)
print(df['video_id'].value_counts())

# 6. Remove exact duplicate rows
df = df.drop_duplicates()

# 7. Convert trending_date into correct datetime format
# Format in INvideos is often yy.dd.mm
df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m', errors='coerce')

# 8. Convert publish_time into datetime format
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# 9. Select useful columns
cols_to_keep = ['video_id', 'trending_date', 'title', 'channel_title', 'category_id', 'publish_time', 'views', 'likes', 'dislikes', 'comment_count']
youtube_df = df[cols_to_keep].copy()

# 10. Create derived features
youtube_df['publish_year'] = youtube_df['publish_time'].dt.year
youtube_df['publish_month'] = youtube_df['publish_time'].dt.month
youtube_df['publish_day'] = youtube_df['publish_time'].dt.day_name()
youtube_df['publish_hour'] = youtube_df['publish_time'].dt.hour

# 11. Create engagement feature
youtube_df['engagement'] = youtube_df['likes'] + youtube_df['comment_count']

# 12. Create engagement_rate feature
youtube_df['engagement_rate'] = (youtube_df['engagement'] / youtube_df['views']) * 100

# Perform EDA
# Top 10 Channels by Trending Videos
top_channels = youtube_df['channel_title'].value_counts().head(10)
print("Top 10 Channels:")
print(top_channels)

# Export processed dataset for the React Dashboard
output_path = os.path.join("..", "dashboard", "public", "youtube_dashboard_data.csv")
# youtube_df.to_csv(output_path, index=False)
print(f"Dataset fully processed and exported to {output_path}")
