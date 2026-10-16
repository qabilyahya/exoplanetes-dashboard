import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_data, fmt, TYPE_ORDER, TYPE_COLORS, ACCENT

st.set_page_config(page_title="Recherche", layout="wide")
df = load_data()

# Filtres
st.sidebar.header("Recherche")
nom = st.sidebar.text_input("Nom de la planète")
types = st.sidebar.multiselect("Type de planète", TYPE_ORDER, default=TYPE_ORDER)
methodes_dispo = df["methode"].value_counts().index.tolist()
methodes = st.sidebar.multiselect("Méthode de découverte", methodes_dispo, default=methodes_dispo)
a_min, a_max = int(df["disc_year"].min()), int(df["disc_year"].max())
annees = st.sidebar.slider("Années de découverte", a_min, a_max, (a_min, a_max))
dist_max = st.sidebar.select_slider("Distance maximale (années-lumière)",
                                    options=[50, 100, 500, 1000, 5000, 10000, "Toutes"], value="Toutes")
seul_terre = st.sidebar.checkbox("Taille proche de la Terre (0,8 à 1,5)")
seul_tempere = st.sidebar.checkbox("Température douce (-73 à +47 °C)")

d = df[df["type_planete"].isin(types)
       & df["methode"].isin(methodes)
       & df["disc_year"].between(*annees)]
if nom:
    d = d[d["pl_name"].str.contains(nom, case=False, na=False)]
if dist_max != "Toutes":
    d = d[d["distance_al"] <= dist_max]
if seul_terre:
    d = d[d["taille_terre"]]
if seul_tempere:
    d = d[d["temperee"]]

st.title("Avec deux critères simples, il ne reste presque aucune autre Terre")

if d.empty:
    st.warning("Aucune planète ne correspond.")
    st.stop()

# KPIs
base = df[df["type_planete"].notna()]
k1, k2, k3 = st.columns(3)
k1.metric("Planètes trouvées", fmt(len(d)),
          f"{fmt(len(d) / len(base) * 100, 1)} % du catalogue", delta_color="off", delta_arrow="off")
med = d["distance_al"].median()
k2.metric("Distance médiane", f"{fmt(med)} al" if pd.notna(med) else "-",
          f"catalogue : {fmt(base['distance_al'].median())} al", delta_color="off", delta_arrow="off")
k3.metric("Température douce", fmt(int(d["temperee"].sum())),
          f"sur {fmt(d['pl_eqt'].notna().sum())} températures connues", delta_color="off", delta_arrow="off")

# Graphiques
t1, t2, t3, t4 = st.tabs(["Taille et température", "Distances", "Liste", "Fiche planète"])

with t1:
    pts = d.dropna(subset=["pl_rade", "temp_c"])
    if pts.empty:
        st.info("Aucune température connue dans cette sélection.")
    else:
        fig = px.scatter(pts, x="pl_rade", y="temp_c", color="type_planete", log_x=True,
                         color_discrete_map=TYPE_COLORS, category_orders={"type_planete": TYPE_ORDER},
                         hover_name="pl_name",
                         hover_data={"type_planete": False, "pl_orbsmax": ":.3f"},
                         labels={"pl_rade": "Taille (nombre de Terres)",
                                 "temp_c": "Température (°C)", "type_planete": "",
                                 "pl_orbsmax": "Distance à l'étoile (UA)"},
                         opacity=0.7)
        fig.update_xaxes(tickvals=[0.5, 1, 2, 5, 10, 20], ticktext=["0,5", "1", "2", "5", "10", "20"])
        fig.add_shape(type="rect", x0=0.8, x1=1.5, y0=-73, y1=47,
                      fillcolor="rgba(42,157,143,0.15)", line=dict(color="#2a9d8f", dash="dash"))
        fig.add_scatter(x=[1], y=[-18], mode="markers+text", text=["Terre"], textposition="top center",
                        marker=dict(size=14, color=ACCENT, symbol="star"), name="Terre")
        fig.update_layout(height=520, legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, width="stretch")
        st.caption("Zone verte : taille et température proches de la Terre.")

