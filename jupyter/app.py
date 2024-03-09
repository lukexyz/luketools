import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

def generate_sample_data(n=20):
    # Generate a DataFrame with sample data
    np.random.seed(0)  # For reproducibility
    dates = []
    test_dates = []
    user_ids = []
    for user_id in range(1, n + 1):
        num_activities = np.random.randint(1, 5)  # Random number of activities per user
        for _ in range(num_activities):
            days = np.random.randint(0, 31)  # January has 31 days
            date = datetime(2024, 1, 1) + timedelta(days=days)
            dates.append(date)
            user_ids.append(f'user_{user_id}')
        
        # Generate test_entry_date between Jan 1 and Jan 15
        test_days = np.random.randint(0, 15) 
        test_date = datetime(2024, 1, 1) + timedelta(days=test_days)
        test_dates.extend([test_date] * num_activities)  # Same test date for all activities of a user

    return pd.DataFrame({
        'user_id': user_ids, 
        'activity_date': dates,
        'test_entry_date': test_dates
    })


n = st.number_input('Enter the number of sample users', min_value=1, value=20, step=1)

if st.button('Apply'):
    data = generate_sample_data(n)
else:
    data = generate_sample_data(20) 


# Calculate the earliest test_entry_date for each user and the relative_days
user_test_date_min = data.groupby('user_id')['test_entry_date'].min().reset_index()
user_test_date_min.rename(columns={'test_entry_date': 'min_test_entry_date'}, inplace=True)
data = data.merge(user_test_date_min, on='user_id')
data['relative_days'] = (data['activity_date'] - data['min_test_entry_date']).dt.days
data.sort_values('min_test_entry_date', inplace=True)

# Calculate metrics
first_activity_days = data.groupby('user_id')['relative_days'].min().reset_index()
avg_days = first_activity_days['relative_days'].mean()
median_days = first_activity_days['relative_days'].median()

# Streamlit UI setup
st.title('User Activity and Test Entry Visualization')

# Use columns to layout the chart and the metrics
col1, col2 = st.columns([3, 1])

# Checkbox to toggle between absolute and relative dates, placed outside columns for full width
date_mode = st.checkbox('Show Relative Days Post Test Entry', False)

with col1:
    # Construct and display the chart as before
    # Base chart with sorted y-axis based on the earliest test_entry_date
    base = alt.Chart(data).encode(
        y=alt.Y('user_id:O', sort=alt.EncodingSortField(field='min_test_entry_date', order='ascending')),
    ).properties(width=1000, height=400)

    if date_mode:
        # Relative days mode
        x_axis = alt.X('relative_days:Q', title='Days Relative to Test Entry')
        tooltip = ['user_id', alt.Tooltip('relative_days:Q', title='Days Post Test Entry')]
    else:
        # Absolute date mode
        x_axis = alt.X('activity_date:T', title='Activity Date')
        tooltip = ['user_id', 'activity_date:T']

    activity_layer = base.mark_circle(size=60, opacity=0.4, color='blue').encode(
        x=x_axis,
        tooltip=tooltip
    ).properties(width=1000, height=400)

    # Combining layers conditionally based on the toggle
    if date_mode:
        chart = activity_layer
    else:
        test_entry_layer = base.mark_text(text='▶', size=12, color='gray').encode(
            x='min_test_entry_date:T',
            tooltip=['user_id', 'min_test_entry_date:T']
        ).transform_filter(
            alt.datum.min_test_entry_date
        ).properties(width=1000, height=400)
        chart = (activity_layer + test_entry_layer).interactive()

    st.altair_chart(chart, use_container_width=False)

with col2:
    # Display the calculated metrics
    st.metric(label="Average Days", value=f"{avg_days:.2f}")
    st.metric(label="Median Days", value=f"{median_days:.2f}")