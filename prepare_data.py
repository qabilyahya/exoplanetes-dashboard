import pandas as pd
import numpy as np

# 1) Chargement + filtre obligatoire : 1 ligne = 1 planète (mesure de référence NASA)
df_raw = pd.read_csv("projet_E_exoplanets.csv", comment="#")
df = df_raw[df_raw["default_flag"] == 1].copy()

# 2) On garde seulement les colonnes compréhensibles par un public débutant
COLS = ["pl_name", "hostname", "discoverymethod", "disc_year", "sy_pnum",
        "pl_orbper", "pl_orbsmax", "pl_rade", "pl_bmasse", "pl_insol", "pl_eqt",
        "st_teff", "sy_dist"]
df = df[COLS]

# 3) Unités "parlantes" : années-lumière et degrés Celsius
df["distance_al"] = df["sy_dist"] * 3.26          # 1 parsec ≈ 3,26 années-lumière
df["temp_c"] = df["pl_eqt"] - 273.15               # Kelvin -> °C
df["distance_etoile_km"] = df["pl_orbsmax"] * 149.6  # UA -> millions de km (1 UA = Terre-Soleil)

# 4) Méthodes de découverte en français
METHODES = {"Transit": "Transit", "Radial Velocity": "Vitesse radiale",
            "Microlensing": "Microlentille", "Imaging": "Imagerie directe"}
df["methode"] = df["discoverymethod"].map(METHODES).fillna("Autres méthodes")

# 5) Type de planète selon son rayon (mêmes seuils que l'AED)
def type_planete(r):
    if pd.isna(r):
        return np.nan
    if r < 1.25:
        return "Rocheuse (comme la Terre)"
    if r < 2:
        return "Super-Terre"
    if r < 6:
        return "Mini-Neptune"
    return "Géante gazeuse (comme Jupiter)"

df["type_planete"] = df["pl_rade"].apply(type_planete)

# 6) Type d'étoile selon sa température
def type_etoile(t):
    if pd.isna(t):
        return "Inconnue"
    if t < 4000:
        return "Étoile froide (naine rouge)"
    if t <= 6500:
        return "Étoile comme le Soleil"
    return "Étoile chaude"

df["type_etoile"] = df["st_teff"].apply(type_etoile)

# 7) Indicateurs simples "comme la Terre"
df["taille_terre"] = df["pl_rade"].between(0.8, 1.5)   # 0,8 à 1,5 fois la Terre
df["temperee"] = df["pl_eqt"].between(200, 320)         # environ -73 °C à +47 °C

# 8) Score de ressemblance avec la Terre (identique au bonus de l'AED)
#    Chaque sous-score vaut 1 si identique à la Terre, et baisse quand on s'éloigne.
ok = df["pl_rade"].notna() & df["pl_eqt"].notna()     # minimum : taille + température
df["score_taille"] = np.where(ok, 1 / (1 + (df["pl_rade"] - 1).abs()), np.nan)
df["score_temperature"] = np.where(ok, 1 / (1 + (df["pl_eqt"] - 255).abs() / 100), np.nan)
df["score_lumiere"] = np.where(ok & df["pl_insol"].notna(),
                               1 / (1 + (df["pl_insol"] - 1).abs()), np.nan)
df["score_masse"] = np.where(ok & df["pl_bmasse"].notna(),
                             1 / (1 + (df["pl_bmasse"] - 1).abs() / 5), np.nan)
df["score_etoile"] = np.where(ok, np.where(df["st_teff"].between(4000, 6500), 1, 0.5), np.nan)

SCORES = ["score_taille", "score_temperature", "score_lumiere", "score_masse", "score_etoile"]
df["score_habitabilite"] = df[SCORES].mean(axis=1, skipna=True)   # moyenne des critères connus

df.to_csv("exoplanetes_clean.csv", index=False)
print(f"✅ exoplanetes_clean.csv : {len(df)} planètes × {df.shape[1]} colonnes\n")

# 9) Les chiffres à connaître pour l'oral
fin = df["disc_year"].max()
print("📋 CHIFFRES POUR TON ORAL")
print(" - Exoplanètes connues                 :", len(df))
print(f" - Découvertes sur les 5 dernières années : {(df['disc_year'] > fin - 5).sum()}")
print(f" - Part trouvée par transit            : {(df['methode'] == 'Transit').mean() * 100:.0f} %")
print(" - Taille de la Terre (0,8 à 1,5 ×)    :", int(df["taille_terre"].sum()),
      f"sur {df['pl_rade'].notna().sum()} dont la taille est connue")
print(" - Taille Terre ET température douce   :", int((df["taille_terre"] & df["temperee"]).sum()))
print(" - Distance à l'étoile connue          :", int(df["pl_orbsmax"].notna().sum()))
print(" - Planètes notées dans le Top         :", int(df["score_habitabilite"].notna().sum()))
print(" - Les 2 années record                 :", df["disc_year"].value_counts().head(2).to_dict())
print(df.nlargest(3, "score_habitabilite")[["pl_name", "pl_rade", "temp_c", "pl_insol", "score_habitabilite"]].round(3))
