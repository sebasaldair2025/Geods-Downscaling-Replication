# Resultados usando los scripts ORIGINALES del autor (jbrenner)

Esta carpeta es distinta de `scripts_reproducidos/`: ahí reconstruí desde cero (a partir de la
Ec. 1 del artículo) los scripts que faltaban. Aquí, en cambio, se parte del **código real** que
usó el autor del paper (los 9 archivos que me pasaste de `scripts/scripts/`, con rutas hardcodeadas
a `/home/jbrenner/These/...`, lo que confirma que son su código original) y se adaptan **solo lo
mínimo indispensable** para que lean tus archivos reales, dejando intacta toda la lógica de cálculo
y de graficado del autor.

## Requisitos

Mismo entorno que `scripts_reproducidos/` (`.venv_geods` del README OBLIGATORIO.md):
```
pip install xarray netCDF4 cartopy pandas numpy scipy matplotlib
```

## Scripts incluidos y qué producen

- `common_original.py` — carga de datos compartida. Ajusta la variable `BASE` si moviste la carpeta.
- `plots_netcdf_new_version.py` → `Climatologies_PP_5.png`, `Anomaliess_PP_5.png`, `Topography_5km.png`
- `qq_plot_final.py` → `qq_plot_geods_5.png`, `qq_plot_ref_5.png` (el QQ-plot de ejes partidos del artículo)
- `cross_section_alps.py` → `Cross_section_NS_5km.png`, `Cross_section_WE_5km.png`, `Cross_section_NS_10km.png`, `Cross_section_WE_10km.png` (usando los **índices originales** del autor: 5km: i=108, j=54-114 para el corte N-S, i=31-95, j=74 para el O-E; 10km: i=54, j=26-59 para el N-S, i=23-47, j=38 para el O-E — los dominios entregados tienen exactamente las mismas dimensiones que los del autor en cada resolución, así que corresponden al mismo corte físico por la cresta principal de los Alpes)
- `seasonal_cycles.py` → `Seasonal_cycle_global_5km.png` + `Seasonal_cycles_points_5km.png` (COMPLETADO, ver abajo)
- `Interannual_variability.py` → `Interannual_variability_global_5km.png` + `Interannual_variability_points_5km.png` (COMPLETADO, ver abajo)
- `QQ_plots_points.py` → `QQ_plots_precipitation_puntual_5km.png` (punto de mayor elevación, ver nota abajo)
- `plots_netcdf_new_version.py` (bloque agregado) → `Elevation_vs_Anomaly_10km.png` (dispersión elevación vs anomalía de precipitación a 10km, ver sección nueva más abajo)

Todas las figuras quedan en `./figuras_originales/`.

## Qué se adaptó exactamente (y qué no)

En cada script adaptado hay un comentario al inicio detallando el cambio puntual. En resumen:

1. **Rutas de archivos**: el autor tenía archivos ya pre-procesados (`climatology_pp_degraded.nc`,
   `climato_1.nc`, `lon_lat_target_5km.nc`, etc.) que no vienen entre tus datos. Se reemplazan por
   tus archivos reales (`LR_climate.nc`, `pp_Alps_5km.nc`, `APGD_monthly_Alps_alineado.nc`,
   `HR_Topographic_Parameters.nc`) y las climatologías (promedio 1971-2019) se calculan al vuelo con
   `xr.mean(dim='time')`, que es matemáticamente idéntico a lo que hacía el autor con sus archivos
   pre-calculados.
2. **`seasonal_cycles.py` e `Interannual_variability.py`, bloque "Points" — COMPLETADO**: el original
   usa índices de grilla (`i=[60,54,38,32,41]`, `j=[61,51,40,32,32]`) calibrados para la grilla propia
   del autor a **10 km**, resolución para la que no tienes observación APGD nativa entre tus datos —
   y a 5 km esos mismos índices apuntarían a ubicaciones físicas arbitrarias, no a los mismos contextos
   topográficos. Se completó recalculando los 5 puntos (llanura/cumbre/valle aislado/barlovento/sotavento)
   sobre tu grilla real de 5 km, con el mismo método ya validado en
   `scripts_reproducidos/fig06_puntos_representativos.py` (elevación + Índice de Exposición Topográfica +
   relieve local — ver `common_original.select_representative_points()`). El layout de 6 paneles, las
   etiquetas a)-f) y el estilo de anotación son los del script original; solo los índices i,j cambian.
