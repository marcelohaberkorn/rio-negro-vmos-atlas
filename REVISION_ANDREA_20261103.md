> Registro histórico de una revisión intermedia. La versión vigente está documentada en [REVISION_CIERRE_20261103.md](REVISION_CIERRE_20261103.md).

# Revisión del 3 de noviembre de 2026

Se conservan los logos y la composición institucional aprobados. Se aplican estas correcciones:

- **Sauce Blanco:** el signo del punto gira 90° para que la línea discontinua quede aproximadamente perpendicular al curso. La referencia mantiene el signo habitual sin giro. Se retiran del popup el renglón de río/localidad solicitado y la atribución de las coordenadas. Villa Llanquín conserva su orientación y su identificación hidrográfica. Las posiciones no cambian.
- **Estaciones:** sólo las cuatro contrastadas con la página del Tren Patagónico tienen popup. Cada uno contiene el nombre de la estación, la dirección y el enlace sobre “Tren Patagónico”. Los otros registros conservan su símbolo y etiqueta al pasar el cursor, sin ventana al hacer clic. Se retiran los textos técnicos solicitados de los popups y la fecha de consulta de esa referencia visible.
- **Fuentes de balsas:** se retira del tablero la frase de atribución de las coordenadas. La procedencia de los datos queda registrada en los archivos de respaldo.
- **Provincias:** se amplían interletrado y separación entre palabras, de manera adaptativa según el espacio disponible y el zoom. No se alteran las reglas de los departamentos. Las cajas de texto deben caber dentro del polígono y evitar controles y otros rótulos.

## Hidrografía

Las capturas señalan problemas distintos: trazados auxiliares en la fuente y una digitalización con pocos vértices en algunos meandros. Aumentar la cantidad de vértices por sí solo no elimina esos quiebres; se redondean las esquinas con curvas locales.

El suavizado conserva los extremos y los vértices de conexión entre tramos y queda limitado a un desplazamiento de dibujo de 80 m. El máximo efectivamente observado es **65,884 m**. No se introducen nuevas autointersecciones en geometrías originalmente simples. Los originales de análisis se conservan íntegros; no se ajustan las coordenadas al mapa base. Las superficies de agua y sus orillas mantienen la representación aprobada.

En los sectores revisados de General Roca y Choele Choel se separan **28 registros cerrados, sin denominación o muy pequeños y aislados** de la representación principal. Entre ellos hay un segmento de 75,56 m cuyos extremos no conectan a otros trazados principales dentro de una tolerancia de 5 m. Permanecen disponibles como **“Trazados hidrográficos auxiliares”**, desactivados al inicio en Ambiente y Asentamientos. Este tratamiento responde a una revisión cartográfica: no demuestra que esos cursos sean inexistentes, estén secos o sean artificiales. La ausencia de una línea en un mapa base no constituye por sí sola una verificación hidrográfica.

Se mantienen los brazos identificados. En particular, El Salado cuenta con documentación del [Gobierno de Río Negro sobre el paseo costero de Choele Choel](https://parqueindustrialcatriel.rionegro.gov.ar/articulo/38515/choele-choel-inicio-la-primera-etapa-de-obras-del-paseo-costero). Esto respalda conservar ese brazo, aunque no valida la precisión de cada vértice de la capa.

El detalle de registros y motivos está en `data/revision_hidrografia_20261103.csv`. Los controles geométricos y de representación se registran en `revision_cartografica_20261103.json`. `Preparar_hidrografia.py` permite reproducir el procesamiento con numpy, shapely y pyproj; no hace falta ejecutarlo para compilar el Rmd.

## Abrir el trabajo

Extraer todo el ZIP y abrir `entrega_rio_negro/Tablero_Rio_Negro.html`. Mantener junto al HTML las carpetas `Tablero_Rio_Negro_files` y `assets`. Para editar, conservar también `data`, el Rmd y el script de compilación. El fondo ArgenMap necesita conexión.
