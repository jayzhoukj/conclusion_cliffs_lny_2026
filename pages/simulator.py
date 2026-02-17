import streamlit as st
import pandas as pd

st.title("Cliffs Simulator — LNY 2026")

df = st.session_state["df"]
best_row = st.session_state["best_row"]
required_cycles = st.session_state["required_cycles"]
n_diamonds_per_cycle = st.session_state["n_diamonds_per_cycle"]
writing_multiplier = st.session_state["writing_multiplier"]
noto_postscript_multiplier = st.session_state["noto_postscript_multiplier"]
fantasy_postscript_multiplier = st.session_state["fantasy_postscript_multiplier"]
n_t2_mats = st.session_state["n_t2_mats"]
n_t3_mats = st.session_state["n_t3_mats"]
n_mallets = st.session_state["n_mallets"]
max_cycles_cap = st.session_state["max_cycles_cap"]

# --- Summary metrics ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Writing Multiplier", f"{writing_multiplier:.0f}x")
col2.metric("Noto Multiplier", f"{noto_postscript_multiplier:.0f}x")
col3.metric("Fantasy Multiplier", f"{fantasy_postscript_multiplier:.0f}x")
col4.metric("Diamonds per Cycle", f"{n_diamonds_per_cycle:.0f}")
col5.metric("Required Cycles", f"{required_cycles:.2f}")

# --- Optimal scenario metrics ---
col6, col7, col8 = st.columns(3)
col6.metric("Max Achievable Cycles", f"{best_row['max_cycles']:.2f}")
col7.metric(
    "Optimal Fantasy Postscript Hunts",
    f"T1 = {best_row['n_hunts_t1_fantasy_postscript']:.0f} / T2 = {best_row['n_hunts_t2_fantasy_postscript']:.0f}",
)
col8.metric("Total CC Used (Max Cycles)", f"{best_row['n_cc_used']:.0f}")

# --- Simulation results table ---
st.subheader("Simulation Results")
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False)
st.download_button("Download CSV", csv, "cliffs_lny2026_simulation_data.csv", "text/csv")

# --- Charts ---
st.subheader("Charts")

chart_df = df.set_index("n_hunts_t2_fantasy_postscript")

st.caption("Net Materials per Cycle")
st.line_chart(chart_df[["net_t2_mats", "net_t3_mats", "net_mallets"]])

st.caption("Max Cycles (T2, T3 & Mallets)")
capped_chart_df = chart_df[["n_cycles_t2", "n_cycles_t3", "n_cycles_mallets"]].clip(upper=max_cycles_cap)
st.line_chart(capped_chart_df)

st.caption("Condensed Creativity Used")
st.line_chart(chart_df[["n_cc_used"]])

# --- Materials over cycles chart ---
st.subheader("Materials Over Cycles")

selected_row = st.selectbox(
    "Fantasy Postscript T2 Hunts scenario",
    range(14),
    index=13,
    format_func=lambda x: f"T2 Hunts = {x} (T1 Hunts = {13 - x})",
)

row = df.iloc[selected_row]
net_t2 = row["net_t2_mats"]
net_t3 = row["net_t3_mats"]
net_m = row["net_mallets"]
max_cycle = int(min(row["n_cycles_t2"], row["n_cycles_t3"], row["n_cycles_mallets"], required_cycles)) + 1

cycles = list(range(max_cycle + 1))
t2_over_cycles = [n_t2_mats + net_t2 * c for c in cycles]
t3_over_cycles = [n_t3_mats + net_t3 * c for c in cycles]
mallets_over_cycles = [n_mallets + net_m * c for c in cycles]

projection_df = pd.DataFrame(
    {"T2 Materials": t2_over_cycles, "T3 Materials": t3_over_cycles, "Mallets": mallets_over_cycles},
    index=pd.Index(cycles, name="Cycle"),
)

st.line_chart(projection_df)
