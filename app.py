import streamlit as st
import pandas as pd
import numpy as np


def compute_multiplier(cc, white_candle, red_candle):
    return 1 + (1 * cc + 1 * white_candle + 2 * red_candle)


def run_simulation(
    n_hunts_t1_writing,
    n_hunts_t2_writing,
    writing_multiplier,
    cc_writing,
    n_hunts_t3_noto_postscript,
    bk,
    noto_postscript_multiplier,
    cc_noto,
    fantasy_postscript_multiplier,
    fantasy_diamond_multiplier,
    cc_fantasy,
    n_t2_mats,
    n_t3_mats,
    required_diamonds,
    available_diamonds,
):
    n_diamonds_per_cycle = 13 * fantasy_diamond_multiplier
    required_cycles = (
        (required_diamonds - available_diamonds) / n_diamonds_per_cycle
        if n_diamonds_per_cycle > 0
        else 0
    )

    all_simulation_data = []

    for n_hunts_t2_fantasy_postscript in range(14):
        n_hunts_t1_fantasy_postscript = 13 - n_hunts_t2_fantasy_postscript

        # T2 mats
        n_hunts_t2_total = n_hunts_t2_writing + n_hunts_t2_fantasy_postscript
        t2_mats_used = n_hunts_t2_total * 12
        t2_mats_farmed = (n_hunts_t1_writing * 1.5 * writing_multiplier) + (
            n_hunts_t1_fantasy_postscript * 3 * fantasy_postscript_multiplier
        )
        net_t2_mats = t2_mats_farmed - t2_mats_used
        n_cycles_t2 = 999 if net_t2_mats > 0 else (n_t2_mats / -net_t2_mats if net_t2_mats != 0 else 999)

        # T3 mats
        n_hunts_t3_total = n_hunts_t3_noto_postscript
        t3_mats_used = n_hunts_t3_total * 30 * (1 / (1 + bk))
        t3_mats_farmed = (n_hunts_t2_writing * 1.2 * writing_multiplier) + (
            n_hunts_t2_fantasy_postscript * 3 * fantasy_postscript_multiplier
        )
        net_t3_mats = t3_mats_farmed - t3_mats_used
        n_cycles_t3 = 999 if net_t3_mats > 0 else (n_t3_mats / -net_t3_mats if net_t3_mats != 0 else 999)

        # CC used
        cc_hunts_per_cycle = (
            cc_writing * (n_hunts_t1_writing + n_hunts_t2_writing)
            + cc_noto * n_hunts_t3_noto_postscript
            + cc_fantasy * 13
        )
        n_cc_used = min(n_cycles_t2, n_cycles_t3, required_cycles) * cc_hunts_per_cycle

        all_simulation_data.append(
            {
                "n_hunts_t1_fantasy_postscript": n_hunts_t1_fantasy_postscript,
                "n_hunts_t2_fantasy_postscript": n_hunts_t2_fantasy_postscript,
                "n_hunts_t2_writing": n_hunts_t2_writing,
                "n_hunts_t2_total": n_hunts_t2_total,
                "t2_mats_used": t2_mats_used,
                "t2_mats_farmed": t2_mats_farmed,
                "net_t2_mats": net_t2_mats,
                "n_cycles_t2": n_cycles_t2,
                "n_hunts_t3_total": n_hunts_t3_total,
                "t3_mats_used": t3_mats_used,
                "t3_mats_farmed": t3_mats_farmed,
                "net_t3_mats": net_t3_mats,
                "n_cycles_t3": n_cycles_t3,
                "n_cc_used": n_cc_used,
            }
        )

    return pd.DataFrame(all_simulation_data), n_diamonds_per_cycle, required_cycles


# --- Page config ---
st.set_page_config(page_title="Cliffs Simulator — LNY 2026", page_icon="⛰️", layout="wide")
st.title("Cliffs Simulator — LNY 2026")

# --- Sidebar parameters ---
st.sidebar.header("Writing Phase")

n_hunts_t1_writing = st.sidebar.number_input("T1 Writing Hunts", min_value=0, value=80, step=10)
n_hunts_t2_writing = st.sidebar.number_input("T2 Writing Hunts", min_value=0, value=40, step=10)
cc_writing = st.sidebar.checkbox("Condensed Creativity (Writing)", value=True)
candle_writing = st.sidebar.radio("LNY 2026 Candle (Writing)", ["None", "White Candle", "Red Candle"], index=0)
writing_multiplier = compute_multiplier(cc_writing, candle_writing == "White Candle", candle_writing == "Red Candle")

