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



months=[]
monthly_APGD_native=[]
monthly_APGD_degraded=[]
monthly_APGD_downscaled=[]



for m in range (1, 13):
    native_mean = APGD_native['pp'].where(APGD_native["time"].dt.month==m).mean().item()
    degraded_mean = APGD_degraded['pp'].where(APGD_degraded["time"].dt.month==m).mean().item()
    downscaled_mean = APGD_downscaled['PP'].where(APGD_downscaled["time"].dt.month==m).mean().item()
    months.append(m)
    monthly_APGD_native.append(native_mean)
    monthly_APGD_degraded.append(degraded_mean)
    monthly_APGD_downscaled.append(downscaled_mean)
    
    
    
fig, ax1 = plt.subplots()
ax1.plot(months, monthly_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax1.plot(months, monthly_APGD_downscaled, color="olivedrab", label="DS")
ax1.plot(months, monthly_APGD_native, color="cornflowerblue", label="Target")
#ax1.set_xlabel("Month", fontname="Arial", fontsize=14)
ax1.set_ylabel("Mean monthly precipitation (mm)", fontname="Arial", fontsize=14)
#ax1.set_title("a)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
#ax1.text(0.03, 0.9, s="Global seasonal cycle",  transform=ax1.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         #bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))
plt.legend(fontsize=8, loc="upper left")
plt.title("Global seasonal cycle")
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


#plaine, windward, sommet, vallée isolée, leeward=près du LM où je suis particulièrement mauvais
i=[60, 54, 38, 32, 41] #30]
j=[61, 51, 40, 32, 32] #46]

#________________________________________________________________________________________________________________________
#seasonal cycles


APGD_native_gridpoint = APGD_native.isel(x=i[0], y=j[0])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[0], y=j[0])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[0], y=j[0])

months=[]
monthly_APGD_native=[]
monthly_APGD_degraded=[]
monthly_APGD_downscaled=[]

for m in range (1, 13):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.month==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.month==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.month==m).mean().item()
    months.append(m)
    monthly_APGD_native.append(native_mean)
    monthly_APGD_degraded.append(degraded_mean)
    monthly_APGD_downscaled.append(downscaled_mean)
    
    
    
fig, axs = plt.subplots(3,2,figsize=(18,12))
ax1=axs[0,1]
ax1.plot(months, monthly_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax1.plot(months, monthly_APGD_downscaled, color="olivedrab", label="DS")
ax1.plot(months, monthly_APGD_native, color="cornflowerblue", label="Target")
#ax1.set_xlabel("Month", fontname="Arial", fontsize=14)
ax1.set_ylabel("Mean monthly precipitation (mm)", fontname="Arial", fontsize=14)
ax1.set_title("b)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax1.text(0.03, 0.9, s="Plain",  transform=ax1.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))

months=[]
monthly_APGD_native=[]
monthly_APGD_degraded=[]
monthly_APGD_downscaled=[]

APGD_native_gridpoint = APGD_native.isel(x=i[1], y=j[1])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[1], y=j[1])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[1], y=j[1])

for m in range (1, 13):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.month==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.month==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.month==m).mean().item()
    months.append(m)
    monthly_APGD_native.append(native_mean)
    monthly_APGD_degraded.append(degraded_mean)
    monthly_APGD_downscaled.append(downscaled_mean)
    
    
ax2=axs[2,0]
ax2.plot(months, monthly_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax2.plot(months, monthly_APGD_downscaled, color="olivedrab", label="DS")
ax2.plot(months, monthly_APGD_native, color="cornflowerblue", label="Target")
#ax2.set_xlabel("Month", fontname="Arial", fontsize=14)
ax2.set_ylabel("Mean monthly precipitation (mm)", fontname="Arial", fontsize=14)
ax2.set_title("e)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax2.text(0.03, 0.9, s="Windward exposure",  transform=ax2.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))



months=[]
monthly_APGD_native=[]
monthly_APGD_degraded=[]
monthly_APGD_downscaled=[]

APGD_native_gridpoint = APGD_native.isel(x=i[2], y=j[2])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[2], y=j[2])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[2], y=j[2])

for m in range (1, 13):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.month==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.month==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.month==m).mean().item()
    months.append(m)
    monthly_APGD_native.append(native_mean)
    monthly_APGD_degraded.append(degraded_mean)
    monthly_APGD_downscaled.append(downscaled_mean)
    
    
ax3=axs[1,0]
ax3.plot(months, monthly_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax3.plot(months, monthly_APGD_downscaled, color="olivedrab", label="DS")
ax3.plot(months, monthly_APGD_native, color="cornflowerblue", label="Target")
#ax3.set_xlabel("Month", fontname="Arial", fontsize=14)
ax3.set_ylabel("Mean monthly precipitation (mm)", fontname="Arial", fontsize=14)
ax3.set_title("b)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax3.text(0.03, 0.9, s="Summit",  transform=ax3.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))



months=[]
monthly_APGD_native=[]
monthly_APGD_degraded=[]
monthly_APGD_downscaled=[]

APGD_native_gridpoint = APGD_native.isel(x=i[3], y=j[3])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[3], y=j[3])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[3], y=j[3])

