# Marvel Champions Card Viewer – v0.2
# --------------------------------------------------
# Simplified demo focused on visual layout only.
#   • Rounded corners (radius 24 px)
#   • Outline stroke colour per card `type`
#   • Automatic stacking of duplicate copies (pair / trio)
#
# How to run
#   pip install streamlit pandas pillow
#   streamlit run app.py
#
# Data model (minimal):
#   name | aspect | tier | img | type | copies
# --------------------------------------------------
from __future__ import annotations

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Dict

# ---------------------------------------------------------------------------
# HELPER ---------------------------------------------------------------------

def _build_card_html(url: str, copies: int, stroke_colour: str) -> str:
    """Return HTML block with 1‑3 stacked images."""
    # ensure at least 1
    copies = max(1, min(copies, 3))
    layers = []
    for idx in range(copies):
        z = 10 - idx  # highest z‑index on top
        shift = STACK_OFFSET_PX * idx
        style = (
            f"position:absolute; top:{shift}px; left:{shift}px; z-index:{z};"
            f"width:100%; border:{BORDER_WIDTH_PX}px solid {stroke_colour};"
            f"border-radius:{BORDER_RADIUS_PX}px;"
        )
        layers.append(f'<img src="{url}" style="{style}">')

    # wrapper sets relative positioning + padding so outer size fits
    pad = STACK_OFFSET_PX * (copies - 1) + BORDER_WIDTH_PX
    wrapper_style = f"position:relative; display:inline-block; padding:{pad}px;"
    return f'<div style="{wrapper_style}">{"".join(layers)}</div>'


st.set_page_config(page_title="MC Card Viewer", page_icon="🃏", layout="wide")

# ---------------------------------------------------------------------------
# CONFIGURABLES --------------------------------------------------------------
# Map card `type` → stroke colour
TYPE_COLOURS: Dict[str, str] = {
    "Hero": "#1b9e77",
    "Event": "#d95f02",
    "Upgrade": "#7570b3",
    "Support": "#e7298a",
    "Ally": "#66a61e",
    "Resource": "#e6ab02",
}

BORDER_RADIUS_PX = 24  # corners
BORDER_WIDTH_PX = 4    # outline thickness
STACK_OFFSET_PX = 18   # shift between duplicates

# ---------------------------------------------------------------------------
# SAMPLE DATA ---------------------------------------------------------------
# In real app replace with CSV / API
sample_url = "https://cdn.jsdelivr.net/gh/alaintxu/mc-ocr@main/images/accepted/01001a.webp"

data = pd.DataFrame([
    {"name": "Spiderman", "aspect": "Justice", "tier": "S", "img": sample_url, "type": "Hero", "copies": 1},
    {"name": "Desperate Defense", "aspect": "Protection", "tier": "A", "img": sample_url, "type": "Event", "copies": 3},
])

# ---------------------------------------------------------------------------
# SIDEBAR -------------------------------------------------------------------
st.sidebar.header("Filtros")
columns = st.sidebar.slider("Columnas", 1, 6, 3)

# ---------------------------------------------------------------------------
# MAIN GRID ------------------------------------------------------------------
cols = st.columns(columns, gap="large")

for i, card in data.iterrows():
    col = cols[i % columns]

    # pick stroke colour from type
    stroke = TYPE_COLOURS.get(card["type"], "#ffffff")

    # container with relative positioning to stack duplicates
    with col:
        n = int(card["copies"])
        container = st.container()
        with container:
            st.markdown(
                _build_card_html(card["img"], n, stroke),
                unsafe_allow_html=True,
            )
        st.caption(card["name"])

