import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    selected_country = st.sidebar.selectbox("Filter by Country", ["All"] + sorted(df["Country"].dropna().unique().tolist()))
    
    # Apply filters
    if search_query:
        df = df[df.apply(lambda row: search_query.lower() in str(row.values).lower(), axis=1)]
    if selected_country != "All":
        df = df[df["Country"] == selected_country]
    
    # Display data
    st.title("Customer Data Analytics Dashboard")
    st.subheader("Filtered Data (Showing first 1000 rows)")
    st.dataframe(df.head(1000))
    
    # Country-wise distribution
    st.subheader("Customer Distribution by Country")
    country_counts = df["Country"].value_counts()
    fig, ax = plt.subplots()
    country_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Country")
    ax.set_ylabel("Number of Customers")
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
    
    # Export filtered data
    st.sidebar.download_button("Download Filtered Data", df.to_csv(index=False), "filtered_customers.csv", "text/csv")
else:
    st.warning("Please upload a CSV file to proceed.")
