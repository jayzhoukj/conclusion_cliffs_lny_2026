import streamlit as st

st.title("User Guide")

st.markdown("""
## What is the Cliffs Simulator?

The Cliffs Simulator is a resource planning tool for the MouseHunt Lunar New Year 2026
event in the Conclusion Cliffs area. It helps you determine the optimal split of T1 and T2 hunts during the
Fantasy Postscript phase to maximize the number of cycles you can complete, given your
available materials, mallets, and diamond requirements.

---

## Sidebar Inputs

The sidebar is shared across all pages — any changes you make are reflected everywhere.

### Writing Phase
- **T1 Writing Hunts** — Number of T1 hunts during the Writing phase (farms T2 materials).
- **T2 Writing Hunts** — Number of T2 hunts during the Writing phase (farms T3 materials,
  consumes T2 materials).
- **Condensed Creativity (Writing)** — Whether to use CC during writing (adds 1x to multiplier).
- **LNY 2026 Candle (Writing)** — Candle type used during writing. White adds 1x, Red adds 2x
  to the multiplier.

### Postscript Phase (Noto)
- **Noto Charging Hunts (T3)** — Number of T3 hunts during Noto postscript (consumes T3
  materials).
- **Baitkeep Charm** — Halves T3 material consumption when enabled.
- **Condensed Creativity / Candle (Noto)** — Multiplier settings for the Noto postscript phase.

### Postscript Phase (Fantasy)
- **Condensed Creativity / Candle (Fantasy)** — Multiplier settings for the Fantasy postscript
  phase. The simulator automatically tests all 14 possible T1/T2 fantasy hunt splits (0–13).

### Materials & Diamonds
- **Available T2/T3 Materials** — Your current stockpile. These are drawn down each cycle.
- **Required / Available Diamonds** — Sets the diamond-based cycle target.

### Motivation Mallets
- **Available Mallets** — Your current mallet stockpile.
- **Break Block / Extend / Short Only** — Toggle mallet usage strategies that affect consumption
  per cycle.

### Chart Settings
- **Max Cycles Cap** — Upper display limit for the cycle constraint chart (visual only, does not
  affect calculations).

---

## Reading the Results

### Summary Metrics
- **Multipliers** — Your effective multiplier for each phase (Writing, Noto, Fantasy).
- **Diamonds per Cycle** — How many diamonds you earn each cycle.
- **Required Cycles** — How many cycles you need to reach your diamond target.

### Optimal Scenario
- **Max Achievable Cycles** — The highest number of cycles achievable under all constraints
  (T2, T3, and mallets).
- **Optimal Fantasy Postscript Hunts** — The T1/T2 split during Fantasy that maximizes
  material-constrained cycles (determined by T2 and T3 only, not mallets).
- **Total CC Used** — Condensed Creativity consumed at the optimal scenario.

### Simulation Table
All 14 Fantasy Postscript scenarios (0–13 T2 hunts) with per-cycle net materials, cycle limits,
and CC usage. Downloadable as CSV.

### Charts
- **Net Materials per Cycle** — Shows whether each resource is gained or lost per cycle at each
  split.
- **Max Cycles** — Shows how many cycles each constraint allows, capped for readability.
- **CC Used** — Total Condensed Creativity consumed.
- **Materials Over Cycles** — Projects your material stockpile over time for a selected scenario.

---

## LNY Event Page

The **LNY Event** page provides a dashboard view with:
- A **live countdown timer** to the event end (24 Feb 2026, 16:00 UTC).
- A summary of all **resource constraints** (T2, T3, mallets) from the simulator.
- A **time constraint** calculated from your hunts per day and remaining event time.
- The **binding constraint** — whichever limit runs out first.
- **Diamond progress** — whether you can reach your target in time.

---

## Saving & Restoring Your Settings

Your sidebar inputs are **not** saved automatically between sessions. However, you can preserve
them using the **Save Settings to URL** button at the bottom of the sidebar.

### How to Save
1. Adjust all sidebar inputs to your desired values.
2. Scroll to the bottom of the sidebar and click **Save Settings to URL**.
3. The browser URL will update to include all your current settings as query parameters
   (e.g., `?t1w=80&t2w=40&ccw=1&...`).
4. **Bookmark the URL** in your browser to save your configuration.

### How to Restore
- Open your bookmark — all sidebar inputs will be pre-filled with the saved values.

### Sharing Settings
- You can share your bookmarked URL with others. Anyone who opens the link will see the
  same sidebar configuration, regardless of whether they are logged into Streamlit Cloud.

---

## Key Concepts

- **Cycle** — One full loop through Writing + Noto Postscript + Fantasy Postscript phases.
  Each cycle consists of 143 hunts total.
- **Net Materials** — Materials farmed minus materials consumed per cycle. Positive means
  self-sustaining; negative means you are drawing down your stockpile.
- **Binding Constraint** — The resource that runs out first, limiting your total cycles.
- **T1 / T2 / T3** — Tier levels of cheese and corresponding materials in Conclusion Cliffs.
""")
