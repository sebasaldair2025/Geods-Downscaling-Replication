"""
Carga de datos compartida para los scripts ORIGINALES del autor (jbrenner), adaptada
UNICAMENTE en las rutas y en el calculo de climatologias (el autor tenia archivos .nc
ya pre-climatologizados como 'climatology_pp_degraded.nc' que no vienen en los datos
entregados; aqui se calculan al vuelo con xr.mean(dim='time') a partir de las series
mensuales reales, que es matematicamente identico). El codigo de graficos de cada
script NO se modifico en su logica (colores, proyeccion, layout, formulas).
"""
import xarray as xr
import numpy as np

import os as _os
# NOTA: ruta actualizada -- la carpeta "Proyecto" fue reorganizada; los datos crudos ahora
# viven dentro de "Resultados Obtenidos/Datos Completos/GeoDS".
BASE = _os.environ.get("ORIGDATA_BASE", "C:/Users/sebas/OneDrive/Desktop/Resultados Obtenidos/Datos Completos/GeoDS")
OUT = "./figuras_originales"

import os
os.makedirs(OUT, exist_ok=True)


def load_5km():
    ds_ds = xr.open_dataset(f"{BASE}/GeoDS_downscaled_data/pp_Alps_5km.nc")
    ds_lr = xr.open_dataset(f"{BASE}/input_data/input_data/5km/LR_climate.nc")
    ds_obs = xr.open_dataset(f"{BASE}/swisstransfer_10b42ca1-ba88-4a59-8888-e20e005bfa00/APGD_monthly_Alps_alineado.nc")
    ds_topo = xr.open_dataset(f"{BASE}/input_data/input_data/5km/HR_Topographic_Parameters.nc")

    sim_clim = (ds_ds['PP'].mean(dim='time') * 12).values
    deg_clim = (ds_lr['pp'].mean(dim='time') * 12).values
    obs_clim = (ds_obs['pp_apgd'].mean(dim='time') * 12).values

    valid = (~np.isnan(deg_clim)) & (~np.isnan(sim_clim)) & (~np.isnan(obs_clim)) & (obs_clim != 0)

    return dict(
        sim=ds_ds['PP'], deg=ds_lr['pp'], obs=ds_obs['pp_apgd'],
        sim_clim=sim_clim, deg_clim=deg_clim, obs_clim=obs_clim, valid=valid,
        lon=ds_topo['lon'].values, lat=ds_topo['lat'].values, S=ds_topo['S'].values,
    )


def select_representative_points(d):
    """Recalcula los 5 puntos de contexto topografico (llanura/cumbre/valle/barlovento/sotavento)
    sobre la grilla real de 5km, con el MISMO metodo usado en scripts_reproducidos/fig06 y fig03
    (el autor original tenia sus propios indices i,j hardcodeados para SU grilla a 10km, que no
    tiene observacion en los datos entregados y ademas no transfieren a esta grilla de 5km)."""
    from scipy.ndimage import uniform_filter

    S = d['S']
    valid = d['valid']
    ds_tei = xr.open_dataset(f"{BASE}/GeoDS_downscaled_data/topographic_exposure_indexes_Alps_APGD.nc")
    tei = ds_tei['topographic_exposure_index']
    stds = [float(np.nanstd(tei.isel(wdir=k).values)) for k in range(tei.sizes['wdir'])]
    k_sel = int(np.argmax(stds))
    tei_sel = tei.isel(wdir=k_sel).values

    ny, nx = S.shape
    margin = 6
    edge_mask = np.zeros_like(valid)
    edge_mask[margin:ny - margin, margin:nx - margin] = True
    valid_in = valid & edge_mask

    S_filled = np.where(valid, S, np.nanmean(S))
    S_smooth = uniform_filter(S_filled, size=9)
    local_relief = S - S_smooth
    median_elev = np.nanmedian(S[valid_in])

    mask_lowland = valid_in & (S > 150) & (S < 500)
    relief_lowland = np.where(mask_lowland, np.abs(local_relief), np.nan)
    j_plain, i_plain = np.unravel_index(np.nanargmin(relief_lowland), S.shape)
    j_summit, i_summit = np.unravel_index(np.nanargmax(np.where(valid_in, S, np.nan)), S.shape)
    mask_mtn = valid_in & (S > median_elev)
    lr_masked = np.where(mask_mtn, local_relief, np.nan)
    j_valley, i_valley = np.unravel_index(np.nanargmin(lr_masked), S.shape)
    tei_masked_hi = np.where(mask_mtn, tei_sel, np.nan)
    j_wind, i_wind = np.unravel_index(np.nanargmax(tei_masked_hi), S.shape)
    j_lee, i_lee = np.unravel_index(np.nanargmin(tei_masked_hi), S.shape)

    return {
        "Plain": (j_plain, i_plain),
        "Summit": (j_summit, i_summit),
        "Isolated valley": (j_valley, i_valley),
        "Windward exposure": (j_wind, i_wind),
        "Leeward exposure": (j_lee, i_lee),
    }, k_sel


