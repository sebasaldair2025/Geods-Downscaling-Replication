#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:31:46 2025

@author: jbrenner
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#_____________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________

# RESULTATS GLOBAUX 

simu="1"

simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_precipitation_Alps_APGD.nc')
degraded = xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/5km/APGD_degraded_1971-2019_full.nc')
observation = xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/5km/APGD_HR_1971-2019_remapnn_5km.nc')

simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})

P_sim = simulation['PP']
P_degraded = degraded['pp']
P_obs = observation['pp']

masked_P_sim = np.ma.masked_invalid(P_sim)
masked_P_degraded = np.ma.masked_invalid(P_degraded)
masked_P_obs = np.ma.masked_invalid(P_obs)


diff = (masked_P_sim - masked_P_obs)
v_rmse = diff**2
v_mae = np.abs(diff)

global_rmse = np.sqrt(np.mean(v_rmse)).item()
global_mae = np.mean(v_mae).item()

rmse_matrix = np.sqrt(np.mean(v_rmse, axis=0))
mae_matrix = np.sqrt(np.mean(v_mae, axis=0))



global_mask=np.ma.mask_or(masked_P_sim.mask, masked_P_obs.mask)
sim_rl=np.ma.masked_array(P_sim, global_mask)
degrad_rl=np.ma.masked_array(P_degraded, global_mask)
obs_rl=np.ma.masked_array(P_obs, global_mask)
sim_rl=sim_rl.compressed()
degrad_rl=degrad_rl.compressed()
obs_rl=obs_rl.compressed()


slope, intercept = np.polyfit(obs_rl, sim_rl, 1)
# Calculate predicted values
predicted = slope * obs_rl + intercept
# Calculate R²
r_squared = 1 - (np.sum((sim_rl - predicted)**2) / np.sum((sim_rl - np.mean(sim_rl))**2))


plt.figure(figsize=(8, 8))
plt.scatter(obs_rl, sim_rl, alpha=0.5)
plt.xlim(0, sim_rl.max())
plt.ylim(0, sim_rl.max())
plt.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
plt.xlabel('Observed Precipitation (mm)')
plt.ylabel('Simulated Precipitation (mm)')
plt.title('Simulated vs Observed Precipitation')
plt.grid()
#plt.axis('equal')
plt.text(0.1 * obs_rl.max(), 0.9 * sim_rl.max(), f'R² = {r_squared:.4f}', fontsize=12, color='blue')
#plt.savefig(f'/home/jbrenner/These/GeoDS_Outputs/Statistics/Simulation/DS_simu_{simu}_global_scatter_plot.png', format='png')
#plt.show()


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# RESULTATS GLOBAUX 

simu="ref"

reso=10

simu="1"
reso=10


simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_precipitation_Alps_APGD.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/pp_obs.nc')


simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})

r2_sim_list=[]
mae_sim=[]
rmse_sim=[]

months=[]


for i in range (1,13):
    ts_sim = simulation['PP'].where(simulation['time'].dt.month==i)
    ts_degraded = degraded['pp'].where(degraded['time'].dt.month==i)
    ts_obs = observation['pp'].where(observation['time'].dt.month==i)

        
    mask_sim = ts_sim.notnull()
    mask_degraded = ts_degraded.notnull()
    mask_obs = ts_obs.notnull()
    
    combined_mask = np.logical_and(np.logical_and(mask_sim, mask_degraded), mask_obs)
    
    
    # Apply the combined mask to each array
    ts_sim_masked = ts_sim.where(combined_mask)
    ts_degraded_masked = ts_degraded.where(combined_mask)
    ts_obs_masked = ts_obs.where(combined_mask)
    
    
    
    
    
    #__________________________________________________________________
    # Degraded stats
    
    
    diff_deg = (ts_degraded_masked - ts_obs_masked)
    v_rmse_deg = diff_deg**2
    v_mae_deg = np.abs(diff_deg)
    
    global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
    global_mae_deg = np.nanmean(v_mae_deg).item()
    
    rmse_matrix_deg = np.ma.sqrt(np.ma.mean(v_rmse_deg, axis=0))
    mae_matrix_deg = np.sqrt(np.ma.mean(v_mae_deg, axis=0))
    
    #_________________________________________________________________
    # DS stats
    
    
    diff = (ts_sim_masked - ts_obs_masked)
    v_rmse = diff**2
    v_mae = np.ma.abs(diff)
    
    global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
    global_mae = np.nanmean(v_mae).item()
    
    rmse_matrix = np.sqrt(np.nanmean(v_rmse, axis=0))
    mae_matrix = np.sqrt(np.nanmean(v_mae, axis=0))
    
       
    ts_sim = simulation['PP'].where(simulation['time'].dt.month==i)
    ts_degraded = degraded['pp'].where(degraded['time'].dt.month==i)
    ts_obs = observation['pp'].where(observation['time'].dt.month==i)
    
    masked_ts_sim = np.ma.masked_invalid(ts_sim)
    masked_ts_degraded = np.ma.masked_invalid(ts_degraded)
    masked_ts_obs = np.ma.masked_invalid(ts_obs)
    
    global_mask=np.ma.mask_or(masked_ts_sim.mask, masked_ts_obs.mask)
    sim_rl=np.ma.masked_array(ts_sim, global_mask)
    deg_rl=np.ma.masked_array(ts_degraded, global_mask)
    obs_rl=np.ma.masked_array(ts_obs, global_mask)
    sim_rl=sim_rl.compressed()
    deg_rl=deg_rl.compressed()
    obs_rl=obs_rl.compressed()
    
    
    
    slope_deg, intercept_deg = np.polyfit(obs_rl, deg_rl, 1)
    # Calculate predicted values
    predicted_deg = slope_deg * obs_rl + intercept_deg
    # Calculate R²
    r2_deg = 1 - (np.sum((deg_rl - predicted_deg)**2) / np.sum((deg_rl - np.mean(deg_rl))**2))
    
    
   
    
    slope, intercept = np.polyfit(obs_rl, sim_rl, 1)
    # Calculate predicted values
    predicted = slope * obs_rl + intercept
    # Calculate R²
    r2 = 1 - (np.sum((sim_rl - predicted)**2) / np.sum((sim_rl - np.mean(sim_rl))**2))
  
    r2_sim_list.append(r2)
    mae_sim.append(global_mae)
    rmse_sim.append(global_rmse)
    
    months.append(i)
    