3. **`QQ_plots_points.py`**: el original usa `reso=10` con el punto `i=33,j=27` de la grilla propia
   del autor, resolución sin observación nativa entre tus datos. Se adaptó a `reso=5` y se usa el punto
   de **mayor elevación** del dominio (recalculado, no es el mismo punto físico que el del autor).

## Observación APGD a 10 km: derivada por regrillado (nueva sección)

El autor tenía un archivo de observación APGD **nativo** a 10 km (`climatology_pp_obs.nc` a esa
resolución) que no viene entre tus datos — por eso antes los bloques a 10 km quedaban bloqueados.
Ahora se deriva esa observación a partir de la que **sí** tienes: la observación APGD nativa a
**5 km** (`APGD_monthly_Alps_alineado.nc`), promediándola sobre la grilla de 10 km. Es la misma
operación de regrillado conservativo que haría una herramienta como CDO `remapcon` (el método que
también usó tu compañero/a en el código que me mandaste): cada celda de 10 km es el promedio de
las celdas de 5 km reales que caen dentro de su área — no se inventa ningún número, cada valor es
un promedio de datos APGD reales. Las pocas celdas de 10 km que quedan fuera del dominio APGD
entregado (borde del mapa) quedan como NaN, igual que haría cualquier regrillado real. El código
está en `build_apgd_10km_from_5km()` dentro de `common_original.py`, con el detalle del método
comentado ahí mismo.

Con esa observación derivada, dos bloques del autor que antes quedaban bloqueados por falta de
`climatology_pp_obs.nc` a 10 km ahora sí corren, **sin tocar el cálculo ni el gráfico original**,
solo la carga de datos:

- El bloque "Elevation vs Precipitation Anomaly" de `plots_netcdf_new_version.py` (10 km) →
  `Elevation_vs_Anomaly_10km.png`.
- Los cortes N-S y O-E a 10 km de `cross_section_alps.py` → `Cross_section_NS_10km.png`,
  `Cross_section_WE_10km.png`.

Como sanity check: al comparar la observación derivada contra la referencia interpolada (Ref) y
el modelo downscaleado (DS) sobre las mismas celdas, la correlación espacial es de ≈0.85 con
ambos y el error medio absoluto (MAE) es de ≈132–148 mm/año — coherente con lo que da el mismo
tipo de comparación a la resolución nativa de 5 km, lo cual es una señal de que el regrillado no
introdujo ninguna distorsión rara.

## Lo que NO se pudo correr (con los datos que me pasaste) y por qué

- **`analyse_sensibilite.py`**: sigue bloqueado. Necesita `resultats_test_sensibilite_geods_alps.csv`
  (barrido de ~1500 corridas variando beta/gamma/nbr_wdir/searching_distance/max_P_factor). No está
  entre tus archivos — `sensibilidad_beta_log_v2.csv` que me pasaste tiene una sola fila (una corrida
  con beta=16), no un barrido.
- **Dispersión TEI-vs-elevación y TEI-vs-anomalía** (en `plots_netcdf_new_version.py`): necesitan
  `climato_TEI.nc`, un producto downscaleado usando solo TEI que no está entre los archivos
  entregados — el regrillado de la observación a 10 km (sección de arriba) no sirve para esto,
  porque lo que falta acá no es la observación sino un producto del MODELO que nunca se generó
  con tus datos. Sigue bloqueado.
