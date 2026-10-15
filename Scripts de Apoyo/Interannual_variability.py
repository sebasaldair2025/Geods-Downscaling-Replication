# ADAPTADO de Interannual_variability.py (script ORIGINAL del autor, jbrenner).
# Bloque "Global": identico en logica al original, solo cambia la carga de datos.
# Bloque "Points" (COMPLETADO): mismo layout de 6 paneles verticales y estilo del original;
# los indices i,j se recalculan (ver nota en seasonal_cycles.py y en
# common_original.select_representative_points()) porque los del autor son de su propia
# grilla a reso=10km, sin observacion en los datos entregados.

from common_original import load_5km, select_representative_points, OUT
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

d = load_5km()
valid_da = xr.DataArray(d['valid'], dims=['y', 'x'])
sim = d['sim'].where(valid_da)
deg = d['deg'].where(valid_da)
obs = d['obs'].where(valid_da)

raw_time = deg['time'].values
year_of_step = np.floor(raw_time).astype(int) // 100

years = []
annual_native = []
annual_degraded = []
annual_downscaled = []
for y in range(1971, 2020):
    sel = year_of_step == y
    if not sel.any():
        continue
    years.append(y)
    annual_native.append(obs.isel(time=sel).mean().item() * 12)
    annual_degraded.append(deg.isel(time=sel).mean().item() * 12)
    annual_downscaled.append(sim.isel(time=sel).mean().item() * 12)

fig, ax1 = plt.subplots()
ax1.plot(years, annual_degraded, color="indianred", label=r"Ref$_{interpolated}$", linewidth=0.8)
ax1.plot(years, annual_downscaled, color="olivedrab", label="DS", linewidth=0.8)
ax1.plot(years, annual_native, color="cornflowerblue", label="Target", linewidth=0.8)
ax1.set_ylabel("Mean annual precipitation (mm)", fontsize=12)
plt.legend(fontsize=8, loc="upper left")
plt.title("Global interannual variability (5km, 1971-2019)")
plt.savefig(f"{OUT}/Interannual_variability_global_5km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Interannual_variability_global_5km.png")

from scipy.stats import pearsonr
r_ref = pearsonr(annual_degraded, annual_native)[0]
r_ds = pearsonr(annual_downscaled, annual_native)[0]
print(f"r(REF,Target)={r_ref:.4f}  r(DS,Target)={r_ds:.4f}")

# ______________________________ Points (COMPLETADO, ver nota arriba) ______________________________
points, k_sel = select_representative_points(d)
print(f"Puntos recalculados (direccion de viento TEI seleccionada: indice {k_sel}):")
for name, (j, i) in points.items():
    print(f"  {name}: j={j}, i={i}")

panels = [("Global", None)] + [(name, idx) for name, idx in points.items()]
letters = "abcdef"

fig, axs = plt.subplots(6, 1, figsize=(14, 25))

for ax, (name, idx), letter in zip(axs, panels, letters):
    if idx is None:
        a_native, a_degraded, a_downscaled = annual_native, annual_degraded, annual_downscaled
    else:
        j, i = idx
        a_native, a_degraded, a_downscaled = [], [], []
        for y in years:
            sel = year_of_step == y
            a_native.append(obs.isel(y=j, x=i, time=sel).mean().item() * 12)
            a_degraded.append(deg.isel(y=j, x=i, time=sel).mean().item() * 12)
            a_downscaled.append(sim.isel(y=j, x=i, time=sel).mean().item() * 12)

    ax.plot(years, a_degraded, color="indianred", label=r"Ref$_{interpolated}$")
    ax.plot(years, a_downscaled, color="olivedrab", label="DS")
    ax.plot(years, a_native, color="cornflowerblue", label="Target")
    ax.set_ylabel("Mean annual precipitation (mm)", fontsize=12)
    ax.set_title(f"{letter})", fontsize=14, loc="left", y=0, pad=-30)
    ax.text(0.03, 0.9, s=name, transform=ax.transAxes, ha='left', fontsize=12, fontstyle="italic",
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))
    ax.legend(fontsize=8, loc='upper right')

axs[-1].set_xlabel("Year", fontsize=12)
plt.tight_layout()
plt.savefig(f"{OUT}/Interannual_variability_points_5km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Interannual_variability_points_5km.png")
