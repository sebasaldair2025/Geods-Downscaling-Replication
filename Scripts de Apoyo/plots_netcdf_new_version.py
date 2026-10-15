# ADAPTADO de plots_netcdf_new_version.py (script ORIGINAL del autor, jbrenner).
# Cambios respecto al original: solo carga de datos (common_original.load_5km/10km en vez de
# xr.open_dataset a archivos .nc pre-climatologizados que no vienen en los datos entregados).
# El codigo de graficado (proyeccion, colores, colorbar, layout) es el mismo del autor.
#
# Bloques reproducidos: Climatologias PP 5km, Anomalias PP 5km, Topografia 5km, Climatologia
# 10km + dispersion Elevacion-vs-Anomalia 10km (usando una observacion APGD a 10km DERIVADA
# por regrillado conservativo de la observacion nativa a 5km -- ver build_apgd_10km_from_5km()
# en common_original.py -- porque el autor tenia un archivo de observacion nativo a 10km que
# no viene entre los datos entregados).
# Bloques NO reproducidos (ver README): los graficos de dispersion TEI-vs-elevacion y
# TEI-vs-anomalia (necesitan 'climato_TEI.nc', un producto downscaleado solo-con-TEI que no
# esta entre los archivos dados, y que el regrillado de arriba no puede sustituir).

from common_original import load_5km, load_10km, OUT, BASE
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.ticker import MaxNLocator

d = load_5km()
lon, lat, S = d['lon'], d['lat'], d['S']

valid_mask = (~np.isnan(d['deg_clim'])) & (~np.isnan(d['sim_clim'])) & (~np.isnan(d['obs_clim']))

pp_degraded = np.where(valid_mask, d['deg_clim'], np.nan)
pp_simu = np.where(valid_mask, d['sim_clim'], np.nan)
pp_HR = np.where(valid_mask, d['obs_clim'], np.nan)

fig, axs = plt.subplots(3, 1, figsize=(15, 18), subplot_kw={'projection': ccrs.LambertAzimuthalEqualArea(central_longitude=10, central_latitude=46)})

ax1 = axs[0]
ax2 = axs[1]
ax3 = axs[2]

pmin = 500
pmax = 3000

