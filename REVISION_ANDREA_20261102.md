> Registro histórico de una revisión intermedia. La versión vigente está documentada en [REVISION_CIERRE_20261103.md](REVISION_CIERRE_20261103.md).

# Revisión cartográfica · 2 de noviembre de 2026

Esta entrega incorpora las correcciones de Andrea, los nuevos logos y las dos balsas georreferenciadas. Incluye el HTML compilado y los recursos necesarios para editarlo desde el Rmd.

## Cambios incorporados

- Hidrografía: se recuperó el detalle de los originales, sustituyendo la generalización anterior de 90 m por una simplificación de 5 m para dibujo. Se redondearon localmente los quiebres de las líneas, conservando sus extremos. El desplazamiento máximo comprobado respecto de los originales es menor de 8 m; las geometrías resultantes son válidas. Los cálculos siguen utilizando los originales.
- Rotulación: provincias y departamentos ajustan ubicación, tamaño, interletrado, separación entre palabras y saltos de línea al espacio visible dentro de sus polígonos. Se evitan controles y otros rótulos; los nombres sin espacio suficiente se omiten hasta un acercamiento adecuado. Se conserva la proyección de Lambert y el norte geográfico dinámico de la presentación.
- Infraestructura: se incorporaron las trazas ferroviarias, estaciones, diques y muros de embalse disponibles en el WFS del IGN. Se conservan las descargas originales y sus enlaces de consulta en `data/originales` y `data/fuentes_infraestructura_IGN_20261102.json`.

| Capa | Asentamientos | Producción | Síntesis | Ambiente | Electricidad |
|---|---|---|---|---|---|
| Ferrocarriles | Visible al inicio | Opcional | Opcional | — | — |
| Estaciones ferroviarias | Activada; signos desde zoom 8 | Opcional; signos desde zoom 8 | Opcional; signos desde zoom 8 | — | — |
| Diques y muros de embalse | Opcional | Opcional | Opcional | Opcional | Opcional |
| Balsas | Visible al inicio | — | Visible al inicio | Visible al inicio | — |

La red ferroviaria aporta contexto de conectividad y articulación productiva. Los diques ayudan a interpretar obras hidráulicas y generación eléctrica. Se evita sumar estas capas a mapas sociales o administrativos donde competirían con la temática sin aportar una lectura directa.

Las estaciones son registros cartográficos, no un inventario validado de paradas actuales. Los atributos disponibles no se interpretan como garantía de servicio vigente, trocha o cantidad de vías. Las estructuras compartidas con provincias vecinas se mantienen como contexto de borde: el recorte incluye elementos situados hasta 500 m del límite. Las trazas ferroviarias se recortan con un margen de 30 m.

## Criterios del IGN

Se consultaron el [Manual de signos cartográficos 2010](https://www.ign.gob.ar/archivos/cartografia/manual_de_signos_cartograficos_2010.pdf) y sus [modificaciones de 2015](https://www.ign.gob.ar/archivos/cartografia/modificaciones_al_manual_de_signos_cartograficos_2015.pdf).

- El manual utiliza **corriente de agua perenne**. No corresponde reemplazarla por “permanente” atribuyendo ese cambio al manual.
- Se diferencia la corriente lineal de las superficies de agua perennes y de los embalses. La categoría areal se mantiene general porque la capa incluye superficies de cauces y no sería correcto denominar a todas “lagos y lagunas”. Embalse y obra de cierre no son sinónimos.
- El eje ferroviario y la estación toman como referencia los signos 52 y 59 (pp. 127 y 129), adaptados a pantalla. El rectángulo de estación se orienta según la traza próxima cuando ésta puede vincularse geométricamente. El signo no codifica número de vías ni trocha.
- El signo puntual de dique o represa toma como referencia el 123 (p. 145). Los muros se muestran por su trazado IGN. No se infieren carreteras sobre la coronación ni funcionamiento hidráulico.
- Para balsas de maroma, el referente es el signo 72 (p. 132). No se agregaron puntos sin ubicación verificable.

Los signos en píxeles y los tamaños variables son adaptaciones para un visor con zoom continuo; no equivalen a reproducir literalmente las dimensiones impresas en milímetros para una única escala.

## Logos y presentación

Los mapas utilizan los tres nuevos logos completos de UNS, DGyT y CDC, sin los recortes de la versión anterior. La presentación utiliza la plantilla SVG recibida, con **“Cartografía elaborada por: Marcelo Haberkorn”** y **2026**. Se conserva el crédito docente de Lic. Andrea Marcela Silva. La imagen se ubica después del subtítulo y antes del texto explicativo, para que quede completa a la vista al ingresar a la presentación. Los textos se acomodaron dentro del recuadro y la versión de visualización convierte los textos en curvas para que no dependan de las fuentes instaladas.

La carpeta `assets` contiene los tres logos, la imagen vectorial terminada y su versión editable. `assets/originales` conserva los dos formatos de la plantilla recibida, SVG y CDR.

## Balsas incorporadas

| Balsa | Latitud WGS 84 | Longitud WGS 84 | Fuente de ubicación |
|---|---:|---:|---|
| Sauce Blanco | -40.455926503807504 | -63.78580257156731 | Coordenadas suministradas por el autor |
| Villa Llanquín | -40.89466666666667 | -71.03905555555556 | Conversión de 40°53′40,8″ S; 71°02′20,6″ O |

La descripción del funcionamiento se contrastó con [Vialidad Rionegrina](https://vialidad.rionegro.gov.ar/servicio/213/balsas?n=ODAw). Los puntos se incluyen en Ambiente, Asentamientos y Síntesis. Ambos usan el signo 72 del IGN: rectángulo oblicuo de proporción 1 × 0,6, apéndice de 0,4, inclinación de 45° y línea discontinua. Se usa **el mismo archivo SVG** para el mapa y las referencias, conservando sus proporciones y trazos. En pantalla se aumenta su tamaño para que resulte legible. Los puntos identifican los cruces; no trazan rutas navegables ni describen zonas de influencia.

## Contraste de estaciones

Se compararon por nombre y ubicación cuatro estaciones del IGN con los puntos enlazados por el [sitio oficial del Tren Patagónico](https://trenpatagonicosa.com.ar/las-estaciones/), consultado el 2 de noviembre de 2026:

| Estación | Separación entre puntos IGN y operador |
|---|---:|
| Viedma | 10,17 m |
| San Antonio Oeste | 16,95 m |
| Ingeniero Jacobacci | 15,88 m |
| San Carlos de Bariloche | 23,29 m |

Las distancias son elipsoidales WGS 84. Son diferencias entre puntos de referencia de una instalación, no una evaluación de precisión topográfica. Se conservan las ubicaciones IGN y se suman a sus consultas la dirección y el vínculo del operador. La oficina de venta del centro de Bariloche y la de CABA no se representan como estaciones. El registro del contraste y sus coordenadas está en `data/contraste_estaciones_Tren_Patagonico.json`.

## Uso

Abrir `Tablero_Rio_Negro.html` después de extraer todo el ZIP. Mantener las carpetas `Tablero_Rio_Negro_files` y `assets` junto al HTML. Para editar y volver a compilar, conservar también `data`, `assets` y el Rmd. La compilación utiliza archivos locales; no vuelve a descargar el WFS. El fondo ArgenMap sí requiere conexión.

Los controles numéricos de población, NBI, producción, distancias e intersecciones se conservan de la entrega anterior. El nuevo informe `revision_cartografica_20261102.json` documenta los controles de las geometrías de dibujo y las capas incorporadas.
