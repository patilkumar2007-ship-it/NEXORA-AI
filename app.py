
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="🌐",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(120deg, #14213d, #283e70);
    color: white;
    margin-bottom: 25px;
}
.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}
.hero p {
    font-size: 17px;
    color: #dbeafe;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>NEXORA AI</h1>
    <p>Simulate. Predict. Optimize.</p>
    <p>Multi-Domain Scenario Simulation Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("NEXORA AI")
st.sidebar.caption("Simulation Control Center")

domain = st.sidebar.selectbox(
    "Choose a domain",
    [
        "Traffic & Transportation",
        "Business & Inventory",
        "Logistics & Delivery",
        "Energy Management",
        "Emergency Planning"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Prototype v0.1")

st.header("Simulation Workspace")
st.write(
    "Change the parameters below to explore different "
    "scenarios and compare their outcomes."
)

# ---------- TRAFFIC ----------
if domain == "Traffic & Transportation":

    st.subheader("🚦 Traffic Scenario Simulator")

    col1, col2 = st.columns(2)

    with col1:
        demand = st.slider(
            "Traffic demand (%)", 10, 100, 65
        )

    with col2:
        capacity = st.slider(
            "Road capacity (%)", 10, 100, 75
        )

    utilization = round(demand / capacity * 100)
    overload = max(0, demand - capacity)
    utilization_display = min(100, utilization)

    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("Traffic Demand", f"{demand}%")
    m2.metric("Road Capacity", f"{capacity}%")
    m3.metric("Capacity Utilization", f"{utilization_display}%")

    chart_data = pd.DataFrame({
        "Metric": ["Traffic Demand", "Road Capacity"],
        "Value": [demand, capacity]
    })

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Value",
        color="Metric",
        text="Value",
        range_y=[0, 110],
        title="Demand vs Available Capacity"
    )

    st.plotly_chart(fig, use_container_width=True)

    if overload > 0:
        st.warning(
            f"Scenario result: demand exceeds capacity by "
            f"{overload} percentage points."
        )
        st.write(
            "Possible actions: increase capacity or reduce "
            "traffic demand."
        )
    else:
        st.success(
            "Scenario result: selected demand is within capacity."
        )

    st.caption(
        "Illustrative calculation only. Not a real-world traffic forecast."
    )

# ---------- BUSINESS ----------
elif domain == "Business & Inventory":

    st.subheader("📦 Business & Inventory Simulator")

    col1, col2 = st.columns(2)

    with col1:
        stock = st.slider(
            "Available inventory (units)", 0, 1000, 400
        )

    with col2:
        demand = st.slider(
            "Expected customer demand (units)", 0, 1000, 550
        )

    shortage = max(0, demand - stock)
    surplus = max(0, stock - demand)

    fulfillment = (
        100 if demand == 0
        else min(100, round(stock / demand * 100))
    )

    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("Available Stock", f"{stock:,}")
    m2.metric("Expected Demand", f"{demand:,}")
    m3.metric("Demand Fulfilled", f"{fulfillment}%")

    chart_data = pd.DataFrame({
        "Metric": ["Available Stock", "Expected Demand"],
        "Units": [stock, demand]
    })

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Units",
        color="Metric",
        text="Units",
        title="Inventory vs Expected Demand"
    )

    st.plotly_chart(fig, use_container_width=True)

    if shortage > 0:
        st.warning(f"Potential shortage: {shortage} units.")
        st.write("Consider replenishing inventory before demand occurs.")
    elif surplus > 0:
        st.success(f"Potential surplus: {surplus} units.")
        st.write("Review future purchasing to avoid excess stock.")
    else:
        st.success("Inventory exactly matches expected demand.")

    st.caption(
        "This is a basic scenario calculation, not an ML prediction."
    )

# ---------- FUTURE DOMAINS ----------
else:
    st.subheader(f"🧪 {domain}")

    st.info(
        "This domain is planned but its simulation engine "
        "has not been implemented yet."
    )

    st.write("Future capabilities may include:")

    if domain == "Logistics & Delivery":
        st.write("- Delivery distance and fleet capacity")
        st.write("- Estimated route costs")
        st.write("- Delivery scenario comparison")

    elif domain == "Energy Management":
        st.write("- Energy demand and available supply")
        st.write("- Resource allocation scenarios")
        st.write("- Estimated consumption comparison")

    elif domain == "Emergency Planning":
        st.write("- Resource availability")
        st.write("- Incident demand scenarios")
        st.write("- Response capacity comparison")

# ---------- FOOTER ----------
st.divider()

left, right = st.columns(2)
left.markdown("**NEXORA AI**")
left.caption("Multi-Domain Simulation Platform")
right.caption("Prototype v0.1 | Local Development")
