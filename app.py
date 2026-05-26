import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Influencer Analytics", layout="wide")

# ---------------------------
# HEADER
# ---------------------------
st.markdown(
    """
    <div style="text-align:center; padding:24px 0;">
      <h1 style="font-size:3rem; margin:0;
          background: linear-gradient(90deg, #dd7000, #d5006f, #4a148c);
          -webkit-background-clip: text; color: transparent;">
         Influencer Marketing Impact Study
      </h1>
      <p style="font-size:1.05rem;">
        Data-driven insights on engagement, revenue, and performance
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.image("https://i.imgur.com/5l9kqB3.jpeg")

st.markdown("""
<style>
.stApp { background-color:#f9f2f0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA (SINGLE SOURCE)
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload CSV (Optional)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Using uploaded dataset ✅")
else:
    df = pd.read_csv("influencer_marketing_sample_dataset.csv")
    st.info("Using default dataset")

# ---------------------------
# MEMORY SAFETY
# ---------------------------
if len(df) > 20000:
    df = df.sample(20000, random_state=42)

# ---------------------------
# FEATURE ENGINEERING
# ---------------------------
df["Revenue_per_Follower"] = df["Revenue_Generated"] / df["Follower_Count"]

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.title("Filters")

platform_filter = st.sidebar.multiselect(
    "Select Platform",
    options=df["Influencer_Platform"].dropna().unique()
)

if len(platform_filter) == 0:
    filtered_df = df.copy()
else:
    filtered_df = df[df["Influencer_Platform"].isin(platform_filter)].copy()

if filtered_df.empty:
    st.warning("No data found for selected filters.")
    st.stop()

# ---------------------------
# KEY METRICS
# ---------------------------
st.markdown("### 📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Influencers", len(filtered_df))
col2.metric("Total Revenue", f"{filtered_df['Revenue_Generated'].sum():,.0f}")
col3.metric("Avg Engagement", f"{filtered_df['Engagement_Rate'].mean():.2f}%")
col4.metric("Avg Revenue/Follower", f"{filtered_df['Revenue_per_Follower'].mean():.4f}")

st.divider()

# ---------------------------
# FULL DATASET
# ---------------------------
st.markdown("### 🧾 Full Dataset")

full_df = filtered_df.reset_index(drop=True).copy()
full_df.insert(0, "S.No", range(1, len(full_df) + 1))

st.dataframe(full_df, use_container_width=True, hide_index=True)

# ---------------------------
# DOWNLOAD BUTTON (NEW)
# ---------------------------
csv = full_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    data=csv,
    file_name="filtered_influencer_data.csv",
    mime="text/csv"
)

st.divider()

# ---------------------------
# TOP INFLUENCERS
# ---------------------------
st.markdown("### 🏆 Top Influencers")

top_df = df.sort_values(by="Follower_Count", ascending=False).head(10).copy()

if "Product_Name" not in top_df.columns:
    top_df["Product_Name"] = "N/A"

st.dataframe(top_df, use_container_width=True)

st.divider()

# ---------------------------
# INSIGHTS (IMPROVED)
# ---------------------------
st.markdown("### 📌 Insights Summary")

best_platform = filtered_df.groupby("Influencer_Platform")["Revenue_Generated"].sum().idxmax()

top_influencer = filtered_df.loc[
    filtered_df["Follower_Count"].idxmax(), "Influencer_Name"
]

best_eng_platform = filtered_df.groupby("Influencer_Platform")["Engagement_Rate"].mean().idxmax()

st.info(f"""
🔥 Best Revenue Platform: {best_platform}  
📈 Highest Engagement Platform: {best_eng_platform}  
⭐ Top Influencer: {top_influencer}  
""")

st.divider()

# ---------------------------
# CORRELATION HEATMAP (NEW)
# ---------------------------
st.markdown("### 📊 Correlation Heatmap")

corr = filtered_df[[
    "Follower_Count",
    "Engagement_Rate",
    "Revenue_Generated",
    "Revenue_per_Follower"
]].corr()

fig, ax = plt.subplots()
cax = ax.imshow(corr)

ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45)
ax.set_yticklabels(corr.columns)

st.pyplot(fig)

st.divider()

# ---------------------------
# GRAPHS
# ---------------------------

st.markdown("### 👥 Followers Distribution")

followers = filtered_df["Follower_Count"].dropna()

if len(followers) > 5000:
    followers = followers.sample(5000, random_state=42)

fig1, ax1 = plt.subplots()
ax1.hist(followers, bins=10)
st.pyplot(fig1)

st.markdown("### 📈 Engagement vs Revenue")

fig2, ax2 = plt.subplots()
ax2.scatter(filtered_df["Engagement_Rate"], filtered_df["Revenue_Generated"])
st.pyplot(fig2)

st.markdown("### 🌍 Platform Distribution")

platform_counts = filtered_df["Influencer_Platform"].value_counts()

fig3, ax3 = plt.subplots()
ax3.pie(platform_counts, labels=platform_counts.index, autopct="%1.1f%%")
st.pyplot(fig3)

st.markdown("### 🏆 Top Revenue Influencers")

top_rev = filtered_df.sort_values(by="Revenue_Generated", ascending=False).head(5)

fig4, ax4 = plt.subplots()
ax4.bar(top_rev["Influencer_Name"], top_rev["Revenue_Generated"])
plt.xticks(rotation=45)
st.pyplot(fig4)

# ---------------------------
# 🏁 CONCLUSION
# ---------------------------
st.markdown("### 🏁 Conclusion")

st.success("""
This project demonstrates how influencer marketing data can be analyzed
to extract meaningful business insights.This dashboard can help marketers choose the right influencers
and optimize campaign performance.
""")

# ---------------------------
# 🧰 TOOLS USED
# ---------------------------
st.markdown("### 🧰 Tools & Technologies Used")

st.info("""
📌 Python (Data Processing)  
📊 Pandas (Data Analysis & Manipulation)  
📉 Matplotlib (Data Visualization)  
🖥️ Streamlit (Interactive Dashboard UI)  
📂 CSV Dataset (Data Source)
""")