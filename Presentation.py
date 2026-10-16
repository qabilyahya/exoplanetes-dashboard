import streamlit as st
import plotly.express as px
from utils import load_data, fmt, TYPE_ORDER, TYPE_COLORS, GRIS, ACCENT

st.set_page_config(page_title="Exoplanètes", layout="wide")
df = load_data()

# Filtres
st.sidebar.header("Filtres")
a_min, a_max = int(df["disc_year"].min()), int(df["disc_year"].max())
annees = st.sidebar.slider("Années de découverte", a_min, a_max, (a_min, a_max))
methodes_dispo = df["methode"].value_counts().index.tolist()
methodes = st.sidebar.multiselect("Méthode de découverte", methodes_dispo, default=methodes_dispo)

d = df[df["disc_year"].between(*annees) & df["methode"].isin(methodes)]
if d.empty:
    st.warning("Aucune planète avec ces filtres.")
    st.stop()

st.title(f"{fmt(len(df))} planètes découvertes hors du système solaire, "
         "mais très peu ressemblent à la Terre")
st.caption("Source : NASA Exoplanet Archive")

# KPIs
fin = int(d["disc_year"].max())
recentes = (d["disc_year"] > fin - 5).sum()
part_transit = (d["methode"] == "Transit").mean() * 100
taille_connue = d["pl_rade"].notna().sum()
taille_terre = int(d["taille_terre"].sum())

k1, k2, k3 = st.columns(3)
k1.metric("Exoplanètes", fmt(len(d)), f"+{fmt(recentes)} en 5 ans")
k2.metric("Découvertes par transit", f"{fmt(part_transit)} %",
          "méthode dominante", delta_color="off", delta_arrow="off")
k3.metric("Taille proche de la Terre", fmt(taille_terre),
          f"{fmt(taille_terre / max(taille_connue, 1) * 100, 1)} % des tailles connues",
          delta_color="off", delta_arrow="off")

# Graphiques
t1, t2, t3 = st.tabs(["Découvertes par année", "Méthodes de découverte", "Types de planètes"])

with t1:
    par_an = d.groupby("disc_year").size().reset_index(name="nb")
    top2 = par_an.nlargest(2, "nb")["disc_year"].tolist()
    par_an["groupe"] = par_an["disc_year"].apply(lambda a: "Années record (Kepler)" if a in top2 else "Autres années")
    fig = px.bar(par_an, x="disc_year", y="nb", color="groupe",
                 color_discrete_map={"Années record (Kepler)": ACCENT, "Autres années": GRIS},
                 labels={"disc_year": "Année", "nb": "Planètes découvertes", "groupe": ""})
    fig.update_layout(legend=dict(orientation="h", y=1.1), height=420)
    st.plotly_chart(fig, width="stretch")

with t2:
    meth = d["methode"].value_counts().reset_index()
    meth.columns = ["methode", "nb"]
    meth["groupe"] = meth["methode"].apply(lambda m: "Transit" if m == "Transit" else "Autres")
    fig = px.bar(meth.sort_values("nb"), x="nb", y="methode", orientation="h", text="nb",
                 color="groupe", color_discrete_map={"Transit": ACCENT, "Autres": GRIS},
                 labels={"nb": "Nombre de planètes", "methode": ""})
    fig.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig, width="stretch")

with t3:
    types = d["type_planete"].value_counts().reindex(TYPE_ORDER).fillna(0).reset_index()
    types.columns = ["type", "nb"]
    fig = px.bar(types, x="type", y="nb", text="nb", color="type",
                 color_discrete_map=TYPE_COLORS, labels={"type": "", "nb": "Nombre de planètes"})
    fig.update_layout(showlegend=False, height=420)
    st.plotly_chart(fig, width="stretch")
    st.caption("Repères : Terre = 1, Neptune ≈ 4, Jupiter ≈ 11 (taille en nombre de Terres).")