fig, ax = plt.subplots(figsize=(10,8))
ax.plot(months, r2_sim_list, label='sim', marker='o')
plt.suptitle("monthly R2 precip")
plt.legend()
plt.show()



#_________________________________________________________________________________________________________________________
# QQ-plots

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

simu="1"
reso=15


simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_precipitation_Alps_APGD.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/Cartes/Greenland/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/Cartes/Greenland/pp_obs.nc')

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



#lim_max=max(max(obs_quantiles), max(sim_quantiles)) + 50
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
plt.savefig(f'/home/jbrenner/These/Resultats/Article/QQ_plots_precipitation_{reso}km.png', format='png')
plt.show()



#QQ plots par mois

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


for i in range (1,13):
    P_sim = simulation['PP'].where(simulation['time'].dt.month==i)
    P_degraded = degraded['pp'].where(degraded['time'].dt.month==i)
    P_obs = observation['pp'].where(observation['time'].dt.month==i)


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
    
    lim_max=max(sim_quantiles)
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
    axs[0].text(25, 275,f"R2={r2_sim:.4f}\nMAE={global_mae_deg:.4f}")
    
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
    axs[1].text(25, 275,f"R2={r2_sim:.4f}\nMAE={global_mae:.4f}")
    plt.suptitle(f"Quantile-Quantile plots of coarse resolution {reso} and downscaled APGD precipitation datasets for month n°{i}", fontsize=16)
    
    # Adjust layout
    plt.tight_layout()
    #plt.savefig('/home/jbrenner/These/Resultats/Article/QQ_plots.png', format='png')
    plt.show()


#QQ plots par saison

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


P_sim = simulation['PP'].where((simulation['time'].dt.month==1) | (simulation['time'].dt.month==2) | (simulation['time'].dt.month==12))
P_degraded = degraded['pp'].where((degraded['time'].dt.month==1) | (degraded['time'].dt.month==2) | (degraded['time'].dt.month==12))
P_obs = observation['pp'].where((observation['time'].dt.month==1) | (observation['time'].dt.month==2) | (observation['time'].dt.month==12))


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
r2_deg_winter = 1 - (np.sum((deg_quantiles - predicted_deg)**2) / np.sum((deg_quantiles - np.mean(deg_quantiles))**2))


slope_sim, intercept_sim = np.polyfit(obs_quantiles, sim_quantiles, 1)
# Calculate predicted values
predicted_sim = slope_sim * obs_quantiles + intercept_sim
# Calculate R²
r2_sim_winter = 1 - (np.sum((sim_quantiles - predicted_sim)**2) / np.sum((sim_quantiles - np.mean(sim_quantiles))**2))

diff = (sim_quantiles - obs_quantiles)
v_rmse = diff**2
v_mae = np.ma.abs(diff)

global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
global_mae_winter = np.nanmean(v_mae).item()


diff_deg = (deg_quantiles - obs_quantiles)
v_rmse_deg = diff_deg**2
v_mae_deg = np.abs(diff_deg)

global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
global_mae_deg_winter = np.nanmean(v_mae_deg).item()

lim_max=max(sim_quantiles)
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
axs[0].text(25, 275,f"R2={r2_sim_winter:.4f}\nMAE={global_mae_deg_winter:.4f}")

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
axs[1].text(25, 275,f"R2={r2_sim_winter:.4f}\nMAE={global_mae_winter:.4f}")
plt.suptitle(f"Quantile-Quantile plots of coarse resolution {reso} and downscaled APGD precipitation datasets during winter", fontsize=16)

# Adjust layout
plt.tight_layout()
#plt.savefig('/home/jbrenner/These/Resultats/Article/QQ_plots.png', format='png')
plt.show()

simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_precipitation_Alps_APGD.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/pp_obs.nc')

simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})


P_sim = simulation['PP'].where((simulation['time'].dt.month==6) | (simulation['time'].dt.month==7) | (simulation['time'].dt.month==8))
P_degraded = degraded['pp'].where((degraded['time'].dt.month==6) | (degraded['time'].dt.month==7) | (degraded['time'].dt.month==8))
P_obs = observation['pp'].where((observation['time'].dt.month==6) | (observation['time'].dt.month==7) | (observation['time'].dt.month==8))


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
r2_deg_summer = 1 - (np.sum((deg_quantiles - predicted_deg)**2) / np.sum((deg_quantiles - np.mean(deg_quantiles))**2))


slope_sim, intercept_sim = np.polyfit(obs_quantiles, sim_quantiles, 1)
# Calculate predicted values
predicted_sim = slope_sim * obs_quantiles + intercept_sim
# Calculate R²
r2_sim_summer = 1 - (np.sum((sim_quantiles - predicted_sim)**2) / np.sum((sim_quantiles - np.mean(sim_quantiles))**2))

