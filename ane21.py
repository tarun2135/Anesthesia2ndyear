import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")

# Load the data
file_path = r"Anesthesia 2nd Year.xlsx"
df = pd.read_excel(file_path)

# Convert relevant columns to numeric
numeric_cols = ['Academic Fees Paid', 'Academic Due Fees', 'Academic Total Fees',
                'Transportation Fees Paid', 'Hostel Fees Paid', 'Hostel Fees Due']

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Function to filter data based on selected fee range
def filter_data(df, column, min_value, max_value):
    return df[(df[column] >= min_value) & (df[column] <= max_value)]

# Slider for fee range specific to area chart
min_value, max_value = st.slider('Select Fee Range for Area Chart (0k to 100k)', 0, 100000, (0, 100000), 1000)

# Filter data for Due Fees and Paid Fees using the area chart specific slider
filtered_df = filter_data(df, 'Academic Due Fees', min_value, max_value)
filtered_df_paid = filter_data(df, 'Academic Fees Paid', min_value, max_value)

# Create an area chart
fig = go.Figure()

fig.add_trace(go.Scatter(x=filtered_df['Name'], y=filtered_df['Academic Due Fees'], fill='tozeroy', name='Due Fees', line=dict(color='rgb(55, 83, 109)')))
fig.add_trace(go.Scatter(x=filtered_df['Name'], y=filtered_df_paid['Academic Fees Paid'], fill='tozeroy', name='Paid Fees', line=dict(color='rgb(26, 118, 255)')))

# Add a red line at y=100,000
fig.add_shape(type="line", x0=0, y0=100000, x1=len(filtered_df['Name'])-1, y1=100000,
              line=dict(color="rgb(184, 115, 51)", width=3))

# Update layout
fig.update_layout(title='Academic Fees with Due Fees and Paid Fees',
                  xaxis_title='Student', yaxis_title='Amount', height=600)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Calculate overall paid fees
overall_paid_transportation = df['Transportation Fees Paid'].sum()
overall_paid_academic = df['Academic Fees Paid'].sum()
overall_paid_hostel = df['Hostel Fees Paid'].sum()

# Create a donut chart for overall paid fees
labels_paid = ['Transportation Fees Paid', 'Academic Fees Paid', 'Hostel Fees Paid']
values_paid = [overall_paid_transportation, overall_paid_academic, overall_paid_hostel]

fig_donut1 = go.Figure(go.Pie(labels=labels_paid, values=values_paid, hole=0.5))
fig_donut1.update_traces(marker=dict(colors=['skyblue', 'lightgreen', 'lightcoral']))

# Calculate overall due fees
overall_due_transportation = df['Transportation Due Fees'].sum() if 'Transportation Due Fees' in df.columns else 0
overall_due_academic = df['Academic Due Fees'].sum()
overall_due_hostel = df['Hostel Fees Due'].sum() if 'Hostel Fees Due' in df.columns else 0

# Create a donut chart for overall due fees
labels_due = ['Transportation Due Fees', 'Academic Due Fees', 'Hostel Due Fees']
values_due = [overall_due_transportation, overall_due_academic, overall_due_hostel]

fig_donut2 = go.Figure(go.Pie(labels=labels_due, values=values_due, hole=0.5))
fig_donut2.update_traces(marker=dict(colors=['lightyellow', 'lightgreen', 'lightcoral']))

# Positioning the charts
col2, col3 = st.columns(2)

# Display the first donut chart (overall paid fees)
col2.plotly_chart(fig_donut1)

# Display the second donut chart (overall due fees)
col3.plotly_chart(fig_donut2)

# Create histograms for Academic Paid Fees, Hostel Paid Fees, and Transportation Paid Fees
fig_hist1 = px.histogram(df, x='Academic Fees Paid', nbins=20, title='Academic Fees Paid Histogram', color_discrete_sequence=['rgb(55, 83, 109)'])
fig_hist2 = px.histogram(df, x='Hostel Fees Paid', nbins=20, title='Hostel Fees Paid Histogram', color_discrete_sequence=['rgb(26, 118, 255)'])
fig_hist3 = px.histogram(df, x='Transportation Fees Paid', nbins=20, title='Transportation Fees Paid Histogram', color_discrete_sequence=['red'])

# Positioning the histograms
col4, col5, col6 = st.columns(3)

# Display the histograms
col4.plotly_chart(fig_hist1)
col5.plotly_chart(fig_hist2)
col6.plotly_chart(fig_hist3)
