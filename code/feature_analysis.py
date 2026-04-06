import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import shap

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

feature_file = os.path.join(BASE_DIR, "..", "data", "diluent_feature.csv")

target_file = os.path.join(
    BASE_DIR,
    "..",
    "results",
    "diluent_vol_conductivity_poly3_fit",
    "diluent_vol_conductivity_poly3_fit.csv"
)

fig_dir = "Figures/feature_analysis"
res_dir = "results/feature_analysis"

os.makedirs(fig_dir, exist_ok=True)
os.makedirs(res_dir, exist_ok=True)

df_feature = pd.read_csv(feature_file)
df_target = pd.read_csv(target_file)

df_feature.columns = df_feature.columns.str.strip()
df_target.columns = df_target.columns.str.strip()

df = pd.merge(df_feature, df_target, on="Diluent")

y = df["Optimal Ionic Conductivity"]

X = df.drop(columns=[
    "Diluent",
    "Optimal Ionic Conductivity",
    "Optimal Content",
    "R2_LOOCV",
    "RMSE_LOOCV"
])

X.columns = X.columns.str.strip()

def find_col(keyword_list):
    for col in X.columns:
        for key in keyword_list:
            if key.lower() in col.lower():
                return col
    return None

feature_pairs = [
    ("LUMO energy", find_col(["lumo"])),
    ("HOMO energy", find_col(["homo"])),
    ("HOMO/LUMO gap", find_col(["gap"])),
    ("dielectric constant", find_col(["dielectric"])),
    ("molecular weight", find_col(["weight", "mw"])),
    ("viscosity coefficient", find_col(["viscosity", "eta"])),
    ("dipole moment", find_col(["dipole"]))
]

missing = [name for name, col in feature_pairs if col is None]
if missing:
    print("feature unfound", missing)
    raise ValueError("false")

feature_names = [p[0] for p in feature_pairs]
feature_cols  = [p[1] for p in feature_pairs]

X = X[feature_cols]
X.columns = feature_names

spearman_corr = df.corr(method='spearman', numeric_only=True)
spearman_corr.to_csv(f"{res_dir}/spearman_correlation.csv")

kendall_corr = df.corr(method='kendall', numeric_only=True)
kendall_corr.to_csv(f"{res_dir}/kendall_correlation.csv")

rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
rf_model.fit(X, y)

importance = rf_model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

importance_df.to_csv(f"{res_dir}/rf_feature_importance.csv", index=False)

plt.figure(figsize=(6,4))

plt.barh(
    importance_df["Feature"],
    importance_df["Importance"],
    color='red'
)

plt.gca().invert_yaxis()
plt.xlim(0, 0.4)

plt.xlabel("RF Importance", fontsize=12, fontname='Arial')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12, fontname='Arial')

for spine in plt.gca().spines.values():
    spine.set_linewidth(1.2)

plt.tight_layout()
plt.savefig(f"{fig_dir}/rf_feature_importance.pdf", dpi=600)
plt.close()

perm = permutation_importance(
    rf_model,
    X,
    y,
    n_repeats=50,
    random_state=42
)

perm_df = pd.DataFrame({
    "Feature": X.columns,
    "Permutation Importance Mean": perm.importances_mean,
    "Permutation Importance Std": perm.importances_std
})

perm_df.to_csv(f"{res_dir}/permutation_importance.csv", index=False)

plt.figure(figsize=(6,4))

plt.barh(
    perm_df["Feature"],
    perm_df["Permutation Importance Mean"],
    xerr=perm_df["Permutation Importance Std"],
    color='red',
    capsize=3
)

ax = plt.gca()

ax.invert_yaxis()
ax.set_xlim(0, 0.4)

plt.xlabel("Permutation Importance", fontsize=12, fontname='Arial')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12, fontname='Arial')

for spine in plt.gca().spines.values():
    spine.set_linewidth(1.2)

plt.tight_layout()
plt.savefig(f"{fig_dir}/permutation_importance.pdf", dpi=600)
plt.close()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

rf_model.fit(X_scaled, y)

explainer = shap.Explainer(rf_model, X_scaled)
shap_values = explainer(X_scaled)

plt.figure(figsize=(6,4))

shap.summary_plot(
    shap_values,
    X,
    plot_type="dot",
    show=False,
    color_bar=True
)

ax = plt.gca()

ax.set_xlim(-1, 1)
ax.set_xticks(np.arange(-1, 1.1, 0.5))
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

ax.set_title("")

ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for side in ["left", "right", "top", "bottom"]:
    ax.spines[side].set_visible(True)
    ax.spines[side].set_linewidth(1.2)

plt.tight_layout()
plt.savefig(f"{fig_dir}/shap_summary.pdf", dpi=600)
plt.close()

print("DONE.")
