#Global

import xarray as xr
import numpy as np
import netCDF4
import xskillscore as xs
import matplotlib.pyplot as plt
import pandas as pd


simu="1"
reso=10


APGD_downscaled = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_precipitation_Alps_APGD.nc')
APGD_degraded = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/degraded_pp_masked.nc')
APGD_native = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/obs_pp_masked.nc')

APGD_native['time'] = xr.DataArray(pd.to_datetime(APGD_native['time'].values, format='%Y%m'), dims='time', coords={'time': APGD_native['time'].values})
APGD_degraded['time'] = xr.DataArray(pd.to_datetime(APGD_degraded['time'].values, format='%Y%m'), dims='time', coords={'time': APGD_degraded['time'].values})
APGD_downscaled['time'] = xr.DataArray(pd.to_datetime(APGD_downscaled['time'].values, format='%Y%m'), dims='time', coords={'time': APGD_downscaled['time'].values})



years=[]
annual_APGD_native=[]
annual_APGD_degraded=[]
annual_APGD_downscaled=[]



for m in range (1971, 2020):
    native_mean = APGD_native['pp'].where(APGD_native["time"].dt.year==m).mean().item()
    degraded_mean = APGD_degraded['pp'].where(APGD_degraded["time"].dt.year==m).mean().item()
    downscaled_mean = APGD_downscaled['PP'].where(APGD_downscaled["time"].dt.year==m).mean().item()
    years.append(m)
    annual_APGD_native.append(native_mean*12)
    annual_APGD_degraded.append(degraded_mean*12)
    annual_APGD_downscaled.append(downscaled_mean*12)
    
    
    
fig, ax1 = plt.subplots()
ax1.plot(years, annual_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$", linewidth=0.8)
ax1.plot(years, annual_APGD_downscaled, color="olivedrab", label="DS", linewidth=0.8)
ax1.plot(years, annual_APGD_native, color="cornflowerblue", label="Target", linewidth=0.8)
#ax1.set_xlabel("Month", fontname="Arial", fontsize=14)
ax1.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
#ax1.set_title("a)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
#ax1.text(0.03, 0.9, s="Global seasonal cycle",  transform=ax1.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         #bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))
plt.legend(fontsize=8, loc="upper left")
plt.title("Global interannual variability")
plt.show()




#____________________________________________________________________________________________________________________________
#Points ponctuels
import xarray as xr
import numpy as np
import netCDF4
import xskillscore as xs
import matplotlib.pyplot as plt
import pandas as pd

simu="1"
reso=10


APGD_downscaled = xr.open_dataset('/home/jbrenner/These/GeoDS_Outputs/monthly_downscaled_precipitation_Alps_APGD.nc')
APGD_degraded = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/degraded_pp_masked.nc')
APGD_native = xr.open_dataset(f'/home/jbrenner/These/Cartes/APGD/final_analysis/{reso}km/obs_pp_masked.nc')

APGD_native['time'] = xr.DataArray(pd.to_datetime(APGD_native['time'].values, format='%Y%m'), dims='time', coords={'time': APGD_native['time'].values})
APGD_degraded['time'] = xr.DataArray(pd.to_datetime(APGD_degraded['time'].values, format='%Y%m'), dims='time', coords={'time': APGD_degraded['time'].values})
APGD_downscaled['time'] = xr.DataArray(pd.to_datetime(APGD_downscaled['time'].values, format='%Y%m'), dims='time', coords={'time': APGD_downscaled['time'].values})


i=[60, 54, 38, 32, 41] #30]
j=[61, 51, 40, 32, 32] #46]

#________________________________________________________________________________________________________________________
#seasonal cycles






fig, axs = plt.subplots(6,1,figsize=(14,25))

#global

years=[]
annual_APGD_native=[]
annual_APGD_degraded=[]
annual_APGD_downscaled=[]



for m in range (1971, 2020):
    native_mean = APGD_native['pp'].where(APGD_native["time"].dt.year==m).mean().item()
    degraded_mean = APGD_degraded['pp'].where(APGD_degraded["time"].dt.year==m).mean().item()
    downscaled_mean = APGD_downscaled['PP'].where(APGD_downscaled["time"].dt.year==m).mean().item()
    years.append(m)
    annual_APGD_native.append(native_mean*12)
    annual_APGD_degraded.append(degraded_mean*12)
    annual_APGD_downscaled.append(downscaled_mean*12)


ax0=axs[0]
ax0.plot(years, annual_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax0.plot(years, annual_APGD_downscaled, color="olivedrab", label="DS")
ax0.plot(years, annual_APGD_native, color="cornflowerblue", label="Target")
#ax1.set_xlabel("Month", fontname="Arial", fontsize=14)
ax0.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax0.set_title("a)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax0.text(0.03, 0.9, s="Global",  transform=ax0.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))

APGD_native_gridpoint = APGD_native.isel(x=i[0], y=j[0])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[0], y=j[0])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[0], y=j[0])


years=[]
annual_APGD_native=[]
annual_APGD_degraded=[]
annual_APGD_downscaled=[]



for m in range (1971, 2020):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.year==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.year==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.year==m).mean().item()
    years.append(m)
    annual_APGD_native.append(native_mean*12)
    annual_APGD_degraded.append(degraded_mean*12)
    annual_APGD_downscaled.append(downscaled_mean*12)


ax1=axs[1]
ax1.plot(years, annual_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax1.plot(years, annual_APGD_downscaled, color="olivedrab", label="DS")
ax1.plot(years, annual_APGD_native, color="cornflowerblue", label="Target")
#ax1.set_xlabel("Month", fontname="Arial", fontsize=14)
ax1.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax1.set_title("b)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax1.text(0.03, 0.9, s="Plain",  transform=ax1.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))


#_____________________________________
APGD_native_gridpoint = APGD_native.isel(x=i[1], y=j[1])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[1], y=j[1])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[1], y=j[1])


