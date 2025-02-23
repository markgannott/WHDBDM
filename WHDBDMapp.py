import streamlit as st
import pandas as pd
import plotly.express as px

# Dark mode state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Setup the page
st.set_page_config(
    page_title="Women's Health Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add theme toggle in sidebar
with st.sidebar:
    st.sidebar.header("Theme Settings")
    if st.toggle('Dark Mode', key='dark_mode'):
        st.markdown("""
            <style>
            .stApp {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            </style>
            """, unsafe_allow_html=True)
        plot_template = "plotly_dark"
    else:
        plot_template = "plotly_white"

# Load Data
data = {
    "Rank": list(range(1, 21)),
    "Company": [
        "AbbVie", "Abbott Laboratories", "Fuji Pharma", "Veru Inc.", "Pulsenmore Ltd.", "Daré Bioscience Inc.",
        "Femasys Inc.", "Aspira Women's Health", "Palatin Technologies", "Mithra Pharmaceuticals", "The Cooper Companies",
        "Hologic Inc.", "Creative Medical Tech", "Minerva Surgical", "Organon & Co.", "INVO Bioscience",
        "Agile Therapeutics", "Bonzun", "Evofem Biosciences Inc.", "Callitas Therapeutics"
    ],
    "Market Cap (USD)": [
        319840000000, 207080000000, 281900000, 40600000, 17500000, 18500000, 20300000, 24700000, 27500000, 28900000,
        20300000000, 19440000000, 30200000, 35700000, 40100000, 2890000, 2030000, 339000, 128000, 3300
    ],
    "Founded Year": [
        2013, 1888, 1965, 1971, 2014, 2004, 2004, 1993, 1986, 1999,
        1958, 1985, 1998, 2008, 2021, 2007, 1997, 2012, 2007, 2003
    ],
    "Total Employees": [
        50000, 113000, 1600, 190, 50, 40, 40, 100, 20, 500, 15000, 6940,
        10, 240, 9000, 20, 20, 50, 40, 0
    ],
    "Headquarters": [
        "Illinois, USA", "Illinois, USA", "Tokyo, Japan", "Florida, USA", "Omer, Israel", "California, USA",
        "Georgia, USA", "Texas, USA", "New Jersey, USA", "Liège, Belgium", "California, USA", "Massachusetts, USA",
        "Arizona, USA", "California, USA", "New Jersey, USA", "Florida, USA", "New Jersey, USA", "Stockholm, Sweden",
        "California, USA", "British Columbia, Canada"
    ],
    "Stock Exchange": [
        "NYSE", "NYSE", "TYO", "NASDAQ", "TASE", "NASDAQ", "NASDAQ", "NASDAQ", "NYSE", "EBR", "NASDAQ", "NASDAQ",
        "NASDAQ", "NASDAQ", "NYSE", "-", "NASDAQ", "STO", "OTCMKTS", "OTCMKTS"
    ]
}

try:
    df = pd.DataFrame(data)

    st.title("Top 20 Women Health-Focused Companies")

    # Sidebar Filters
    st.sidebar.header("Filter Options")
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        df["Headquarters"].unique(),
        default=df["Headquarters"].unique()
    )
    selected_exchanges = st.sidebar.multiselect(
        "Select Stock Exchanges",
        df["Stock Exchange"].unique(),
        default=df["Stock Exchange"].unique()
    )
    market_cap_range = st.sidebar.slider(
        "Market Cap Range (USD)",
        int(df["Market Cap (USD)"].min()),
        int(df["Market Cap (USD)"].max()),
        (int(df["Market Cap (USD)"].min()), int(df["Market Cap (USD)"].max()))
    )

    # Apply Filters
    filtered_df = df[
        (df["Headquarters"].isin(selected_countries)) &
        (df["Stock Exchange"].isin(selected_exchanges)) &
        (df["Market Cap (USD)"].between(market_cap_range[0], market_cap_range[1]))
    ]

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Company Analysis", "Market Trends", "Geographic Distribution"])

    with tab1:
        st.subheader("Dashboard Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Market Cap", f"${filtered_df['Market Cap (USD)'].sum():,.0f}")
        col2.metric("Average Market Cap", f"${filtered_df['Market Cap (USD)'].mean():,.0f}")
        col3.metric("Median Founded Year", f"{int(filtered_df['Founded Year'].median())}")
        col4.metric("Number of Companies", f"{len(filtered_df)}")
        
        # Download button above the dataframe
        st.download_button(
            "Download Filtered Data as CSV",
            filtered_df.to_csv(index=False),
            "filtered_companies.csv",
            "text/csv"
        )
        
        st.dataframe(filtered_df, use_container_width=True)

    with tab2:
        st.subheader("Company Market Cap Distribution")
        fig_bar = px.bar(
            filtered_df,
            x="Market Cap (USD)",
            y="Company",
            orientation='h',
            title="Market Capitalization of Companies",
            template=plot_template
        )
        fig_bar.update_layout(height=600)
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        st.subheader("Market Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_scatter = px.scatter(
                filtered_df,
                x="Founded Year",
                y="Market Cap (USD)",
                size="Market Cap (USD)",
                color="Company",
                title="Founded Year vs. Market Cap",
                template=plot_template
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Employee vs Market Cap visualization
            fig_emp = px.scatter(
                filtered_df,
                x="Total Employees",
                y="Market Cap (USD)",
                size="Market Cap (USD)",
                color="Company",
                title="Employees vs. Market Cap",
                template=plot_template
            )
            fig_emp.update_layout(height=400)
            st.plotly_chart(fig_emp, use_container_width=True)

    with tab4:
        st.subheader("Geographic Distribution")
        # Count companies by headquarters
        headquarters_counts = filtered_df['Headquarters'].value_counts()
        
        # Create bar chart for geographic distribution
        fig_geo = px.bar(
            x=headquarters_counts.index,
            y=headquarters_counts.values,
            title="Companies by Location",
            labels={'x': 'Headquarters Location', 'y': 'Number of Companies'},
            template=plot_template
        )
        fig_geo.update_layout(
            xaxis_tickangle=-45,
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig_geo, use_container_width=True)
        
        # Display summary statistics
        st.subheader("Geographic Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Locations", len(headquarters_counts))
        col2.metric("Most Common Location", headquarters_counts.index[0])

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.error("Please check your requirements.txt has: streamlit, pandas, and plotly")
