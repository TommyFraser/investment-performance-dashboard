# Import the libraries needed for the dashboard
# streamlit = creates the web dashboard
# pandas = reads and manipulates the CSV data
# plotly.express = creates interactive charts
import streamlit as st
import pandas as pd
import plotly.express as px


# ------------------------------------------------------------
# PAGE SETUP
# This controls the browser tab title and makes the dashboard wide
# ------------------------------------------------------------
st.set_page_config(
    page_title="Investment Performance Dashboard",
    layout="wide"
)


# ------------------------------------------------------------
# DASHBOARD TITLE
# This is the heading shown at the top of the web page
# ------------------------------------------------------------
st.title("Investment Performance Dashboard")
st.caption("Portfolio returns, benchmark comparison, excess return and asset allocation")


# ------------------------------------------------------------
# LOAD THE DATA
# This reads the CSV file sitting in the same folder as app.py
# ------------------------------------------------------------
df = pd.read_csv("investment_data.csv")


# Clean column names in case there are accidental spaces
# Example: " Date" becomes "Date"
df.columns = df.columns.str.strip()


# Convert the Date column from text into a real date format
# Your CSV uses Australian date format: day/month/year
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")


# ------------------------------------------------------------
# CALCULATE PERFORMANCE METRICS
# This section creates new calculated columns for the dashboard
# ------------------------------------------------------------

# Excess return shows how much the portfolio beat or missed the benchmark
df["Excess_Return"] = df["Portfolio_Return"] - df["Benchmark_Return"]


# Portfolio growth starts at 100 and compounds each monthly return
# This shows how $100 would grow over time in the portfolio
df["Portfolio_Growth"] = (1 + df["Portfolio_Return"]).cumprod() * 100


# Benchmark growth does the same thing for the benchmark
df["Benchmark_Growth"] = (1 + df["Benchmark_Return"]).cumprod() * 100


# Rolling 3-month average smooths the monthly results
# This helps show the short-term trend instead of one noisy month
df["Rolling_3M_Portfolio"] = df["Portfolio_Return"].rolling(window=3).mean()
df["Rolling_3M_Benchmark"] = df["Benchmark_Return"].rolling(window=3).mean()


# Portfolio peak tracks the highest portfolio value reached so far
df["Portfolio_Peak"] = df["Portfolio_Growth"].cummax()


# Drawdown shows how far the portfolio has fallen from its previous peak
# This is a common investment risk/performance metric
df["Drawdown"] = (df["Portfolio_Growth"] - df["Portfolio_Peak"]) / df["Portfolio_Peak"]


# ------------------------------------------------------------
# SIDEBAR FILTERS
# These allow the user to choose a date range
# ------------------------------------------------------------
start_date = st.sidebar.date_input("Start date", df["Date"].min())
end_date = st.sidebar.date_input("End date", df["Date"].max())


# Filter the data based on the selected date range
filtered = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]


# Stop the dashboard safely if the selected date range has no data
if filtered.empty:
    st.warning("No data available for the selected date range.")
    st.stop()


# ------------------------------------------------------------
# SUMMARY KPI CALCULATIONS
# These numbers appear at the top of the dashboard
# ------------------------------------------------------------

# Total portfolio return over the selected period
total_portfolio_return = (
    filtered["Portfolio_Growth"].iloc[-1] / filtered["Portfolio_Growth"].iloc[0]
) - 1


# Total benchmark return over the selected period
total_benchmark_return = (
    filtered["Benchmark_Growth"].iloc[-1] / filtered["Benchmark_Growth"].iloc[0]
) - 1


# Total excess return over the selected period
total_excess_return = total_portfolio_return - total_benchmark_return


# Average monthly return
average_monthly_return = filtered["Portfolio_Return"].mean()


# Volatility is the standard deviation of monthly returns
# Higher volatility means returns moved around more
volatility = filtered["Portfolio_Return"].std()


# Worst drawdown during the selected period
max_drawdown = filtered["Drawdown"].min()


# ------------------------------------------------------------
# DISPLAY KPI CARDS
# This creates six summary metric boxes across the top
# ------------------------------------------------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Portfolio Return", f"{total_portfolio_return:.2%}")
col2.metric("Benchmark Return", f"{total_benchmark_return:.2%}")
col3.metric("Excess Return", f"{total_excess_return:.2%}")
col4.metric("Avg Monthly Return", f"{average_monthly_return:.2%}")
col5.metric("Volatility", f"{volatility:.2%}")
col6.metric("Max Drawdown", f"{max_drawdown:.2%}")


