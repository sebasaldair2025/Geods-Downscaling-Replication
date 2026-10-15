import xarray as xr
import numpy as np
import netCDF4
import xskillscore as xs
import matplotlib.pyplot as plt
import pandas as pd


APGD_native_climatology=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/5km/precipitation/climatology_pp_obs.nc')
APGD_degraded=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/5km/precipitation/climatology_pp_degraded.nc')
APGD_downscaled=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/5km/precipitation/climato_1.nc')
#Topography=xr.open_dataset('/home/jbrenner/These/Cartes/APGD/preliminary_analysis/Topography_APGD.nc')

Topography=xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/5km/Topography_5km.nc')


lon_lat = xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/5km/lon_lat_target_5km.nc')


#North-south cross section


i=108
j_inf=54 #80
j_sup=114
j_list=np.arange(j_inf, j_sup)

APGD_native_cross_section=APGD_native_climatology.isel(x=i, y=j_list, time=0)
APGD_degraded_cross_section=APGD_degraded.isel(x=i, y=j_list, time=0)
APGD_downscaled_cross_section=APGD_downscaled.isel(x=i, y=j_list, time=0)
Topography_cross_section=Topography.isel(x=i, y=j_list)

latitudes = lon_lat['lat'].isel(x=i, y=j_list).values


