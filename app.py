import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NEXORA AI", page_icon="🌐", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1250px;}
.hero {padding: 25px; border-radius: 18px; background: linear-gradient(120deg,#14213d,#283e70); color: white; margin-bottom: 22px;}
.hero h1 {font-size: 42px; margin-bottom: 5px;}
.hero p {font-size: 17px; color: #dbeafe;}
[data-testid="stMetric"] {background: rgba(128,128,128,.08); padding: 12px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>NEXORA AI</h1>
<p>Simulate. Predict. Optimize.</p>
<p>Multi-Domain Scenario Simulation Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("NEXORA AI")
st.sidebar.caption("Simulation Control Center")
domain = st.sidebar.selectbox("Choose a domain", [
    "Traffic & Transportation", "Business & Inventory",
    "Logistics & Delivery", "Energy Management", "Emergency Planning"
])
st.sidebar.divider()
st.sidebar.caption("Prototype v0.2")

st.header("Simulation Workspace")
st.write("Adjust the scenario inputs and compare the baseline with your proposed plan.")

def show_chart(data, title, x="Scenario", y=None, color="Scenario"):
    fig = px.bar(data, x=x, y=y, color=color, barmode="group", title=title, text_auto=".2s")
    fig.update_layout(legend_title_text="", margin=dict(t=55, b=20))
    st.plotly_chart(fig, use_container_width=True)

def show_result(rows, title="Scenario comparison"):
    st.subheader(title)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

if domain == "Traffic & Transportation":
    st.subheader("🚦 Traffic Scenario Simulator")
    a, b = st.columns(2)
    with a: demand = st.slider("Traffic demand (%)", 10, 100, 65)
    with b: capacity = st.slider("Road capacity (%)", 10, 120, 75)
    utilization = round(demand / capacity * 100) if capacity else 0
    overload = max(0, demand-capacity)
    c1,c2,c3 = st.columns(3)
    c1.metric("Traffic demand", f"{demand}%")
    c2.metric("Road capacity", f"{capacity}%")
    c3.metric("Capacity utilization", f"{utilization}%")
    show_chart(pd.DataFrame({"Metric":["Demand","Capacity"],"Value":[demand,capacity]}),"Demand vs available capacity","Metric","Value","Metric")
    if overload: st.warning(f"Demand exceeds capacity by {overload} percentage points.")
    else: st.success("Selected demand is within road capacity.")

elif domain == "Business & Inventory":
    st.subheader("📦 Business & Inventory Simulator")
    a,b = st.columns(2)
    with a: stock = st.slider("Available inventory (units)",0,2000,400)
    with b: demand = st.slider("Expected customer demand (units)",0,2000,550)
    fulfilled = min(stock,demand)
    rate = round(fulfilled/demand*100) if demand else 100
    shortage=max(0,demand-stock); surplus=max(0,stock-demand)
    c1,c2,c3=st.columns(3)
    c1.metric("Available stock",f"{stock:,}")
    c2.metric("Expected demand",f"{demand:,}")
    c3.metric("Demand fulfilled",f"{rate}%")
    show_chart(pd.DataFrame({"Metric":["Stock","Demand","Fulfilled"],"Units":[stock,demand,fulfilled]}),"Inventory and demand","Metric","Units","Metric")
    if shortage: st.warning(f"Potential stock shortage: {shortage} units. Consider replenishment.")
    elif surplus: st.info(f"Potential surplus: {surplus} units. Review future purchasing.")
    else: st.success("Inventory exactly matches expected demand.")

elif domain == "Logistics & Delivery":
    st.subheader("🚚 Logistics & Delivery Simulator")
    st.caption("Estimate fleet requirements, delivery cost and operational capacity.")
    a,b,c = st.columns(3)
    with a: orders = st.slider("Daily deliveries",50,2000,500,step=50)
    with b: fleet = st.slider("Available vehicles",1,100,20)
    with c: capacity_per_vehicle = st.slider("Deliveries per vehicle",5,100,30)
    d,e,f = st.columns(3)
    with d: avg_distance = st.slider("Average route distance (km)",1,100,20)
    with e: cost_per_km = st.slider("Operating cost (₹ / km)",1,100,18)
    with f: shift_hours = st.slider("Working hours per vehicle",4,16,8)
    total_capacity = fleet*capacity_per_vehicle
    required_vehicles = (orders+capacity_per_vehicle-1)//capacity_per_vehicle
    utilization = round(orders/total_capacity*100) if total_capacity else 0
    trips = (orders+capacity_per_vehicle-1)//capacity_per_vehicle
    total_km = orders*avg_distance
    estimated_cost = total_km*cost_per_km
    per_order = estimated_cost/orders if orders else 0
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Fleet capacity",f"{total_capacity:,} deliveries")
    c2.metric("Fleet utilization",f"{utilization}%")
    c3.metric("Vehicles required",f"{required_vehicles}")
    c4.metric("Estimated daily cost",f"₹{estimated_cost:,.0f}")
    show_chart(pd.DataFrame({"Metric":["Daily orders","Fleet capacity"],"Deliveries":[orders,total_capacity]}),"Delivery demand vs fleet capacity","Metric","Deliveries","Metric")
    show_result([
        {"Metric":"Daily deliveries","Current scenario":orders,"Capacity / estimate":total_capacity},
        {"Metric":"Vehicles required","Current scenario":required_vehicles,"Capacity / estimate":fleet},
        {"Metric":"Estimated distance (vehicle-km)","Current scenario":total_km,"Capacity / estimate":None},
        {"Metric":"Estimated cost per delivery (₹)","Current scenario":round(per_order,2),"Capacity / estimate":None},
        {"Metric":"Working hours available per vehicle","Current scenario":shift_hours,"Capacity / estimate":None}
    ])
    if orders>total_capacity:
        st.error(f"Fleet overload: {orders-total_capacity} deliveries exceed current fleet capacity. Add at least {required_vehicles-fleet} vehicle(s) at the selected capacity.")
    else:
        st.success("Fleet capacity is sufficient for the selected delivery demand.")
    st.info("Planning insight: consolidate nearby orders and improve route density to reduce vehicle-kilometres and cost. Estimates assume the entered average distance per delivery.")

elif domain == "Energy Management":
    st.subheader("⚡ Energy Management Simulator")
    st.caption("Compare electricity demand, supply mix, grid dependence and estimated operating cost.")
    a,b,c = st.columns(3)
    with a: demand = st.slider("Daily energy demand (kWh)",100,50000,12000,step=100)
    with b: supply = st.slider("Available energy supply (kWh)",100,50000,14000,step=100)
    with c: renewable_share = st.slider("Renewable share of supply (%)",0,100,35)
    d,e = st.columns(2)
    with d: tariff = st.slider("Grid tariff (₹ / kWh)",1,30,8)
    with e: reduction = st.slider("Demand reduction target (%)",0,50,10)
    adjusted_demand = round(demand*(1-reduction/100))
    shortage=max(0,adjusted_demand-supply)
    surplus=max(0,supply-adjusted_demand)
    grid_energy=max(0,adjusted_demand-round(min(supply,adjusted_demand)*renewable_share/100))
    grid_cost=grid_energy*tariff
    renewable_energy=round(min(supply,adjusted_demand)*renewable_share/100)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Adjusted demand",f"{adjusted_demand:,} kWh",f"-{reduction}%")
    c2.metric("Supply gap",f"{shortage:,} kWh")
    c3.metric("Renewable contribution",f"{renewable_energy:,} kWh")
    c4.metric("Estimated grid cost",f"₹{grid_cost:,.0f}")
    show_chart(pd.DataFrame({"Source":["Renewable","Grid"],"Energy (kWh)":[renewable_energy,grid_energy]}),"Estimated energy mix","Source","Energy (kWh)","Source")
    show_result([
        {"Metric":"Original demand (kWh)","Baseline":demand,"Optimized scenario":adjusted_demand},
        {"Metric":"Available supply (kWh)","Baseline":supply,"Optimized scenario":supply},
        {"Metric":"Energy shortage (kWh)","Baseline":max(0,demand-supply),"Optimized scenario":shortage},
        {"Metric":"Renewable energy (kWh)","Baseline":round(min(supply,demand)*renewable_share/100),"Optimized scenario":renewable_energy},
        {"Metric":"Estimated grid cost (₹)","Baseline":max(0,demand-round(min(supply,demand)*renewable_share/100))*tariff,"Optimized scenario":grid_cost}
    ])
    if shortage: st.error(f"Energy shortfall of {shortage:,} kWh remains. Increase supply, shift loads or reduce demand further.")
    else: st.success(f"Supply covers adjusted demand with {surplus:,} kWh spare capacity.")
    st.info("Planning insight: shift flexible loads away from peak periods and increase renewable availability where practical. Cost is an estimate based on the entered flat tariff.")

elif domain == "Emergency Planning":
    st.subheader("🚨 Emergency Response Planning Simulator")
    st.caption("Estimate response capacity, team workload and resource coverage for an incident scenario.")
    a,b,c = st.columns(3)
    with a: incidents = st.slider("Expected incidents",1,500,80)
    with b: teams = st.slider("Available response teams",1,100,15)
    with c: team_capacity = st.slider("Incidents each team can handle",1,30,5)
    d,e,f = st.columns(3)
    with d: avg_response = st.slider("Average response time (minutes)",2,120,25)
    with e: resources = st.slider("Available resource units",10,2000,300)
    with f: resources_per_incident = st.slider("Resources needed per incident",1,20,3)
    response_capacity=teams*team_capacity
    coverage=min(100,round(response_capacity/incidents*100)) if incidents else 100
    resource_need=incidents*resources_per_incident
    resource_coverage=min(100,round(resources/resource_need*100)) if resource_need else 100
    team_workload=round(incidents/teams,1) if teams else 0
    uncovered=max(0,incidents-response_capacity)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Incident demand",incidents)
    c2.metric("Response capacity",response_capacity)
    c3.metric("Team coverage",f"{coverage}%")
    c4.metric("Resource coverage",f"{resource_coverage}%")
    show_chart(pd.DataFrame({"Metric":["Incident demand","Team response capacity"],"Incidents":[incidents,response_capacity]}),"Incident demand vs response capacity","Metric","Incidents","Metric")
    show_result([
        {"Metric":"Expected incidents","Scenario value":incidents},
        {"Metric":"Available response teams","Scenario value":teams},
        {"Metric":"Incidents per team","Scenario value":team_workload},
        {"Metric":"Uncovered incidents","Scenario value":uncovered},
        {"Metric":"Estimated response time (minutes)","Scenario value":avg_response},
        {"Metric":"Resources required","Scenario value":resource_need},
        {"Metric":"Resources available","Scenario value":resources}
    ])
    if uncovered or resource_coverage<100:
        st.warning(f"Capacity gap: {uncovered} incident(s) exceed team capacity; resource coverage is {resource_coverage}%. Consider staging extra teams and supplies.")
    else:
        st.success("Current teams and resources cover the selected incident scenario.")
    st.info("Planning insight: stage teams near high-risk zones, maintain reserve supplies and reassess response times as conditions change. This is a planning model, not a live emergency dispatch system.")

st.divider()
left,right=st.columns(2)
left.markdown("**NEXORA AI**")
left.caption("Multi-Domain Scenario Simulation Platform")
right.caption("Prototype v0.2 | Illustrative planning estimates")
