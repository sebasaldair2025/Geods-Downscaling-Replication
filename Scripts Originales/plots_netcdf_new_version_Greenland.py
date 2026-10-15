import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator

reso = 15
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climato_1.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/Greenland/sup_maps/lonlat_15km.nc')

#HR = HR.assign_coords({
#    'x': HR['x'].astype('float64'),
#     'y': HR['y'].astype('float64')
# })
# HR['y']=np.round(HR["y"], 3)
# HR['x']=np.round(HR["x"], 0)


#HR2 = HR.transpose('time', 'x', 'y')
# Create a mask for valid data
valid_mask = (~degraded['pp'].isnull()) & (~simu['PP'].isnull()) & (~HR['pp'].isnull())

# Apply the mask to each dataset and squeeze to remove singleton dimensions
pp_degraded = degraded.where(valid_mask).isel(time=0).squeeze()
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

pmin=0 #pp_HR["pp"].min().item()
pmax=800

mapping = ax1.pcolormesh(lon, lat, pp_degraded["pp"], transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax1.set_title("a)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax1.coastlines(linestyle='dashed', linewidth=0.5)
#ax1.set_xlim(-450000, 550000)
gl = ax1.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

# Plotting for the second dataset
mapping = ax2.pcolormesh(lon, lat, pp_simu["PP"], transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax2.set_title("b)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax2.coastlines(linestyle='dashed', linewidth=0.5)
#ax2.set_xlim(-450000, 550000)
gl = ax2.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

# Plotting for the third dataset
mapping = ax3.pcolormesh(lon, lat, pp_HR["pp"], transform=ccrs.PlateCarree(), shading="gouraud", cmap="Blues", vmin=pmin, vmax=pmax)
ax3.set_title("c)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax3.coastlines(linestyle='dashed', linewidth=0.5)
#ax3.set_xlim(-450000, 550000)
gl = ax3.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

cb = fig.colorbar(mapping, ax=[ax1, ax2, ax3], orientation='horizontal', pad=0.05, shrink=0.4)
cb.set_label("Mean annual precipitation (mm)", fontsize='x-large', fontname="Arial")
plt.show()
plt.savefig(f'/home/jbrenner/These/Resultats/Article/Climatologies_PP_{reso}_Greenland.png', format='png')




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

reso = 15
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climato_1.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/Greenland/sup_maps/lonlat_15km.nc')

topo=xr.open_dataset(f'/home/jbrenner/These/Cartes/Greenland/HR_Topographic_Parameters.nc')

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


fig, axs = plt.subplots(1, 2, figsize=(15, 15), subplot_kw={'projection': ccrs.Stereographic(central_longitude=-42, central_latitude=70)})


# Create a meshgrid for the longitude and latitude
lon = lon_lat["lon"]
lat = lon_lat["lat"]

# Plotting
ax1 = axs[0]
ax2 = axs[1]
#ax3 = axs[2]

pmin=min(diff_simu.min(), diff_degraded.min())
pmax=max(diff_simu.max(), diff_degraded.max())

cmap = plt.get_cmap('bwr_r')
#norm = mpl.colors.BoundaryNorm([pmin, -500, 200, pmax], ncolors=3)
norm=colors.SymLogNorm(linthresh=400, linscale=0.05, vmin=pmin, vmax=-pmin)

cmap2=plt.get_cmap('Oranges')


mapping = ax1.pcolormesh(lon, lat, diff_degraded, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, norm=norm) #, vmin=pmin, vmax=pmax)
gl = ax1.gridlines(draw_labels=True, linewidth=0.4)
ax1.set_title("a)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax1.coastlines(linestyle='dashed', linewidth=0.5)
gl.left_labels = True
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

# Plotting for the second dataset
mapping = ax2.pcolormesh(lon, lat, diff_simu, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, norm=norm) #, vmin=pmin, vmax=pmax)
ax2.set_title("b)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax2.coastlines(linestyle='dashed', linewidth=0.5)
gl = ax2.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

tick_locator = MaxNLocator(nbins=3)


cb = fig.colorbar(mapping, ax=[ax1, ax2], orientation='horizontal', pad=0.05, shrink=0.8, ticks=[-1000, 0, 1000])
cb.ax.locator_params(nbins=3)
cb.set_label("Mean annual precipitation anomaly (mm)", fontsize='x-large', fontname="Arial")

plt.savefig(f'/home/jbrenner/These/Resultats/Article/Anomaliess_PP_{reso}.png', format='png')


mapping = ax3.pcolormesh(lon, lat, topo['S'].isel(time=1), transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap2) #, vmin=pmin, vmax=pmax)
ax3.set_title("c)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax3.coastlines(linestyle='dashed', linewidth=0.5)
gl = ax3.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

cb2 = fig.colorbar(mapping, ax=[ax3], orientation='vertical', pad=0.05, shrink=0.5)
cb2.set_label("Elevation (in meters ASL)", fontsize='x-large', fontname="Arial")

plt.savefig(f'/home/jbrenner/These/Resultats/Article/Anomaliess_PP_{reso}.png', format='png')
plt.show()

#_______________________________________

#plots anomaly climatology simu/obs

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
import matplotlib.colors as colors

reso = 15
# Load your dataset
degraded = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climatology_pp_degraded.nc')
simu = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climato_1.nc')
HR = xr.open_dataset(f'/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Greenland/{reso}km/precipitation/climatology_pp_obs.nc')

lon_lat = xr.open_dataset(f'/home/jbrenner/These/Cartes/Greenland/sup_maps/lonlat_15km.nc')

topo=xr.open_dataset(f'/home/jbrenner/These/Cartes/Greenland/HR_Topographic_Parameters.nc')

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

diff_degraded=(pp_degraded['pp']-pp_HR['pp'])/pp_HR['pp']
diff_simu=(pp_simu['PP']-pp_HR['pp'])/pp_HR['pp']


fig, axs = plt.subplots(1, 3, figsize=(25, 18), subplot_kw={'projection': ccrs.LambertAzimuthalEqualArea(central_longitude=10, central_latitude=46)})

# Create a meshgrid for the longitude and latitude
lon = lon_lat["lon"]
lat = lon_lat["lat"]

# Plotting
ax1 = axs[0]
ax2 = axs[1]
ax3 = axs[2]

pmin=-2
pmax=2

cmap = plt.get_cmap('bwr_r')
#norm = mpl.colors.BoundaryNorm([pmin, -500, 200, pmax], ncolors=3)
cmap2=plt.get_cmap('Oranges')


mapping = ax1.pcolormesh(lon, lat, diff_degraded, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, vmin=pmin, vmax=pmax)
ax1.set_title("a)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax1.coastlines(linestyle='dashed', linewidth=0.5)
gl = ax1.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

# Plotting for the second dataset
mapping = ax2.pcolormesh(lon, lat, diff_simu, transform=ccrs.PlateCarree(), shading="gouraud", cmap=cmap, vmin=pmin, vmax=pmax)
ax2.set_title("b)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax2.coastlines(linestyle='dashed', linewidth=0.5)
gl = ax2.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

cb = fig.colorbar(mapping, ax=[ax1, ax2], orientation='horizontal', pad=0.05, shrink=0.5)
cb.set_label("Mean annual precipitation anomaly (mm)", fontsize='x-large', fontname="Arial")

mapping = ax3.pcolormesh(lon, lat, topo['S'].isel(time=1), transform=ccrs.PlateCarree(), shading="gouraud") #, vmin=pmin, vmax=pmax)
ax3.set_title("c)", fontsize=16, loc='left', y=0.01, pad=-30, fontname="Arial")
ax3.coastlines(linestyle='dashed', linewidth=0.5)
gl = ax3.gridlines(draw_labels=True, linewidth=0.4)
gl.xlocator = MaxNLocator(nbins=5)  # Set number of longitude gridlines
gl.ylocator = MaxNLocator(nbins=5)  # Set number of latitude gridlines
gl.right_labels = False
gl.left_labels = False
gl.xlabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}
gl.ylabel_style = {'size': 8, 'color': 'dimgrey', 'name': 'Arial'}

cb2 = fig.colorbar(mapping, ax=[ax3], orientation='horizontal', pad=0.05, shrink=0.5)
cb2.set_label("Elevation (in meters ASL)", fontsize='x-large', fontname="Arial")

plt.savefig(f'/home/jbrenner/These/Resultats/Article/Anomaliess_PP_{reso}.png', format='png')
plt.show()
