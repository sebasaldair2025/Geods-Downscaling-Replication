import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator

reso = 5
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/{reso}km/precipitation/climato_1.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/lon_lat_target_{reso}km.nc')

# Create a mask for valid data
valid_mask = (~degraded['pp'].isnull()) & (~simu['PP'].isnull()) & (~HR['pp'].isnull())

# Apply the mask to each dataset and squeeze to remove singleton dimensions
pp_degraded = degraded.isel(time=0).where(valid_mask).squeeze()
pp_simu = simu.isel(time=0).where(valid_mask).squeeze()
pp_HR = HR.isel(time=0).where(valid_mask).squeeze()

# Scale the precipitation data
pp_degraded['pp'] = pp_degraded['pp'] * 12
pp_simu['PP'] = pp_simu["PP"] * 12
pp_HR["pp"] = pp_HR["pp"] * 12

fig, axs = plt.subplots(3, 1, figsize=(15, 18), subplot_kw={'projection': ccrs.LambertAzimuthalEqualArea(central_longitude=10, central_latitude=46)})

# Create a meshgrid for the longitude and latitude
lon = lon_lat["lon"]
lat = lon_lat["lat"]

# Plotting
ax1 = axs[0]
ax2 = axs[1]
ax3 = axs[2]

pmin=500 #pp_HR["pp"].min().item()
pmax=3000

