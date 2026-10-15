# ADAPTADO de cross_section_alps.py (script ORIGINAL del autor, jbrenner).
# Cambios respecto al original: carga via common_original.load_5km() (climatologias
# calculadas al vuelo en vez de archivos climatology_pp_*.nc pre-armados que no vienen
# en los datos entregados). Los indices de corte (i=108, j 54-114 para N-S; i 31-95,
# j=74 para O-E) son EXACTAMENTE los del script original -- se mantienen sin cambio
# porque el dominio de 5km entregado tiene las mismas dimensiones (x=219,y=138) que
# el dominio del autor, por lo que corresponden al mismo corte fisico por la cresta
# principal de los Alpes.
# Tambien se agrega la version de 10km (bloques originales en lineas 141-276 del script
# del autor): antes no se reproducia porque no hay observacion APGD nativa a 10km entre los
# datos entregados; ahora se usa la observacion a 10km DERIVADA por regrillado conservativo
# de la observacion nativa a 5km (build_apgd_10km_from_5km(), ver common_original.py y el
# LEEME de esta carpeta). Los indices de corte a 10km (i=54, j 26-59 para N-S; i 23-47, j=38
# para O-E) son tambien EXACTAMENTE los del script original.

from common_original import load_5km, load_10km, OUT
import numpy as np
import matplotlib.pyplot as plt

d = load_5km()
lon, lat, S = d['lon'], d['lat'], d['S']
APGD_native_cross = d['obs_clim']
APGD_degraded_cross = d['deg_clim']
APGD_downscaled_cross = d['sim_clim']

# --- North-south cross section (indices originales del autor) ---
i = 108
j_inf, j_sup = 54, 114
j_list = np.arange(j_inf, j_sup)

ny, nx = S.shape
if i >= nx or j_sup > ny:
    print(f"AVISO: indices originales (i={i}, j hasta {j_sup}) fuera del dominio entregado (nx={nx}, ny={ny}); recortando al dominio disponible.")
    i = min(i, nx - 1)
    j_list = j_list[j_list < ny]

latitudes = lat[j_list, i]

fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.set_xlabel("Latitude (°N)", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontsize=12)
ax1.plot(j_list, APGD_native_cross[j_list, i], color='cornflowerblue', label="Target")
ax1.plot(j_list, APGD_degraded_cross[j_list, i], color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(j_list, APGD_downscaled_cross[j_list, i], color='olivedrab', label="DS")
plt.legend(fontsize=8, loc="upper left")

ax2 = ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontsize=12)
ax2.plot(j_list, S[j_list, i], color='grey', linewidth=0.1)
ax2.fill_between(j_list, S[j_list, i], color='grey', alpha=0.25)

