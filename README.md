# ⚡ ECM Battery Simulator

A Python-based Equivalent Circuit Model (ECM) that simulates lithium-ion battery discharge behaviour — modelling terminal voltage and State of Charge in real time using the same principles found in production BMS systems.

---

## What this project does

This simulator models a lithium-ion cell as an electrical circuit and answers the core BMS question every second:

> *"Given the current flowing out — what is the voltage and how much charge is left?"*

---

## Core concepts

### Equivalent Circuit Model (ECM)
Models a battery as an electrical circuit using three components — R0 (internal resistance), R1 (polarisation resistance), and C1 (capacitance). Simpler than physics-based models but accurate enough for real BMS applications.

### Open Circuit Voltage (OCV)
The resting voltage of a battery when no current flows. A lithium-ion cell ranges from 3.0V (empty) to 4.2V (full) — never reaching zero due to its electrochemical nature. OCV is the foundation for voltage-based SoC estimation.

### Coulomb Counting
Tracks State of Charge by measuring how much current flows in or out every second. Simple and effective short-term but accumulates error over time due to sensor noise and self-discharge.

### Terminal Voltage
The actual voltage measured at battery terminals under load — always lower than OCV due to resistive losses. Calculated every second using Ohm's Law across R0 and R1/C1.

### Polarisation Effect (R1/C1)
Models the slow voltage recovery seen after a load is removed — the reason a phone battery percentage sometimes jumps up slightly when you stop using it.

---

## Limitations

| Limitation | Impact |
|-----------|--------|
| Coulomb counting drift | SoC estimate becomes less accurate over long periods |
| Fixed R0, R1, C1 values | Real parameters change with temperature and aging |
| Constant current only | Real EV discharge is dynamic, not constant |
| No temperature modelling | Cold batteries behave significantly differently |
| Empirical OCV curve | Based on typical NMC cell, not a specific measured cell |

These limitations are exactly why real BMS systems combine ECM with Kalman Filters and thermal models — the natural next steps in this project series.

---

## Project files

| File | Description |
|------|-------------|
| `ecm_battery_model.ipynb` | Step by step Python code — full simulation with plots |
| `ecm_dashboard.py` | Interactive Streamlit dashboard with discharge current slider |

---

## How to run

**Jupyter notebook:**
```bash
jupyter notebook ecm_battery_model.ipynb
```

**Streamlit dashboard:**
```bash
streamlit run ecm_dashboard.py
```

---

## Results

The simulation runs for 3600 seconds (1 hour) at a configurable discharge current and outputs:

- Terminal voltage over time
- State of Charge over time
- Key metrics — final SoC, final voltage, charge used

---

## Tech stack

Python, NumPy, Matplotlib, Streamlit

---

## About

Built as part of a self-directed battery engineering learning path — progressing from empirical degradation modelling toward full BMS simulation.

*Part of an ongoing series of EV battery engineering projects.*
