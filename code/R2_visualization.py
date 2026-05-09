import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "data", "diluent_model_R2_data.csv")
df = pd.read_csv(file_path, index_col=0)

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 20

red = (201/255, 71/255, 55/255)         
light_brown = (252/255, 240/255, 225/255)  

custom_cmap = LinearSegmentedColormap.from_list(
    "custom_map",
    [light_brown, red]
)

fig, ax = plt.subplots(figsize=(8, 5))

im = ax.imshow(
    df.values,
    cmap=custom_cmap,
    vmin=0.75,   
    vmax=1.0, 
    aspect='auto'
)

ax.set_xticks(np.arange(len(df.columns)))
ax.set_yticks(np.arange(len(df.index)))

ax.set_xticklabels(df.columns)
ax.set_yticklabels(df.index)

ax.tick_params(axis='both', which='both', length=0)

for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        value = df.iloc[i, j] * 100

        color = "white" if df.iloc[i, j] > 0.95 else "black"
        weight = 'bold' if df.iloc[i, j] > 0.95 else 'normal'

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

ticks = np.linspace(0.75, 1.0, 2)
cbar.set_ticks(ticks)
cbar.set_ticklabels([f"{int(t*100)}%" for t in ticks])

cbar.ax.tick_params(length=0)

for spine in cbar.ax.spines.values():
    spine.set_linewidth(2)

ax.set_title(r"Coefficient of Determination ($R^2$, %)", pad=15)

plt.tight_layout()

fig_dir = "figures/data_visualization"
os.makedirs(fig_dir, exist_ok=True)

save_path = f"{fig_dir}/diluent_model_R2_visualization.pdf"

plt.savefig(save_path, dpi=600, bbox_inches='tight')

print("done", save_path)
plt.close()