diff = (sim_quantiles - obs_quantiles)
v_rmse = diff**2
v_mae = np.ma.abs(diff)

global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
global_mae_summer = np.nanmean(v_mae).item()


diff_deg = (deg_quantiles - obs_quantiles)
v_rmse_deg = diff_deg**2
v_mae_deg = np.abs(diff_deg)

global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
global_mae_deg_summer = np.nanmean(v_mae_deg).item()



lim_max=max(sim_quantiles)
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
axs[0].text(25, 275,f"R2={r2_sim_summer:.4f}\nMAE={global_mae_deg_summer:.4f}")

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
axs[1].text(25, 275,f"R2={r2_sim_summer:.4f}\nMAE={global_mae_summer:.4f}")
plt.suptitle(f"Quantile-Quantile plots of coarse resolution {reso} and downscaled APGD precipitation datasets during summer", fontsize=16)

# Adjust layout
plt.tight_layout()
#plt.savefig('/home/jbrenner/These/Resultats/Article/QQ_plots.png', format='png')
plt.show()


#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________________________________________


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# RESULTATS GLOBAUX 

simu="simu"

reso=10

simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_temperature_Alps_APGD.nc')
ref = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_ref.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_obs.nc')


simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
ref['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})

#degraded=degraded.drop_dims('bnds')
#observation=observation.drop_dims('bnds')


ts_sim = simulation['ts']
ts_ref = ref['ts']
ts_degraded = degraded['ts']
ts_obs = observation['ts']


mask_sim = ts_sim.notnull()
mask_degraded = ts_degraded.notnull()
mask_obs = ts_obs.notnull()

combined_mask = np.logical_and(np.logical_and(mask_sim, mask_degraded), mask_obs)


# Apply the combined mask to each array
ts_sim_masked = ts_sim.where(combined_mask)
ts_ref_masked = ts_ref.where(combined_mask)
ts_degraded_masked = ts_degraded.where(combined_mask)
ts_obs_masked = ts_obs.where(combined_mask)





#__________________________________________________________________
# Degraded stats


diff_deg = (ts_degraded_masked - ts_obs_masked)
v_rmse_deg = diff_deg**2
v_mae_deg = np.abs(diff_deg)

global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
global_mae_deg = np.nanmean(v_mae_deg).item()

rmse_matrix_deg = np.ma.sqrt(np.ma.mean(v_rmse_deg, axis=0))
mae_matrix_deg = np.sqrt(np.ma.mean(v_mae_deg, axis=0))

#________________________________________________________________
#Ref 

diff_ref = (ts_ref_masked - ts_obs_masked)
v_rmse_ref = diff_ref**2
v_mae_ref = np.abs(diff_ref)

global_rmse_ref = np.sqrt(np.nanmean(v_rmse_ref)).item()
global_mae_ref = np.nanmean(v_mae_ref).item()

rmse_matrix_ref = np.ma.sqrt(np.ma.mean(v_rmse_ref, axis=0))
mae_matrix_ref = np.sqrt(np.ma.mean(v_mae_ref, axis=0))

#_________________________________________________________________
# DS stats


diff = (ts_sim_masked - ts_obs_masked)
v_rmse = diff**2
v_mae = np.ma.abs(diff)

global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
global_mae = np.nanmean(v_mae).item()

rmse_matrix = np.sqrt(np.nanmean(v_rmse, axis=0))
mae_matrix = np.sqrt(np.nanmean(v_mae, axis=0))



ts_sim = simulation['ts']
ts_ref = ref["ts"]
ts_degraded = degraded['ts']
ts_obs = observation['ts']

masked_ts_sim = np.ma.masked_invalid(ts_sim)
masked_ts_ref = np.ma.masked_invalid(ts_ref)
masked_ts_degraded = np.ma.masked_invalid(ts_degraded)
masked_ts_obs = np.ma.masked_invalid(ts_obs)

global_mask=np.ma.mask_or(masked_ts_sim.mask, masked_ts_obs.mask)
ref_rl = np.ma.masked_array(ts_ref, global_mask)
sim_rl=np.ma.masked_array(ts_sim, global_mask)
deg_rl=np.ma.masked_array(ts_degraded, global_mask)
obs_rl=np.ma.masked_array(ts_obs, global_mask)
sim_rl=sim_rl.compressed()
ref_rl = ref_rl.compressed()
deg_rl=deg_rl.compressed()
obs_rl=obs_rl.compressed()



slope_deg, intercept_deg = np.polyfit(obs_rl, deg_rl, 1)
# Calculate predicted values
predicted_deg = slope_deg * obs_rl + intercept_deg
# Calculate R²
r2_deg = 1 - (np.sum((deg_rl - predicted_deg)**2) / np.sum((deg_rl - np.mean(deg_rl))**2))



slope_ref, intercept_ref = np.polyfit(obs_rl, ref_rl, 1)
# Calculate predicted values
predicted_ref = slope_ref * obs_rl + intercept_ref
# Calculate R²
r2_ref = 1 - (np.sum((ref_rl - predicted_ref)**2) / np.sum((ref_rl - np.mean(ref_rl))**2))


slope, intercept = np.polyfit(obs_rl, sim_rl, 1)
# Calculate predicted values
predicted = slope * obs_rl + intercept
# Calculate R²
r2 = 1 - (np.sum((sim_rl - predicted)**2) / np.sum((sim_rl - np.mean(sim_rl))**2))


fig, axs = plt.subplots(1,3, figsize=(15,5))

ax1=axs[0]
ax2=axs[1]
ax3=axs[2]

ax1.scatter(obs_rl, deg_rl, alpha=0.5)
#ax1.set_xlim(0, deg_rl.max())
#ax1.set_ylim(0, deg_rl.max())
ax1.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
ax1.set_xlabel('Observed temperatures (°C)')
ax1.set_ylabel('Simulated temperatures (°C)')
ax1.set_title('Simulated vs Observed temperatures')
ax1.grid()
ax1.axis('equal')
ax1.text(0.1 * obs_rl.max(), 0.9 * deg_rl.max(), f'R² = {r2_deg:.4f} \n MAE={global_mae_deg:.4f} \n RMSE={global_rmse_deg:.4f}', fontsize=12, color='blue')
ax1.set_title(f'degraded')

ax2.scatter(obs_rl, ref_rl, alpha=0.5)
ax2.set_xlim(0, ref_rl.max())
ax2.set_ylim(0, ref_rl.max())
ax2.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
ax2.set_xlabel('Observed temperatures (°C)')
ax2.set_ylabel('Simulated temperatures (°C)')
ax2.set_title('Simulated vs Observed temperatures')
ax2.grid()
ax2.axis('equal')
ax2.text(0.1 * obs_rl.max(), 0.9 * ref_rl.max(), f'R² = {r2_ref:.4f} \n MAE={global_mae_ref:.4f} \n RMSE={global_rmse_ref:.4f}', fontsize=12, color='blue')
ax2.set_title(f'ref')

ax3.scatter(obs_rl, sim_rl, alpha=0.5)
ax3.set_xlim(0, sim_rl.max())
ax3.set_ylim(0, sim_rl.max())
ax3.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
ax3.set_xlabel('Observed temperatures (°C)')
ax3.set_ylabel('Simulated temperatures (°C)')
ax3.set_title('Simulated vs Observed temperatures')
ax3.grid()
ax3.axis('equal')
ax3.text(0.1 * obs_rl.max(), 0.9 * sim_rl.max(), f'R² = {r2:.4f} \n MAE={global_mae:.4f} \n RMSE={global_rmse:.4f}', fontsize=12, color='blue')
ax3.set_title(f'simu')

plt.show()


# plt.figure(figsize=(8, 8))
# plt.scatter(obs_rl, degrad_rl, alpha=0.5)
# plt.xlim(0, degrad_rl.max())
# plt.ylim(0, degrad_rl.max())
# plt.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
# plt.xlabel('Observed temperatures (°C)')
# plt.ylabel('Simulated temperatures (°C)')
# plt.title('Simulated vs Observed temperatures')
# plt.grid()
# plt.axis('equal')
# plt.text(0.1 * obs_rl.max(), 0.9 * degrad_rl.max(), f'R² = {r2_deg:.4f} \n MAE={global_mae_deg:.4f} \n RMSE={global_rmse_deg}:.4f', fontsize=12, color='blue')
# plt.title('/home/jbrenner/These/GeoDS_Outputs/Statistics/Simulation/DS_simu_degraded_global_scatter_plot.png')
# plt.show()

# plt.figure(figsize=(8, 8))
# plt.scatter(obs_rl, sim_rl, alpha=0.5)
# plt.xlim(0, sim_rl.max())
# plt.ylim(0, sim_rl.max())
# plt.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
# plt.xlabel('Observed temperatures (°C)')
# plt.ylabel('Simulated temperatures (°C)')
# plt.title('Simulated vs Observed temperatures')
# plt.grid()
# plt.axis('equal')
# plt.text(0.1 * obs_rl.max(), 0.9 * sim_rl.max(), f'R² = {r2:.4f} \n MAE={global_mae:.4f} \n RMSE={global_rmse}:.4f', fontsize=12, color='blue')
# plt.title(f'/home/jbrenner/These/GeoDS_Outputs/Statistics/Simulation/DS_simu_{simu}_global_scatter_plot.png')
# #plt.savefig(f'/home/jbrenner/These/GeoDS_Outputs/Statistics/Simulation/DS_simu_{simu}_global_scatter_plot.png', format='png')
# plt.show()


# print(f'RMSE degradé : {global_rmse_deg}')
# print(f'MAE degradé : {global_mae_deg}')
# print(f'R2 degradé : {r2_deg}')

# print(f'RMSE downscalé : {global_rmse}')
# print(f'MAE downscalé : {global_mae}')
# print(f'R2 downscalé : {r2}')
























# Par mois


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# RESULTATS GLOBAUX 

simu="simu"

reso=10

simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_temperature_Alps_APGD.nc')
ref = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_ref.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_obs.nc')


simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
ref['time'] = xr.DataArray(pd.to_datetime(ref['time'].values, format='%Y%m'), dims='time', coords={'time': ref['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})

r2_ref_list=[]
mae_ref=[]
rmse_ref=[]

r2_sim_list=[]
mae_sim=[]
rmse_sim=[]

months=[]


for i in range (1,13):
    ts_sim = simulation['ts'].where(simulation['time'].dt.month==i)
    ts_degraded = degraded['ts'].where(degraded['time'].dt.month==i)
    ts_ref = ref["ts"].where(ref['time'].dt.month==i)
    ts_obs = observation['ts'].where(observation['time'].dt.month==i)

        
    mask_sim = ts_sim.notnull()
    mask_degraded = ts_degraded.notnull()
    mask_obs = ts_obs.notnull()
    
    combined_mask = np.logical_and(np.logical_and(mask_sim, mask_degraded), mask_obs)
    
    
    # Apply the combined mask to each array
    ts_sim_masked = ts_sim.where(combined_mask)
    ts_ref_masked = ts_ref.where(combined_mask)
    ts_degraded_masked = ts_degraded.where(combined_mask)
    ts_obs_masked = ts_obs.where(combined_mask)
    
    
    
    
    
    #__________________________________________________________________
    # Degraded stats
    
    
    diff_deg = (ts_degraded_masked - ts_obs_masked)
    v_rmse_deg = diff_deg**2
    v_mae_deg = np.abs(diff_deg)
    
    global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
    global_mae_deg = np.nanmean(v_mae_deg).item()
    
    rmse_matrix_deg = np.ma.sqrt(np.ma.mean(v_rmse_deg, axis=0))
    mae_matrix_deg = np.sqrt(np.ma.mean(v_mae_deg, axis=0))
    
    #________________________________________________________________
    #Ref 
    
    diff_ref = (ts_ref_masked - ts_obs_masked)
    v_rmse_ref = diff_ref**2
    v_mae_ref = np.abs(diff_ref)
    
    global_rmse_ref = np.sqrt(np.nanmean(v_rmse_ref)).item()
    global_mae_ref = np.nanmean(v_mae_ref).item()
    
    rmse_matrix_ref = np.ma.sqrt(np.ma.mean(v_rmse_ref, axis=0))
    mae_matrix_ref = np.sqrt(np.ma.mean(v_mae_ref, axis=0))
    
    #_________________________________________________________________
    # DS stats
    
    
    diff = (ts_sim_masked - ts_obs_masked)
    v_rmse = diff**2
    v_mae = np.ma.abs(diff)
    
    global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
    global_mae = np.nanmean(v_mae).item()
    
    rmse_matrix = np.sqrt(np.nanmean(v_rmse, axis=0))
    mae_matrix = np.sqrt(np.nanmean(v_mae, axis=0))
    
       
    ts_sim = simulation['ts'].where(simulation['time'].dt.month==i)
    ts_degraded = degraded['ts'].where(degraded['time'].dt.month==i)
    ts_ref = ref["ts"].where(degraded['time'].dt.month==i)
    ts_obs = observation['ts'].where(observation['time'].dt.month==i)
    
    masked_ts_sim = np.ma.masked_invalid(ts_sim)
    masked_ts_ref = np.ma.masked_invalid(ts_ref)
    masked_ts_degraded = np.ma.masked_invalid(ts_degraded)
    masked_ts_obs = np.ma.masked_invalid(ts_obs)
    
    global_mask=np.ma.mask_or(masked_ts_sim.mask, masked_ts_obs.mask)
    ref_rl = np.ma.masked_array(ts_ref, global_mask)
    sim_rl=np.ma.masked_array(ts_sim, global_mask)
    deg_rl=np.ma.masked_array(ts_degraded, global_mask)
    obs_rl=np.ma.masked_array(ts_obs, global_mask)
    sim_rl=sim_rl.compressed()
    ref_rl = ref_rl.compressed()
    deg_rl=deg_rl.compressed()
    obs_rl=obs_rl.compressed()
    
    
    
    slope_deg, intercept_deg = np.polyfit(obs_rl, deg_rl, 1)
    # Calculate predicted values
    predicted_deg = slope_deg * obs_rl + intercept_deg
    # Calculate R²
    r2_deg = 1 - (np.sum((deg_rl - predicted_deg)**2) / np.sum((deg_rl - np.mean(deg_rl))**2))
    
    
    
    slope_ref, intercept_ref = np.polyfit(obs_rl, ref_rl, 1)
    # Calculate predicted values
    predicted_ref = slope_ref * obs_rl + intercept_ref
    # Calculate R²
    r2_ref = 1 - (np.sum((ref_rl - predicted_ref)**2) / np.sum((ref_rl - np.mean(ref_rl))**2))
    
    
    slope, intercept = np.polyfit(obs_rl, sim_rl, 1)
    # Calculate predicted values
    predicted = slope * obs_rl + intercept
    # Calculate R²
    r2 = 1 - (np.sum((sim_rl - predicted)**2) / np.sum((sim_rl - np.mean(sim_rl))**2))
    
    r2_ref_list.append(r2_ref)
    mae_ref.append(global_mae_ref)
    rmse_ref.append(global_rmse_ref)

    r2_sim_list.append(r2)
    mae_sim.append(global_mae)
    rmse_sim.append(global_rmse)
    
    months.append(i)
    
    fig, axs = plt.subplots(1,3, figsize=(15,5))
    
    ax1=axs[0]
    ax2=axs[1]
    ax3=axs[2]
    
    ax1.scatter(obs_rl, deg_rl, alpha=0.5)
    #ax1.set_xlim(0, deg_rl.max())
    #ax1.set_ylim(0, deg_rl.max())
    ax1.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
    ax1.set_xlabel('Observed temperatures (°C)')
    ax1.set_ylabel('Simulated temperatures (°C)')
    ax1.set_title('Simulated vs Observed temperatures')
    ax1.grid()
    ax1.axis('equal')
    ax1.text(0.1 * obs_rl.max(), 0.9 * deg_rl.max(), f'R² = {r2_deg:.4f} \n MAE={global_mae_deg:.4f} \n RMSE={global_rmse_deg:.4f}', fontsize=12, color='blue')
    ax1.set_title(f'degraded')
    
    ax2.scatter(obs_rl, ref_rl, alpha=0.5)
    ax2.set_xlim(0, ref_rl.max())
    ax2.set_ylim(0, ref_rl.max())
    ax2.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
    ax2.set_xlabel('Observed temperatures (°C)')
    ax2.set_ylabel('Simulated temperatures (°C)')
    ax2.set_title('Simulated vs Observed temperatures')
    ax2.grid()
    ax2.axis('equal')
    ax2.text(0.1 * obs_rl.max(), 0.9 * ref_rl.max(), f'R² = {r2_ref:.4f} \n MAE={global_mae_ref:.4f} \n RMSE={global_rmse_ref:.4f}', fontsize=12, color='blue')
    ax2.set_title(f'ref')
    
    ax3.scatter(obs_rl, sim_rl, alpha=0.5)
    ax3.set_xlim(0, sim_rl.max())
    ax3.set_ylim(0, sim_rl.max())
    ax3.plot([0, obs_rl.max()], [0, obs_rl.max()], 'r--')  # Line of equality
    ax3.set_xlabel('Observed temperatures (°C)')
    ax3.set_ylabel('Simulated temperatures (°C)')
    ax3.set_title('Simulated vs Observed temperatures')
    ax3.grid()
    ax3.axis('equal')
    ax3.text(0.1 * obs_rl.max(), 0.9 * sim_rl.max(), f'R² = {r2:.4f} \n MAE={global_mae:.4f} \n RMSE={global_rmse:.4f}', fontsize=12, color='blue')
    ax3.set_title(f'simu')
    
    plt.suptitle(f'MONTH n°{i}')
    
    plt.show()



fig, ax = plt.subplots(figsize=(10,8))
ax.plot(months, r2_ref_list, label='ref', marker='o')
ax.plot(months, r2_sim_list, label='sim', marker='o')
plt.suptitle("monthly R2 comparison")
plt.legend()
plt.show()



fig, ax = plt.subplots(figsize=(10,8))
ax.plot(months, mae_ref, label='ref', marker='o')
ax.plot(months, mae_sim, label='sim', marker='o')
plt.suptitle("monthly mae comparison")
plt.legend()
plt.show()


# diff=[]
# for i in range (len(r2_sim_list)):
#     diff.append(r2_sim_list[i] - r2_ref_list[i])

# fig, ax = plt.subplots(figsize=(10,8))
# ax.plot(months, diff, label='diff', marker='o')
# plt.suptitle("monthly mae comparison")
# plt.legend()
# plt.show()

















# QQ_plots températures
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

reso=10
simu="simu"

simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_temperature_Alps_APGD.nc')
ref = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_ref.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_obs.nc')

ref['time'] = xr.DataArray(pd.to_datetime(ref['time'].values, format='%Y%m'), dims='time', coords={'time': ref['time'].values})
simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})



ts_sim = simulation['ts']
ts_ref = ref['ts']
ts_degraded = degraded['ts']
ts_obs = observation['ts']

masked_ts_sim = np.ma.masked_invalid(ts_sim)
masked_ts_ref = np.ma.masked_invalid(ts_ref)
masked_ts_degraded = np.ma.masked_invalid(ts_degraded)
masked_ts_obs = np.ma.masked_invalid(ts_obs)

global_mask=np.ma.mask_or(masked_ts_sim.mask, masked_ts_obs.mask)
sim_rl=np.ma.masked_array(ts_sim, global_mask)
ref_rl=np.ma.masked_array(ts_ref, global_mask)
degrad_rl=np.ma.masked_array(ts_degraded, global_mask)
obs_rl=np.ma.masked_array(ts_obs, global_mask)
ref_rl = ref_rl.compressed()
sim_rl=sim_rl.compressed()
degrad_rl=degrad_rl.compressed()
obs_rl=obs_rl.compressed()

quantiles = np.linspace(0, 1, 50)
sim_quantiles = np.quantile(sim_rl, quantiles)
ref_quantiles = np.quantile(ref_rl, quantiles)
deg_quantiles = np.quantile(degrad_rl, quantiles)
obs_quantiles = np.quantile(obs_rl, quantiles)



diff = (sim_quantiles - obs_quantiles)
v_rmse = diff**2
v_mae = np.ma.abs(diff)

global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
global_mae = np.nanmean(v_mae).item()

diff_ref = (ref_quantiles - obs_quantiles)
v_rmse_ref = diff_ref**2
v_mae_ref = np.abs(diff_ref)

global_rmse_ref = np.sqrt(np.nanmean(v_rmse_ref)).item()
global_mae_ref = np.nanmean(v_mae_ref).item()


diff_deg = (deg_quantiles - obs_quantiles)
v_rmse_deg = diff_deg**2
v_mae_deg = np.abs(diff_deg)

global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
global_mae_deg = np.nanmean(v_mae_deg).item()



slope_deg, intercept_deg = np.polyfit(obs_quantiles, deg_quantiles, 1)
# Calculate predicted values
predicted_deg = slope_deg * obs_quantiles + intercept_deg
# Calculate R²
r2_deg = 1 - (np.sum((deg_quantiles - predicted_deg)**2) / np.sum((deg_quantiles - np.mean(deg_quantiles))**2))


slope_ref, intercept_ref = np.polyfit(obs_quantiles, ref_quantiles, 1)
# Calculate predicted values
predicted_ref = slope_ref * obs_quantiles + intercept_ref
# Calculate R²
r2_ref = 1 - (np.sum((ref_quantiles - predicted_ref)**2) / np.sum((ref_quantiles - np.mean(ref_quantiles))**2))


slope_sim, intercept_sim = np.polyfit(obs_quantiles, sim_quantiles, 1)
# Calculate predicted values
predicted_sim = slope_sim * obs_quantiles + intercept_sim
# Calculate R²
r2_sim = 1 - (np.sum((sim_quantiles - predicted_sim)**2) / np.sum((sim_quantiles - np.mean(sim_quantiles))**2))


lim_max=max(sim_quantiles)
lim_max=33
lim_min=-10

fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 2 columns
# First subplot for original simulated data
axs[0].scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black")
axs[0].set_xlim(lim_min, lim_max)
axs[0].set_ylim(lim_min, lim_max)
axs[0].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
axs[0].set_xlabel('Observed temperatures quantiles (mm)', fontname="Arial", fontsize=14)
axs[0].set_ylabel('Simulated temperatures quantiles (mm)', fontname="Arial", fontsize=14)
#axs[0].set_xticks(fontname="Arial", fontsize=14)
#axs[0].set_yticks(fontname="Arial", fontsize=14)
axs[0].set_title('a) degraded', fontname="Arial", y=0, pad=-50, loc="left")
axs[0].grid(linewidth=0.4, linestyle="dotted")
axs[0].text(5, 25,f"R2={r2_deg:.4f} \n MAE={global_mae_deg} \n RMSE={global_rmse_deg}")

axs[1].scatter(obs_quantiles, ref_quantiles, color="lightgrey", edgecolors="black")
axs[1].set_xlim(lim_min, lim_max)
axs[1].set_ylim(lim_min, lim_max)
axs[1].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
axs[1].set_xlabel('Observed temperatures quantiles (mm)', fontname="Arial", fontsize=14)
axs[1].set_ylabel('Simulated temperatures quantiles (mm)', fontname="Arial", fontsize=14)
#axs[0].set_xticks(fontname="Arial", fontsize=14)
#axs[0].set_yticks(fontname="Arial", fontsize=14)
axs[1].set_title('b) ref', fontname="Arial", y=0, pad=-50, loc="left")
axs[1].grid(linewidth=0.4, linestyle="dotted")
axs[1].text(5, 25,f"R2={r2_ref:.4f} \n MAE={global_mae_ref} \n RMSE={global_rmse_ref}")


# Second subplot for degrad_rl data
axs[2].scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black")
axs[2].set_xlim(lim_min, lim_max)
axs[2].set_ylim(lim_min, lim_max)
axs[2].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
axs[2].set_xlabel('Observed temperatures quantiles (mm)', fontname="Arial", fontsize=14)
axs[2].set_ylabel('Simulated temperatures quantiles (mm)', fontname="Arial", fontsize=14)
#axs[2].set_xticks(fontname="Arial", fontsize=14)
#axs[2].set_yticks(fontname="Arial", fontsize=14)
axs[2].set_title(f'c) {simu}', fontname="Arial", y=0, pad=-50, loc="left")
axs[2].grid(linewidth=0.4, linestyle="dotted")
axs[2].text(5, 25,f"R2={r2_sim:.4f} \n MAE={global_mae} \n RMSE={global_rmse}")
#plt.suptitle(f"Quantile-Quantile plots of coarse resolution and downscaled EOBS temperatures datasets", fontsize=16)
plt.suptitle(f"Quantiles globaux {simu}", fontsize=16)


# Adjust layout
plt.tight_layout()
#plt.savefig('/home/jbrenner/These/Resultats/Article/QQ_plots_temperatures.png', format='png')
plt.show()




































#par mois 
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

simu="simu"
reso=10


simulation = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_temperature_Alps_APGD.nc')
ref = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_ref.nc')
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/LR_climate.nc')
observation = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/temperature/ts_obs.nc')


simulation['time'] = xr.DataArray(pd.to_datetime(simulation['time'].values, format='%Y%m'), dims='time', coords={'time': simulation['time'].values})
ref['time'] = xr.DataArray(pd.to_datetime(ref['time'].values, format='%Y%m'), dims='time', coords={'time': ref['time'].values})
degraded['time'] = xr.DataArray(pd.to_datetime(degraded['time'].values, format='%Y%m'), dims='time', coords={'time': degraded['time'].values})
observation['time'] = xr.DataArray(pd.to_datetime(observation['time'].values, format='%Y%m'), dims='time', coords={'time': observation['time'].values})

r2_quantiles_list=[]

for i in range (1,13):
    ts_sim = simulation['ts'].where(simulation['time'].dt.month==i)
    ts_ref = ref['ts'].where(ref['time'].dt.month==i)
    ts_degraded = degraded['ts'].where(degraded['time'].dt.month==i)
    ts_obs = observation['ts'].where(observation['time'].dt.month==i)

    
    masked_ts_sim = np.ma.masked_invalid(ts_sim)
    masked_ts_ref = np.ma.masked_invalid(ts_ref)
    masked_ts_degraded = np.ma.masked_invalid(ts_degraded)
    masked_ts_obs = np.ma.masked_invalid(ts_obs)
    
    global_mask=np.ma.mask_or(masked_ts_sim.mask, masked_ts_obs.mask)
    sim_rl=np.ma.masked_array(ts_sim, global_mask)
    ref_rl=np.ma.masked_array(ts_ref, global_mask)
    degrad_rl=np.ma.masked_array(ts_degraded, global_mask)
    obs_rl=np.ma.masked_array(ts_obs, global_mask)
    ref_rl = ref_rl.compressed()
    sim_rl=sim_rl.compressed()
    degrad_rl=degrad_rl.compressed()
    obs_rl=obs_rl.compressed()
    
    quantiles = np.linspace(0, 1, 50)
    sim_quantiles = np.quantile(sim_rl, quantiles)
    ref_quantiles = np.quantile(ref_rl, quantiles)
    deg_quantiles = np.quantile(degrad_rl, quantiles)
    obs_quantiles = np.quantile(obs_rl, quantiles)
    
    
    
    diff = (sim_quantiles - obs_quantiles)
    v_rmse = diff**2
    v_mae = np.ma.abs(diff)
    
    global_rmse = np.sqrt(np.nanmean(v_rmse)).item()
    global_mae = np.nanmean(v_mae).item()
    
    diff_ref = (ref_quantiles - obs_quantiles)
    v_rmse_ref = diff_ref**2
    v_mae_ref = np.abs(diff_ref)
    
    global_rmse_ref = np.sqrt(np.nanmean(v_rmse_ref)).item()
    global_mae_ref = np.nanmean(v_mae_ref).item()
    
    
    diff_deg = (deg_quantiles - obs_quantiles)
    v_rmse_deg = diff_deg**2
    v_mae_deg = np.abs(diff_deg)
    
    global_rmse_deg = np.sqrt(np.nanmean(v_rmse_deg)).item()
    global_mae_deg = np.nanmean(v_mae_deg).item()
    
    
    
    slope_deg, intercept_deg = np.polyfit(obs_quantiles, deg_quantiles, 1)
    # Calculate predicted values
    predicted_deg = slope_deg * obs_quantiles + intercept_deg
    # Calculate R²
    r2_deg = 1 - (np.sum((deg_quantiles - predicted_deg)**2) / np.sum((deg_quantiles - np.mean(deg_quantiles))**2))
    
    
    slope_ref, intercept_ref = np.polyfit(obs_quantiles, ref_quantiles, 1)
    # Calculate predicted values
    predicted_ref = slope_ref * obs_quantiles + intercept_ref
    # Calculate R²
    r2_ref = 1 - (np.sum((ref_quantiles - predicted_ref)**2) / np.sum((ref_quantiles - np.mean(ref_quantiles))**2))
    
    
    slope_sim, intercept_sim = np.polyfit(obs_quantiles, sim_quantiles, 1)
    # Calculate predicted values
    predicted_sim = slope_sim * obs_quantiles + intercept_sim
    # Calculate R²
    r2_sim = 1 - (np.sum((sim_quantiles - predicted_sim)**2) / np.sum((sim_quantiles - np.mean(sim_quantiles))**2))
    
    
    lim_max=max(sim_quantiles)
    lim_max=33
    lim_min=-10
    
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 2 columns
    # First subplot for original simulated data
    axs[0].scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black")
    axs[0].set_xlim(lim_min, lim_max)
    axs[0].set_ylim(lim_min, lim_max)
    axs[0].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
    axs[0].set_xlabel('Observed temperatures quantiles (mm)', fontname="Arial", fontsize=14)
    axs[0].set_ylabel('Simulated temperatures quantiles (mm)', fontname="Arial", fontsize=14)
    #axs[0].set_xticks(fontname="Arial", fontsize=14)
    #axs[0].set_yticks(fontname="Arial", fontsize=14)
    axs[0].set_title('a) degraded', fontname="Arial", y=0, pad=-50, loc="left")
    axs[0].grid(linewidth=0.4, linestyle="dotted")
    axs[0].text(5, 25,f"R2={r2_deg:.4f} \n MAE={global_mae_deg} \n RMSE={global_rmse_deg}")
    
    axs[1].scatter(obs_quantiles, ref_quantiles, color="lightgrey", edgecolors="black")
    axs[1].set_xlim(lim_min, lim_max)
    axs[1].set_ylim(lim_min, lim_max)
    axs[1].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
    axs[1].set_xlabel('Observed temperatures quantiles (mm)', fontname="Arial", fontsize=14)
    axs[1].set_ylabel('Simulated temperatures quantiles (mm)', fontname="Arial", fontsize=14)
    #axs[0].set_xticks(fontname="Arial", fontsize=14)
    #axs[0].set_yticks(fontname="Arial", fontsize=14)
    axs[1].set_title('b) ref', fontname="Arial", y=0, pad=-50, loc="left")
    axs[1].grid(linewidth=0.4, linestyle="dotted")
    axs[1].text(5, 25,f"R2={r2_ref:.4f} \n MAE={global_mae_ref} \n RMSE={global_rmse_ref}")
    
    
    # Second subplot for degrad_rl data
    axs[2].scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black")
    axs[2].set_xlim(lim_min, lim_max)
    axs[2].set_ylim(lim_min, lim_max)
    axs[2].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)  # Line of equality
    axs[2].set_xlabel('Observed temperatures quantiles (mm)', fontname="Arial", fontsize=14)
    axs[2].set_ylabel('Simulated temperatures quantiles (mm)', fontname="Arial", fontsize=14)
    #axs[2].set_xticks(fontname="Arial", fontsize=14)
    #axs[2].set_yticks(fontname="Arial", fontsize=14)
    axs[2].set_title(f'c) {simu}', fontname="Arial", y=0, pad=-50, loc="left")
    axs[2].grid(linewidth=0.4, linestyle="dotted")
    axs[2].text(5, 25,f"R2={r2_sim:.4f} \n MAE={global_mae} \n RMSE={global_rmse}")
    #plt.suptitle(f"Quantile-Quantile plots of coarse resolution and downscaled EOBS temperatures datasets", fontsize=16)
    plt.suptitle(f"MONTH n°{i}", fontsize=16)
    
    
    # Adjust layout
    plt.tight_layout()
    #plt.savefig('/home/jbrenner/These/Resultats/Article/QQ_plots_temperatures.png', format='png')
    plt.show()



print("r2 quantiles :", r2_quantiles_list)









