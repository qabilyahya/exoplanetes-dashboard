import pandas as pd
import streamlit as st

DATA_PATH = "exoplanetes_clean.csv"

TYPE_ORDER = ["Rocheuse (comme la Terre)", "Super-Terre",
              "Mini-Neptune", "Géante gazeuse (comme Jupiter)"]
TYPE_COLORS = {"Rocheuse (comme la Terre)": "#2a9d8f",
               "Super-Terre": "#8ab17d",
               "Mini-Neptune": "#5b8bd6",
               "Géante gazeuse (comme Jupiter)": "#e76f51"}
GRIS = "#c7c7c7"
ACCENT = "#e9a23b"


@st.cache_data
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Chargement mis en cache : le CSV n'est lu qu'une seule fois."""
    return pd.read_csv(path)


def fmt(n, dec=0):
    """Nombre à la française : 5 903 / 1,6"""
    s = f"{n:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s
