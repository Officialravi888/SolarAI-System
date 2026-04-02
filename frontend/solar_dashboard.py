import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# ------------------- Page Configuration -------------------
st.set_page_config(page_title="SolarGreen Dashboard", layout="wide")
st.title("☀️ SolarGreen – Integrated Solar Management Dashboard")

# ------------------- Sidebar Navigation -------------------
menu = st.sidebar.radio(
    "📌 Menu",
    ["🏠 Home", "📦 Installation", "🚚 Logistics", "🔧 Maintenance", "🔋 Battery Management", "⚡ Consumption & Forecast"]
)

# ------------------- Dummy Data (Replace with your DB) -------------------
@st.cache_data
def load_installation_data():
    return pd.DataFrame({
        "Site": ["A", "B", "C", "D"],
        "Capacity_kW": [10, 25, 15, 30],
        "Install_Date": ["2024-01-10", "2024-02-15", "2024-03-20", "2024-04-05"],
        "Status": ["Completed", "Completed", "In Progress", "Scheduled"]
    })

@st.cache_data
def load_logistics():
    return pd.DataFrame({
        "Order_ID": ["L101", "L102", "L103"],
        "Item": ["Solar Panel", "Inverter", "Battery"],
        "Qty": [50, 10, 20],
        "Status": ["Shipped", "Pending", "Delivered"]
    })

@st.cache_data
def load_maintenance():
    return pd.DataFrame({
        "Site": ["A", "B", "C"],
        "Last_Service": ["2024-01-20", "2024-02-10", "2024-03-01"],
        "Next_Due": ["2024-07-20", "2024-08-10", "2024-09-01"],
        "Issue": ["None", "Inverter noise", "Cleaning needed"]
    })

@st.cache_data
def load_battery():
    return pd.DataFrame({
        "Battery_ID": ["B1", "B2", "B3"],
        "SoC_%": [85, 62, 94],
        "Health_%": [98, 87, 99],
        "Temp_C": [32, 35, 31]
    })

@st.cache_data
def load_consumption_history():
    dates = pd.date_range(start="2024-01-01", periods=90, freq="D")
    np.random.seed(42)
    consumption = 20 + 5 * np.sin(np.linspace(0, 3*np.pi, 90)) + np.random.normal(0, 2, 90)
    return pd.DataFrame({"Date": dates, "kWh": consumption})

# ------------------- Home Page -------------------
if menu == "🏠 Home":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔧 Active Sites", "4")
    col2.metric("⚡ Total Capacity (kW)", "80")
    col3.metric("🔋 Avg Battery SoC", "80%")
    col4.metric("📅 Next Maintenance", "In 5 days")
    st.info("👉 Select any section from the sidebar.")
    st.image("https://img.icons8.com/fluency/96/solar-panel.png", width=100)

# ------------------- Installation -------------------
elif menu == "📦 Installation":
    st.header("📦 Solar Installation Tracking")
    df_install = load_installation_data()
    st.dataframe(df_install, use_container_width=True)
    fig = px.bar(df_install, x="Site", y="Capacity_kW", color="Status", title="Installation by Capacity")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("➕ Add New Installation"):
        with st.form("new_install"):
            site = st.text_input("Site Name")
            cap = st.number_input("Capacity (kW)")
            date = st.date_input("Install Date")
            status = st.selectbox("Status", ["Scheduled", "In Progress", "Completed"])
            if st.form_submit_button("Add"):
                st.success("✅ Added in demo mode (connect with real DB)")

# ------------------- Logistics -------------------
elif menu == "🚚 Logistics":
    st.header("🚚 Logistics & Supply Chain")
    df_log = load_logistics()
    st.dataframe(df_log, use_container_width=True)
    fig = px.pie(df_log, names="Status", title="Order Status")
    st.plotly_chart(fig, use_container_width=True)

# ------------------- Maintenance -------------------
elif menu == "🔧 Maintenance":
    st.header("🔧 Predictive Maintenance")
    df_maint = load_maintenance()
    st.dataframe(df_maint, use_container_width=True)
    df_maint["Next_Due"] = pd.to_datetime(df_maint["Next_Due"])
    today = datetime.now().date()
    df_maint["Days_Left"] = (df_maint["Next_Due"].dt.date - today).dt.days
    fig = px.bar(df_maint, x="Site", y="Days_Left", title="Days Until Next Maintenance", color="Issue")
    st.plotly_chart(fig, use_container_width=True)

# ------------------- Battery Management -------------------
elif menu == "🔋 Battery Management":
    st.header("🔋 Battery Health & SoC")
    df_batt = load_battery()
    st.dataframe(df_batt, use_container_width=True)
    g1 = go.Figure()
    g1.add_trace(go.Bar(x=df_batt["Battery_ID"], y=df_batt["SoC_%"], name="State of Charge %", marker_color="green"))
    g1.add_trace(go.Bar(x=df_batt["Battery_ID"], y=df_batt["Health_%"], name="Health %", marker_color="blue"))
    g1.update_layout(barmode="group", title="Battery SoC & Health")
    st.plotly_chart(g1, use_container_width=True)

# ------------------- Consumption & Forecast -------------------
elif menu == "⚡ Consumption & Forecast":
    st.header("⚡ Electricity Consumption History & Forecast")
    df_cons = load_consumption_history()
    st.subheader("📈 Last 90 Days Consumption")
    fig_hist = px.line(df_cons, x="Date", y="kWh", title="Daily Electricity Consumption")
    st.plotly_chart(fig_hist, use_container_width=True)

    # Forecast model (Holt-Winters)
    st.subheader("🔮 Next 7 Days Forecast")
    series = df_cons.set_index("Date")["kWh"]
    model = ExponentialSmoothing(series, trend="add", seasonal=None, initialization_method="estimated")
    fit = model.fit()
    forecast = fit.forecast(7)
    forecast_dates = [series.index[-1] + timedelta(days=i+1) for i in range(7)]

    df_forecast = pd.DataFrame({"Date": forecast_dates, "Forecast_kWh": forecast})
    fig_fore = go.Figure()
    fig_fore.add_trace(go.Scatter(x=series.index, y=series, mode="lines", name="Historical"))
    fig_fore.add_trace(go.Scatter(x=forecast_dates, y=forecast, mode="lines+markers", name="Forecast", line=dict(dash="dot")))
    fig_fore.update_layout(title="Electricity Consumption Forecast", xaxis_title="Date", yaxis_title="kWh")
    st.plotly_chart(fig_fore, use_container_width=True)

    st.dataframe(df_forecast)
    st.info("💡 Forecast based on Holt-Winters model. You can use LSTM or other ML models for improved predictions.")