fig, ax1 = plt.subplots(figsize=(9,6))
ax1.set_xlabel("Latitude (°N)", fontname="Arial", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax1.plot(APGD_native_cross_section['y'], APGD_native_cross_section['pp']*12, color='cornflowerblue', label="Target")
ax1.plot(APGD_degraded_cross_section['y'], APGD_degraded_cross_section['pp']*12, color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(APGD_downscaled_cross_section['y'], APGD_downscaled_cross_section['PP']*12, color='olivedrab', label="DS")
plt.legend(fontsize = 8, loc="upper left")

ax2=ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontname = "Arial", fontsize=12)
ax2.plot(Topography_cross_section['y'], Topography_cross_section['S'], color='grey', linewidth=0.1)
ax2.fill_between(Topography_cross_section['y'], Topography_cross_section['S'], color='grey', alpha=0.25)

ax1.set_xticks(APGD_native_cross_section['y'].values)  # Set the ticks to the Y values
ax1.set_xticklabels(latitudes, rotation=90)
formatted_latitudes = [f"{lat:.2f}" for lat in latitudes]

ticks = ax1.get_xticks()  # Get the current ticks
ax1.set_xticks(ticks[::19])  # Set ticks to every other tick
ax1.set_xticklabels(formatted_latitudes[::19], rotation=45, fontsize=8, fontname="Arial")

elevation_ticks = ax2.get_yticks()  # Get the current elevation ticks
for x in range(1,len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)
ax1.tick_params(labelfontfamily="Arial", size=8)
ax2.tick_params(labelfontfamily="Arial", size=8)

plt.savefig("/home/jbrenner/These/Resultats/Article/Cross_section_NS_5km.png", format='png')
plt.show()


#_____________________________________________________________________________________________
#West-East cross-section

import xarray as xr
import numpy as np
import netCDF4
import xskillscore as xs
import matplotlib.pyplot as plt
import pandas as pd


APGD_native_climatology=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/5km/precipitation/climatology_pp_obs.nc')
APGD_degraded=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/5km/precipitation/climatology_pp_degraded.nc')
APGD_downscaled=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/5km/precipitation/climato_1.nc')

Topography=xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/5km/Topography_5km.nc')

lon_lat = xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/5km/lon_lat_target_5km.nc')


#74 pas mal, sinon 71
i_inf=31
i_sup=95
j=74

i_list=np.arange(i_inf, i_sup)

APGD_native_cross_section=APGD_native_climatology.isel(x=i_list, y=j, time=0)
APGD_degraded_cross_section=APGD_degraded.isel(x=i_list, y=j, time=0)
APGD_downscaled_cross_section=APGD_downscaled.isel(x=i_list, y=j, time=0)
Topography_cross_section=Topography.isel(x=i_list, y=j)

#latitudes = APGD_native_cross_section['lat'].values
#lon = lon_lat['lon'].isel(x=i, y=j_list)
longitudes = lon_lat['lon'].isel(x=i_list, y=j).values

fig, ax1 = plt.subplots(figsize=(9,6))
ax1.set_xlabel("Longitude (°E)", fontname="Arial", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax1.plot(APGD_native_cross_section['x'], APGD_native_cross_section['pp']*12, color='cornflowerblue', label="Target")
ax1.plot(APGD_degraded_cross_section['x'], APGD_degraded_cross_section['pp']*12, color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(APGD_downscaled_cross_section['x'], APGD_downscaled_cross_section['PP']*12, color='olivedrab', label="DS")
plt.legend(fontsize = 8, loc="upper left")

ax2=ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontname = "Arial", fontsize=12)
ax2.plot(Topography_cross_section['x'], Topography_cross_section['S'], color='grey', linewidth=0.1)
ax2.fill_between(Topography_cross_section['x'], Topography_cross_section['S'], color='grey', alpha=0.25)

ax1.set_xticks(APGD_native_cross_section['x'].values)  # Set the ticks to the Y values
ax1.set_xticklabels(longitudes, rotation=90)
formatted_longitudes = [f"{lat:.2f}" for lat in longitudes]

ticks = ax1.get_xticks()  # Get the current ticks
ax1.set_xticks(ticks[::19])  # Set ticks to every other tick
ax1.set_xticklabels(formatted_longitudes[::19], rotation=45, fontsize=8, fontname="Arial")

elevation_ticks = ax2.get_yticks()  # Get the current elevation ticks
for x in range(1,len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)
ax1.tick_params(labelfontfamily="Arial", size=8)
ax2.tick_params(labelfontfamily="Arial", size=8)

ax2.text(4104000, 2000, 'Sion valley', fontname = "Arial", fontweight="bold", fontstyle="italic")
ax2.arrow(4114000, 1980, 0, -1250, linestyle="dashed")
plt.title("Mean annual precipitation along a longitudinal cross section")
plt.savefig("/home/jbrenner/These/Resultats/Article/Cross_section_WE_5km.png", format='png')
plt.show()


#__________________________________________________________________________________________________________________________________
# VERSION 10 km


import xarray as xr
import numpy as np
import netCDF4
import xskillscore as xs
import matplotlib.pyplot as plt
import pandas as pd


APGD_native_climatology=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/10km/precipitation/climatology_pp_obs.nc')
APGD_degraded=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/10km/precipitation/climatology_pp_degraded.nc')
APGD_downscaled=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/10km/precipitation/climato_1.nc')
#Topography=xr.open_dataset('/home/jbrenner/These/Cartes/APGD/preliminary_analysis/Topography_APGD.nc')

Topography=xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/10km/sup_maps/Topography_10km.nc')


lon_lat = xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/10km/lon_lat_target_10km.nc')


#North-south cross section


i=54
j_inf=26 #80
j_sup=59
j_list=np.arange(j_inf, j_sup)

APGD_native_cross_section=APGD_native_climatology.isel(x=i, y=j_list, time=0)
APGD_degraded_cross_section=APGD_degraded.isel(x=i, y=j_list, time=0)
APGD_downscaled_cross_section=APGD_downscaled.isel(x=i, y=j_list, time=0)
Topography_cross_section=Topography.isel(x=i, y=j_list)

latitudes = lon_lat['lat'].isel(x=i, y=j_list).values


fig, ax1 = plt.subplots(figsize=(9,6))
ax1.set_xlabel("Latitude (°N)", fontname="Arial", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax1.plot(APGD_native_cross_section['y'], APGD_native_cross_section['pp']*12, color='cornflowerblue', label="Target")
ax1.plot(APGD_degraded_cross_section['y'], APGD_degraded_cross_section['pp']*12, color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(APGD_downscaled_cross_section['y'], APGD_downscaled_cross_section['PP']*12, color='olivedrab', label="DS")
plt.legend(fontsize = 8, loc="upper left")

ax2=ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontname = "Arial", fontsize=12)
ax2.plot(Topography_cross_section['y'], Topography_cross_section['S'], color='grey', linewidth=0.1)
ax2.fill_between(Topography_cross_section['y'], Topography_cross_section['S'], color='grey', alpha=0.25)

ax1.set_xticks(APGD_native_cross_section['y'].values)  # Set the ticks to the Y values
ax1.set_xticklabels(latitudes, rotation=90)
formatted_latitudes = [f"{lat:.2f}" for lat in latitudes]

ticks = ax1.get_xticks()  # Get the current ticks
ax1.set_xticks(ticks[::15])  # Set ticks to every other tick
ax1.set_xticklabels(formatted_latitudes[::15], rotation=45, fontsize=8, fontname="Arial")

elevation_ticks = ax2.get_yticks()  # Get the current elevation ticks
for x in range(1,len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)
ax1.tick_params(labelfontfamily="Arial", size=8)
ax2.tick_params(labelfontfamily="Arial", size=8)

plt.title("Mean annual precipitation along a latitudinal cross section")
plt.savefig("/home/jbrenner/These/Resultats/Article/Cross_section_NS_10km.png", format='png')
plt.show()



import xarray as xr
import numpy as np
import netCDF4
import xskillscore as xs
import matplotlib.pyplot as plt
import pandas as pd



APGD_native_climatology=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/10km/precipitation/climatology_pp_obs.nc')
APGD_degraded=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/10km/precipitation/climatology_pp_degraded.nc')
APGD_downscaled=xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/tests_sensibilite/Alps_APGD/10km/precipitation/climato_1.nc')
#Topography=xr.open_dataset('/home/jbrenner/These/Cartes/APGD/preliminary_analysis/Topography_APGD.nc')

Topography=xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/10km/sup_maps/Topography_10km.nc')


lon_lat = xr.open_dataset('/home/jbrenner/These/Cartes/APGD/final_analysis/10km/lon_lat_target_10km.nc')


#74 pas mal, sinon 71
i_inf=23
i_sup=47
j=38

i_list=np.arange(i_inf, i_sup)

APGD_native_cross_section=APGD_native_climatology.isel(x=i_list, y=j, time=0)
APGD_degraded_cross_section=APGD_degraded.isel(x=i_list, y=j, time=0)
APGD_downscaled_cross_section=APGD_downscaled.isel(x=i_list, y=j, time=0)
Topography_cross_section=Topography.isel(x=i_list, y=j)

#latitudes = APGD_native_cross_section['lat'].values
#lon = lon_lat['lon'].isel(x=i, y=j_list)
longitudes = lon_lat['lon'].isel(x=i_list, y=j).values

fig, ax1 = plt.subplots(figsize=(9,6))
ax1.set_xlabel("Longitude (°E)", fontname="Arial", fontsize=12)
ax1.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax1.plot(APGD_native_cross_section['x'], APGD_native_cross_section['pp']*12, color='cornflowerblue', label="Target")
ax1.plot(APGD_degraded_cross_section['x'], APGD_degraded_cross_section['pp']*12, color='indianred', label=r"Ref$_{interpolated}$")
ax1.plot(APGD_downscaled_cross_section['x'], APGD_downscaled_cross_section['PP']*12, color='olivedrab', label="DS")
plt.legend(fontsize = 8, loc="upper left")

ax2=ax1.twinx()
ax2.set_ylabel("Elevation ASL (m)", fontname = "Arial", fontsize=12)
ax2.plot(Topography_cross_section['x'], Topography_cross_section['S'], color='grey', linewidth=0.1)
ax2.fill_between(Topography_cross_section['x'], Topography_cross_section['S'], color='grey', alpha=0.25)

ax1.set_xticks(APGD_native_cross_section['x'].values)  # Set the ticks to the Y values
ax1.set_xticklabels(longitudes, rotation=90)
formatted_longitudes = [f"{lat:.2f}" for lat in longitudes]

ticks = ax1.get_xticks()  # Get the current ticks
ax1.set_xticks(ticks[::19])  # Set ticks to every other tick
ax1.set_xticklabels(formatted_longitudes[::19], rotation=45, fontsize=8, fontname="Arial")

elevation_ticks = ax2.get_yticks()  # Get the current elevation ticks
for x in range(1,len(elevation_ticks)):
    ax2.axhline(y=elevation_ticks[x], color='black', linestyle='--', linewidth=0.5, alpha=0.35)
ax1.tick_params(labelfontfamily="Arial", size=8)
ax2.tick_params(labelfontfamily="Arial", size=8)

ax2.text(4122000, 2200, 'Sion valley', fontname = "Arial", fontweight="bold", fontstyle="italic")
ax2.arrow(4134000, 2180, 0, -850, linestyle="dashed")
plt.title("Mean annual precipitation along a longitudinal cross section")
plt.savefig("/home/jbrenner/These/Resultats/Article/Cross_section_WE_10km.png", format='png')
plt.show()




