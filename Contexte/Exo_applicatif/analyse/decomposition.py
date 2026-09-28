# -*- coding: utf-8 -*-
"""Etude : la serie est-elle a decomposition ADDITIVE ou MULTIPLICATIVE ?"""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose

OUT = __file__.rsplit("/",1)[0]
df = pd.read_csv(OUT+"/../monthly_timeseries_10y.csv", parse_dates=["date"]).set_index("date")
df.index.freq = "MS"
y = df["value"]; L = []
p = L.append

p("="*70); p("ETAPE 0 - APERCU DES DONNEES"); p("="*70)
p(f"Periode        : {y.index[0].date()} -> {y.index[-1].date()}")
p(f"Nb observations: {len(y)}  (frequence mensuelle, s = 12)")
p(f"Moyenne globale: {y.mean():.3f}   Ecart-type: {y.std(ddof=1):.3f}")
p(f"Min / Max      : {y.min():.3f} / {y.max():.3f}")

# --- ETAPE 1 : verification de l'identite de reconstruction -------------
p(""); p("="*70); p("ETAPE 1 - LE FICHIER CONTIENT DEJA trend/seasonal/residual"); p("="*70)
add = df.trend + df.seasonal + df.residual
mul = df.trend * df.seasonal * df.residual
p(f"max|value - (T+S+R)| = {np.abs(y-add).max():.6f}   <-- additif")
p(f"max|value - (T*S*R)| = {np.abs(y-mul).max():.6f}   <-- multiplicatif")
p(f"S varie entre {df.seasonal.min():.3f} et {df.seasonal.max():.3f} (moyenne {df.seasonal.mean():.4f})")
p("Une saisonnalite NEGATIVE et de moyenne ~0 est le signe d'un modele ADDITIF")
p("(en multiplicatif, S oscille autour de 1 et reste positif).")

# --- ETAPE 2 : Buys-Ballot : moyenne et ecart-type par annee -----------
p(""); p("="*70); p("ETAPE 2 - TABLE DE BUYS-BALLOT (moyenne & ecart-type annuels)"); p("="*70)
g = y.groupby(y.index.year)
bb = pd.DataFrame({"n":g.size(), "moyenne":g.mean(), "ecart_type":g.std(ddof=1),
                   "etendue":g.max()-g.min()})
bb["CV_%"] = 100*bb.ecart_type/bb.moyenne
full = bb[bb.n==12]           # on ne garde que les annees completes
p(bb.round(3).to_string())
p("")
p("Lecture : si l'AMPLITUDE (ecart-type, etendue) grandit avec le NIVEAU")
p("(moyenne) -> multiplicatif. Si elle reste stable -> additif.")
p("Si le COEFFICIENT DE VARIATION est stable -> multiplicatif ;")
p("s'il DECROIT quand le niveau monte -> additif.")

# --- ETAPE 3 : regression lineaire ecart-type ~ moyenne ----------------
p(""); p("="*70); p("ETAPE 3 - REGRESSION LINEAIRE  ecart_type = a + b * moyenne"); p("="*70)
x, s = full.moyenne.values, full.ecart_type.values
r = stats.linregress(x, s)
p(f"Annees completes utilisees : {list(full.index)}")
p(f"pente b   = {r.slope:.5f}   (erreur std {r.stderr:.5f})")
p(f"ordonnee a= {r.intercept:.4f}")
p(f"r         = {r.rvalue:.4f}    R2 = {r.rvalue**2:.4f}")
p(f"p-value   = {r.pvalue:.4f}")
p("")
p("REGLE DE DECISION :")
p("  b non significativement different de 0 (p > 0.05) -> ADDITIF")
p("  b significativement > 0                            -> MULTIPLICATIF")
p(f"  ==> ici p = {r.pvalue:.4f} -> pente {'NON significative -> ADDITIF' if r.pvalue>0.05 else 'significative -> MULTIPLICATIF'}")

# meme test sur l'etendue
r2 = stats.linregress(full.moyenne.values, full.etendue.values)
p(f"[controle] etendue ~ moyenne : b = {r2.slope:.5f}, p = {r2.pvalue:.4f}")

# --- ETAPE 4 : tendance de la serie ------------------------------------
p(""); p("="*70); p("ETAPE 4 - TENDANCE : regression value = a + b * t"); p("="*70)
t = np.arange(len(y))
rt = stats.linregress(t, y.values)
p(f"pente = {rt.slope:.4f} par mois  (soit {12*rt.slope:.3f} par an), p = {rt.pvalue:.2e}, R2 = {rt.rvalue**2:.3f}")
p("Tendance lineaire croissante et reguliere -> compatible avec un modele additif.")

