import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ── Page config ───────────────────────────────────────────
st.set_page_config(page_title="ECM Battery Simulator", layout="wide")
st.title("⚡ ECM Battery Simulator")
st.markdown("Simulate real lithium-ion cell discharge behaviour using an Equivalent Circuit Model.")

# ── Sidebar slider ────────────────────────────────────────
st.sidebar.header("Battery parameters")
i_load = st.sidebar.slider("Discharge current (A)", 5, 100, 25)

# ── Fixed parameters ──────────────────────────────────────
CAPACITY_AH = 50.0
SOC_INIT    = 1.0
R0          = 0.01
R1          = 0.02
C1          = 2500.0
DT          = 1
TOTAL_TIME  = 3600

# ── OCV lookup table ──────────────────────────────────────
SOC_POINTS = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5,
                        0.6, 0.7, 0.8, 0.9, 1.0])
OCV_POINTS  = np.array([3.0, 3.3, 3.5, 3.6, 3.65, 3.7,
                         3.75, 3.8, 3.9, 4.0, 4.2])

def get_ocv(soc):
    return np.interp(soc, SOC_POINTS, OCV_POINTS)

# ── Simulation ────────────────────────────────────────────
time_log, voltage_log, soc_log = [], [], []
soc  = SOC_INIT
i_r1 = 0.0

for t in range(TOTAL_TIME):
    ocv        = get_ocv(soc)
    dv_r1      = (i_load - i_r1) / C1
    i_r1       = i_r1 + dv_r1 * DT
    v_terminal = ocv - (i_load * R0) - i_r1
    soc        = np.clip(soc - (i_load * DT) / (CAPACITY_AH * 3600), 0.0, 1.0)
    time_log.append(t / 60)
    voltage_log.append(v_terminal)
    soc_log.append(soc * 100)

# ── Metrics ───────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Discharge Current", f"{i_load}A")
col2.metric("Final SoC",         f"{round(soc_log[-1], 1)}%")
col3.metric("Final Voltage",     f"{round(voltage_log[-1], 3)}V")

st.markdown("---")

# ── Plot 1 — Voltage ──────────────────────────────────────
st.subheader("Terminal Voltage over time")
fig1, ax1 = plt.subplots(figsize=(10, 3))
ax1.plot(time_log, voltage_log, color='steelblue', linewidth=2)
ax1.axhline(y=3.0, color='red', linestyle='--', linewidth=1, label='Cutoff 3.0V')
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Voltage (V)')
ax1.set_ylim(2.8, 4.4)
ax1.legend()
ax1.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig1)

# ── Plot 2 — SoC ─────────────────────────────────────────
st.subheader("State of Charge over time")
fig2, ax2 = plt.subplots(figsize=(10, 3))
ax2.fill_between(time_log, soc_log, alpha=0.2, color='green')
ax2.plot(time_log, soc_log, color='green', linewidth=2)
ax2.axhline(y=20, color='red', linestyle='--', linewidth=1, label='20% low battery')
ax2.set_xlabel('Time (minutes)')
ax2.set_ylabel('SoC (%)')
ax2.set_ylim(0, 105)
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)