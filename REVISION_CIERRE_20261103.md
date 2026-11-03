# Ajustes de cierre · 3 de noviembre de 2026

- Se retiró del visor la capa de trazados hidrográficos auxiliares y su referencia.
- La depuración opera por partes de geometría: se mantienen las 28 exclusiones de la revisión anterior y se seleccionan otros 21 tramos aislados, incluidos fragmentos sin enlace al dibujo principal en el corredor del río Negro. El CSV `data/depuracion_corrientes_20261103.csv` identifica las 49 partes excluidas. Se conservan los originales y las coordenadas suavizadas de los tramos retenidos. Esta selección de representación no redefine la red hidrográfica oficial.
- Se recortó la representación departamental y sus máscaras de rótulos por el límite provincial, incluido el exceso al norte de Bariloche. Los datos censales, productivos y los cálculos mantienen las geometrías analíticas originales.
- Se alineó la franja costera del dibujo de San Antonio Oeste con la misma línea de costa del visor. Se conservaron atributos, límites interiores y resultados de intersección; la ampliación de dibujo no constituye una delimitación administrativa nueva.
- Diques, muros de embalse, embalses y superficies de agua muestran el nombre al pasar el cursor, sin ventana al hacer clic.
- Se amplió el espaciado provincial condicionado al espacio disponible dentro del polígono. Se mantienen las reglas de tipografía departamental.
- En Asentamientos se retiraron los botones Contexto provincial y Cercanía al VMOS y se dejó una única zona desplazable en el selector de capas.
- Se aplicaron las eliminaciones y sustituciones de fuentes y aclaraciones sobre la numeración de la versión recibida. El texto común de infraestructura reemplaza el párrafo ferroviario en Producción, Electricidad, Asentamientos y Síntesis.
- Los logos y la presentación institucional aprobados se conservan.

## Uso

Extraer todo el ZIP y abrir `Tablero_Rio_Negro.html` conservando junto a él su carpeta de recursos y `assets`. Para editar o recompilar, usar `Tablero_Rio_Negro.Rmd` desde esta carpeta y `Compilar_tablero.R`. El Rmd separado requiere también los datos y recursos incluidos en el ZIP.

La generación HTML usa recursos adjuntos y cálculo/conversión en procesos separados para reducir la memoria requerida por Pandoc. Los fondos ArgenMap requieren conexión al servicio del IGN.

## Verificación de la entrega

HTML compilado con R y Pandoc en procesos separados. Diez pestañas revisadas en Chromium, sin errores de JavaScript ni recursos locales faltantes. Se verificaron 30 logos, 156 posiciones de rótulos, una única zona desplazable en el selector de Asentamientos y ausencia de ventanas al hacer clic en las capas de agua, diques y muros. Los 13 departamentos no presentan superficie exterior a la máscara provincial; la costa de San Antonio Oeste coincide con el contorno visible en el sector indicado y no introduce solapamientos nuevos con otros municipios. No se ejecutó en el equipo Windows del autor.