# --- ETAPE 5 : decomposition additive vs multiplicative ---------------
p(""); p("="*70); p("ETAPE 5 - COMPARAISON DES DEUX DECOMPOSITIONS (moving average)"); p("="*70)
da = seasonal_decompose(y, model="additive",       period=12)
dm = seasonal_decompose(y, model="multiplicative", period=12)
ra = da.resid.dropna(); rm = dm.resid.dropna()
p(f"ADDITIF        : residu moyen {ra.mean():+.4f}, ecart-type {ra.std(ddof=1):.4f}")
p(f"MULTIPLICATIF  : residu moyen {rm.mean():+.4f}, ecart-type {rm.std(ddof=1):.4f} (autour de 1)")
# residus multiplicatifs ramenes a l'echelle de la serie pour comparer
rm_abs = y.loc[rm.index] - dm.trend.loc[rm.index]*dm.seasonal.loc[rm.index]
p(f"Residus ramenes en unites de la serie : additif RMSE = {np.sqrt((ra**2).mean()):.4f}"
  f" | multiplicatif RMSE = {np.sqrt((rm_abs**2).mean()):.4f}")
# correlation |residu| vs niveau : si >0 pour l'additif -> multiplicatif prefere
c_add = stats.pearsonr(da.trend.loc[ra.index], ra.abs())
p(f"corr(|residu additif| , tendance) = {c_add[0]:+.3f}  (p={c_add[1]:.3f})")
p("Une correlation ~0 confirme que la dispersion NE depend PAS du niveau -> ADDITIF.")

# --- ETAPE 6 : coefficients saisonniers --------------------------------
p(""); p("="*70); p("ETAPE 6 - COEFFICIENTS SAISONNIERS (modele additif retenu)"); p("="*70)
sc = da.seasonal.groupby(da.seasonal.index.month).mean()
mois = ["Jan","Fev","Mar","Avr","Mai","Jun","Jul","Aou","Sep","Oct","Nov","Dec"]
for m,v in sc.items(): p(f"  {mois[m-1]} : {v:+7.3f}")
p(f"  Somme = {sc.sum():+.4f} (~0 : normalisation additive OK)")

# --- CONCLUSION --------------------------------------------------------
p(""); p("="*70); p("CONCLUSION"); p("="*70)
verdict = "ADDITIVE" if r.pvalue > 0.05 else "MULTIPLICATIVE"
p(f"La decomposition est {verdict} :  Y(t) = T(t) + S(t) + e(t)")
p("Arguments :")
p(f"  1. value = T+S+R a la precision machine (ecart max {np.abs(y-add).max():.1e}) ;")
p("  2. la saisonnalite prend des valeurs negatives et somme a 0 ;")
p(f"  3. l'amplitude annuelle est stable ({full.ecart_type.min():.2f} a {full.ecart_type.max():.2f})")
p(f"     alors que le niveau passe de {full.moyenne.min():.1f} a {full.moyenne.max():.1f} ;")
p(f"  4. regression ecart-type~moyenne : pente {r.slope:.4f}, p={r.pvalue:.3f} -> non significative ;")
p(f"  5. le CV decroit de {full['CV_%'].iloc[0]:.1f}% a {full['CV_%'].iloc[-1]:.1f}%, ce qui est")
p("     exactement le comportement d'une amplitude FIXE sur un niveau croissant.")

txt = "\n".join(str(v) for v in L)
open(OUT+"/rapport_decomposition.txt","w",encoding="utf-8").write(txt)
print(txt)

# --- GRAPHIQUES --------------------------------------------------------
fig, ax = plt.subplots(2,2, figsize=(14,9))
ax[0,0].plot(y.index, y.values, lw=1.2, color="#2b6cb0")
ax[0,0].plot(da.trend.index, da.trend.values, lw=2, color="#c53030", label="tendance")
ax[0,0].set_title("Serie et tendance"); ax[0,0].legend()
ax[0,1].errorbar(full.moyenne, full.ecart_type, fmt="o", color="#2b6cb0")
xx=np.linspace(full.moyenne.min(),full.moyenne.max(),50)
ax[0,1].plot(xx, r.intercept+r.slope*xx, "--", color="#c53030",
             label=f"pente={r.slope:.4f} (p={r.pvalue:.2f})")
for yr,row in full.iterrows(): ax[0,1].annotate(str(yr),(row.moyenne,row.ecart_type),fontsize=7)
ax[0,1].set_xlabel("moyenne annuelle"); ax[0,1].set_ylabel("ecart-type annuel")
ax[0,1].set_title("Test amplitude vs niveau (Buys-Ballot)"); ax[0,1].legend()
for yr,gr in y.groupby(y.index.year):
    if len(gr)==12: ax[1,0].plot(range(1,13), gr.values, marker="o", ms=3, lw=1, label=str(yr))
ax[1,0].set_title("Profil saisonnier par annee (amplitude constante)")
ax[1,0].set_xlabel("mois"); ax[1,0].legend(fontsize=6, ncol=2)
ax[1,1].plot(ra.index, ra.values, lw=1, color="#2f855a"); ax[1,1].axhline(0, color="k", lw=.8)
ax[1,1].set_title("Residus du modele ADDITIF (bruit homoscedastique)")
plt.tight_layout(); plt.savefig(OUT+"/figures_decomposition.png", dpi=130)

fig2 = da.plot(); fig2.set_size_inches(11,8); fig2.suptitle("Decomposition additive", y=1.01)
plt.tight_layout(); plt.savefig(OUT+"/decomposition_additive.png", dpi=130)
print("\n[figures ecrites]")
