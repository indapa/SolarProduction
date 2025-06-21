import streamlit as st
import polars as pl
import pandas as pd
from pathlib import Path
import plotly.express as px


# Load data
solar_file = Path(__file__).parent.parent / "solar_production.csv"


st.sidebar.markdown("# Comparative Production" + ":chart:")
time_frame_select = st.sidebar.selectbox(
    "Select Time Period", (["year", "month", "quarter", "cumulative"])
)


# plot cumulative production by year, with each year as  line
def plotly_yearly_production():
    q = (
        pl.scan_csv(solar_file)
        .with_columns(
            # Convert the Time column to a proper date
            pl.col("Time").str.strptime(pl.Date, format="%Y-%m-%d").alias("Date")
        )
        .with_columns(
            year_str=pl.col("Date").dt.strftime("%Y"),
            year_num=pl.col("Date").dt.year(),
            month_str=pl.col("Date").dt.strftime("%B"),
            month_num=pl.col("Date").dt.month(),
        )
        .group_by([pl.col("year_num"), pl.col("year_str")])
        # Now compute the year sum
        .agg(pl.col("Production").sum().round(2).alias("Yearly_Production"))
        # round avg_production_kWh to 2 decimal places
        .sort(["year_num"])
    )

    year_df = q.collect()

    fig = px.bar(
        year_df, x="year_str", y="Yearly_Production", color="year_str", barmode="group"
    )

    # adjust offset and  width so bars are centered nicely
    fig.update_traces(offset=-0.2, width=0.4)

    # Improve layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Yearly Production (kWh)",
        xaxis=dict(type="category"),  # ensure x-axis is treated as categorical
        bargap=0.2,  # play with bargap for spacing
    )

    fig.update_layout(xaxis_title="Year", yaxis_title="Yearly Production (kWh)")
    st.plotly_chart(fig)


# plot cumulative production by year
def plotly_cumulative_production():
    q = (
        pl.scan_csv(solar_file)
        .with_columns(
            # Convert the Time column to a proper date
            pl.col("Time").str.strptime(pl.Date, format="%Y-%m-%d").alias("Date"),
        )
        .sort("Date")
        # add column with cumulative sum
        .with_columns(
            year=pl.col("Date").dt.year(),
        )
        .with_columns(
            pl.col("Production")
            .cum_sum()
            .over("year")
            .round(2)
            .alias("cumulative_production"),
        )
    )
    data = q.collect().to_pandas()  # convert to pandas dataframe because I can't figure out how to plot cumulative sum in polars

    data["Date"] = pd.to_datetime(data["Date"])  # Convert to datetime format

    data["MMDD"] = data["Date"].dt.strftime("%m-%d")
    data["MMDD"] = pd.to_datetime(data["MMDD"], format="%m-%d", errors="coerce")
    data["MMDD"] = data["MMDD"].apply(lambda x: x.replace(year=2024))  # leap year

    data["YYYY"] = data["Date"].dt.strftime("%Y")

    # add a column for cumulative production by year

    data["Cumulative Production"] = data.groupby("YYYY")["Production"].cumsum()
    data.sort_values(by=["YYYY", "MMDD"], inplace=True)
    fig = px.line(
        data,
        x="MMDD",
        y="Cumulative Production",
        color="YYYY",
        title="Cumulative Solar Production by Year",
        labels={
            "YYYY": "Year",
            "MMDD": "Month",
            "Cumulative Production": "Cumulative Production",
        },
    )
    fig.update_xaxes(dtick="M1", tickformat="%b")

    st.plotly_chart(fig, use_container_width=True)


# plot quarterly comparative production
def plotly_quarterly_comparative_production():
    q = (
        pl.scan_csv(solar_file)
        .with_columns(
            # Convert the Time column to a proper date
            pl.col("Time").str.strptime(pl.Date, format="%Y-%m-%d").alias("Date"),
        )
        .sort("Date")
        .with_columns(
            month=pl.col("Date").dt.month(),
            year=pl.col("Date").dt.year(),
        )
        .with_columns(
            pl.when(pl.col("month") <= 3)
            .then(1)
            .when(pl.col("month") <= 6)
            .then(2)
            .when(pl.col("month") <= 9)
            .then(3)
            .otherwise(4)
            .alias("Quarter")
        )
        .group_by(["year", "Quarter"])
        # compute quarterly production
        .agg(pl.col("Production").sum().round(2).alias("Quarterly_Production"))
        .sort(["year", "Quarter"])
        .select("year", "Quarter", "Quarterly_Production")
        .with_columns(
            pl.col("Quarter")
            .replace_strict([1, 2, 3, 4], ["Q1", "Q2", "Q3", "Q4"])
            .alias("Quarter"),
            pl.col("year").cast(pl.Utf8).alias("year"),
        )
        # cast year to string
    )

    year_quarter_df = q.collect()
    fig = px.bar(
        year_quarter_df,
        x="year",
        y="Quarterly_Production",
        color="Quarter",
        barmode="group",
    )
    fig.update_layout(xaxis_title="Quarter", yaxis_title="Quarterly Production (kWh)")
    st.plotly_chart(fig)


def plotly_monthly_production():
    q = (
        pl.scan_csv(solar_file)
        .with_columns(
            # Convert the Time column to a proper date
            pl.col("Time").str.strptime(pl.Date, format="%Y-%m-%d").alias("Date"),
        )
        .with_columns(
            year_str=pl.col("Date").dt.strftime("%Y"),
            year_num=pl.col("Date").dt.year(),
            month_str=pl.col("Date").dt.strftime("%B"),
            month_num=pl.col("Date").dt.month(),
        )
        .group_by(
            [
                pl.col("year_num"),
                pl.col("year_str"),
                pl.col("month_num"),
                pl.col("month_str"),
            ]
        )
        # sum the production for each month
        .agg(pl.col("Production").sum().round(2).alias("Monthly_Production"))
        # round avg_production_kWh to 2 decimal places
        .sort(["year_num", "month_num"])
        # convert year_num to string and month_num to string
        .select("month_str", "year_str", "Monthly_Production")
        .rename(
            {
                "month_str": "month",
                "year_str": "year",
                "Monthly_Production": "production",
            }
        )
    )

    df = q.collect()

    fig = px.bar(df, x="month", y="production", color="year", barmode="group")
    fig.update_layout(xaxis_title="Month", yaxis_title="Monthly Production (kWh)")

    st.plotly_chart(fig)


def main():
    st.markdown("# Comparative Production" + ":sun_with_face:")

    # select time period sidebar

    if time_frame_select == "year":
        plotly_yearly_production()
    elif time_frame_select == "month":
        plotly_monthly_production()
    elif time_frame_select == "cumulative":
        plotly_cumulative_production()

    else:
        plotly_quarterly_comparative_production()


if __name__ == "__main__":
    main()
