# Marvel Champions Card Explorer – Streamlit demo
# -------------------------------------------------
# BEFORE RUNNING:
#   pip install streamlit pandas pillow streamlit-draggable-list
#
# Run with:
#   streamlit run app.py

from __future__ import annotations

import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------- CONFIG -----------------------------------------
st.set_page_config(page_title="Marvel Champions Explorer", page_icon="🃏", layout="wide")

# Small CSS tweak for nicer card shadows & rounded corners
st.markdown(
    """
    <style>
    .card-img {
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------- DATA -------------------------------------------
# Replace this with your own CSV or API. Minimum columns: name, tier, aspect, img
@st.cache_data
def load_data() -> pd.DataFrame:
    data = [
        {
            "name": "Spider‑Man",
            "tier": "S",
            "aspect": "Justice",
            "img": "https://raw.githubusercontent.com/streamlit/example-data/master/spiderman.png",
        },
        {
            "name": "Captain Marvel",
            "tier": "A",
            "aspect": "Aggression",
            "img": "https://raw.githubusercontent.com/streamlit/example-data/master/captain_marvel.png",
        },
        {
            "name": "Hulk",
            "tier": "B",
            "aspect": "Protection",
            "img": "https://raw.githubusercontent.com/streamlit/example-data/master/hulk.png",
        },
        # Add the rest of your cards here …
    ]
    return pd.DataFrame(data)

df = load_data()

# --------------------------- SIDEBAR ----------------------------------------
with st.sidebar:
    st.header("Filtros")
    aspect_options = sorted(df["aspect"].unique())
    tier_options = sorted(df["tier"].unique())

    selected_aspects = st.multiselect("Aspecto", aspect_options, default=aspect_options)
    selected_tiers = st.multiselect("Tier", tier_options, default=tier_options)

    n_cols = st.slider("Cartas por fila", 2, 6, 4)

# Apply filters
filtered = df[df["aspect"].isin(selected_aspects) & df["tier"].isin(selected_tiers)]

# --------------------------- MAIN GRID --------------------------------------

st.subheader(f"Mostrando {len(filtered)} carta(s)")

if filtered.empty:
    st.info("No hay cartas que coincidan con los filtros.")
else:
    cols = st.columns(n_cols, gap="small")
    for i, (_, row) in enumerate(filtered.iterrows()):
        with cols[i % n_cols]:
            st.image(row["img"], caption=f"{row['name']} • Tier {row['tier']}", use_column_width=True, output_format="PNG", clamp=True, channels="RGB")
        if (i + 1) % n_cols == 0 and i + 1 < len(filtered):
            cols = st.columns(n_cols, gap="small")

# --------------------------- DRAG‑&‑DROP TIER LIST (opcional) --------------
try:
    import streamlit_draggable_list as dl

    st.markdown("---")
    st.header("Ordena tus cartas arrastrando")
    # The component expects a list of strings (e.g., card names) – you can extend this to images.
    ordering = dl.draggable_list(
        items=filtered["name"].tolist(),
        height=300,
        style={"backgroundColor": "#fafafa"},
    )
    st.write("Nuevo orden:", ordering)
except ModuleNotFoundError:
    st.warning("Instala `streamlit-draggable-list` para habilitar la función de arrastrar y soltar.")

# --------------------------- FOOTER ----------------------------------------
st.markdown("---")
st.caption("App demo creada con Streamlit • © 2025")