ax1.set_xticks(j_list)
ax1.set_xticklabels(latitudes, rotation=90)
formatted_latitudes = [f"{lt:.2f}" for lt in latitudes]
ticks = ax1.get_xticks()
ax1.set_xticks(ticks[::19] if len(ticks) > 19 else ticks[::max(1, len(ticks)//8)])
step = 19 if len(ticks) > 19 else max(1, len(ticks)//8)
ax1.set_xticklabels(formatted_latitudes[::step], rotation=45, fontsize=8)

elevation_ticks = ax2.get_yticks()
for x in range(1, len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)

plt.title("Mean annual precipitation along a latitudinal cross section (5km)")
plt.savefig(f"{OUT}/Cross_section_NS_5km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Cross_section_NS_5km.png")

# --- West-East cross-section (indices originales del autor) ---
i_inf, i_sup = 31, 95
j = 74
i_list = np.arange(i_inf, i_sup)

if j >= ny or i_sup > nx:
    print(f"AVISO: indices originales (i hasta {i_sup}, j={j}) fuera del dominio entregado (nx={nx}, ny={ny}); recortando.")
    j = min(j, ny - 1)
    i_list = i_list[i_list < nx]

longitudes = lon[j, i_list]

fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.set_xlabel("Longitude (°E)", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontsize=12)
ax1.plot(i_list, APGD_native_cross[j, i_list], color='cornflowerblue', label="Target")
ax1.plot(i_list, APGD_degraded_cross[j, i_list], color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(i_list, APGD_downscaled_cross[j, i_list], color='olivedrab', label="DS")
plt.legend(fontsize=8, loc="upper left")

ax2 = ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontsize=12)
ax2.plot(i_list, S[j, i_list], color='grey', linewidth=0.1)
ax2.fill_between(i_list, S[j, i_list], color='grey', alpha=0.25)

ax1.set_xticks(i_list)
ax1.set_xticklabels(longitudes, rotation=90)
formatted_longitudes = [f"{ln:.2f}" for ln in longitudes]
ticks = ax1.get_xticks()
step = 19 if len(ticks) > 19 else max(1, len(ticks)//8)
ax1.set_xticks(ticks[::step])
ax1.set_xticklabels(formatted_longitudes[::step], rotation=45, fontsize=8)

elevation_ticks = ax2.get_yticks()
for x in range(1, len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)

plt.title("Mean annual precipitation along a longitudinal cross section (5km)")
plt.savefig(f"{OUT}/Cross_section_WE_5km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Cross_section_WE_5km.png")

# ============================== VERSION 10 km ==============================
d10 = load_10km()
lon10, lat10, S10 = d10['lon'], d10['lat'], d10['S']
APGD_native_cross10 = d10['obs_clim']
APGD_degraded_cross10 = d10['deg_clim']
APGD_downscaled_cross10 = d10['sim_clim']
ny10, nx10 = S10.shape

# --- North-south cross section 10km (indices originales del autor) ---
i = 54
j_inf, j_sup = 26, 59
j_list = np.arange(j_inf, j_sup)
if i >= nx10 or j_sup > ny10:
    print(f"AVISO: indices originales 10km (i={i}, j hasta {j_sup}) fuera del dominio (nx={nx10}, ny={ny10}); recortando.")
    i = min(i, nx10 - 1)
    j_list = j_list[j_list < ny10]

latitudes10 = lat10[j_list, i]

fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.set_xlabel("Latitude (°N)", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontsize=12)
ax1.plot(j_list, APGD_native_cross10[j_list, i], color='cornflowerblue', label="Target")
ax1.plot(j_list, APGD_degraded_cross10[j_list, i], color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(j_list, APGD_downscaled_cross10[j_list, i], color='olivedrab', label="DS")
plt.legend(fontsize=8, loc="upper left")

ax2 = ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontsize=12)
ax2.plot(j_list, S10[j_list, i], color='grey', linewidth=0.1)
ax2.fill_between(j_list, S10[j_list, i], color='grey', alpha=0.25)

ax1.set_xticks(j_list)
ax1.set_xticklabels(latitudes10, rotation=90)
formatted_latitudes10 = [f"{lt:.2f}" for lt in latitudes10]
ticks = ax1.get_xticks()
step = 15 if len(ticks) > 15 else max(1, len(ticks) // 8)
ax1.set_xticks(ticks[::step])
ax1.set_xticklabels(formatted_latitudes10[::step], rotation=45, fontsize=8)

elevation_ticks = ax2.get_yticks()
for x in range(1, len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)

plt.title("Mean annual precipitation along a latitudinal cross section (10km)")
plt.savefig(f"{OUT}/Cross_section_NS_10km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Cross_section_NS_10km.png")

# --- West-East cross-section 10km (indices originales del autor) ---
i_inf, i_sup = 23, 47
j = 38
i_list = np.arange(i_inf, i_sup)
if j >= ny10 or i_sup > nx10:
    print(f"AVISO: indices originales 10km (i hasta {i_sup}, j={j}) fuera del dominio (nx={nx10}, ny={ny10}); recortando.")
    j = min(j, ny10 - 1)
    i_list = i_list[i_list < nx10]

longitudes10 = lon10[j, i_list]

fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.set_xlabel("Longitude (°E)", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontsize=12)
ax1.plot(i_list, APGD_native_cross10[j, i_list], color='cornflowerblue', label="Target")
ax1.plot(i_list, APGD_degraded_cross10[j, i_list], color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(i_list, APGD_downscaled_cross10[j, i_list], color='olivedrab', label="DS")
plt.legend(fontsize=8, loc="upper left")

ax2 = ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontsize=12)
ax2.plot(i_list, S10[j, i_list], color='grey', linewidth=0.1)
ax2.fill_between(i_list, S10[j, i_list], color='grey', alpha=0.25)

ax1.set_xticks(i_list)
ax1.set_xticklabels(longitudes10, rotation=90)
formatted_longitudes10 = [f"{ln:.2f}" for ln in longitudes10]
ticks = ax1.get_xticks()
step = 19 if len(ticks) > 19 else max(1, len(ticks) // 8)
ax1.set_xticks(ticks[::step])
ax1.set_xticklabels(formatted_longitudes10[::step], rotation=45, fontsize=8)

elevation_ticks = ax2.get_yticks()
for x in range(1, len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)

plt.title("Mean annual precipitation along a longitudinal cross section (10km)")
plt.savefig(f"{OUT}/Cross_section_WE_10km.png", format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Cross_section_WE_10km.png")
