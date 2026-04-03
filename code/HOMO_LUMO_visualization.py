import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 18

# Data
diluents = ["FBn", "dFBn", "tFBn", "hFBn"]
HOMO = np.array([-9.07, -9.23, -9.46, -9.89])
LUMO = np.array([-0.43, -0.33, -0.21, -0.78])
gap = LUMO - HOMO

x = np.arange(len(diluents))

# Figure setup (Nature-like aspect ratio)
plt.figure(figsize=(8, 5))

# Plot HOMO & LUMO levels
for i in range(len(x)):
    # HOMO line
    plt.hlines(HOMO[i], x[i]-0.25, x[i]+0.25, colors="red", linewidth=5)
    
    # LUMO line
    plt.hlines(LUMO[i], x[i]-0.25, x[i]+0.25, colors="red", linewidth=5)
    
    # Gap arrow (double arrow)
    plt.annotate(
        '',
        xy=(x[i], LUMO[i]),
        xytext=(x[i], HOMO[i]),
        arrowprops=dict(
            arrowstyle='<->',
            linewidth=3.0,
            shrinkA=0,
            shrinkB=0
        )
    )
    
    # Gap value annotation (centered)
    plt.text(
        x[i] + 0.05,
        (HOMO[i] + LUMO[i]) / 2,
        f"{abs(gap[i]):.2f}",
        va='center',
        fontsize=18
    )

# Axes formatting
plt.xticks(x, diluents, fontsize=18)
plt.ylabel("Energy (eV)", fontsize=18)

# Y range (clean scientific range)
plt.ylim(-10.9, 0.9)

# Spine styling (Nature style: no top/right)
ax = plt.gca()
for spine in ax.spines.values():
    spine.set_linewidth(2)

# Tick styling
ax.tick_params(direction='out', length=3, width=2, labelsize=18)

# Minor ticks (subtle but professional)
ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
ax.tick_params(which='minor', length=2, width=2)

# Tight layout
plt.tight_layout()

fig_dir = "figures/data_visualization"
os.makedirs(fig_dir, exist_ok=True)

# Save high-quality figure (recommended for publication)

save_path = f"{fig_dir}/HOMO_LUMO_visualization.pdf"

plt.savefig(save_path, dpi=600, bbox_inches='tight')

print("done", save_path)
plt.close()
