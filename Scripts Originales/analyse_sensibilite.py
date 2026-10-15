import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import LogFormatter
from matplotlib import ticker

# 1. Load data
df = pd.read_csv('/home/jbrenner/These/Algorithmes/Scripts_Python/APGD_scripts/resultats_test_sensibilite_geods_alps.csv', sep=';')

# 2. Calculate log transformations
df['log_MAE'] = np.log(df['MAE'])
df['log_MAE_quantiles'] = np.log(df['MAE_quantiles'])
df["searching_distance"] = df["searching_distance"] / 1000

# Formatter to display original values
def original_scale_formatter(x, pos):
    return f"$e^{{{x:.1f}}}$"

# 3. Configure parameters and figure
#norm = Normalize(vmin=df['MAE'].min()-0.025, vmax=df['MAE'].max()-0.8)
norm=LogNorm(vmin=15, vmax=50)
cmap = plt.get_cmap('viridis_r')

fig, axs = plt.subplots(2, 3, figsize=(22, 14))

# Find indices of 10 points with lowest MAE
lowest_mae_indices = df.nsmallest(10, 'MAE').index

# Plot 1: beta vs log_MAE_quantiles
ax1 = axs[0,0]
sc1 = ax1.scatter(df["beta"], df['MAE_quantiles'], c=df['MAE'], cmap=cmap, norm=norm, alpha=0.7, s=25)
ax1.scatter(df["beta"].iloc[lowest_mae_indices], df['MAE_quantiles'].iloc[lowest_mae_indices], 
            edgecolor='red', facecolor='none', s=30, linewidth=1.5)
ax1.set_xlabel('beta', fontsize=18)
ax1.set_ylabel(r'MAE$_{quantiles}$ (mm)', fontsize=18)
ax1.axhline(y=14.6796, c='red')
ax1.set_yscale('log')
ax1.set_yticks([1, 10, 100, 1000])


# Plot 2: delta vs log_MAE_quantiles
ax2 = axs[0,1]
sc2 = ax2.scatter(df["delta"], df['MAE_quantiles'], c=df['MAE'], cmap=cmap, norm=norm, alpha=0.7, s=25)
ax2.scatter(df["delta"].iloc[lowest_mae_indices], df['MAE_quantiles'].iloc[lowest_mae_indices], 
            edgecolor='red', facecolor='none', s=30, linewidth=1.5)
ax2.set_xlabel('gamma', fontsize=18)
ax2.set_ylabel(r'MAE$_{quantiles}$ (mm)', fontsize=18)
ax2.axhline(y=14.6796, c='red')
ax2.set_yscale('log')
ax2.set_yticks([1, 10, 100, 1000])


# Plot 3: nbr_wdir vs log_MAE_quantiles
ax3 = axs[0,2]
sc3 = ax3.scatter(df["nbr_wdir"], df['MAE_quantiles'], c=df['MAE'], cmap=cmap, norm=norm, alpha=0.7, s=25)
ax3.scatter(df["nbr_wdir"].iloc[lowest_mae_indices], df['MAE_quantiles'].iloc[lowest_mae_indices], 
            edgecolor='red', facecolor='none', s=30, linewidth=1.5)
ax3.set_xlabel('nbr_wdir', fontsize=18)
ax3.set_ylabel(r'MAE$_{quantiles}$ (mm)', fontsize=18)
ax3.axhline(y=14.6796, c='red')
ax3.set_yscale('log')
ax3.set_yticks([1, 10, 100, 1000])

# Plot 4: searching_distance vs log_MAE_quantiles
ax4 = axs[1,0]
sc4 = ax4.scatter(df["searching_distance"], df['MAE_quantiles'], c=df['MAE'], cmap=cmap, norm=norm, alpha=0.7, s=25)
ax4.scatter(df["searching_distance"].iloc[lowest_mae_indices], df['MAE_quantiles'].iloc[lowest_mae_indices], 
            edgecolor='red', facecolor='none', s=30, linewidth=1.5)
ax4.set_xlabel('searching_distance (km)', fontsize=18)
ax4.set_ylabel(r'MAE$_{quantiles}$ (mm)', fontsize=18)
ax4.axhline(y=14.6796, c='red')
ax4.set_yscale('log')
ax4.set_yticks([1, 10, 100, 1000])


# Plot 5: max_P_factor vs log_MAE_quantiles
ax5 = axs[1,1]
sc5 = ax5.scatter(df["max_P_factor"], df['MAE_quantiles'], c=df['MAE'], cmap=cmap, norm=norm, alpha=0.7, s=25)
ax5.scatter(df["max_P_factor"].iloc[lowest_mae_indices], df['MAE_quantiles'].iloc[lowest_mae_indices], 
            edgecolor='red', facecolor='none', s=30, linewidth=1.5)
ax5.set_xlabel('max_P_factor', fontsize=16)
ax5.set_ylabel(r'MAE$_{quantiles}$ (mm)', fontsize=16)
ax5.axhline(y=14.6796, c='red')
ax5.set_yscale('log')
ax5.set_yticks([1, 10, 100, 1000])


# Turn off the last subplot
axs[1,2].set_axis_off()

# Add colorbar
cbar = fig.colorbar(sc1, ax=axs,orientation='horizontal',aspect=80,pad=0.08)
cbar.set_label(label="MAE (mm)", size=16)
tick_locator = ticker.MaxNLocator(nbins=7)
cbar.locator = tick_locator
cbar.update_ticks()
cbar.set_ticks([15, 20, 25, 30, 35, 40, 45], labels=['15', '20', '25', '30', '35', '40', '45'])
cbar.ax.tick_params(labelsize=14)
#cbar.set_ticks([1,10,100,1000])
#cbar.set_ticklabels([1,10,100,1000])

#plt.tight_layout()
plt.rc('xtick',labelsize=16)
plt.rc('ytick',labelsize=16)
plt.savefig("/home/jbrenner/These/Resultats/Article/Analyse_Sensibilite")
plt.show()