years=[]
annual_APGD_native=[]
annual_APGD_degraded=[]
annual_APGD_downscaled=[]



for m in range (1971, 2020):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.year==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.year==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.year==m).mean().item()
    years.append(m)
    annual_APGD_native.append(native_mean*12)
    annual_APGD_degraded.append(degraded_mean*12)
    annual_APGD_downscaled.append(downscaled_mean*12)



ax2=axs[2]
ax2.plot(years, annual_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax2.plot(years, annual_APGD_downscaled, color="olivedrab", label="DS")
ax2.plot(years, annual_APGD_native, color="cornflowerblue", label="Target")
#ax2.set_xlabel("Month", fontname="Arial", fontsize=14)
ax2.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax2.set_title("c)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax2.text(0.03, 0.9, s="Windward exposure",  transform=ax2.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))


#________________________________________
APGD_native_gridpoint = APGD_native.isel(x=i[2], y=j[2])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[2], y=j[2])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[2], y=j[2])


years=[]
annual_APGD_native=[]
annual_APGD_degraded=[]
annual_APGD_downscaled=[]



for m in range (1971, 2020):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.year==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.year==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.year==m).mean().item()
    years.append(m)
    annual_APGD_native.append(native_mean*12)
    annual_APGD_degraded.append(degraded_mean*12)
    annual_APGD_downscaled.append(downscaled_mean*12)



ax3=axs[3]
ax3.plot(years, annual_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax3.plot(years, annual_APGD_downscaled, color="olivedrab", label="DS")
ax3.plot(years, annual_APGD_native, color="cornflowerblue", label="Target")
#ax3.set_xlabel("Month", fontname="Arial", fontsize=14)
ax3.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax3.set_title("d)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax3.text(0.03, 0.9, s="Summit",  transform=ax3.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))


#__________________________________________
APGD_native_gridpoint = APGD_native.isel(x=i[3], y=j[3])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[3], y=j[3])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[3], y=j[3])


years=[]
annual_APGD_native=[]
annual_APGD_degraded=[]
annual_APGD_downscaled=[]



for m in range (1971, 2020):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.year==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.year==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.year==m).mean().item()
    years.append(m)
    annual_APGD_native.append(native_mean*12)
    annual_APGD_degraded.append(degraded_mean*12)
    annual_APGD_downscaled.append(downscaled_mean*12)



ax4=axs[4]
ax4.plot(years, annual_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax4.plot(years, annual_APGD_downscaled, color="olivedrab", label="DS")
ax4.plot(years, annual_APGD_native, color="cornflowerblue", label="Target")
#ax4.set_xlabel("Month", fontname="Arial", fontsize=14)
ax4.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax4.set_title("e)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax4.text(0.03, 0.9, s="Isolated valley",  transform=ax4.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))

#_________________________________________________
APGD_native_gridpoint = APGD_native.isel(x=i[4], y=j[4])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[4], y=j[4])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[4], y=j[4])


years=[]
annual_APGD_native=[]
annual_APGD_degraded=[]
annual_APGD_downscaled=[]



for m in range (1971, 2020):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.year==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.year==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.year==m).mean().item()
    years.append(m)
    annual_APGD_native.append(native_mean*12)
    annual_APGD_degraded.append(degraded_mean*12)
    annual_APGD_downscaled.append(downscaled_mean*12)



ax5=axs[5]
ax5.plot(years, annual_APGD_degraded, color="indianred", label="coarse resolution")
ax5.plot(years, annual_APGD_downscaled, color="olivedrab", label="DS")
ax5.plot(years, annual_APGD_native, color="cornflowerblue", label="Target")
#ax5.set_xlabel("Month", fontname="Arial", fontsize=14)
ax5.set_ylabel("Mean annual precipitation (mm)", fontname="Arial", fontsize=12)
ax5.set_title("f)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax5.text(0.03, 0.9, s="Leeward exposure",  transform=ax5.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))


ax0.legend(fontsize=8, loc='upper right')
ax1.legend(fontsize=8, loc='upper right')
ax2.legend(fontsize=8, loc='upper right')
ax3.legend(fontsize=8, loc='upper right')
ax4.legend(fontsize=8, loc='upper right')
ax5.legend(fontsize=8, loc='upper right')

#fig.suptitle("Mean annual precipitation for different geographic contexts and\ndifferent versions of the APGD over the period 1971-2019", y=0.93)
plt.savefig("/home/jbrenner/These/Resultats/Article/Interannual_variability.png", format="png")
plt.show()
    


#_________________________________________________________________________________________________________________________
#Interannual variability

# plt.figure(figsize=(40,10))

# plt.scatter(APGD_native_gridpoint["time"], APGD_native_gridpoint["pp"], marker="none", label="Observations")
# plt.plot(APGD_native_gridpoint["time"], APGD_native_gridpoint["pp"])

# plt.scatter(APGD_degraded_gridpoint["time"], APGD_degraded_gridpoint["pp"], marker="none", label="Degraded APGD")
# plt.plot(APGD_degraded_gridpoint["time"], APGD_degraded_gridpoint["pp"])

# plt.scatter(APGD_downscaled_gridpoint["time"], APGD_downscaled_gridpoint["PP"], marker="none", label="Downscaled APGD")
# plt.plot(APGD_downscaled_gridpoint["time"], APGD_downscaled_gridpoint["PP"])

# plt.xlabel("time")
# plt.ylabel("Monthly Precipitation (mm)")
# plt.title("Precipitation climatologies at a given gridpoint for the APGD native dataset, the APGD degraded and the APGD downscaled simulations")
# plt.legend()
# plt.show()