with t2:
    tranches = pd.cut(d["distance_al"], bins=[0, 100, 500, 1000, 5000, float("inf")],
                      labels=["< 100", "100 - 500", "500 - 1 000", "1 000 - 5 000", "> 5 000"])
    dist = tranches.value_counts().sort_index().reset_index()
    dist.columns = ["tranche", "nb"]
    fig = px.bar(dist, x="tranche", y="nb", text="nb",
                 labels={"tranche": "Distance (années-lumière)", "nb": "Nombre de planètes"})
    fig.update_traces(marker_color="#5b8bd6")
    fig.update_layout(height=380, title="Distance depuis la Terre")
    st.plotly_chart(fig, width="stretch")

    # Distance planète - étoile, comparée au système solaire (1 UA = Terre-Soleil)
    zones = pd.cut(d["pl_orbsmax"], bins=[0, 0.1, 0.4, 0.8, 1.5, 5, float("inf")],
                   labels=["< 0,1 UA", "0,1 - 0,4 (Mercure)", "0,4 - 0,8 (Vénus)",
                           "0,8 - 1,5 (Terre)", "1,5 - 5 (Mars)", "> 5 (Jupiter et +)"])
    orb = zones.value_counts().sort_index().reset_index()
    orb.columns = ["zone", "nb"]
    orb["groupe"] = orb["zone"].astype(str).apply(lambda z: "Comme la Terre" if "Terre" in z else "Autres")
    fig = px.bar(orb, x="zone", y="nb", text="nb", color="groupe",
                 color_discrete_map={"Comme la Terre": ACCENT, "Autres": "#5b8bd6"},
                 labels={"zone": "Distance à son étoile (UA)", "nb": "Nombre de planètes", "groupe": ""})
    fig.update_layout(height=380, title="Distance à son étoile (Terre-Soleil = 1 UA)", showlegend=False)
    st.plotly_chart(fig, width="stretch")
    st.caption(f"1 UA = 150 millions de km. Distance à l'étoile connue pour "
               f"{fmt(d['pl_orbsmax'].notna().sum())} planètes sur {fmt(len(d))}.")

with t3:
    tableau = d[["pl_name", "type_planete", "pl_rade", "temp_c", "pl_orbsmax",
                 "distance_al", "disc_year", "methode"]].rename(
        columns={"pl_name": "Planète", "type_planete": "Type", "pl_rade": "Taille (x Terre)",
                 "temp_c": "Température (°C)", "pl_orbsmax": "Distance à l'étoile (UA)", "distance_al": "Distance (al)",
                 "disc_year": "Découverte", "methode": "Méthode"})
    st.dataframe(tableau.round(2), width="stretch", hide_index=True)
    st.download_button("Télécharger (CSV)", tableau.to_csv(index=False).encode("utf-8"),
                       "recherche_exoplanetes.csv", "text/csv")

with t4:
    choix = st.selectbox("Planète", sorted(d["pl_name"]))
    p = d[d["pl_name"] == choix].iloc[0]

    def val(x, texte):
        return texte if pd.notna(x) else "inconnue"

    c1, c2, c3 = st.columns(3)
    c1.metric("Taille", val(p["pl_rade"], f"{fmt(p['pl_rade'], 2)} x Terre"))
    c2.metric("Température", val(p["temp_c"], f"{fmt(p['temp_c'])} °C"),
              "Terre : -18 °C", delta_color="off", delta_arrow="off")
    c3.metric("Durée d'une année", val(p["pl_orbper"], f"{fmt(p['pl_orbper'], 1)} jours"),
              "Terre : 365 jours", delta_color="off", delta_arrow="off")

    c4, c5, _ = st.columns(3)
    c4.metric("Distance à son étoile", val(p["pl_orbsmax"], f"{fmt(p['pl_orbsmax'], 3)} UA"),
              val(p["pl_orbsmax"], f"{fmt(p['distance_etoile_km'])} millions de km · Terre-Soleil : 1 UA"),
              delta_color="off", delta_arrow="off")
    c5.metric("Distance de la Terre", val(p["distance_al"], f"{fmt(p['distance_al'])} al"))

    st.caption(f"{p['type_planete']} · {p['type_etoile']} · découverte en {int(p['disc_year'])} ({p['methode']})")
