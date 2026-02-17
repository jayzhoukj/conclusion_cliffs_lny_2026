import streamlit as st
import pandas as pd
import numpy as np

CANDLE_OPTIONS = ["None", "White Candle", "Red Candle"]


def qp_int(key, default, min_value=0):
    """Read an integer query parameter, falling back to default."""
    val = st.query_params.get(key)
    if val is not None:
        try:
            return max(int(val), min_value)
        except (ValueError, TypeError):
            pass
    return default


def qp_bool(key, default):
    """Read a boolean query parameter (1/0), falling back to default."""
    val = st.query_params.get(key)
    if val is not None:
        return val == "1"
    return default


def qp_radio_index(key, default, max_index=2):
    """Read a radio button index query parameter, falling back to default."""
    val = st.query_params.get(key)
    if val is not None:
        try:
            v = int(val)
            if 0 <= v <= max_index:
                return v
        except (ValueError, TypeError):
            pass
    return default


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
    n_mallets,
    noto_break_block,
    fantasy_postscript_break_block,
    fantasy_writing_short_only,
    fantasy_postscript_extend,
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

        # Mallets
        noto_extend_ps_probability = 0.2
        mallets_used = (
            noto_break_block * 30
            + 19  # noto writing
            + noto_extend_ps_probability * 30
            + fantasy_postscript_break_block * 30
            + 5.18 * 5  # fantasy writing (med / short)
            + fantasy_writing_short_only * ((12.52 - 5.18) * 5)
            + fantasy_postscript_extend * 30
        )
        no_extend_prob = 0.5
        avg_noto_ps_hunts = (
            (no_extend_prob / (no_extend_prob + noto_extend_ps_probability)) * 10
            + (noto_extend_ps_probability / (no_extend_prob + noto_extend_ps_probability)) * 13
        )
        mallets_farmed = (
            0.6 * noto_postscript_multiplier * avg_noto_ps_hunts
            + 2.5 * fantasy_postscript_multiplier * 13
        )
        net_mallets = mallets_farmed - mallets_used
        n_cycles_mallets = 999 if net_mallets >= 0 else (n_mallets / -net_mallets if net_mallets != 0 else 999)

        # CC used
        cc_hunts_per_cycle = (
            cc_writing * (n_hunts_t1_writing + n_hunts_t2_writing)
            + cc_noto * n_hunts_t3_noto_postscript
            + cc_fantasy * 13
        )
        n_cc_used = min(n_cycles_t2, n_cycles_t3, n_cycles_mallets, required_cycles) * cc_hunts_per_cycle

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
                "mallets_used": mallets_used,
                "mallets_farmed": mallets_farmed,
                "net_mallets": net_mallets,
                "n_cycles_mallets": n_cycles_mallets,
                "n_cc_used": n_cc_used,
            }
        )

    return pd.DataFrame(all_simulation_data), n_diamonds_per_cycle, required_cycles


# --- Page config & navigation ---
st.set_page_config(page_title="Cliffs Simulator — LNY 2026", page_icon="⛰️", layout="wide")

page = st.navigation([
    st.Page("pages/guide.py", title="User Guide", icon="📖"),
    st.Page("pages/simulator.py", title="Cliffs Simulator", icon="⛰️", default=True),
    st.Page("pages/event.py", title="LNY Event", icon="🧧"),
])

# --- Shared sidebar parameters ---
st.sidebar.header("Writing Phase")

n_hunts_t1_writing = st.sidebar.number_input("T1 Writing Hunts", min_value=0, value=qp_int("t1w", 80), step=10)
n_hunts_t2_writing = st.sidebar.number_input("T2 Writing Hunts", min_value=0, value=qp_int("t2w", 40), step=10)
cc_writing = st.sidebar.checkbox("Condensed Creativity (Writing)", value=qp_bool("ccw", True))
candle_writing = st.sidebar.radio("LNY 2026 Candle (Writing)", CANDLE_OPTIONS, index=qp_radio_index("cw", 0))
writing_multiplier = compute_multiplier(cc_writing, candle_writing == "White Candle", candle_writing == "Red Candle")

st.sidebar.header("Postscript Phase (Noto)")

n_hunts_t3_noto_postscript = st.sidebar.number_input("Noto Charging Hunts (T3)", min_value=0, value=qp_int("t3n", 13), step=1)
bk = st.sidebar.checkbox("Baitkeep Charm (T3 Cheese)", value=qp_bool("bk", True))
cc_noto = st.sidebar.checkbox("Condensed Creativity (Noto)", value=qp_bool("ccn", True))
candle_noto = st.sidebar.radio("LNY 2026 Candle (Noto)", CANDLE_OPTIONS, index=qp_radio_index("cn", 1))
noto_postscript_multiplier = compute_multiplier(cc_noto, candle_noto == "White Candle", candle_noto == "Red Candle")