for m in range (1, 13):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.month==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.month==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.month==m).mean().item()
    months.append(m)
    monthly_APGD_native.append(native_mean)
    monthly_APGD_degraded.append(degraded_mean)
    monthly_APGD_downscaled.append(downscaled_mean)
    
    
ax4=axs[1,1]
ax4.plot(months, monthly_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax4.plot(months, monthly_APGD_downscaled, color="olivedrab", label="DS")
ax4.plot(months, monthly_APGD_native, color="cornflowerblue", label="Target")
ax4.set_xlabel("Month", fontname="Arial", fontsize=14)
ax4.set_ylabel("Mean monthly precipitation (mm)", fontname="Arial", fontsize=14)
ax4.set_title("d)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax4.text(0.03, 0.9, s="Isolated valley",  transform=ax4.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))


months=[]
monthly_APGD_native=[]
monthly_APGD_degraded=[]
monthly_APGD_downscaled=[]

APGD_native_gridpoint = APGD_native.isel(x=i[4], y=j[4])
APGD_degraded_gridpoint = APGD_degraded.isel(x=i[4], y=j[4])
APGD_downscaled_gridpoint = APGD_downscaled.isel(x=i[4], y=j[4])

for m in range (1, 13):
    native_mean = APGD_native_gridpoint['pp'].where(APGD_native_gridpoint["time"].dt.month==m).mean().item()
    degraded_mean = APGD_degraded_gridpoint['pp'].where(APGD_degraded_gridpoint["time"].dt.month==m).mean().item()
    downscaled_mean = APGD_downscaled_gridpoint['PP'].where(APGD_downscaled_gridpoint["time"].dt.month==m).mean().item()
    months.append(m)
    monthly_APGD_native.append(native_mean)
    monthly_APGD_degraded.append(degraded_mean)
    monthly_APGD_downscaled.append(downscaled_mean)

ax5=axs[2,1]
ax5.plot(months, monthly_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax5.plot(months, monthly_APGD_downscaled, color="olivedrab", label="DS")
ax5.plot(months, monthly_APGD_native, color="cornflowerblue", label="Target")
ax5.set_xlabel("Month", fontname="Arial", fontsize=14)
ax5.set_ylabel("Mean monthly precipitation (mm)", fontname="Arial", fontsize=14)
ax5.set_title("f)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax5.text(0.03, 0.9, s="Leeward exposure",  transform=ax5.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))


months=[]
monthly_APGD_native=[]
monthly_APGD_degraded=[]
monthly_APGD_downscaled=[]



for m in range (1, 13):
    native_mean = APGD_native['pp'].where(APGD_native["time"].dt.month==m).mean().item()
    degraded_mean = APGD_degraded['pp'].where(APGD_degraded["time"].dt.month==m).mean().item()
    downscaled_mean = APGD_downscaled['PP'].where(APGD_downscaled["time"].dt.month==m).mean().item()
    months.append(m)
    monthly_APGD_native.append(native_mean)
    monthly_APGD_degraded.append(degraded_mean)
    monthly_APGD_downscaled.append(downscaled_mean)

ax6=axs[0,0]
ax6.plot(months, monthly_APGD_degraded, color="indianred", label=r"Ref$_{interpolated}$")
ax6.plot(months, monthly_APGD_downscaled, color="olivedrab", label="DS")
ax6.plot(months, monthly_APGD_native, color="cornflowerblue", label="Target")
ax6.set_xlabel("Month", fontname="Arial", fontsize=14)
ax6.set_ylabel("Mean monthly precipitation (mm)", fontname="Arial", fontsize=14)
ax6.set_title("a)", fontname="Arial", fontsize=14, loc="left", y=0, pad=-30)
ax6.text(0.03, 0.9, s="Global",  transform=ax6.transAxes, ha='left', fontsize=12, fontname="Arial", fontstyle="italic",
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='square,pad=0.3'))
    



ax1.legend(fontsize=7, loc='upper right')
ax2.legend(fontsize=7, loc='upper right')
ax3.legend(fontsize=7, loc='upper right')
ax4.legend(fontsize=7, loc='upper right')
ax5.legend(fontsize=7, loc='upper right')
ax6.legend(fontsize=7, loc='upper right')

fig.suptitle("Average seasonal cycles for different geographic contexts and\ndifferent versions of the APGD over the period 1971-2019", y=0.93)
#plt.savefig("/home/jbrenner/These/Resultats/Article/Various_topographic_context.png", format="png")
plt.savefig(f'/home/jbrenner/These/Resultats/Article/Seasonal_cycles_{reso}.png', format='png')
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
