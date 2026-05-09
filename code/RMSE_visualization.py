import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "data", "diluent_model_RMSE_data.csv")
df = pd.read_csv(file_path, index_col=0)

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 20

blue = (45/255, 60/255, 129/255)        
light_blue = (218/255, 226/255, 237/255)  

custom_cmap = LinearSegmentedColormap.from_list(
    "custom_map",
    [blue, light_blue]
)

fig, ax = plt.subplots(figsize=(8, 5))

im = ax.imshow(
    df.values,
    cmap=custom_cmap,
    vmin=1.00,  
    vmax=0.00,   
    aspect='auto'
)

ax.set_xticks(np.arange(len(df.columns)))
ax.set_yticks(np.arange(len(df.index)))

ax.set_xticklabels(df.columns)
ax.set_yticklabels(df.index)

ax.tick_params(axis='both', which='both', length=0)

for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        value = df.iloc[i, j]

        color = "white" if df.iloc[i, j] < 0.25 else "black"
        weight = 'bold' if df.iloc[i, j] < 0.25 else 'normal'

        ax.text(j, i, f"{value:.2f}",
                ha='center', va='center',
                color=color)

for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(2)

ax.set_xticks(np.arange(-0.5, len(df.columns), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(df.index), 1), minor=True)

ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
ax.tick_params(which='minor', bottom=False, left=False)

cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

ticks = np.linspace(1.00, 0.00, 2)
cbar.set_ticks(ticks)
cbar.set_ticklabels([f"{t:.2f}" for t in ticks])

cbar.ax.tick_params(length=0)

for spine in cbar.ax.spines.values():
    spine.set_linewidth(2)

ax.set_title(r"Root Mean Square Error (RMSE)", pad=15)

plt.tight_layout()

fig_dir = "figures/data_visualization"
os.makedirs(fig_dir, exist_ok=True)

save_path = f"{fig_dir}/diluent_model_RMSE_visualization.pdf"

plt.savefig(save_path, dpi=600, bbox_inches='tight')

print("done", save_path)
plt.close()
