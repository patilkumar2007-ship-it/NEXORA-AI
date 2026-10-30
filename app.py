import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NEXORA AI", page_icon="🌐", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 1.5rem;}
.hero {padding: 24px; border-radius: 16px; background: linear-gradient(120deg,#14213d,#31558a); color: white;}
.hero h1 {font-size: 40px; margin: 0;}
.hero p {color: #e5efff; margin: 5px 0 0 0;}
div[data-testid="stMetric"] {background: rgba(128,128,128,.08); padding: 12px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>NEXORA AI</h1><p>Simulate. Predict. Optimize.</p><p>Multi-Domain Scenario Simulation Platform</p></div>', unsafe_allow_html=True)

st.sidebar.title("🌐 NEXORA AI")
st.sidebar.caption("Simulation Control Center")
domain = st.sidebar.selectbox("Select simulation", [
    "Traffic & Transportation",
    "Business & Inventory",
    "Logistics & Delivery",
    "Energy Management",
    "Emergency Planning"
])
st.sidebar.divider()
st.sidebar.caption("Prototype v0.3")

st.title(domain)
st.write("Change the inputs to explore a scenario. Results are illustrative planning estimates, not live operational predictions.")

def metrics(items):
    cols = st.columns(len(items))
    for col, (label, value, help_text) in zip(cols, items):
        col.metric(label, value, help=help_text)

def bar_chart(labels, values, title, y_title):
    frame = pd.DataFrame({"Category": labels, "Value": values})
    fig = px.bar(frame, x="Category", y="Value", color="Category", title=title)
    fig.update_layout(showlegend=False, yaxis_title=y_title, xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

def comparison_table(rows):
    st.subheader("Scenario breakdown")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

if domain == "Traffic & Transportation":
    st.subheader("🚦 Traffic capacity planner")
    a, b = st.columns(2)
    demand = a.slider("Traffic demand (%)", 10, 100, 65)
    capacity = b.slider("Road capacity (%)", 10, 120, 75)
    utilization = round(demand / capacity * 100) if capacity else 0
    gap = max(0, demand - capacity)
    metrics([("Traffic demand", f"{demand}%","Selected demand"),("Road capacity",f"{capacity}%","Available capacity"),("Capacity utilization",f"{utilization}%","Demand divided by capacity")])
    bar_chart(["Demand","Capacity"],[demand,capacity],"Traffic demand vs road capacity","Percent")
    comparison_table([{"Metric":"Demand (%)","Selected scenario":demand},{"Metric":"Capacity (%)","Selected scenario":capacity},{"Metric":"Overload (percentage points)","Selected scenario":gap}])
    if gap: st.error(f"Over capacity by {gap} percentage points. Consider traffic diversion or capacity improvements.")
    else: st.success("Demand is within the selected road capacity.")

elif domain == "Business & Inventory":
    st.subheader("📦 Inventory and demand planner")
    a,b = st.columns(2)
    stock = a.slider("Available inventory (units)",0,5000,400)
    demand = b.slider("Expected demand (units)",0,5000,550)
    fulfilled = min(stock,demand)
    fill_rate = round(fulfilled/demand*100) if demand else 100
    shortage = max(0,demand-stock)
    surplus = max(0,stock-demand)
    metrics([("Available stock",f"{stock:,}","Inventory units"),("Expected demand",f"{demand:,}","Forecast input"),("Demand fill rate",f"{fill_rate}%","Share of demand that can be fulfilled"),("Shortage",f"{shortage:,} units","Unfulfilled demand")])
    bar_chart(["Stock","Demand","Fulfilled"],[stock,demand,fulfilled],"Inventory position","Units")
    comparison_table([{"Metric":"Available stock","Value":stock},{"Metric":"Expected demand","Value":demand},{"Metric":"Fulfilled demand","Value":fulfilled},{"Metric":"Surplus","Value":surplus},{"Metric":"Shortage","Value":shortage}])
    if shortage: st.warning(f"Replenishment suggestion: arrange at least {shortage} additional units.")
    elif surplus: st.info(f"Potential surplus: {surplus} units. Review purchasing to avoid overstock.")
    else: st.success("Inventory exactly matches demand.")

elif domain == "Logistics & Delivery":
    st.subheader("🚚 Fleet and delivery planner")
    a,b,c = st.columns(3)
    orders = a.slider("Daily delivery orders",1,3000,500,step=25)
    vehicles = b.slider("Available vehicles",1,150,20)
    capacity_each = c.slider("Deliveries per vehicle per day",1,150,30)
    d,e,f = st.columns(3)
    distance = d.slider("Average distance per delivery (km)",1,150,20)
    cost_km = e.slider("Operating cost per km (₹)",1,150,18)
    hours = f.slider("Operating hours per vehicle",1,24,8)
    fleet_capacity = vehicles * capacity_each
    vehicles_needed = (orders + capacity_each - 1) // capacity_each
    utilization = round(orders/fleet_capacity*100) if fleet_capacity else 0
    total_distance = orders * distance
    total_cost = total_distance * cost_km
    metrics([("Fleet capacity",f"{fleet_capacity:,} orders","Vehicles multiplied by daily capacity"),("Fleet utilization",f"{utilization}%","Orders divided by fleet capacity"),("Vehicles needed",str(vehicles_needed),"At the selected per-vehicle capacity"),("Estimated daily cost",f"₹{total_cost:,.0f}","Distance multiplied by cost per km")])
    bar_chart(["Orders","Fleet capacity"],[orders,fleet_capacity],"Delivery demand vs fleet capacity","Deliveries")
    comparison_table([{"Metric":"Daily orders","Value":orders},{"Metric":"Fleet capacity","Value":fleet_capacity},{"Metric":"Vehicles available","Value":vehicles},{"Metric":"Vehicles required","Value":vehicles_needed},{"Metric":"Total vehicle-kilometres (estimate)","Value":total_distance},{"Metric":"Estimated cost per order (₹)","Value":round(total_cost/orders,2)},{"Metric":"Working hours per vehicle","Value":hours}])
    if orders > fleet_capacity: st.error(f"Fleet shortfall: {orders-fleet_capacity} orders. Add at least {vehicles_needed-vehicles} vehicle(s) at the selected capacity.")
    else: st.success("Available fleet capacity covers the selected order volume.")
    st.info("Planning idea: group nearby deliveries and optimize routes to reduce travel distance. Distance and cost are simplified estimates.")

elif domain == "Energy Management":
    st.subheader("⚡ Energy demand and supply planner")
    a,b,c = st.columns(3)
    demand = a.slider("Daily energy demand (kWh)",100,100000,12000,step=100)
    supply = b.slider("Available energy supply (kWh)",100,100000,14000,step=100)
    renewable = c.slider("Renewable share of available supply (%)",0,100,35)
    d,e = st.columns(2)
    reduction = d.slider("Demand reduction target (%)",0,60,10)
    tariff = e.slider("Grid electricity tariff (₹/kWh)",1,50,8)
    adjusted = round(demand*(1-reduction/100))
    renewable_energy = round(min(supply,adjusted)*renewable/100)
    grid_energy = max(0,adjusted-renewable_energy)
    shortage = max(0,adjusted-supply)
    grid_cost = grid_energy*tariff
    metrics([("Adjusted demand",f"{adjusted:,} kWh","After demand reduction"),("Supply gap",f"{shortage:,} kWh","Demand not covered by total supply"),("Renewable contribution",f"{renewable_energy:,} kWh","Estimated renewable energy used"),("Estimated grid cost",f"₹{grid_cost:,.0f}","Grid energy multiplied by tariff")])
    bar_chart(["Renewable","Grid"],[renewable_energy,grid_energy],"Estimated energy mix","Energy (kWh)")
    comparison_table([{"Metric":"Original demand (kWh)","Value":demand},{"Metric":"Adjusted demand (kWh)","Value":adjusted},{"Metric":"Available supply (kWh)","Value":supply},{"Metric":"Renewable energy used (kWh)","Value":renewable_energy},{"Metric":"Grid energy required (kWh)","Value":grid_energy},{"Metric":"Energy shortfall (kWh)","Value":shortage},{"Metric":"Estimated grid cost (₹)","Value":grid_cost}])
    if shortage: st.error(f"Supply gap of {shortage:,} kWh remains. Increase supply or reduce demand further.")
    else: st.success(f"Supply covers adjusted demand with {supply-adjusted:,} kWh spare.")
    st.info("Planning idea: shift flexible loads away from peak hours and increase renewable availability. This uses a simplified flat-tariff estimate.")

elif domain == "Emergency Planning":
    st.subheader("🚨 Emergency response capacity planner")
    a,b,c = st.columns(3)
    incidents = a.slider("Expected incidents",1,1000,80)
    teams = b.slider("Available response teams",1,200,15)
    team_capacity = c.slider("Incidents handled per team",1,50,5)
    d,e,f = st.columns(3)
    response_time = d.slider("Average response time (minutes)",1,180,25)
    resources = e.slider("Available resource units",1,10000,300)
    resources_each = f.slider("Resource units needed per incident",1,50,3)
    capacity = teams*team_capacity
    uncovered = max(0,incidents-capacity)
    team_coverage = min(100,round(capacity/incidents*100))
    needed_resources = incidents*resources_each
    resource_coverage = min(100,round(resources/needed_resources*100)) if needed_resources else 100
    workload = round(incidents/teams,1)
    metrics([("Incident demand",str(incidents),"Expected incidents"),("Team capacity",str(capacity),"Teams multiplied by handling capacity"),("Team coverage",f"{team_coverage}%","Share of incidents within team capacity"),("Resource coverage",f"{resource_coverage}%","Available resources divided by requirement")])
    bar_chart(["Incident demand","Team capacity"],[incidents,capacity],"Emergency demand vs response capacity","Incidents")
    comparison_table([{"Metric":"Expected incidents","Value":incidents},{"Metric":"Available teams","Value":teams},{"Metric":"Incidents per team","Value":workload},{"Metric":"Uncovered incidents","Value":uncovered},{"Metric":"Average response time (minutes)","Value":response_time},{"Metric":"Resources required","Value":needed_resources},{"Metric":"Resources available","Value":resources}])
    if uncovered or resource_coverage < 100: st.warning(f"Capacity gap: {uncovered} incident(s) exceed team capacity; resource coverage is {resource_coverage}%. Consider additional teams and reserve supplies.")
    else: st.success("Selected teams and resources cover the scenario.")
    st.info("Planning idea: stage teams near risk zones and maintain reserve supplies. This is a simulation, not a live emergency dispatch system.")

st.divider()
left,right = st.columns(2)
left.markdown("**NEXORA AI**")
left.caption("Multi-Domain Scenario Simulation Platform")
right.caption("Prototype v0.3 | Illustrative planning model")
