# Marvel Champions Card Explorer – Streamlit demo
# -------------------------------------------------
# Requires:
#     pip install streamlit pandas pillow
#     pip install streamlit-draggable-list   # (optional) for tier-list drag & drop
#
# Run with:
#     streamlit run app.py

from __future__ import annotations

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Marvel Champions Explorer", page_icon="🃏", layout="wide")

# ------------------ CSS tweaks ------------------
st.markdown(
    '''
    <style>
    .card-img {
        border-radius: 0.5rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        transition: transform .1s ease-in-out;
    }
    .card-img:hover {
        transform: scale(1.03);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# ------------------ Data ------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    """Return a DataFrame with Marvel Champions cards.
    Replace this stub with your own CSV or API call.
    """
    sample_data = [
        {"name": "Spider-ghub", "aspect": "Leadership", "tier": "S", "img": "https://cdn.jsdelivr.net/gh/alaintxu/mc-ocr@main/images/accepted/01001a.webp"},
        {"name": "Spider Fran", "aspect": "Justice", "tier": "A", "img": "https://raw.githubusercontent.com/bluefireF5ran/streamlit-MC_app/refs/heads/main/MC_Images/01001A.jpg?token=GHSAT0AAAAAADCPWJ642KVHAX3D5K5GKFEO2CBNV3Q"},
    ]
    return pd.DataFrame(sample_data)


df = load_data()

# ------------------ Sidebar ------------------
st.sidebar.header("Filtros")
aspects = st.sidebar.multiselect("Aspectos", options=sorted(df["aspect"].unique()), default=df["aspect"].unique())

tiers = st.sidebar.multiselect("Tier", options=sorted(df["tier"].unique()), default=df["tier"].unique())

cols = st.sidebar.slider("Columnas", 1, 6, 4)

filtered = df[df["aspect"].isin(aspects) & df["tier"].isin(tiers)]

# ------------------ Grid display ------------------
if filtered.empty:
    st.info("No hay cartas que coincidan con los filtros.")
else:
    rows = [filtered.iloc[i : i + cols] for i in range(0, len(filtered), cols)]
    for row in rows:
        columns = st.columns(len(row))
        for card, col in zip(row.itertuples(), columns):
            with col:
                st.image(card.img, caption=f"{card.name} [{card.tier}]", use_container_width=True)

# ------------------ Tier‑list drag & drop (opcional) ------------------
st.markdown("---")
st.header("Crea tu propia Tier List")

try:
    from streamlit_draggable_list import draggable_list

    tiers_order = ["S", "A", "B", "C", "D"]
    cards = [f"{row.name} ({row.tier})" for _, row in df.iterrows()]
    new_order = draggable_list(cards, tiers_order)
    st.success("Nuevo orden guardado en variable `new_order`.")
except ModuleNotFoundError:
    st.warning(
        "👉 Instala **streamlit-draggable-list** para habilitar la función de arrastrar y soltar:\n\n"
        "```bash\npip install streamlit-draggable-list\n```"
    )
