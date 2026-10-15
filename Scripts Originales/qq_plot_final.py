#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 12:52:12 2025

@author: jbrenner
"""


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

simu="1"
reso=10


simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_precipitation_Alps_APGD.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/pp_obs.nc')

simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})

P_sim = simulation['PP']
P_degraded = degraded['pp']
P_obs = observation['pp']

masked_P_sim = np.ma.masked_invalid(P_sim)
masked_P_degraded = np.ma.masked_invalid(P_degraded)
masked_P_obs = np.ma.masked_invalid(P_obs)

global_mask=np.ma.mask_or(masked_P_sim.mask, masked_P_obs.mask)
sim_rl=np.ma.masked_array(P_sim, global_mask)
degrad_rl=np.ma.masked_array(P_degraded, global_mask)
obs_rl=np.ma.masked_array(P_obs, global_mask)
sim_rl=sim_rl.compressed()
degrad_rl=degrad_rl.compressed()
obs_rl=obs_rl.compressed()

quantiles = np.linspace(0, 1, 50)
sim_quantiles = np.quantile(sim_rl, quantiles)
deg_quantiles = np.quantile(degrad_rl, quantiles)
obs_quantiles = np.quantile(obs_rl, quantiles)

slope_deg, intercept_deg = np.polyfit(obs_quantiles, deg_quantiles, 1)
# Calculate predicted values
predicted_deg = slope_deg * obs_quantiles + intercept_deg
# Calculate R²
r2_deg = 1 - (np.sum((deg_quantiles - predicted_deg)**2) / np.sum((deg_quantiles - np.mean(deg_quantiles))**2))


slope_sim, intercept_sim = np.polyfit(obs_quantiles, sim_quantiles, 1)
# Calculate predicted values
predicted_sim = slope_sim * obs_quantiles + intercept_sim
# Calculate R²
r2_sim = 1 - (np.sum((sim_quantiles - predicted_sim)**2) / np.sum((sim_quantiles - np.mean(sim_quantiles))**2))


diff = (sim_quantiles - obs_quantiles)
v_rmse = diff**2
v_mae = np.ma.abs(diff)

global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
global_mae = np.nanmean(v_mae).item()


diff_deg = (deg_quantiles - obs_quantiles)
v_rmse_deg = diff_deg**2
v_mae_deg = np.abs(diff_deg)

global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
global_mae_deg = np.nanmean(v_mae_deg).item()



t=16

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

n=3

fig, axs = plt.subplots(2, 2, figsize=(12,12))
fig.subplots_adjust(hspace=0.1, wspace=0.1)  # adjust space between Axes


ax1=axs[0,0]
ax2=axs[0,1]
ax3=axs[1,0]
ax4=axs[1,1]
# plot the same data on both Axes
ax1.scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black")
ax2.scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black",s=150, linewidths=1.5)
ax3.scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black",s=150, linewidths=1.5)
ax4.scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black")



# zoom-in / limit the view to different portions of the data
ax1.set_ylim(750,1200)   # outliers only
ax1.set_xlim(0,350)
ax3.set_ylim(0, 350)  # most of the data
ax3.set_xlim(0,350)
ax4.set_xlim(750,1200)   # outliers only
ax4.set_ylim(0,350)
ax2.set_xlim(750, 1200)
ax2.set_ylim(750,1200) 

ax3.plot([0, 350], [0, 350], color="red", linewidth=1.5)
ax2.plot([750, 1200], [750, 1200], color="red", linewidth=1.5)

# ax1.set_ylim(800,1400)   # outliers only
# ax1.set_xlim(0,600)
# ax3.set_ylim(0, 600)  # most of the data
# ax3.set_xlim(0,600)
# ax4.set_xlim(800,1400)   # outliers only
# ax4.set_ylim(0,800)
# ax2.set_xlim(800,1400)
# ax2.set_ylim(800,1400) 


# ax3.plot([0, 600], [0, 600], color="red", linewidth=1.5)
# ax2.plot([800, 1400], [800, 1400], color="red", linewidth=1.5)

#ax1.set_ylabel('Simulated quantiles (mm)', position=(0,0), loc="bottom")

yticks = ticker.MultipleLocator(100)

# hide the spines between ax and ax2
ax1.spines.bottom.set_visible(False)
ax1.spines.right.set_visible(False)
ax3.spines.top.set_visible(False)
ax3.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)
ax2.spines.bottom.set_visible(False)
ax4.spines.top.set_visible(False)
ax4.spines.left.set_visible(False)

ax1.xaxis.tick_top()
ax3.yaxis.set_major_locator(yticks)

y2ticks = ticker.MultipleLocator(100)

ax1.yaxis.set_major_locator(y2ticks)
#ax3.yaxis.set_major_locator(yticks)
ax1.tick_params(axis='both', top=False, labeltop=False, labelsize=t)  # don't put tick labels at the top



ax2.tick_params(axis='both', left=False, bottom=False, labelleft=False, labelright=False,labeltop=False, labelbottom=False, labelsize=t)
ax4.tick_params(axis='both', left=False, labelleft=False, labelright=False,labeltop=False, labelsize=t)
ax4.tick_params(axis='x', labelsize=t, labelrotation=45)
ax3.tick_params(axis='x', labelsize=t, labelrotation=45)
ax3.tick_params(axis='y', labelsize=t)

ax1.text(50, 1080,f"R2={r2_sim:.8f}", fontsize=18)
ax1.text(50, 1015,r"MAE$_{quantiles}$" f"={global_mae:.4f} mm", fontsize=18)
ax1.text(50, 950,f"MAE=17.6523 mm", fontsize=18)

plt.figtext(0.4, 0.03, "Observed quantiles (mm)", fontsize=20)
plt.figtext(0.03, 0.4, "Predicted quantiles (mm)", fontsize=20, rotation="vertical")
plt.savefig(f'/home/jbrenner/These/Resultats/Article/qq_plot_geods_{reso}.png', format='png')
plt.show()





import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

n=3

fig, axs = plt.subplots(2, 2, figsize=(12,12))
fig.subplots_adjust(hspace=0.1, wspace=0.1)  # adjust space between Axes


ax1=axs[0,0]
ax2=axs[0,1]
ax3=axs[1,0]
ax4=axs[1,1]
# plot the same data on both Axes
ax1.scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black")
ax2.scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black",s=150, linewidths=1.5)
ax3.scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black",s=150, linewidths=1.5)
ax4.scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black")



# zoom-in / limit the view to different portions of the data
ax1.set_ylim(750,1200)   # outliers only
ax1.set_xlim(0,350)
ax3.set_ylim(0, 350)  # most of the data
ax3.set_xlim(0,350)
ax4.set_xlim(750,1200)   # outliers only
ax4.set_ylim(0,350)
ax2.set_xlim(750, 1200)
ax2.set_ylim(750,1200) 

ax3.plot([0, 350], [0, 350], color="red", linewidth=1.5)
ax2.plot([750, 1200], [750, 1200], color="red", linewidth=1.5)


# ax1.set_ylim(800,1400)   # outliers only
# ax1.set_xlim(0,600)
# ax3.set_ylim(0, 600)  # most of the data
# ax3.set_xlim(0,600)
# ax4.set_xlim(800,1400)   # outliers only
# ax4.set_ylim(0,800)
# ax2.set_xlim(800,1400)
# ax2.set_ylim(800,1400) 


# ax3.plot([0, 600], [0, 600], color="red", linewidth=1.5)
# ax2.plot([800, 1400], [800, 1400], color="red", linewidth=1.5)

#ax1.set_ylabel('Simulated quantiles (mm)', position=(0,0), loc="bottom")

yticks = ticker.MultipleLocator(100)

# hide the spines between ax and ax2
ax1.spines.bottom.set_visible(False)
ax1.spines.right.set_visible(False)
ax3.spines.top.set_visible(False)
ax3.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)
ax2.spines.bottom.set_visible(False)
ax4.spines.top.set_visible(False)
ax4.spines.left.set_visible(False)

ax1.xaxis.tick_top()
ax3.yaxis.set_major_locator(yticks)

y2ticks = ticker.MultipleLocator(100)

ax1.yaxis.set_major_locator(y2ticks)
#ax3.yaxis.set_major_locator(yticks)
ax1.tick_params(axis='both', top=False, labeltop=False, labelsize=t)  # don't put tick labels at the top



ax2.tick_params(axis='both', left=False, bottom=False, labelleft=False, labelright=False,labeltop=False, labelbottom=False, labelsize=t)
ax4.tick_params(axis='both', left=False, labelleft=False, labelright=False,labeltop=False, labelsize=t)
ax4.tick_params(axis='x', labelsize=t, labelrotation=45)
ax3.tick_params(axis='x', labelsize=t, labelrotation=45)
ax3.tick_params(axis='y', labelsize=t)




ax1.text(50, 1080,f"R2={r2_sim:.8f}", fontsize=18)
ax1.text(50, 1015,r"MAE$_{quantiles}$" f"=14.6787 mm", fontsize=18)
ax1.text(50, 950,f"MAE=16.6283 mm", fontsize=18)

plt.figtext(0.4, 0.03, "Observed quantiles (mm)", fontsize=20)
plt.figtext(0.03, 0.4, "Predicted quantiles (mm)", fontsize=20, rotation="vertical")
plt.savefig(f'/home/jbrenner/These/Resultats/Article/qq_plot_ref_{reso}.png', format='png')
plt.show()
























#______________________________________________________________________________________________________________________________







