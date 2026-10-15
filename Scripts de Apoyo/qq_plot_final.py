# ADAPTADO de qq_plot_final.py (script ORIGINAL del autor, jbrenner).
# Cambios respecto al original: carga de datos via common_original.load_5km() en vez de
# xr.open_dataset a rutas /home/jbrenner/..., y reso=5 (unica resolucion con observacion
# APGD nativa completa en los datos entregados; a 10km no hay observacion nativa).
# El calculo de R2 (regresion de pendiente/intercepto LIBRES via np.polyfit, linea 48-59
# del original) y el estilo de grafico (ejes partidos/broken axis) son EXACTAMENTE los
# del autor. Los textos con valores hardcodeados del original (ej. "MAE=17.6523 mm") se
# reemplazan aqui por los valores reales calculados con los datos entregados.

from common_original import load_5km, OUT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker

d = load_5km()

masked_P_sim = np.ma.masked_invalid(d['sim'].values)
masked_P_degraded = np.ma.masked_invalid(d['deg'].values)
masked_P_obs = np.ma.masked_invalid(d['obs'].values)

global_mask = np.ma.mask_or(masked_P_sim.mask, masked_P_obs.mask)
sim_rl = np.ma.masked_array(d['sim'].values, global_mask).compressed()
degrad_rl = np.ma.masked_array(d['deg'].values, global_mask).compressed()
obs_rl = np.ma.masked_array(d['obs'].values, global_mask).compressed()

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

diff = sim_quantiles - obs_quantiles
global_mae = np.nanmean(np.abs(diff)).item()

diff_deg = deg_quantiles - obs_quantiles
global_mae_deg = np.nanmean(np.abs(diff_deg)).item()

# MAE real (no de cuantiles), sobre la serie pooled completa -- para el texto del panel
mae_full_sim = float(np.mean(np.abs(sim_rl - obs_rl)))
mae_full_deg = float(np.mean(np.abs(degrad_rl - obs_rl)))

print(f"5km: R2_sim(libre)={r2_sim:.6f} slope={slope_sim:.4f}  MAE_quantiles={global_mae:.4f}  MAE_full={mae_full_sim:.4f}")
print(f"5km: R2_deg(libre)={r2_deg:.6f} slope={slope_deg:.4f}  MAE_quantiles={global_mae_deg:.4f}  MAE_full={mae_full_deg:.4f}")

t = 16
lim_lo, lim_hi_low = 0, max(obs_quantiles[obs_quantiles < 500].max() if (obs_quantiles < 500).any() else 350, deg_quantiles[deg_quantiles < 500].max() if (deg_quantiles < 500).any() else 350, sim_quantiles[sim_quantiles < 500].max() if (sim_quantiles < 500).any() else 350) * 1.1
lim_hi_out = max(obs_quantiles.max(), sim_quantiles.max()) * 1.05


def broken_qq(pred_quantiles, r2, mae_q, mae_full, fname):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    ax1, ax2, ax3, ax4 = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]

    for ax in (ax1, ax2, ax3, ax4):
        ax.scatter(obs_quantiles, pred_quantiles, color="lightgrey", edgecolors="black")

    ax1.set_ylim(lim_hi_low, lim_hi_out)
    ax1.set_xlim(0, lim_hi_low)
    ax3.set_ylim(0, lim_hi_low)
    ax3.set_xlim(0, lim_hi_low)
    ax4.set_xlim(lim_hi_low, lim_hi_out)
    ax4.set_ylim(0, lim_hi_low)
    ax2.set_xlim(lim_hi_low, lim_hi_out)
    ax2.set_ylim(lim_hi_low, lim_hi_out)

    ax3.plot([0, lim_hi_low], [0, lim_hi_low], color="red", linewidth=1.5)
    ax2.plot([lim_hi_low, lim_hi_out], [lim_hi_low, lim_hi_out], color="red", linewidth=1.5)

    yticks = ticker.MaxNLocator(nbins=5)
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
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    ax1.tick_params(axis='both', top=False, labeltop=False, labelsize=t)

    ax2.tick_params(axis='both', left=False, bottom=False, labelleft=False, labelright=False, labeltop=False, labelbottom=False, labelsize=t)
    ax4.tick_params(axis='both', left=False, labelleft=False, labelright=False, labeltop=False, labelsize=t)
    ax4.tick_params(axis='x', labelsize=t, labelrotation=45)
    ax3.tick_params(axis='x', labelsize=t, labelrotation=45)
    ax3.tick_params(axis='y', labelsize=t)

    xpos = lim_hi_low * 0.15
    ax1.text(xpos, lim_hi_out - 0.10 * (lim_hi_out - lim_hi_low), f"R2={r2:.6f}", fontsize=16)
    ax1.text(xpos, lim_hi_out - 0.17 * (lim_hi_out - lim_hi_low), r"MAE$_{quantiles}$" f"={mae_q:.4f} mm", fontsize=16)
    ax1.text(xpos, lim_hi_out - 0.24 * (lim_hi_out - lim_hi_low), f"MAE={mae_full:.4f} mm", fontsize=16)

    plt.figtext(0.4, 0.03, "Observed quantiles (mm)", fontsize=20)
    plt.figtext(0.03, 0.4, "Predicted quantiles (mm)", fontsize=20, rotation="vertical")
    plt.savefig(f'{OUT}/{fname}', format='png', dpi=140, bbox_inches='tight')
    plt.close()


broken_qq(sim_quantiles, r2_sim, global_mae, mae_full_sim, "qq_plot_geods_5.png")
print("OK qq_plot_geods_5.png")
broken_qq(deg_quantiles, r2_deg, global_mae_deg, mae_full_deg, "qq_plot_ref_5.png")
print("OK qq_plot_ref_5.png")
