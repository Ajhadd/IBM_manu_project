import streamlit as st
from manufacturing_calc import (
    calculate_oee,
    calculate_cycle_time,
    calculate_defect_rate,
    calculate_throughput,
    estimate_production_cost
)

# Title
st.title("Manufacturing Dashboard")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

availability = st.sidebar.slider("Availability", 0.0, 1.0, 0.87)
performance = st.sidebar.slider("Performance", 0.0, 1.0, 0.91)
quality = st.sidebar.slider("Quality", 0.0, 1.0, 0.996)

total_time = st.sidebar.number_input("Total Time (seconds)", value=28800)
units = st.sidebar.number_input("Units Produced", value=3450)

defective_units = st.sidebar.number_input("Defective Units", value=14)
total_units = st.sidebar.number_input("Total Units", value=3464)

hours = st.sidebar.number_input("Hours", value=8.0)

material_cost = st.sidebar.number_input("Material Cost per Unit", value=1.85)
labor_cost = st.sidebar.number_input("Labor Cost per Hour", value=32.0)

# Calculations
oee = calculate_oee(availability, performance, quality)
cycle_time = calculate_cycle_time(total_time, units)
defect_rate = calculate_defect_rate(defective_units, total_units)
throughput = calculate_throughput(units, hours)
cost = estimate_production_cost(units, material_cost, labor_cost, hours)

# Display Results
st.subheader("Results")

col1, col2, col3 = st.columns(3)

col1.metric("OEE", oee)
col2.metric("Cycle Time (sec)", cycle_time)
col3.metric("Defect Rate (%)", defect_rate)

col4, col5 = st.columns(2)

col4.metric("Throughput (units/hr)", throughput)
col5.metric("Production Cost ($)", cost)

# Simple Chart
st.subheader("OEE Visualization")
st.line_chart([availability, performance, quality])