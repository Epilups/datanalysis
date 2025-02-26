import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File uploader
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

def load_data(file):
    df = pd.read_csv(file, parse_dates=["Subscription Date"])
    return df

if uploaded_file:
    df = load_data(uploaded_file)
    
    # Sidebar for filters
    st.sidebar.header("Filters")
    search_query = st.sidebar.text_input("Search (Name, Email, Company)")
    selected_countries = st.sidebar.multiselect("Filter by Country", sorted(df["Country"].dropna().unique().tolist()))
    sort_by = st.sidebar.selectbox("Sort by", ["Subscription Date", "Country", "Company"], index=0)
    ascending_order = st.sidebar.checkbox("Ascending Order", value=True)
    
    # Apply filters
    if search_query:
        df = df[df.apply(lambda row: search_query.lower() in str(row.values).lower(), axis=1)]
    if selected_countries:
        df = df[df["Country"].isin(selected_countries)]
    df = df.sort_values(by=sort_by, ascending=ascending_order)
    
    # Display data
    st.title("Customer Data Analytics Dashboard")
    st.subheader("Filtered Data (Showing first 1000 rows)")
    st.dataframe(df.head(1000))
    
    # Country-wise distribution
    st.subheader("Top 50 Customer Distribution by Country")
    country_counts = df["Country"].value_counts().nlargest(50)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=country_counts.index, y=country_counts.values, ax=ax)
    ax.set_xlabel("Country")
    ax.set_ylabel("Number of Customers")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)
    
    # Pie chart for country distribution
    st.subheader("Top 10 Countries - Customer Distribution")
    top_10_countries = df["Country"].value_counts().nlargest(10)
    fig, ax = plt.subplots()
    ax.pie(top_10_countries, labels=top_10_countries.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.axis("equal")
    st.pyplot(fig)
    
    # Subscription trends
    df["Subscription Year"] = df["Subscription Date"].dt.year
    subscription_trends = df.groupby("Subscription Year").size()
    st.subheader("Subscription Trends Over Time")
    fig, ax = plt.subplots()
    subscription_trends.plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Subscriptions")
    st.pyplot(fig)
    
    # Extreme value analysis
    st.subheader("Top 10 Companies with the Most Customers")
    top_companies = df["Company"].value_counts().nlargest(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_companies.index, y=top_companies.values, ax=ax)
    ax.set_xlabel("Company")
    ax.set_ylabel("Number of Customers")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)
    
    st.subheader("Customers with the Longest Subscription")
    oldest_subscriptions = df.sort_values("Subscription Date").head(10)
    st.dataframe(oldest_subscriptions[["First Name", "Last Name", "Company", "Subscription Date"]])
    
    # Replacing duplicate "Top 10 Companies" chart with new feature
    st.subheader("Subscription Growth Rate")
    df["Subscription Month-Year"] = df["Subscription Date"].dt.to_period("M")
    subscription_growth = df.groupby("Subscription Month-Year").size()
    fig, ax = plt.subplots()
    subscription_growth.plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Month-Year")
    ax.set_ylabel("Number of New Subscriptions")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Most common subscription months
    st.subheader("Most Common Subscription Months")
    df["Subscription Month"] = df["Subscription Date"].dt.month
    month_counts = df["Subscription Month"].value_counts().sort_index()
    fig, ax = plt.subplots()
    sns.barplot(x=month_counts.index, y=month_counts.values, ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Subscriptions")
    ax.set_xticks(range(12))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    st.pyplot(fig)
    
    # Customers with multiple phone numbers
    st.subheader("Customers with Multiple Phone Numbers")
    multi_phone_customers = df[df["Phone 2"].notna()]
    st.dataframe(multi_phone_customers[["First Name", "Last Name", "Company", "Phone 1", "Phone 2"]])
    
    # Export filtered data
    st.sidebar.download_button("Download Filtered Data", df.to_csv(index=False), "filtered_customers.csv", "text/csv")
else:
    st.warning("Please upload a CSV file to proceed.")