# ------------------------------------------------------------
# CHART 1: PORTFOLIO GROWTH VS BENCHMARK
# This compares how the portfolio grew against the benchmark
# ------------------------------------------------------------

# Reshape the data so Plotly can draw both lines on one chart
growth_chart = filtered[["Date", "Portfolio_Growth", "Benchmark_Growth"]].melt(
    id_vars="Date",
    var_name="Series",
    value_name="Value"
)

fig_growth = px.line(
    growth_chart,
    x="Date",
    y="Value",
    color="Series",
    title="Portfolio Growth vs Benchmark"
)

st.plotly_chart(fig_growth)


# ------------------------------------------------------------
# CHART 2 AND 3 LAYOUT
# These two charts sit side-by-side
# ------------------------------------------------------------
col_left, col_right = st.columns(2)


# ------------------------------------------------------------
# CHART 2: MONTHLY EXCESS RETURN
# This shows whether the portfolio beat or missed the benchmark each month
# ------------------------------------------------------------
fig_excess = px.bar(
    filtered,
    x="Date",
    y="Excess_Return",
    title="Monthly Excess Return"
)

col_left.plotly_chart(fig_excess)


# ------------------------------------------------------------
# CHART 3: ROLLING 3-MONTH RETURN
# This smooths the data to show the recent trend
# ------------------------------------------------------------

# Reshape rolling return data so both series appear on one chart
rolling_chart = filtered[["Date", "Rolling_3M_Portfolio", "Rolling_3M_Benchmark"]].melt(
    id_vars="Date",
    var_name="Series",
    value_name="Return"
)

fig_rolling = px.line(
    rolling_chart,
    x="Date",
    y="Return",
    color="Series",
    title="Rolling 3-Month Average Return"
)

col_right.plotly_chart(fig_rolling)


# ------------------------------------------------------------
# CHART 4 AND 5 LAYOUT
# These two charts sit side-by-side
# ------------------------------------------------------------
col_left2, col_right2 = st.columns(2)


# ------------------------------------------------------------
# CHART 4: PORTFOLIO DRAWDOWN
# This shows the fall from the previous portfolio high point
# ------------------------------------------------------------
fig_drawdown = px.area(
    filtered,
    x="Date",
    y="Drawdown",
    title="Portfolio Drawdown"
)

col_left2.plotly_chart(fig_drawdown)


# ------------------------------------------------------------
# CHART 5: LATEST ASSET ALLOCATION
# This uses the most recent row in the selected date range
# ------------------------------------------------------------

# Get the latest allocation percentages from the filtered data
latest_allocation = filtered.iloc[-1][
    [
        "Australian_Equities",
        "International_Equities",
        "Fixed_Income",
        "Cash",
        "Property"
    ]
]


# Convert the allocation data into a format suitable for a pie chart
allocation_df = pd.DataFrame({
    "Asset Class": latest_allocation.index,
    "Allocation": latest_allocation.values
})

fig_allocation = px.pie(
    allocation_df,
    names="Asset Class",
    values="Allocation",
    title="Latest Asset Allocation"
)

col_right2.plotly_chart(fig_allocation)


# ------------------------------------------------------------
# PERFORMANCE DATA TABLE
# This shows the underlying numbers used in the dashboard
# ------------------------------------------------------------
st.subheader("Performance Data")


# Select only the columns we want to display
display_df = filtered[
    [
        "Date",
        "Portfolio_Return",
        "Benchmark_Return",
        "Excess_Return",
        "Portfolio_Growth",
        "Benchmark_Growth",
        "Drawdown"
    ]
].copy()


# Format dates and percentages so they are easier to read
display_df["Date"] = display_df["Date"].dt.strftime("%d/%m/%Y")
display_df["Portfolio_Return"] = display_df["Portfolio_Return"].map("{:.2%}".format)
display_df["Benchmark_Return"] = display_df["Benchmark_Return"].map("{:.2%}".format)
display_df["Excess_Return"] = display_df["Excess_Return"].map("{:.2%}".format)
display_df["Drawdown"] = display_df["Drawdown"].map("{:.2%}".format)
display_df["Portfolio_Growth"] = display_df["Portfolio_Growth"].map("{:.2f}".format)
display_df["Benchmark_Growth"] = display_df["Benchmark_Growth"].map("{:.2f}".format)


# Display the final formatted table
st.dataframe(display_df)