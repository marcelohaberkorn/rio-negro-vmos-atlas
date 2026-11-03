# Historial de versiones

## 2026-11-03 · Revisión de cierre publicada

Actualiza la edición publicada el 26 de octubre de 2026 con la última entrega aprobada por el autor.

### Presentación y cartografía

- Logos UNS, DGyT y CDC actualizados; crédito “Cartografía elaborada por: Marcelo Haberkorn” y año 2026. Se incluyen los recursos vectoriales y sus originales editables.
- Proyección acimutal equiárea de Lambert en la vista bicontinental, con orientación geográfica dinámica.
- Rotulación adaptada al polígono y a la escala, con mayor separación entre letras y palabras en provincias y departamentos.
- Recorte cartográfico de los 13 departamentos por la máscara provincial, corrigiendo el exceso al norte de Bariloche.
- Alineación de la franja costera representada de San Antonio Oeste con la misma línea de costa del visor, sin nuevos solapamientos municipales.

### Hidrografía e infraestructura

- Suavizado local de cursos de agua que conserva extremos y nodos; desplazamiento máximo observado de 65,884 m respecto del original. Los originales se mantienen para análisis.
- Selección por partes de geometría: 49 partes excluidas del dibujo, incluidas las 28 exclusiones de la revisión anterior y 21 nuevas. Los criterios y registros están en `data/depuracion_corrientes_20261103.csv`; la selección no redefine la red oficial ni demuestra inexistencia de los cursos.
- Retiro completo del selector y de las referencias de la capa de trazados hidrográficos auxiliares.
- Incorporación de ferrocarriles y estaciones del IGN como contexto de conectividad; cuatro estaciones con información contrastada con Tren Patagónico y popup. Los demás registros conservan etiqueta y símbolo.
- Incorporación de diques y muros de embalse; consulta por nombre al pasar el cursor, sin ventana al hacer clic. El mismo comportamiento se aplica a embalses y superficies de agua.
- Dos balsas: Sauce Blanco y Villa Llanquín. Giro de 90° del signo de Sauce Blanco; fuente Vialidad Rionegrina y posiciones documentadas.

### Información temática y uso

- Clasificación común de NBI total 2010 y 2022: cuatro intervalos iguales de cinco puntos porcentuales y la misma paleta. Los componentes NBI corresponden al Censo 2022.
- Población validada en viviendas particulares: 747.697 personas; población total provincial: 750.768. Se identifican los universos y la desagregación urbana/rural.
- Producción ovina 2022 y bovina 2021 identificada como existencias en cabezas. `PerMan_18` representa superficie conjunta de peras y manzanas 2018 en hectáreas, con fuente documental.
- Síntesis con mapa integrado, análisis y conclusiones, explicitando límites de las inferencias territoriales.
- Asentamientos: menú con una sola zona desplazable y retiro de los botones Contexto provincial y Cercanía al VMOS.
- Fuentes y aclaraciones revisadas por pestaña; preservación de cifras, tablas analíticas y geometrías originales frente a los ajustes de dibujo.

### Reproducción y publicación

- Se actualizan el Rmd, HTML, datos, scripts, recursos institucionales, copias visuales y controles.
- `Compilar_tablero.R` separa cálculo de R y conversión de Pandoc para reducir el pico de memoria. La salida usa recursos adjuntos (`self_contained: false`).
- `docs/index.html` reproduce la salida aprobada con los diez bloques de datos cartográficos en scripts externos. `Publicar_tablero.py` conserva el texto de cada bloque y archiva el HTML original, sin cambios, en `distribucion/Tablero_Rio_Negro.html.gz`. Esta preparación permite publicar sin superar el límite de 16 MiB por solicitud de la conexión de GitHub. GitHub Pages conserva su URL: https://marcelohaberkorn.github.io/rio-negro-vmos-atlas/
- La publicación incluye un identificador de versión en `docs/version.json` para comprobar qué edición se está sirviendo, sin modificar el tablero.

### Validación previa a publicar

- Compilación finalizada con R y Pandoc en procesos separados.
- Diez pestañas revisadas en Chromium, sin errores JavaScript ni recursos locales faltantes; 30 logos cargados.
- 156 posiciones de rótulos verificadas dentro de su polígono y del visor.
- Un solo desplazamiento en el selector de Asentamientos; agua y diques sin popups al hacer clic.
- Sin superficie departamental fuera de la máscara provincial; coincidencia del contorno costero de San Antonio Oeste en el sector solicitado y ausencia de nuevos solapamientos municipales.
- No se ejecutó la compilación en el equipo Windows del autor. Los fondos ArgenMap requieren conexión al IGN.

## 2026-10-26 · Publicación anterior

Primera versión del atlas y su sitio GitHub Pages en `main:/docs`. La revisión del README y los archivos publicados se conservan en el historial de Git.
