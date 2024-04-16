import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans

# Function to read CSV file and return a DataFrame
def read_csv_file(file_path, columns):
    return pd.read_csv(file_path, usecols=columns)

# File paths and column names
covid_file_path = r'C:\Users\utkar\OneDrive\Desktop\Scifor\projects\nasa\covid.csv'
nasa_file_path = r'C:\Users\utkar\OneDrive\Desktop\Scifor\projects\nasa\nasa.csv'

covid_columns = ['Date', 'Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered', 'WHO Region']
nasa_columns = ['name', 'est_diameter_min', 'est_diameter_max', 'orbiting_body', 'relative_velocity']

# Read data from CSV files into DataFrames
covid_df = read_csv_file(covid_file_path, covid_columns)
nasa_df = read_csv_file(nasa_file_path, nasa_columns)

# Advanced analysis and visualization for COVID-19 data
covid_df['Date'] = pd.to_datetime(covid_df['Date'])
covid_over_time = covid_df.groupby('Date')['Confirmed'].sum().reset_index()
covid_over_time = covid_over_time.set_index('Date')
plt.figure(figsize=(12, 6))
covid_over_time.plot()
plt.title('COVID-19 Confirmed Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Confirmed Cases')
plt.grid(True)
plt.show()

# Advanced analysis and visualization for NASA asteroid data
asteroid_data = nasa_df[['est_diameter_max', 'est_diameter_min', 'relative_velocity']].dropna()
X = asteroid_data.values
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
nasa_df['cluster'] = kmeans.labels_

plt.figure(figsize=(10, 6))
sns.scatterplot(x='est_diameter_max', y='est_diameter_min', hue='cluster', data=nasa_df, palette='viridis')
plt.title('K-means Clustering of Asteroids by Diameter')
plt.xlabel('Maximum Estimated Diameter (meters)')
plt.ylabel('Minimum Estimated Diameter (meters)')
plt.show()
