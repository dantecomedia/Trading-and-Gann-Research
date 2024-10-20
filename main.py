import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to calculate time intervals and projected dates
def calculate_time_cycles(low_time, high_time, intervals):
    projections = []
    initial_duration = (high_time - low_time).total_seconds() / 60  # in minutes
    num_intervals = initial_duration / intervals  # Number of intervals

    # Gann's key numbers and Fibonacci ratios
    gann_numbers = [num_intervals, 90, 144, 180, 270, 360]
    squares = [64, 81]
    fibonacci_ratios = [0.618, 1, 1.618, 2.618]

    # Time projections based on initial movement
    for num in gann_numbers:
        minutes_to_add = num * intervals
        projected_time = high_time + timedelta(minutes=minutes_to_add)
        projections.append({
            'Description': f'Gann Number {num}',
            'Projected Time': projected_time
        })

    # Time projections based on squares
    for square in squares:
        minutes_to_add = square * intervals
        projected_time = high_time + timedelta(minutes=minutes_to_add)
        projections.append({
            'Description': f'Square of {int(square ** 0.5)}',
            'Projected Time': projected_time
        })

    # Time projections based on Fibonacci ratios
    for ratio in fibonacci_ratios:
        minutes_to_add = num_intervals * ratio * intervals
        projected_time = high_time + timedelta(minutes=minutes_to_add)
        projections.append({
            'Description': f'Fibonacci Ratio {ratio}',
            'Projected Time': projected_time
        })

    return projections

# Function to calculate price targets
def calculate_price_targets(low_price, high_price):
    projections = []
    price_movement = high_price - low_price

    # Bullish scenarios
    bullish_multipliers = [1, 1.25, 1.5, 2, 1.618, 2.618]
    for mult in bullish_multipliers:
        projected_price = high_price + price_movement * mult
        projections.append({
            'Scenario': f'Bullish Extension {mult * 100}%',
            'Projected Price': projected_price
        })

    # Bearish scenarios
    bearish_multipliers = [0.382, 0.5, 0.618, 1]
    for mult in bearish_multipliers:
        projected_price = high_price - price_movement * mult
        projections.append({
            'Scenario': f'Bearish Retracement {mult * 100}%',
            'Projected Price': projected_price
        })

    return projections

# Streamlit application
def main():
    st.title("Gann Time Cycle Analysis for BTC")

    # User inputs
    st.header("Input Significant Highs and Lows")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Significant Low")
        low_price = st.number_input("Low Price", value=67651.0, format="%.2f")
        low_time_str = st.text_input("Low Time (YYYY-MM-DD HH:MM)", "2024-10-18 18:25")
        low_time = datetime.strptime(low_time_str, "%Y-%m-%d %H:%M")

    with col2:
        st.subheader("Significant High")
        high_price = st.number_input("High Price", value=68995.0, format="%.2f")
        high_time_str = st.text_input("High Time (YYYY-MM-DD HH:MM)", "2024-10-19 00:15")
        high_time = datetime.strptime(high_time_str, "%Y-%m-%d %H:%M")

    intervals = st.number_input("Time Interval (minutes)", value=5, step=1)

    # Calculate projections
    time_projections = calculate_time_cycles(low_time, high_time, intervals)
    price_projections = calculate_price_targets(low_price, high_price)

    # Display results
    st.header("Projected Reversal Dates and Times")
    time_df = pd.DataFrame(time_projections)
    st.table(time_df)

    st.header("Projected Price Targets")
    price_df = pd.DataFrame(price_projections)
    st.table(price_df)

    # Optionally, add charts or additional analysis

if __name__ == "__main__":
    main()