mapping = ax1.pcolormesh(lon, lat, pp_degraded["pp"], transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax1.set_title("a)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax1.coastlines(linestyle='dashed', linewidth=0.5)
ax1.set_xlim(-450000, 550000)
gl = ax1.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=4)  # Set number of latitude gridlines
#gl.right_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

# Plotting for the second dataset
mapping = ax2.pcolormesh(lon, lat, pp_simu["PP"], transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax2.set_title("b)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax2.coastlines(linestyle='dashed', linewidth=0.5)
ax2.set_xlim(-450000, 550000)
gl = ax2.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=4)  # Set number of latitude gridlines
#gl.right_labels = False
#gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

# Plotting for the third dataset
mapping = ax3.pcolormesh(lon, lat, pp_HR["pp"], transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax3.set_title("c)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax3.coastlines(linestyle='dashed', linewidth=0.5)
ax3.set_xlim(-450000, 550000)
gl = ax3.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=4)  # Set number of latitude gridlines
#gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

cb = fig.colorbar(mapping, ax=[ax1, ax2, ax3], orientation='horizontal', pad=0.05, shrink=0.4)
cb.set_label("Mean annual precipitation (mm)", fontsize=18, fontname="Arial")

plt.savefig(f'/home/jbrenner/These/Resultats/Article/Climatologies_PP_{reso}.png', format='png')




#__________________________________________________________________________________________
#plots anomaly climatology simu/obs

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import matplotlib.colors as colors

reso = 5
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/{reso}km/precipitation/climato_1.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/lon_lat_target_{reso}km.nc')
topo=xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/HR_Topographic_Parameters.nc')

# Create a mask for valid data
valid_mask = (~degraded['pp'].isnull()) & (~simu['PP'].isnull()) & (~HR['pp'].isnull())

# Apply the mask to each dataset and squeeze to remove singleton dimensions
pp_degraded = degraded.isel(time=0).where(valid_mask).squeeze()
pp_simu = simu.isel(time=0).where(valid_mask).squeeze()
pp_HR = HR.isel(time=0).where(valid_mask).squeeze()

# Scale the precipitation data
pp_degraded['pp'] = pp_degraded['pp'] * 12
pp_simu['PP'] = pp_simu["PP"] * 12
pp_HR["pp"] = pp_HR["pp"] * 12

diff_degraded=pp_degraded['pp']-pp_HR['pp']
diff_simu=pp_simu['PP']-pp_HR['pp']


fig, axs = plt.subplots(1, 2, figsize=(15, 18), subplot_kw={'projection': ccrs.LambertAzimuthalEqualArea(central_longitude=10, central_latitude=46)})

# Create a meshgrid for the longitude and latitude
lon = lon_lat["lon"]
lat = lon_lat["lat"]

# Plotting
ax1 = axs[0]
ax2 = axs[1]

pmin=min(diff_simu.min(), diff_degraded.min())
pmax=max(diff_simu.max(), diff_degraded.max())

cmap = plt.get_cmap('bwr_r')
#norm = mpl.colors.BoundaryNorm([pmin, -500, 200, pmax], ncolors=3)
norm=colors.SymLogNorm(linthresh=400, linscale=0.05, vmin=pmin, vmax=-pmin)

mapping = ax1.pcolormesh(lon, lat, diff_degraded, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, norm=norm) #, vmin=pmin, vmax=pmax)
ax1.set_title("a)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax1.coastlines(linestyle='dashed', linewidth=0.5)
ax1.set_xlim(-450000, 550000)
gl = ax1.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=4)  # Set number of latitude gridlines
gl.right_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

# Plotting for the second dataset
mapping = ax2.pcolormesh(lon, lat, diff_simu, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, norm=norm) #, vmin=pmin, vmax=pmax)
ax2.set_title("b)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax2.coastlines(linestyle='dashed', linewidth=0.5)
ax2.set_xlim(-450000, 550000)
gl = ax2.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=4)  # Set number of latitude gridlines
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}


cb = fig.colorbar(mapping, ax=[ax1, ax2], orientation='horizontal', pad=0.05, shrink=0.5, ticks=[-1000, 0, 1000])
cb.set_label("Mean annual precipitation anomaly (mm)", fontsize=18, fontname="Arial")

plt.savefig(f'/home/jbrenner/These/Resultats/Article/Anomaliess_PP_{reso}.png', format='png')
plt.show()

#_______________________________________

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import matplotlib.colors as colors

reso = 10
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climato_1.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/lon_lat_target_{reso}km.nc')
topo=xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/sup_maps/Topography_10km.nc')

# Create a mask for valid data
valid_mask = (~degraded['pp'].isnull()) & (~simu['PP'].isnull()) & (~HR['pp'].isnull())

# Apply the mask to each dataset and squeeze to remove singleton dimensions
pp_degraded = degraded.isel(time=0).where(valid_mask).squeeze()
pp_simu = simu.isel(time=0).where(valid_mask).squeeze()
pp_HR = HR.isel(time=0).where(valid_mask).squeeze()

# Scale the precipitation data
pp_degraded['pp'] = pp_degraded['pp'] * 12
pp_simu['PP'] = pp_simu["PP"] * 12
pp_HR["pp"] = pp_HR["pp"] * 12

diff_degraded=pp_degraded['pp']-pp_HR['pp']
diff_simu=pp_simu['PP']-pp_HR['pp']
elevation = topo['S'].where(valid_mask).values.flatten()
anomaly = diff_simu.where(valid_mask).values.flatten()

# Remove invalid (NaN) points
valid_points = ~np.isnan(elevation) & ~np.isnan(anomaly)
elevation = elevation[valid_points]
anomaly = anomaly[valid_points]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(anomaly, elevation, s=5, alpha=0.4, color='royalblue')
plt.xlabel("Precipitation Anomaly (mm/year)")
plt.ylabel("Elevation (m)")
plt.title("Elevation vs Precipitation Anomaly")
plt.grid(True)
plt.tight_layout()
plt.show()

#_______________________________________
# LIEN ALTITUDE-TEI
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import matplotlib.colors as colors

reso = 10
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climato_TEI.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/lon_lat_target_{reso}km.nc')
topo=xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/sup_maps/Topography_10km.nc')

# Create a mask for valid data
valid_mask = (~degraded['pp'].isnull()) & (~simu['PP'].isnull()) & (~HR['pp'].isnull())

# Apply the mask to each dataset and squeeze to remove singleton dimensions
pp_degraded = degraded.isel(time=0).where(valid_mask).squeeze()
pp_simu = simu.isel(time=0).where(valid_mask).squeeze()
pp_HR = HR.isel(time=0).where(valid_mask).squeeze()

# Scale the precipitation data
pp_degraded['pp'] = pp_degraded['pp'] * 12
pp_simu['PP'] = pp_simu["PP"] * 12
pp_HR["pp"] = pp_HR["pp"] * 12

diff_degraded=pp_degraded['pp']-pp_HR['pp']
diff_simu=pp_simu['PP']
elevation = topo['S'].where(valid_mask).values.flatten()
anomaly = diff_simu.where(valid_mask).values.flatten()

# Remove invalid (NaN) points
valid_points = ~np.isnan(elevation) & ~np.isnan(anomaly)
elevation = elevation[valid_points]
anomaly = anomaly[valid_points]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(anomaly, elevation, s=5, alpha=0.4, color='royalblue')
plt.xlabel("Topographic Exposure Index")
plt.ylabel("Elevation (m)")
plt.title("TEI vs Elevation")
plt.grid(True)
plt.tight_layout()
plt.show()

#___________________________________________
# LIEN Anomaly-TEI
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import matplotlib.colors as colors

reso = 10
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climato_1.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/lon_lat_target_{reso}km.nc')
TEI=xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/{reso}km/precipitation/climato_TEI.nc')

# Create a mask for valid data
valid_mask = (~degraded['pp'].isnull()) & (~simu['PP'].isnull()) & (~HR['pp'].isnull())

# Apply the mask to each dataset and squeeze to remove singleton dimensions
pp_degraded = degraded.isel(time=0).where(valid_mask).squeeze()
pp_simu = simu.isel(time=0).where(valid_mask).squeeze()
pp_HR = HR.isel(time=0).where(valid_mask).squeeze()

# Scale the precipitation data
pp_degraded['pp'] = pp_degraded['pp'] * 12
pp_simu['PP'] = pp_simu["PP"] * 12
pp_HR["pp"] = pp_HR["pp"] * 12

diff_degraded=pp_degraded['pp']-pp_HR['pp']
diff_simu = pp_simu['PP'] - pp_HR["pp"]
tei = TEI['PP'].where(valid_mask).values.flatten()
anomaly = diff_simu.where(valid_mask).values.flatten()

# Remove invalid (NaN) points
valid_points = ~np.isnan(tei) & ~np.isnan(anomaly)
tei = tei[valid_points]
anomaly = anomaly[valid_points]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(anomaly, tei, s=5, alpha=0.4, color='royalblue')
plt.xlabel("Anomaly")
plt.ylabel("TEI")
plt.title("TEI vs Anomaly")
plt.grid(True)
plt.tight_layout()
plt.show()



















#__________________________________topographie




import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator

reso = 5
topo = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/HR_Topographic_Parameters.nc')
lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/lon_lat_target_{reso}km.nc')

fig, ax = plt.subplots(1, 1, figsize=(10, 8), subplot_kw={'projection': ccrs.LambertAzimuthalEqualArea(central_longitude=10, central_latitude=46)})

# Create a meshgrid for the longitude and latitude
lon = lon_lat["lon"]
lat = lon_lat["lat"]

# Plotting
mapping = ax.pcolormesh(lon, lat, topo["S"], transform=ccrs.PlateCarree(), shading="gouraud", cmap="Oranges")
#ax.set_title("", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax.coastlines(linestyle='dashed', linewidth=0.5)
ax.set_xlim(-450000, 550000)
gl = ax.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=4)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=4)  # Set number of latitude gridlines
#gl.right_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

cb = fig.colorbar(mapping, orientation='vertical', pad=0.05, shrink=0.4)
cb.set_label("Elevation ASL (m)", fontsize=14, fontname="Arial")

plt.savefig(f'/home/jbrenner/These/Resultats/Article/Topography_5km{reso}.png', format='png')