st.sidebar.header("Postscript Phase (Fantasy)")

cc_fantasy = st.sidebar.checkbox("Condensed Creativity (Fantasy)", value=qp_bool("ccf", True))
candle_fantasy = st.sidebar.radio("LNY 2026 Candle (Fantasy)", CANDLE_OPTIONS, index=qp_radio_index("cf", 2))
fantasy_postscript_multiplier = compute_multiplier(cc_fantasy, candle_fantasy == "White Candle", candle_fantasy == "Red Candle")
fantasy_diamond_multiplier = 1 + (1 * (candle_fantasy == "White Candle") + 2 * (candle_fantasy == "Red Candle"))

st.sidebar.header("Materials & Diamonds")

n_t2_mats = st.sidebar.number_input("Available T2 Materials", min_value=0, value=qp_int("t2m", 1000), step=1)
n_t3_mats = st.sidebar.number_input("Available T3 Materials", min_value=0, value=qp_int("t3m", 500), step=1)
required_diamonds = st.sidebar.number_input("Required Diamonds", min_value=0, value=qp_int("rd", 355), step=1)
available_diamonds = st.sidebar.number_input("Available Diamonds", min_value=0, value=qp_int("ad", 0), step=1)

st.sidebar.header("Motivation Mallets")

n_mallets = st.sidebar.number_input("Available Mallets", min_value=0, value=qp_int("mal", 50), step=1)
noto_break_block = st.sidebar.checkbox("Noto: Break Block (30 mallets)", value=qp_bool("nbb", True))
fantasy_postscript_break_block = st.sidebar.checkbox("Fantasy: Break Block (30 mallets)", value=qp_bool("fbb", True))
fantasy_writing_short_only = st.sidebar.checkbox("Fantasy: Writing Short Only", value=qp_bool("fws", True))
fantasy_postscript_extend = st.sidebar.checkbox("Fantasy: Extend Postscript (30 mallets)", value=qp_bool("fpe", True))

st.sidebar.header("Chart Settings")
max_cycles_cap = st.sidebar.number_input("Max Cycles Cap (for charts)", min_value=1, value=qp_int("cap", 30, min_value=1), step=1)

# --- Save settings to URL ---
st.sidebar.divider()
if st.sidebar.button("Save Settings to URL"):
    st.session_state["_settings_saved"] = True
    params = {
        "t1w": str(n_hunts_t1_writing),
        "t2w": str(n_hunts_t2_writing),
        "ccw": str(int(cc_writing)),
        "cw": str(CANDLE_OPTIONS.index(candle_writing)),
        "t3n": str(n_hunts_t3_noto_postscript),
        "bk": str(int(bk)),
        "ccn": str(int(cc_noto)),
        "cn": str(CANDLE_OPTIONS.index(candle_noto)),
        "ccf": str(int(cc_fantasy)),
        "cf": str(CANDLE_OPTIONS.index(candle_fantasy)),
        "t2m": str(n_t2_mats),
        "t3m": str(n_t3_mats),
        "rd": str(required_diamonds),
        "ad": str(available_diamonds),
        "mal": str(n_mallets),
        "nbb": str(int(noto_break_block)),
        "fbb": str(int(fantasy_postscript_break_block)),
        "fws": str(int(fantasy_writing_short_only)),
        "fpe": str(int(fantasy_postscript_extend)),
        "cap": str(max_cycles_cap),
    }
    st.query_params.clear()
    st.query_params.update(params)

if st.session_state.pop("_settings_saved", False):
    st.sidebar.success("URL updated! Bookmark this page to save your settings.")

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
    n_mallets,
    noto_break_block,
    fantasy_postscript_break_block,
    fantasy_writing_short_only,
    fantasy_postscript_extend,
)

# --- Compute derived columns ---
df["max_cycles_mats"] = df[["n_cycles_t2", "n_cycles_t3"]].min(axis=1)
df["max_cycles"] = df[["n_cycles_t2", "n_cycles_t3", "n_cycles_mallets"]].min(axis=1)
best_idx = df["max_cycles_mats"].idxmax()
best_row = df.loc[best_idx]

# --- Store results in session state for all pages ---
st.session_state["df"] = df
st.session_state["best_row"] = best_row
st.session_state["required_cycles"] = required_cycles
st.session_state["n_diamonds_per_cycle"] = n_diamonds_per_cycle
st.session_state["writing_multiplier"] = writing_multiplier
st.session_state["noto_postscript_multiplier"] = noto_postscript_multiplier
st.session_state["fantasy_postscript_multiplier"] = fantasy_postscript_multiplier
st.session_state["n_t2_mats"] = n_t2_mats
st.session_state["n_t3_mats"] = n_t3_mats
st.session_state["n_mallets"] = n_mallets
st.session_state["max_cycles_cap"] = max_cycles_cap

# --- Run the selected page ---
page.run()
