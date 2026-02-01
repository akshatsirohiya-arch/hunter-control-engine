# app.py
import streamlit as st
from engine.score import compute_damage_score
from engine.permissions import get_regime, get_permissions
from engine.data_fetch import get_vix_change_pct, get_breadth_percent

st.set_page_config(page_title="Hunter Control Engine", layout="centered")

st.title("🧠 Hunter Control Engine")
st.caption("Rule-based market regime & permissions system")

# Fetch live inputs
breadth_percent = get_breadth_percent()
vix_change_pct = get_vix_change_pct()

# Compute score
damage_score = compute_damage_score(
    breadth_percent=breadth_percent,
    vix_change_pct=vix_change_pct
)

regime = get_regime(damage_score)
permissions = get_permissions(damage_score)

st.subheader("Market Status")
st.metric("Damage Score", f"{damage_score} / 6")
st.metric("Market Regime", regime)

st.subheader("Allowed Actions")
for k, v in permissions.items():
    st.write(f"**{k}:** {v}")

st.divider()

st.caption("This system restricts behavior. It does not predict markets.")
