import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_data, fmt, GRIS, ACCENT

st.set_page_config(page_title="Top 3", layout="wide")
df = load_data()

CRITERES = {"score_taille": "Taille", "score_temperature": "Température",
            "score_lumiere": "Lumière reçue", "score_masse": "Masse", "score_etoile": "Étoile"}

# Filtres
st.sidebar.header("Classement")
exiger_lumiere = st.sidebar.checkbox("Exiger la lumière reçue mesurée")
dist_max = st.sidebar.select_slider("Distance maximale (années-lumière)",
                                    options=[100, 500, 1000, 2000, 5000, "Toutes"], value="Toutes")
etoiles = st.sidebar.multiselect("Type d'étoile", sorted(df["type_etoile"].unique()),
                                 default=sorted(df["type_etoile"].unique()))
n_top = st.sidebar.slider("Planètes affichées", 5, 20, 10)

c = df[df["score_habitabilite"].notna() & df["type_etoile"].isin(etoiles)]
if exiger_lumiere:
    c = c[c["pl_insol"].notna()]
if dist_max != "Toutes":
    c = c[c["distance_al"] <= dist_max]
c = c.sort_values("score_habitabilite", ascending=False)

st.title("Les 3 exoplanètes à observer en priorité")
st.caption("Score de 0 à 1 (Terre = 1) : moyenne de 5 critères comparés à la Terre — "
           "taille, température, lumière reçue, masse, étoile.")

if len(c) < 3:
    st.warning("Pas assez de planètes avec ces réglages.")
    st.stop()

# Podium
top3 = c.head(3)
for col, rang, (_, p) in zip(st.columns(3), ["1", "2", "3"], top3.iterrows()):
    with col:
        st.subheader(f"{rang}. {p['pl_name']}")
        st.metric("Score", fmt(p["score_habitabilite"], 2))
        lumiere = f"{fmt(p['pl_insol'], 2)} x Terre" if pd.notna(p["pl_insol"]) else "non mesurée"
        distance = f"{fmt(p['distance_al'])} al" if pd.notna(p["distance_al"]) else "inconnue"
        etoile = f"{fmt(p['pl_orbsmax'], 2)} UA" if pd.notna(p["pl_orbsmax"]) else "inconnue"
        st.markdown(f"""
- Taille : **{fmt(p['pl_rade'], 2)} x Terre**
- Température : **{fmt(p['temp_c'])} °C**
- Lumière reçue : **{lumiere}**
- Distance à son étoile : **{etoile}** (Terre-Soleil = 1 UA)
- Distance de la Terre : **{distance}**
""")

# Graphiques
t1, t2 = st.tabs(["Classement", "Détail des critères"])

with t1:
    top_n = c.head(n_top).copy()
    top_n["groupe"] = ["Top 3" if i < 3 else "Suivantes" for i in range(len(top_n))]
    top_n = top_n.iloc[::-1]
    fig = px.bar(top_n, x="score_habitabilite", y="pl_name", orientation="h", color="groupe",
                 color_discrete_map={"Top 3": ACCENT, "Suivantes": GRIS},
                 text=top_n["score_habitabilite"].round(2),
                 labels={"score_habitabilite": "Score (Terre = 1)", "pl_name": "", "groupe": ""})
    fig.update_xaxes(range=[0, 1.1])
    fig.add_vline(x=1, line_dash="dash", annotation_text="Terre", annotation_position="top left")
    fig.update_layout(height=max(380, 32 * len(top_n)), legend=dict(orientation="h", y=1.08))
    st.plotly_chart(fig, width="stretch")

with t2:
    crit = top3.melt(id_vars="pl_name", value_vars=list(CRITERES), var_name="critere", value_name="note")
    crit["critere"] = crit["critere"].map(CRITERES)
    fig = px.bar(crit, x="critere", y="note", color="pl_name", barmode="group",
                 color_discrete_sequence=[ACCENT, "#5b8bd6", "#2a9d8f"],
                 labels={"critere": "", "note": "Note (Terre = 1)", "pl_name": ""})
    fig.update_yaxes(range=[0, 1.05])
    fig.update_layout(height=430, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, width="stretch")
    st.caption("Barre absente = donnée non mesurée.")

st.caption("Ce score aide à choisir quoi observer : il ne prouve pas qu'une planète est habitable.")
