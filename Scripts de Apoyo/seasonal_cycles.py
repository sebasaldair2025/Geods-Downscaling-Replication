# ADAPTADO de seasonal_cycles.py (script ORIGINAL del autor, jbrenner).
# Bloque "Global": identico en logica al original, solo cambia la carga de datos.
# Bloque "Points" (COMPLETADO): el layout de 6 paneles (3x2), las etiquetas a)-f) y el
# estilo de anotacion son los del script original. Lo unico que cambia son los indices
# i,j de los 5 puntos: los del autor (i=[60,54,38,32,41], j=[61,51,40,32,32]) estan
# calibrados para SU grilla propia a reso=10km (sin observacion APGD nativa en los datos
# entregados), y no transfieren a esta grilla de 5km. Se recalculan con el mismo metodo
# ya validado en scripts_reproducidos/fig06_puntos_representativos.py (elevacion + TEI +
# relieve local), documentado en common_original.select_representative_points().

from common_original import load_5km, select_representative_points, OUT
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

d = load_5km()
valid_da = xr.DataArray(d['valid'], dims=['y', 'x'])
sim = d['sim'].where(valid_da)
deg = d['deg'].where(valid_da)
obs = d['obs'].where(valid_da)

# El calculo de mes requiere info de calendario; deg/sim usan la codificacion AAAAMM.51
# (float), no datetime64 -- se reconstruye el mes igual que en common.py del otro paquete.
# obs (APGD_monthly_Alps_alineado.nc) esta alineado paso a paso con deg/sim (mismo largo
# de tiempo, 588 pasos), asi que se indexa por posicion con la misma mascara.
raw_time = deg['time'].values
month_of_step = (np.floor(raw_time).astype(int) % 100)

months = []
monthly_native = []
monthly_degraded = []
monthly_downscaled = []
for m in range(1, 13):
    sel = month_of_step == m
    native_mean = obs.isel(time=sel).mean().item()
    degraded_mean = deg.isel(time=sel).mean().item()
    downscaled_mean = sim.isel(time=sel).mean().item()
    months.append(m)
    monthly_native.append(native_mean)
    monthly_degraded.append(degraded_mean)
    monthly_downscaled.append(downscaled_mean)

fig, ax1 = plt.subplots()
ax1.plot(months, monthly_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax1.plot(months, monthly_downscaled, color="olivedrab", label="DS")
ax1.plot(months, monthly_native, color="cornflowerblue", label="Target")
ax1.set_ylabel("Mean monthly precipitation (mm)", fontsize=14)
ax1.set_xlabel("Month")
plt.legend(fontsize=8, loc="upper left")
plt.title("Global seasonal cycle (5km, 1971-2019)")
plt.savefig(f"{OUT}/Seasonal_cycle_global_5km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Seasonal_cycle_global_5km.png")
print("Promedios mensuales (mm/mes): Target=", [round(v, 1) for v in monthly_native])
print("                              REF   =", [round(v, 1) for v in monthly_degraded])
print("                              DS    =", [round(v, 1) for v in monthly_downscaled])

# ______________________________ Points (COMPLETADO, ver nota arriba) ______________________________
points, k_sel = select_representative_points(d)
print(f"Puntos recalculados (direccion de viento TEI seleccionada: indice {k_sel}):")
for name, (j, i) in points.items():
    print(f"  {name}: j={j}, i={i}")

panels = [("Global", None)] + [(name, idx) for name, idx in points.items()]

fig, axs = plt.subplots(3, 2, figsize=(18, 12))
axs = axs.flatten()
letters = "abcdef"

for ax, (name, idx), letter in zip(axs, panels, letters):
    if idx is None:
        m_native, m_degraded, m_downscaled = monthly_native, monthly_degraded, monthly_downscaled
    else:
        j, i = idx
        m_native, m_degraded, m_downscaled = [], [], []
        for m in range(1, 13):
            sel = month_of_step == m
            m_native.append(obs.isel(y=j, x=i, time=sel).mean().item())
            m_degraded.append(deg.isel(y=j, x=i, time=sel).mean().item())
            m_downscaled.append(sim.isel(y=j, x=i, time=sel).mean().item())

    ax.plot(months, m_degraded, color="indianred", label=r"Ref$_{interpolated}$")
    ax.plot(months, m_downscaled, color="olivedrab", label="DS")
    ax.plot(months, m_native, color="cornflowerblue", label="Target")
    ax.set_xlabel("Month", fontsize=14)
    ax.set_ylabel("Mean monthly precipitation (mm)", fontsize=14)
    ax.set_title(f"{letter})", fontsize=14, loc="left", y=0, pad=-30)
    ax.text(0.03, 0.9, s=name, transform=ax.transAxes, ha='left', fontsize=12, fontstyle="italic",
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))
    ax.legend(fontsize=7, loc='upper right')

fig.suptitle("Average seasonal cycles for different geographic contexts and\ndifferent versions of the APGD over the period 1971-2019 (5km)", y=0.995)
plt.tight_layout()
plt.savefig(f"{OUT}/Seasonal_cycles_points_5km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Seasonal_cycles_points_5km.png")
