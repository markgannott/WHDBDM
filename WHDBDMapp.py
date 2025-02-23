import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Your existing data dictionary
data = {
    "Rank": list(range(1, 21)),
    "Company": [
        "AbbVie", "Abbott Laboratories", "Fuji Pharma", "Veru Inc.", "Pulsenmore Ltd.", "Daré Bioscience Inc.",
        "Femasys Inc.", "Aspira Women's Health", "Palatin Technologies", "Mithra Pharmaceuticals", "The Cooper Companies",
        "Hologic Inc.", "Creative Medical Tech", "Minerva Surgical", "Organon & Co.", "INVO Bioscience",
        "Agile Therapeutics", "Bonzun", "Evofem Biosciences Inc.", "Callitas Therapeutics"
    ],
    # ... rest of your data ...
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
        fig_scatter = px.scatter(
            filtered_df,
            x="Founded Year",
            y="Market Cap (USD)",
            size="Market Cap (USD)",
            color="Company",
            title="Founded Year vs. Market Cap",
            template=plot_template
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab4:
        st.subheader("Geographic Analysis")
        # Count companies by headquarters
        geo_counts = filtered_df['Headquarters'].value_counts().reset_index()
        geo_counts.columns = ['Headquarters', 'Count']
        
        fig_geo = px.bar(
            geo_counts,
            x='Headquarters',
            y='Count',
            title="Companies by Location",
            template=plot_template
        )
        st.plotly_chart(fig_geo, use_container_width=True)

        # Add a download button in the first tab
        st.download_button(
            "Download Filtered Data as CSV",
            filtered_df.to_csv(index=False),
            "filtered_companies.csv",
            "text/csv"
        )

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.error("Please check your requirements.txt has: streamlit, pandas, and plotly")