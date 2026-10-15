# Geods-Downscaling-Replication

Replicación del modelo de downscaling de precipitación **GeoDS** (Brenner et al.), basado en el índice de exposición topográfica (TEI). Incluye climatología, mapas de anomalía y validación mediante diagramas cuantil-cuantil, aplicados a los Alpes (dominio de calibración, con observaciones APGD) y a Groenlandia (prueba de generalización a una topografía distinta).

## Qué hicimos

Este repositorio replica tres piezas clave del artículo original de GeoDS:

- **Climatología y anomalías (Alpes)** — comparación espacial entre el dato interpolado (REF), la salida downscaleada del modelo (DS) y las observaciones reales (APGD).
- **Validación cuantil-cuantil (QQ-plot)** — compara la distribución estadística completa de REF y DS contra las observaciones, con R² y MAE como métricas de ajuste.
- **Generalización a Groenlandia** — se aplicó la misma lógica a un dominio con topografía completamente distinta (hielo/glaciares en vez de montaña). Al adaptar el script original se encontraron y resolvieron dos problemas reales de los datos entregados: las rutas de archivos precalculados del autor no existían (se recalculó la climatología directamente de los datos crudos) y el dominio de Groenlandia no traía coordenadas lon/lat explícitas (se derivaron con `pyproj` a partir de la proyección incluida en los archivos). Groenlandia tampoco cuenta con un dataset de observaciones, por lo que ahí la comparación se hace entre REF y DS, no contra observaciones.

## Autor

**Sebastián Chancusig** — estudiante de Ingeniería Civil, quinto semestre, Escuela Politécnica Nacional (EPN). Proyecto desarrollado en el marco de una pasantía preprofesional.

## Créditos

- **Ing. Marcos Villacís Erazo, PhD** — tutor de la pasantía, Profesor Titular, Facultad de Ingeniería Civil y Ambiental (FICA), Escuela Politécnica Nacional. Por la oportunidad y la guía durante el desarrollo del proyecto.
- **Brenner et al.** — autores del modelo GeoDS original y del artículo publicado en *Geoscientific Model Development*, en el que se basa esta replicación.

## Estructura del repositorio

- `Scripts Originales/` — los tres scripts principales replicados
- `Scripts de Apoyo/` — scripts auxiliares del modelo
- `Figuras Originales/` — figuras generadas (climatología, anomalías, QQ-plot)
- `Guías de Interpretación/` — documentación de apoyo (bitácora, glosario de variables, guía de figuras)
