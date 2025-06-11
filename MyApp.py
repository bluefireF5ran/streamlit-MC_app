# Marvel Champions Card Viewer – v0.3  (stacking fix + up to 4 copies)
# ---------------------------------------------------------------------------
# Focus: better visual size for 1‑4 stacked copies, tunable radius & stroke.
#
# Run:
#   pip install streamlit pandas pillow
#   streamlit run app.py

from __future__ import annotations


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import copy

from hero_image_urls import hero_image_urls
from aspect_colors import aspect_colors
from card_data import card_data


# ---------- TUNABLE CONSTANTS ------------------------------------------------
CARD_BASE_W = 240          # px – width of the front card
OFFSET_PX   = 22           # px – shift per stacked copy
BORDER_RADIUS_PX = 14      # corner radius (px)




st.set_page_config(page_title="MC Card Viewer", layout="wide", page_icon="🃏")

# ----------------- SAMPLE DATA ----------------------------------------------
data = card_data

# ----------------- CARD HTML RENDER -----------------------------------------

def render_card(row: pd.Series) -> str:
    """Return raw HTML for one card with 1‑4 stacked copies."""
    stroke = aspect_colors.get(row["aspect"], "#ffffff")
    copies = int(max(1, min(row["copies"], 4)))  # clamp 1‑4

    layers: list[str] = []

    # scale factors so the pile fits visually; front card always at 1.0
    SCALE = [1.0, 0.96, 0.92, 0.88]

    for idx in range(copies):
        # back layers first so front card stays on top
        scale = SCALE[idx]
        left  = OFFSET_PX * (copies - idx - 1)  # reverse order
        top   = OFFSET_PX * (copies - idx - 1)
        layers.append(
            f"<img src='{row['img']}' style='"
            f"position:absolute;"
            f"left:{left}px;top:{top}px;"
            f"width:{CARD_BASE_W * scale}px;"
            f"border-radius:{BORDER_RADIUS_PX}px;"
            f"outline:4px solid {stroke};"
            f"background-clip:padding-box;"
            f"' />"
        )

    inner = "".join(layers)
    width_total = CARD_BASE_W + OFFSET_PX * (copies - 1)
    height_total = int(CARD_BASE_W * 1.4) + OFFSET_PX * (copies - 1)  # image ratio ≈ 1.4

    return (
        f"<div style='position:relative;width:{width_total}px;"
        f"height:{height_total}px;margin:0 auto;'>" + inner + "</div>"
    )

# ----------------------------- UI -------------------------------------------
background_image_url = "https://raw.githubusercontent.com/bluefireF5ran/streamlit-MC_app/500c99d17e2073dab68b38c88cc0475cb8e9da82/images/background.png"
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url({background_image_url}) no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Marvel Champions Legacy")
st.subheader("Marvel Champions Legacy Redux by Bluefire")


cols = st.slider("Columnas", 1, 6, 3, key="cols")

grid_cols = st.columns(cols)
for idx, (_, row) in enumerate(data.iterrows()):
    with grid_cols[idx % cols]:
        st.markdown(render_card(row), unsafe_allow_html=True)
        st.caption(row["name"])



# ------------------------- SIDEBAR -----------------------------------------
with st.sidebar:
    st.markdown("### Main Page")
        
    # GitHub link
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[📖 GitHub Repository](https://github.com/bluefireF5ran/streamlit-MC_app.git)")
    st.markdown("[🎮 Marvel Champions BGG](https://boardgamegeek.com/boardgame/285774/marvel-champions-card-game)")
    st.markdown("[🍋‍🟩 Living Tier List by Daring Lime](https://marvelchampionslivingtierlist.streamlit.app)")
    st.markdown("[🤖 Marvel Champions Simulator by forsooth](https://www.marvelsimulator.com)")
    st.markdown("[📊 Marvel Champions Tracker by StarLordOfThunder](https://marvelchampionstracker.com/home)")
    st.markdown("[❓ Marvel Champions Randomizer by krassek](https://krasstek.shinyapps.io/marvelchampioner)")
    
    
    # Credits
    st.markdown("---")
    st.markdown("### 👨‍💻 Credits")
    st.markdown("Page created by Bluefire.")
    st.markdown("Inspiration to create the page from Daring Lime's Living Tier List.")    
    st.markdown("Official card images are from the Cerebro Discord bot developed by UnicornSnuggler. Thank you!")
    st.markdown("Other card images are from their respective homebrew creators, they're awesome, check their content!")

