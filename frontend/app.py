import streamlit as st
import pandas as pd

st.set_page_config(page_title="Solar Dashboard", layout="wide")

st.title("☀️ Solar Energy Dashboard (India)")


@st.cache_data
def load_data():
    return pd.read_csv("data/solar1.csv")

df = load_data()

st.sidebar.header("🔍 Filter")

selected_state = st.sidebar.multiselect(
    "Select State",
    options=df["state"].unique(),
    default=df["state"].unique()
)

filtered_df = df[df["state"].isin(selected_state)].copy()


col1, col2, col3 = st.columns(3)

col1.metric("⚡ Total Generation", int(filtered_df["solar_generation"].sum()))
col2.metric("📈 Average", round(filtered_df["solar_generation"].mean(), 2))
col3.metric("🏙️ Total States", filtered_df["state"].nunique())


st.subheader("📄 Solar Data Table")
st.dataframe(filtered_df, width='stretch')


st.subheader("📊 State-wise Solar Generation")
state_group = filtered_df.groupby("state")["solar_generation"].sum()
st.bar_chart(state_group)

# -----------------------------
# Line Chart
# -----------------------------
st.subheader("📈 Generation Trend")
st.line_chart(filtered_df["solar_generation"])

# -----------------------------
# Solar Panel Image
# -----------------------------
st.subheader("🔆 Solar Panel Overview")

st.image(
    "D:\Ai_06_month_placement\solar-project\img\images.jpg",
    caption="Solar Panels",
    width='stretch'
)

# -----------------------------
# Panel Calculation
# -----------------------------
st.subheader("⚙️ Solar Panel Requirement")

panel_df = filtered_df.copy()
panel_df["panels_required"] = panel_df["solar_generation"] / 0.4

st.dataframe(panel_df[["state", "solar_generation", "panels_required"]], width='stretch')

# -----------------------------
# Top State (Safe)
# -----------------------------
st.subheader("🏆 Top Performing State")

if not panel_df.empty:
    top_state = panel_df.sort_values("solar_generation", ascending=False).iloc[0]
    st.success(f"{top_state['state']} is leading with {top_state['solar_generation']} kW 🚀")
else:
    st.warning("No data available")

# -----------------------------
# Cost Calculation
# -----------------------------
st.subheader("💰 Installation Cost Estimation")

cost_per_panel = st.number_input("Enter Cost per Panel (₹)", value=20000)

cost_df = panel_df.copy()
cost_df["total_cost"] = cost_df["panels_required"] * cost_per_panel

# Round values
cost_df["panels_required"] = cost_df["panels_required"].round(0)
cost_df["total_cost"] = cost_df["total_cost"].round(0)

st.dataframe(cost_df[["state", "panels_required", "total_cost"]], width='stretch')

# Total Cost
total_cost = int(cost_df["total_cost"].sum())
st.success(f"💸 Total Estimated Cost: ₹{total_cost:,}")