st.sidebar.header("Postscript Phase (Noto)")

n_hunts_t3_noto_postscript = st.sidebar.number_input("Noto Charging Hunts (T3)", min_value=0, value=13, step=1)
bk = st.sidebar.checkbox("Baitkeep Charm (T3 Cheese)", value=True)
cc_noto = st.sidebar.checkbox("Condensed Creativity (Noto)", value=True)
candle_noto = st.sidebar.radio("LNY 2026 Candle (Noto)", ["None", "White Candle", "Red Candle"], index=1)
noto_postscript_multiplier = compute_multiplier(cc_noto, candle_noto == "White Candle", candle_noto == "Red Candle")

st.sidebar.header("Postscript Phase (Fantasy)")

cc_fantasy = st.sidebar.checkbox("Condensed Creativity (Fantasy)", value=True)
candle_fantasy = st.sidebar.radio("LNY 2026 Candle (Fantasy)", ["None", "White Candle", "Red Candle"], index=2)
fantasy_postscript_multiplier = compute_multiplier(cc_fantasy, candle_fantasy == "White Candle", candle_fantasy == "Red Candle")
fantasy_diamond_multiplier = 1 + (1 * (candle_fantasy == "White Candle") + 2 * (candle_fantasy == "Red Candle"))

st.sidebar.header("Materials & Diamonds")

n_t2_mats = st.sidebar.number_input("Available T2 Materials", min_value=0, value=1000, step=1)
n_t3_mats = st.sidebar.number_input("Available T3 Materials", min_value=0, value=500, step=1)
required_diamonds = st.sidebar.number_input("Required Diamonds", min_value=0, value=355, step=1)
available_diamonds = st.sidebar.number_input("Available Diamonds", min_value=0, value=0, step=1)

st.sidebar.header("Chart Settings")
max_cycles_cap = st.sidebar.number_input("Max Cycles Cap (for charts)", min_value=1, value=30, step=1)

# --- Run simulation ---
df, n_diamonds_per_cycle, required_cycles = run_simulation(
    n_hunts_t1_writing,
    n_hunts_t2_writing,
    writing_multiplier,
    cc_writing,
    n_hunts_t3_noto_postscript,
    bk,
    noto_postscript_multiplier,
    cc_noto,
    fantasy_postscript_multiplier,
    fantasy_diamond_multiplier,
    cc_fantasy,
    n_t2_mats,
    n_t3_mats,
    required_diamonds,
    available_diamonds,
)

# --- Summary metrics ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Writing Multiplier", f"{writing_multiplier:.0f}x")
col2.metric("Noto Multiplier", f"{noto_postscript_multiplier:.0f}x")
col3.metric("Fantasy Multiplier", f"{fantasy_postscript_multiplier:.0f}x")
col4.metric("Diamonds per Cycle", f"{n_diamonds_per_cycle:.0f}")
col5.metric("Required Cycles", f"{required_cycles:.2f}")

# --- Optimal scenario metrics ---
df["max_cycles"] = df[["n_cycles_t2", "n_cycles_t3"]].min(axis=1)
best_idx = df["max_cycles"].idxmax()
best_row = df.loc[best_idx]

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
st.line_chart(chart_df[["net_t2_mats", "net_t3_mats"]])

st.caption("Max Cycles (T2 & T3)")
capped_chart_df = chart_df[["n_cycles_t2", "n_cycles_t3"]].clip(upper=max_cycles_cap)
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
max_cycle = int(min(row["n_cycles_t2"], row["n_cycles_t3"], required_cycles)) + 1

cycles = list(range(max_cycle + 1))
t2_over_cycles = [n_t2_mats + net_t2 * c for c in cycles]
t3_over_cycles = [n_t3_mats + net_t3 * c for c in cycles]

projection_df = pd.DataFrame(
    {"T2 Materials": t2_over_cycles, "T3 Materials": t3_over_cycles},
    index=pd.Index(cycles, name="Cycle"),
)

st.line_chart(projection_df)
