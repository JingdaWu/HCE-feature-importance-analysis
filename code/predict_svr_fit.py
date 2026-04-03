import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from matplotlib.ticker import MultipleLocator
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

file_path = r"data\diluent_vol_conductivity_data.csv"
df = pd.read_csv(file_path, header=None)

additives = df.iloc[0, 1:6].values

os.makedirs("results", exist_ok=True)
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

    model = SVR(
    kernel='rbf', 
    C=10,
    gamma=0.1,
    epsilon=0.1
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_all)

    model.fit(X_scaled, y_all)

    y_pred = model.predict(X_scaled)

    loo = LeaveOneOut()
    y_true_all = []
    y_pred_all = []

    for train_index, test_index in loo.split(X_all):

        scaler = StandardScaler()

        X_train = scaler.fit_transform(X_all[train_index])
        X_test = scaler.transform(X_all[test_index])

        y_train, y_test = y_all[train_index], y_all[test_index]

        model_loo = SVR(
            kernel='rbf',
            C=10,
            gamma=0.1,
            epsilon=0.1
        )

        model_loo.fit(X_train, y_train)
        y_pred_test = model_loo.predict(X_test)

        y_true_all.append(y_test[0])
        y_pred_all.append(y_pred_test[0])

        y_pred_test = model_loo.predict(X_test)

    r2 = r2_score(y_true_all, y_pred_all)
    rmse = np.sqrt(mean_squared_error(y_true_all, y_pred_all))

    X_range = np.linspace(min(X_all), max(X_all), 200).reshape(-1, 1)
    X_range_scaled = scaler.transform(X_range)
    y_range_pred = model.predict(X_range_scaled)

    best_idx = np.argmax(y_range_pred)
    best_X = X_range[best_idx][0]
    best_y = y_range_pred[best_idx]

    plt.figure()

    plt.scatter(X_all, y_all, color='black')

    plt.plot(X_range, y_range_pred, color='red')

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
    fontsize=30,
    fontname='Arial',
    verticalalignment='top'
)

    fig_dir = "figures/diluent_vol_conductivity_svr_fit"
    os.makedirs(fig_dir, exist_ok=True)

    plt.savefig(f"{fig_dir}/{additive}.pdf", dpi=600, bbox_inches='tight')
    plt.close()

    results_list.append({
        "Diluent": additive,
        "Optimal Content": best_X,
        "Optimal Ionic Conductivity": best_y,
        "R2_LOOCV": r2,
        "RMSE_LOOCV": rmse
    })

results_dir = "results/diluent_vol_conductivity_svr_fit"
os.makedirs(results_dir, exist_ok=True)

results_df = pd.DataFrame(results_list)
results_df.to_csv(f"{results_dir}/diluent_vol_conductivity_svr_fit.csv", index=False)

print("Done.")