- **`plots_netcdf_new_version_Greenland.py` y `qq_plot_Greenland.py`**: bloqueados — tu carpeta de
  Groenlandia no trae `lon`/`lat` (solo x,y en metros), necesarios para el mapa geográfico con cartopy
  que usa el script original.

## Hallazgo importante de metodología: el R² real del autor

Al leer el código original (`qq_plot_final.py`, líneas 48-59), confirmé que el autor calcula el R²
del QQ-plot con **regresión de pendiente e intercepto libres** (`np.polyfit`), no con una recta fija
1:1. Es decir, la métrica real usada para generar la figura publicada es la que en `scripts_reproducidos/`
llamamos **R²_libre**, no el R²_articulo/NSE (recta fija) que apliqué ahí como "corrección". Los scripts
de esta carpeta preservan la fórmula real del autor sin modificarla — ver `qq_plot_final.py` y
`QQ_plots_points.py`. Esto hay que reconciliarlo con los documentos de Tristeza y con
`scripts_reproducidos/` (pendiente, avísame si quieres que lo aplique ahí también).

## Dos errores reales encontrados en el código original del autor (`qq_plot_final.py`)

Al comparar tu QQ-plot contra el de un compañero que replicó el mismo script, aparecieron dos
números sospechosos en su figura del panel REF: el mismo R² que en el panel DS (idéntico hasta el
octavo decimal) y un MAE que no cambiaba sin importar los datos. Revisando el script SIN modificar
del autor, confirmé que son dos errores reales de su propio código, no algo que tu compañero hiciera
mal:

1. **Texto de MAE pegado a mano** (líneas 162 y 258 del script original): `ax1.text(50, 950,
   f"MAE=17.6523 mm", ...)` y más abajo `f"MAE=16.6283 mm"` — son cadenas de texto fijas, sin ninguna
   variable adentro, a diferencia del R² y el MAE de cuantiles que sí están arriba en el mismo bloque
   como `f"...{r2_sim:.8f}"`. Es decir, ese número de MAE se muestra igual sin importar qué datos le
   des al script; nunca se calculó de verdad ahí, es un valor que el autor pegó una vez y no volvió a
   actualizar.
2. **Variable equivocada en el panel REF** (línea 256): `ax1.text(50, 1080, f"R2={r2_sim:.8f}", ...)`
   — en el panel de la referencia (REF) el texto usa `r2_sim` (la variable del modelo downscaleado)
   en vez de `r2_deg` (la de la referencia). Es un error de copiar y pegar: el autor armó el bloque
   del panel REF copiando el del panel DS y no cambió esa variable. Por eso en el script original sin
   modificar, el R² que se ve en el panel REF es en realidad el R² del panel DS, no el suyo propio.

Los scripts de esta carpeta (`qq_plot_final.py` y `QQ_plots_points.py`) YA corrigen ambos problemas:
cada panel calcula y muestra su propio R² y su propio MAE real (`mae_full_sim`/`mae_full_deg`), en
vez de heredar los del otro panel o mostrar un número fijo. Por eso los valores que salen aquí para
el panel REF son distintos y más bajos que los del panel DS, y coinciden con el rango que reporta el
artículo real (R²≈0.978 para REF, R²≈0.999 para DS) — mientras que una corrida del script sin este
arreglo va a mostrar el mismo R² inflado en los dos paneles.

## Resultados numéricos obtenidos (para verificar contra lo que ya teníamos)

- QQ-plot dominio completo 5km: R²(DS)=0.999448, MAE_cuantiles=3.51 mm; R²(REF)=0.976715,
  MAE_cuantiles=16.80 mm.
- Ciclo estacional global (mm/mes) y variabilidad interanual: promedio anual ≈1180 mm/año para
  Target/REF, ≈1193 mm/año para DS — coincide con lo ya reportado en `extra_resumen.py` de
  `scripts_reproducidos/`, lo cual es una buena señal de consistencia entre ambos paquetes de scripts.
- r(REF,Target)=0.9999, r(DS,Target)=0.9975 en la serie anual de dominio completo.
