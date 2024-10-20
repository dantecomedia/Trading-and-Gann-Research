import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# Function to calculate time intervals and projected dates remains the same
# Function to calculate price targets remains the same

def calculate_time_cycles(low_time, high_time, intervals):
    projections = []
    initial_duration = (high_time - low_time).total_seconds() / 60  # in minutes
    st.write(f"Initial Duration: {initial_duration} minutes")
    num_intervals = initial_duration / intervals  # Number of intervals
    st.write(f"Number of Intervals: {num_intervals}")

    if num_intervals <= 0:
        st.error("Number of intervals calculated is zero or negative. Check your input times and intervals.")
        return []

    # Gann's key numbers and Fibonacci ratios
    gann_numbers = [num_intervals, 90, 144, 180, 270, 360]
    squares = [64, 81]
    fibonacci_ratios = [0.618, 1, 1.618, 2.618]

    # Time projections based on initial movement
    for num in gann_numbers:
        minutes_to_add = num * intervals
        # Check for reasonable minutes_to_add
        if minutes_to_add > 1e6:
            st.error(f"Minutes to add is excessively large ({minutes_to_add}). Check your inputs.")
            continue
        projected_time = high_time + timedelta(minutes=minutes_to_add)
        projections.append({
            'Description': f'Gann Number {num:.2f}',
            'Projected Time': projected_time.strftime('%Y-%m-%d %H:%M')
        })

    # ... rest of the function ...


def main():
    st.title("Gann Time Cycle Analysis for BTC")

    # User inputs
    st.header("Input Significant Highs and Lows")

    col1, col2 = st.columns(2)

    # Generate times at 5-minute intervals
    times = [time(h, m) for h in range(0, 24) for m in range(0, 60, 5)]
    time_options = [t.strftime('%H:%M') for t in times]

    with col1:
        st.subheader("Significant Low")
        low_price = st.number_input("Low Price", value=67651.0, format="%.2f")

        # Date input
        low_date = st.date_input("Low Date", value=datetime(2024, 10, 18))

        # Time dropdown with default index
        try:
            default_index_low = time_options.index('18:25')
        except ValueError:
            default_index_low = 0  # Fallback index if '18:25' is not in time_options

        low_time_str = st.selectbox("Low Time", options=time_options, index=default_index_low)
        low_time = datetime.combine(low_date, datetime.strptime(low_time_str, '%H:%M').time())

    with col2:
        st.subheader("Significant High")
        high_price = st.number_input("High Price", value=68995.0, format="%.2f")

        # Date input
        high_date = st.date_input("High Date", value=datetime(2024, 10, 19))

        # Time dropdown with default index
        try:
            default_index_high = time_options.index('00:15')
        except ValueError:
            default_index_high = 0  # Fallback index if '00:15' is not in time_options

        high_time_str = st.selectbox("High Time", options=time_options, index=default_index_high)
        high_time = datetime.combine(high_date, datetime.strptime(high_time_str, '%H:%M').time())

    # Ensure high_time is after low_time
    if high_time <= low_time:
        st.error("Significant High Time must be after Significant Low Time.")
        return

    intervals = st.number_input("Time Interval (minutes)", value=5, step=1)

    # Validate intervals
    if intervals <= 0:
        st.error("Time Interval must be a positive number.")
        return

    # Output variable values for debugging
    st.write(f"Low Time: {low_time}")
    st.write(f"High Time: {high_time}")
    st.write(f"Intervals: {intervals}")

    # Calculate projections with error handling
    try:
        time_projections = calculate_time_cycles(low_time, high_time, intervals)
    except Exception as e:
        st.error(f"An error occurred in calculate_time_cycles: {e}")
        return

    try:
        price_projections = calculate_price_targets(low_price, high_price)
    except Exception as e:
        st.error(f"An error occurred in calculate_price_targets: {e}")
        return

    # Display results
    st.header("Projected Reversal Dates and Times")
    time_df = pd.DataFrame(time_projections)
    st.table(time_df)

    st.header("Projected Price Targets")
    price_df = pd.DataFrame(price_projections)
    st.table(price_df)

if __name__ == "__main__":
    main()