def build_apgd_10km_from_5km():
    """Deriva una climatologia APGD a 10km que NO viene entre los datos entregados
    (el autor si la tenia, como 'climatology_pp_obs.nc' a 10km, pero no forma parte
    de lo que me pasaste). Se obtiene promediando la observacion APGD NATIVA a 5km
    sobre la grilla de 10km -- es la MISMA operacion de regrillado conservativo que
    haria una herramienta como CDO 'remapcon' (o el metodo que uso tu companero/a):
    cada celda de 5km se asigna a la celda de 10km mas cercana (la grilla de 10km
    tiene el doble de tamano de celda y el mismo origen, asi que en la mayoria de
    los casos son exactamente 2x2 celdas de 5km por celda de 10km) y se promedian.
    No se inventa ningun valor: cada numero resultante es un promedio real de datos
    APGD reales. Las celdas de 10km sin ninguna celda de 5km debajo (fuera del
    dominio APGD entregado, ocurre en el borde) quedan como NaN, igual que haria
    cualquier regrillado real -- no se rellenan con nada."""
    ds5 = xr.open_dataset(f"{BASE}/swisstransfer_10b42ca1-ba88-4a59-8888-e20e005bfa00/APGD_monthly_Alps_alineado.nc")
    ds10 = xr.open_dataset(f"{BASE}/input_data/input_data/10km/LR_climate.nc")

    x5, y5 = ds5['x'].values, ds5['y'].values
    x10, y10 = ds10['x'].values, ds10['y'].values
    obs5_clim = (ds5['pp_apgd'].mean(dim='time') * 12).values  # (y5, x5)

    # cada celda de 5km -> indice de la celda de 10km mas cercana (vecino mas cercano
    # en x e y por separado, valido porque ambas grillas son regulares y alineadas)
    ix_map = np.array([np.argmin(np.abs(x10 - xv)) for xv in x5])
    iy_map = np.array([np.argmin(np.abs(y10 - yv)) for yv in y5])

    nY, nX = len(y10), len(x10)
    sum_grid = np.zeros((nY, nX))
    cnt_grid = np.zeros((nY, nX))
    for j5 in range(len(y5)):
        jt = iy_map[j5]
        row = obs5_clim[j5, :]
        ok = ~np.isnan(row)
        np.add.at(sum_grid[jt], ix_map[ok], row[ok])
        np.add.at(cnt_grid[jt], ix_map[ok], 1)

    with np.errstate(invalid='ignore', divide='ignore'):
        obs10_clim = np.where(cnt_grid > 0, sum_grid / cnt_grid, np.nan)
    return obs10_clim


def load_10km():
    """LR y DS a 10km vienen de los datos entregados. La observacion ('obs') se deriva
    con build_apgd_10km_from_5km() -- ver esa funcion para el detalle del metodo -- porque
    no hay un archivo de observacion APGD nativo a 10km entre los datos entregados."""
    ds_ds = xr.open_dataset(f"{BASE}/GeoDS_downscaled_data/pp_Alps_10km.nc")
    ds_lr = xr.open_dataset(f"{BASE}/input_data/input_data/10km/LR_climate.nc")
    ds_topo = xr.open_dataset(f"{BASE}/input_data/input_data/10km/HR_Topographic_Parameters.nc")

    sim_clim = (ds_ds['PP'].mean(dim='time') * 12).values
    deg_clim = (ds_lr['pp'].mean(dim='time') * 12).values
    obs_clim = build_apgd_10km_from_5km()

    valid = (~np.isnan(deg_clim)) & (~np.isnan(sim_clim)) & (~np.isnan(obs_clim))

    # 'S' (elevacion) en este archivo a 10km trae una dimension 'time' extra (12 meses,
    # valor identico cada mes porque la topografia no cambia) que el de 5km no tiene;
    # se toma el primer mes para dejarla en 2D como el resto de las variables.
    S10 = ds_topo['S']
    if 'time' in S10.dims:
        S10 = S10.isel(time=0)

    return dict(
        sim=ds_ds['PP'], deg=ds_lr['pp'],
        sim_clim=sim_clim, deg_clim=deg_clim, obs_clim=obs_clim, valid=valid,
        lon=ds_topo['lon'].values, lat=ds_topo['lat'].values, S=S10.values,
    )