mapping = ax1.pcolormesh(lon, lat, pp_degraded, transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax1.set_title("a)", fontsize=16, loc='left', y=0.01, pad=-30)
ax1.coastlines(linestyle='dashed', linewidth=0.5)
ax1.set_xlim(-450000, 550000)
gl = ax1.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)
gl.ylocator = MaxNLocator(nbins=4)
gl.xlabel_style = {'size': 8, 'color': 'dimgrey'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey'}

mapping = ax2.pcolormesh(lon, lat, pp_simu, transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax2.set_title("b)", fontsize=16, loc='left', y=0.01, pad=-30)
ax2.coastlines(linestyle='dashed', linewidth=0.5)
ax2.set_xlim(-450000, 550000)
gl = ax2.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)
gl.ylocator = MaxNLocator(nbins=4)
gl.xlabel_style = {'size': 8, 'color': 'dimgrey'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey'}

mapping = ax3.pcolormesh(lon, lat, pp_HR, transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax3.set_title("c)", fontsize=16, loc='left', y=0.01, pad=-30)
ax3.coastlines(linestyle='dashed', linewidth=0.5)
ax3.set_xlim(-450000, 550000)
gl = ax3.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)
gl.ylocator = MaxNLocator(nbins=4)
gl.xlabel_style = {'size': 8, 'color': 'dimgrey'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey'}

cb = fig.colorbar(mapping, ax=[ax1, ax2, ax3], orientation='horizontal', pad=0.05, shrink=0.4)
cb.set_label("Mean annual precipitation (mm)", fontsize=18)

plt.savefig(f'{OUT}/Climatologies_PP_5.png', format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Climatologies_PP_5.png")

# ______________________________ anomalias (5km) ______________________________
# CORREGIDO: el articulo (Fig. A3) muestra 3 paneles -- (a) REF-APGD, (b) DS SIN efecto de
# secado, (c) DS CON efecto de secado -- pero la version anterior de este script solo graficaba
# 2 (le faltaba el panel del DS sin efecto de secado). Se agrega aqui usando el archivo
# 'pp_Alps_5km_drying-effect-deactivated.nc' que SI viene entre los datos entregados (el
# 'pp_Alps_5km.nc' normal, usado en 'sim'/pp_simu arriba, es la version CON efecto de secado,
# la parametrizacion P1 usada en el resto del articulo).
import matplotlib.colors as colors

ds_ds_nodrying = xr.open_dataset(f"{BASE}/GeoDS_downscaled_data/pp_Alps_5km_drying-effect-deactivated.nc")
sim_nodrying_clim = (ds_ds_nodrying['PP'].mean(dim='time') * 12).values
pp_simu_nodrying = np.where(valid_mask, sim_nodrying_clim, np.nan)

diff_degraded = pp_degraded - pp_HR
diff_simu_nodrying = pp_simu_nodrying - pp_HR
diff_simu = pp_simu - pp_HR

fig, axs = plt.subplots(1, 3, figsize=(20, 18), subplot_kw={'projection': ccrs.LambertAzimuthalEqualArea(central_longitude=10, central_latitude=46)})
ax1, ax2, ax3 = axs

pmin = np.nanmin([np.nanmin(diff_simu), np.nanmin(diff_simu_nodrying), np.nanmin(diff_degraded)])
cmap = plt.get_cmap('bwr_r')
norm = colors.SymLogNorm(linthresh=400, linscale=0.05, vmin=pmin, vmax=-pmin)

mapping = ax1.pcolormesh(lon, lat, diff_degraded, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, norm=norm)
ax1.set_title("a)", fontsize=16, loc='left', y=0.01, pad=-30)
ax1.coastlines(linestyle='dashed', linewidth=0.5)
ax1.set_xlim(-450000, 550000)
gl = ax1.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)
gl.ylocator = MaxNLocator(nbins=4)
gl.right_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey'}

mapping = ax2.pcolormesh(lon, lat, diff_simu_nodrying, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, norm=norm)
ax2.set_title("b)", fontsize=16, loc='left', y=0.01, pad=-30)
ax2.coastlines(linestyle='dashed', linewidth=0.5)
ax2.set_xlim(-450000, 550000)
gl = ax2.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)
gl.ylocator = MaxNLocator(nbins=4)
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey'}

mapping = ax3.pcolormesh(lon, lat, diff_simu, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, norm=norm)
ax3.set_title("c)", fontsize=16, loc='left', y=0.01, pad=-30)
ax3.coastlines(linestyle='dashed', linewidth=0.5)
ax3.set_xlim(-450000, 550000)
gl = ax3.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)
gl.ylocator = MaxNLocator(nbins=4)
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey'}

cb = fig.colorbar(mapping, ax=[ax1, ax2, ax3], orientation='horizontal', pad=0.05, shrink=0.5, ticks=[-1000, 0, 1000])
cb.set_label("Mean annual precipitation anomaly (mm)", fontsize=18)

plt.savefig(f'{OUT}/Anomaliess_PP_5.png', format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Anomaliess_PP_5.png (a=REF, b=DS sin secado, c=DS con secado)")

# ______________________________ topografia (5km) ______________________________
fig, ax = plt.subplots(1, 1, figsize=(10, 8), subplot_kw={'projection': ccrs.LambertAzimuthalEqualArea(central_longitude=10, central_latitude=46)})
mapping = ax.pcolormesh(lon, lat, S, transform=ccrs.PlateCarree(), shading="gouraud", cmap="Oranges")
ax.coastlines(linestyle='dashed', linewidth=0.5)
ax.set_xlim(-450000, 550000)
gl = ax.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)
gl.ylocator = MaxNLocator(nbins=4)
gl.xlabel_style = {'size': 8, 'color': 'dimgrey'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey'}

cb = fig.colorbar(mapping, orientation='vertical', pad=0.05, shrink=0.4)
cb.set_label("Elevation ASL (m)", fontsize=14)

plt.savefig(f'{OUT}/Topography_5km.png', format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Topography_5km.png")

# ______________________ dispersion Elevacion vs Anomalia (10km) ______________________
# ADAPTADO del bloque "reso=10" del original (lineas 184-224): el autor cargaba
# 'climatology_pp_obs.nc' a 10km ya pre-calculado; aqui se usa la observacion APGD a 10km
# DERIVADA por regrillado conservativo (build_apgd_10km_from_5km(), ver common_original.py
# y el LEEME de esta carpeta) porque ese archivo no viene entre los datos entregados. El
# resto -- que es lo unico que produce esta figura: un scatter de elevacion vs anomalia de
# precipitacion del modelo downscaleado -- es el codigo original sin cambios.
d10 = load_10km()
elevation_10 = d10['S'][d10['valid']].flatten()
anomaly_10 = (d10['sim_clim'] - d10['obs_clim'])[d10['valid']].flatten()

plt.figure(figsize=(10, 6))
plt.scatter(anomaly_10, elevation_10, s=5, alpha=0.4, color='royalblue')
plt.xlabel("Precipitation Anomaly (mm/year)")
plt.ylabel("Elevation (m)")
plt.title("Elevation vs Precipitation Anomaly (10km)")
plt.grid(True)
plt.tight_layout()
plt.savefig(f'{OUT}/Elevation_vs_Anomaly_10km.png', format='png', dpi=150, bbox_inches='tight')
plt.close()
print("OK Elevation_vs_Anomaly_10km.png")
