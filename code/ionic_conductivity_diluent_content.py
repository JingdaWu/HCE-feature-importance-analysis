import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from matplotlib.ticker import MultipleLocator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "data", "diluent_vol_conductivity_data.csv")
df = pd.read_csv(file_path, header=None)

additives = df.iloc[0, 1:6].values

os.makedirs("figures", exist_ok=True)

results_list = []

for i, additive in enumerate(additives):

    X_raw = df.iloc[1:, 0]
    y_raw = df.iloc[1:, i+1]

    X_numeric = pd.to_numeric(X_raw, errors='coerce')
    y_numeric = pd.to_numeric(y_raw, errors='coerce')

    valid_mask = X_numeric.notna() & y_numeric.notna()

    X_all = X_numeric[valid_mask].values.reshape(-1, 1)
    y_all = y_numeric[valid_mask].values

    plt.figure()

    plt.scatter(X_all, y_all, color='black')

    plt.ylim(0, 10)
    plt.xlim(-5, 85) 

    plt.yticks([0, 2, 4, 6, 8, 10], fontname='Arial', fontsize=18)

    plt.gca().yaxis.set_minor_locator(MultipleLocator(1))

    plt.gca().xaxis.set_major_locator(MultipleLocator(10))

    plt.gca().xaxis.set_minor_locator(MultipleLocator(5))

    plt.xticks(fontname='Arial', fontsize=18)

    plt.tick_params(direction='in', which='both')

    plt.xlabel("Diluent content (vol%)", fontname='Arial', fontsize=18)
    plt.ylabel("Ionic Conductivity (mS cm$^{-1}$)", fontname='Arial', fontsize=18)

    plt.text(
    0.03, 0.95,             
    f"{additive}-LiFSI-DME",
    transform=plt.gca().transAxes,
    fontsize=18,
    fontname='Arial',
    verticalalignment='top'
)

    fig_dir = "figures/diluent_vol_conductivity"
    os.makedirs(fig_dir, exist_ok=True)

    plt.savefig(f"{fig_dir}/{additive}.pdf", dpi=600, bbox_inches='tight')
    plt.close()

print("Done.")
