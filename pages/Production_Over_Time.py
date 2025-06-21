import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

import polars as pl
import plotly.graph_objects as go  # Import Plotly's graph_objects module for adding traces

# Load data
st.sidebar.markdown("# Production Over Time" + ":chart:")
solar_file = Path(__file__).parent.parent / "solar_production.csv"
data = (
    pl.read_csv(solar_file)
    .with_columns(
        # Convert the Time column to a proper date
        pl.col("Time")
        .str.strptime(pl.Date, format="%Y-%m-%d")  # Correct date format
        .alias("Time")
    )
    .sort("Time")
)


start_date = data["Time"].min()
end_date = data["Time"].max()

# create a date slidebar to select date range
date_range = st.sidebar.slider(
    "Select Date Range", start_date, end_date, (start_date, end_date)
)


# subset data to selected date range
data = data.filter(
    (pl.col("Time") >= date_range[0]) & (pl.col("Time") <= date_range[1])
)


def _plot_data_over_time_plotly(data: pd.DataFrame):
    # Calculate the mean value of 'Production'
    mean_production = data["Production"].mean()

    # Create a scatter plot
    fig = px.scatter(data, x="Time", y="Production", title="Production Over Time")

    # Add a dashed line for the mean value
    fig.add_trace(
        go.Scatter(
            x=[data["Time"].min(), data["Time"].max()],  # Line spans the entire x-axis
            y=[mean_production, mean_production],
            mode="lines",
            line=dict(dash="dash"),
            name=f"Mean Production: {mean_production:.2f} kWh",
        )
    )

    # Set figure size
    fig.update_layout(height=600, width=800)

    # Set axis labels
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Production (kWh)")

    return fig


def main():
    st.markdown("# Daily Production Over Time" + ":sun_with_face:")

    fig = _plot_data_over_time_plotly(data)

    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
