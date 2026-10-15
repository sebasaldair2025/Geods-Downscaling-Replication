#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 20 16:01:41 2025

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

i=33
j=27

P_sim = simulation['PP'].isel(x=i, y=j)
P_degraded = degraded['pp'].isel(x=i, y=j)
P_obs = observation['pp'].isel(x=i, y=j)

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



lim_max=max(max(obs_quantiles), max(sim_quantiles)) + 50
lim_max=300

fig, axs = plt.subplots(1, 2, figsize=(14, 8))  # 1 row, 2 columns
# First subplot for original simulated data
axs[0].scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black")
axs[0].set_xlim(0, lim_max)
axs[0].set_ylim(0, lim_max)
axs[0].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
axs[0].set_xlabel('Observed precipitation quantiles (mm)', fontname="Arial", fontsize=14)
axs[0].set_ylabel('Simulated precipitation quantiles (mm)', fontname="Arial", fontsize=14)
#axs[0].set_xticks(fontname="Arial", fontsize=14)
#axs[0].set_yticks(fontname="Arial", fontsize=14)
axs[0].set_title('a)', fontname="Arial", y=0, pad=-50, loc="left")
axs[0].grid(linewidth=0.4, linestyle="dotted")
axs[0].text(25, 275,f"R2={r2_deg:.8f}\nMAE={global_mae_deg:.4f}")

# Second subplot for degrad_rl data
axs[1].scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black")
axs[1].set_xlim(0, lim_max)
axs[1].set_ylim(0, lim_max)
axs[1].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
axs[1].set_xlabel('Observed precipitation quantiles (mm)', fontname="Arial", fontsize=14)
axs[1].set_ylabel('Simulated precipitation quantiles (mm)', fontname="Arial", fontsize=14)
#axs[1].set_xticks(fontname="Arial", fontsize=14)
#axs[1].set_yticks(fontname="Arial", fontsize=14)
axs[1].set_title('b)', fontname="Arial", y=0, pad=-50, loc="left")
axs[1].grid(linewidth=0.4, linestyle="dotted")
axs[1].text(25, 275,f"R2={r2_sim:.8f}\nMAE={global_mae:.4f}")
plt.suptitle("Quantile-Quantile plots of coarse resolution and downscaled APGD precipitation datasets", fontsize=16)

# Adjust layout
plt.tight_layout()
#plt.savefig(f'/home/jbrenner/These/Resultats/Article/QQ_plots_precipitation_{reso}km.png', format='png')
plt.show()