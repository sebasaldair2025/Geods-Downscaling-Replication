# ADAPTADO de QQ_plots_points.py (script ORIGINAL del autor, jbrenner).
# El original usa reso=10 con i=33,j=27 (indices propios de la grilla del autor a 10km),
# resolucion para la que NO hay observacion APGD nativa en los datos entregados.
# Aqui se usa reso=5 (unica resolucion con observacion completa) y, en vez de los indices
# originales (que no corresponden a ningun punto fisico particular sin la grilla exacta
# del autor), se selecciona el punto de mayor elevacion del dominio (la "Cumbre"), el punto
# donde el efecto GeoDS es mas relevante. El resto del codigo (dos paneles QQ lado a lado,
# limites de ejes, estilo) es el del script original.

from common_original import load_5km, OUT
import numpy as np
import matplotlib.pyplot as plt

d = load_5km()
S = d['S']
valid = ~np.isnan(d['deg_clim']) & ~np.isnan(d['sim_clim']) & ~np.isnan(d['obs_clim']) & ~np.isnan(S)
j, i = np.unravel_index(np.nanargmax(np.where(valid, S, -np.inf)), S.shape)
print(f"Punto usado (Cumbre, mayor elevacion): j={j}, i={i}, S={S[j, i]:.0f} m "
      f"(en el original: i=33, j=27 de su propia grilla a 10km, no transferible)")

P_sim = d['sim'].isel(y=j, x=i).values
P_degraded = d['deg'].isel(y=j, x=i).values
P_obs = d['obs'].isel(y=j, x=i).values

masked_P_sim = np.ma.masked_invalid(P_sim)
masked_P_degraded = np.ma.masked_invalid(P_degraded)
masked_P_obs = np.ma.masked_invalid(P_obs)

global_mask = np.ma.mask_or(masked_P_sim.mask, masked_P_obs.mask)
sim_rl = np.ma.masked_array(P_sim, global_mask).compressed()
degrad_rl = np.ma.masked_array(P_degraded, global_mask).compressed()
obs_rl = np.ma.masked_array(P_obs, global_mask).compressed()

quantiles = np.linspace(0, 1, 50)
sim_quantiles = np.quantile(sim_rl, quantiles)
deg_quantiles = np.quantile(degrad_rl, quantiles)
obs_quantiles = np.quantile(obs_rl, quantiles)

slope_deg, intercept_deg = np.polyfit(obs_quantiles, deg_quantiles, 1)
predicted_deg = slope_deg * obs_quantiles + intercept_deg
r2_deg = 1 - (np.sum((deg_quantiles - predicted_deg) ** 2) / np.sum((deg_quantiles - np.mean(deg_quantiles)) ** 2))

slope_sim, intercept_sim = np.polyfit(obs_quantiles, sim_quantiles, 1)
predicted_sim = slope_sim * obs_quantiles + intercept_sim
r2_sim = 1 - (np.sum((sim_quantiles - predicted_sim) ** 2) / np.sum((sim_quantiles - np.mean(sim_quantiles)) ** 2))

global_mae = np.nanmean(np.abs(sim_quantiles - obs_quantiles)).item()
global_mae_deg = np.nanmean(np.abs(deg_quantiles - obs_quantiles)).item()

lim_max = max(max(obs_quantiles), max(sim_quantiles), max(deg_quantiles)) + 20

fig, axs = plt.subplots(1, 2, figsize=(14, 8))
axs[0].scatter(obs_quantiles, deg_quantiles, color="lightgrey", edgecolors="black")
axs[0].set_xlim(0, lim_max)
axs[0].set_ylim(0, lim_max)
axs[0].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)
axs[0].set_xlabel('Observed precipitation quantiles (mm)', fontsize=14)
axs[0].set_ylabel('Simulated precipitation quantiles (mm)', fontsize=14)
axs[0].set_title('a) REF interpolado', loc="left")
axs[0].grid(linewidth=0.4, linestyle="dotted")
axs[0].text(lim_max * 0.08, lim_max * 0.9, f"R2={r2_deg:.6f}\nMAE={global_mae_deg:.4f}")

axs[1].scatter(obs_quantiles, sim_quantiles, color="lightgrey", edgecolors="black")
axs[1].set_xlim(0, lim_max)
axs[1].set_ylim(0, lim_max)
axs[1].plot([0, lim_max], [0, lim_max], color="red", linewidth=0.8)
axs[1].set_xlabel('Observed precipitation quantiles (mm)', fontsize=14)
axs[1].set_ylabel('Simulated precipitation quantiles (mm)', fontsize=14)
axs[1].set_title('b) DS (GeoDS)', loc="left")
axs[1].grid(linewidth=0.4, linestyle="dotted")
axs[1].text(lim_max * 0.08, lim_max * 0.9, f"R2={r2_sim:.6f}\nMAE={global_mae:.4f}")

plt.suptitle("Quantile-Quantile plots at the highest-elevation gridpoint (Cumbre) - Alps 5km", fontsize=16)
plt.tight_layout()
plt.savefig(f"{OUT}/QQ_plots_precipitation_puntual_5km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print(f"OK QQ_plots_precipitation_puntual_5km.png  R2_deg={r2_deg:.6f} R2_sim={r2_sim:.6f}")
