import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load CSV data
df = pd.read_csv("influencer_marketing_sample_dataset.csv")  
print("Data Preview:")
print(df.head())

# Step 2: Basic Statistics
print("\nBasic Statistics:")
print("Total Revenue Generated:", df['Revenue_Generated'].sum())
print("Average Engagement Rate:", df['Engagement_Rate'].mean())
print("Average Campaign Cost:", df['Campaign_Cost'].mean())
print("Max Followers Count:", df['Follower_Count'].max())
print("Min Followers Count:", df['Follower_Count'].min())

# Step 3: Visualizations

# 1️⃣ Histogram – Followers Count
plt.figure(figsize=(8,5))
plt.hist(df['Follower_Count'], bins=5, color='red', edgecolor='black')
plt.xlabel("Followers Count")
plt.ylabel("Frequency")
plt.title("Followers Count Distribution")
plt.show()

# 2️⃣ Scatter – Engagement Rate vs Revenue
plt.figure(figsize=(8,5))
plt.scatter(df['Engagement_Rate'], df['Revenue_Generated'], color='green')
plt.xlabel("Engagement Rate (%)")
plt.ylabel("Revenue Generated")
plt.title("Engagement Rate vs Revenue Generated")
plt.show()

# 3️⃣ Pie Chart – Platform Distribution
plt.figure(figsize=(6,6))
platform_counts = df['Influencer_Platform'].value_counts()
plt.pie(platform_counts, labels=platform_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Platform Distribution")
plt.show()

# 4️⃣ Bar Chart – Top 5 Influencers by Revenue
top_influencers = df.sort_values(by='Revenue_Generated', ascending=False).head(5)
plt.figure(figsize=(8,5))
plt.bar(top_influencers['Influencer_Name'], top_influencers['Revenue_Generated'], color='orange')
plt.xlabel("Influencer Name")
plt.ylabel("Revenue Generated")
plt.title("Top 5 Influencers by Revenue")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

