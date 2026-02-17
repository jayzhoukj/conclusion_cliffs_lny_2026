import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timezone

st.title("LNY 2026 Event Dashboard")

# --- Live countdown timer ---
EVENT_END_UTC = "2026-02-24T16:00:00Z"

countdown_html = f"""
<div id="countdown" style="font-size: 2rem; font-weight: bold; text-align: center;
     padding: 1rem; background: #262730; color: #fafafa; border-radius: 8px;
     font-family: 'Source Sans Pro', sans-serif;">
    Loading...
</div>
<script>
    const endDate = new Date("{EVENT_END_UTC}");
    function updateCountdown() {{
        const now = new Date();
        const diff = endDate - now;
        if (diff <= 0) {{
            document.getElementById("countdown").innerText = "Event has ended!";
            return;
        }}
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        document.getElementById("countdown").innerText =
            days + "d " + hours + "h " + minutes + "m " + seconds + "s remaining";
    }}
    updateCountdown();
    setInterval(updateCountdown, 1000);
</script>
"""

st.subheader("Event Countdown")
components.html(countdown_html, height=80)

# --- Read simulation results ---
best_row = st.session_state["best_row"]
required_cycles = st.session_state["required_cycles"]
n_diamonds_per_cycle = st.session_state["n_diamonds_per_cycle"]

# --- Time constraint ---
st.subheader("Time Constraint")

HUNTS_PER_CYCLE = 143
hunts_per_day = st.session_state["hunts_per_day"]

event_end = datetime(2026, 2, 24, 16, 0, 0, tzinfo=timezone.utc)
now = datetime.now(timezone.utc)
remaining_seconds = max(0, (event_end - now).total_seconds())
remaining_days = remaining_seconds / 86400

total_remaining_hunts = remaining_days * hunts_per_day
n_cycles_time = total_remaining_hunts / HUNTS_PER_CYCLE

tcol1, tcol2 = st.columns(2)
tcol1.metric("Remaining Days", f"{remaining_days:.2f}")
tcol2.metric("Max Cycles (Time)", f"{n_cycles_time:.2f}")

# --- Constraint summary ---
st.subheader("Constraint Summary")

constraints = {
    "T2 Materials": best_row["n_cycles_t2"],
    "T3 Materials": best_row["n_cycles_t3"],
    "Mallets": best_row["n_cycles_mallets"],
    "Time": n_cycles_time,
}


def format_cycles(value):
    return "Unconstrained" if value >= 999 else f"{value:.2f}"


binding_name = min(constraints, key=constraints.get)
binding_value = constraints[binding_name]

col1, col2, col3, col4 = st.columns(4)
col1.metric("T2 Cycles", format_cycles(best_row["n_cycles_t2"]))
col2.metric("T3 Cycles", format_cycles(best_row["n_cycles_t3"]))
col3.metric("Mallets Cycles", format_cycles(best_row["n_cycles_mallets"]))
col4.metric("Time Cycles", format_cycles(n_cycles_time))

st.divider()

bcol1, bcol2 = st.columns(2)
bcol1.metric("Binding Constraint", binding_name)
bcol2.metric("Effective Max Cycles", format_cycles(binding_value))

# --- Diamond progress ---
st.subheader("Diamond Progress")

dcol1, dcol2 = st.columns(2)
dcol1.metric("Diamonds per Cycle", f"{n_diamonds_per_cycle:.0f}")
dcol2.metric("Required Cycles (Diamonds)", f"{required_cycles:.2f}")

if binding_value >= required_cycles:
    st.success("You have enough resources and time to reach your diamond target!")
else:
    deficit = required_cycles - binding_value
    st.error(f"You are {deficit:.2f} cycles short of your diamond target.")
