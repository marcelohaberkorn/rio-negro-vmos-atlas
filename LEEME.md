# Atlas territorial de Río Negro y VMOS

**Versión final · 23 de octubre de 2026.**

## Abrir y editar

1. Extraer el ZIP completo en una carpeta local.
2. Abrir `entrega_rio_negro/Tablero_Rio_Negro.html` con un navegador.
3. Conservar junto al HTML su carpeta de recursos `Tablero_Rio_Negro_files`.
   La carpeta y su nombre forman parte de la entrega; no mover sólo el HTML.
4. Para editar, abrir `Tablero_Rio_Negro.Rmd` desde esa misma carpeta en RStudio.
5. Ejecutar Knit o `source("Compilar_tablero.R")` desde la carpeta del proyecto.

La cartografía ArgenMap requiere conexión al servicio del IGN. Los datos temáticos,
controles y bibliotecas del visor se incluyen en el proyecto. La salida HTML usa
recursos locales adjuntos (`self_contained: false`) para reducir la conversión de
Pandoc y evitar el empaquetado de todo el tablero en un único archivo enorme.
No se modifican opciones de Windows ni el archivo de paginación del equipo.

El error `VirtualAlloc MEM_COMMIT` comunicado ocurría después del cálculo de R,
durante la conversión de Pandoc. Esta versión reduce también los objetos gráficos:
las copias de visualización se generalizan, media tensión se dibuja como un único
objeto multilineal y los análisis conservan las geometrías originales. El script
`Compilar_tablero.R` separa cálculo y conversión en dos procesos para liberar la
memoria de R antes de iniciar Pandoc. No se verificó en el equipo Windows del autor.

Si faltan paquetes, instalar desde la consola de R:

```r
install.packages(c('flexdashboard','leaflet','sf','htmltools','htmlwidgets',
                  'base64enc','jsonlite','lwgeom','classInt'))
```

## Diez pestañas desarrolladas

1. Presentación y localización: composición bicontinental del proyecto IGN 2025,
   proyección acimutal equiárea de Lambert y Río Negro destacado.
2. Ecorregiones y regiones productivas: regionalizaciones, tramas y agua.
3. Población: atlas con población total, población en radios rurales o mixtos,
   población en radios urbanos y densidad. Incluye trece tortas departamentales
   sobre el mapa y una torta provincial fija, sobre viviendas particulares.
4. Condiciones de vida: hogares con al menos una NBI en 2022; referencia 2010 y
   cinco dimensiones del Censo 2022 consultables. Los totales 2010 y 2022 comparten
   cuatro intervalos iguales de cinco puntos porcentuales y la misma paleta;
   los componentes se clasifican por separado con cortes naturales.
5. Producción: existencias ovinas 2022, bovinas 2021 y superficie cultivada de peras y manzanas en conjunto, 2018 (hectáreas).
6. Infraestructura eléctrica: redes, centrales, estaciones y VMOS.
7. Gobiernos locales: siete municipios intersectados y demás jurisdicciones.
8. Zonas sanitarias: seis zonas, tres intersectadas e indicadores.
9. Asentamientos y conectividad: 356 registros BAHRA, 58 hasta 20 km, tipos,
   dos fondos ArgenMap, rutas y contexto hidrográfico opcional.
10. Síntesis: mapa integrado, resultados cuantificados, análisis territorial,
    oportunidades de seguimiento, presiones posibles y conclusiones con límites
    explícitos de lo que permiten afirmar las capas disponibles.

## Población y NBI: universos y controles

La capa `Departamentos.geojson` se conserva con sus valores originales. Su campo
`pob_22` suma 750.768 habitantes. La tabla validada tiene 747.697 personas en viviendas
particulares, coincidentes con INDEC, Censo 2022, cuadro 1.16 de la publicación de
población afrodescendiente. La diferencia es de universo censal, no un error de suma.
La unión usa el código INDEC de cinco caracteres; 13/13 departamentos coinciden.
Los nombres de los campos originales `pob_urb_10` y `pob_rur_10` no se utilizan
como datos de 2022.

El CSV divide la población por radios U, R y M. Su columna rural total suma R+M.
Por eso el gráfico dice radios urbanos / radios rurales o mixtos: no es una
estimación de condición urbana/rural individual por localidad. Los valores en radios
R son 6.518 y en M 48.114. Los gráficos y las opciones del atlas identifican los tipos de radio y el universo
de viviendas particulares.

Se detectó que `NBI_TOTAL` suma las cinco privaciones en todos los departamentos.
No se utiliza como porcentaje de hogares únicos con NBI. Se recuperaron de
Poblaciones/CONICET los hogares con al menos una NBI y el total de hogares de 2022,
procesados por Pablo de Grande y Agustín Salvia a partir de REDATAM INDEC.
Fuente: https://datosdeinvestigacion.conicet.gov.ar/handle/11336/277944

La extracción departamental está en `data/nbi_2022_verificado.csv`; los registros
de origen y el método de vinculación se conservan en `data/nbi_2022_fuente.json`.
El punto representativo de cada registro cae dentro del departamento y sus
13 denominadores coinciden exactamente con `HOGARES` en la capa del autor.
El total verificado es 278.935 hogares; 16.447 tienen al menos una NBI (5,8964 %).
El indicador se calcula de nuevo a partir de esos conteos; no se suman componentes.

## Producción y períodos

Se conservan `ovinos_22` y `bovinos_21` como existencias en cabezas de los años
indicados. SENASA publica distintos cortes de stock; no se los sustituye por
otros del mismo año sin saber la fecha exacta de la capa.

El campo `PerMan_18` reúne peras y manzanas en conjunto para 2018. La fuente
verificada es el Informe productivo provincial Río Negro de mayo de 2022, página 17,
con base en CNA 2018 y SENASA. El mapa original mide superficie cultivada en
hectáreas y reproduce los cortes 3.730 y 24.504. Por ello se corrigió la unidad
de la versión anterior: estos valores no representan toneladas. Se conservan
los números de la capa. Fuente directa:
https://www.argentina.gob.ar/sites/default/files/39_2022_rio_negro.pdf#page=17

Las cinco dimensiones
de NBI de la capa corresponden al Censo 2022, según la precisión del autor.

## Análisis y visualización

Las distancias BAHRA se calculan sobre WGS 84 elipsoidal. Intersecciones y longitudes
locales se calculan con las geometrías originales en una proyección azimutal local.
El entorno dibujado de 20 km es una referencia cartográfica, no un área de impacto.
Los porcentajes poblacionales y ganaderos de departamentos atravesados se refieren
al departamento completo: no se prorratean por superficie ni se asignan al corredor.

Las copias `data/visual` generalizan a 90 m (40 m para rutas y traza) para aliviar
el visor. Donde las capas forman coberturas válidas, se preservan sus bordes comunes.
El JSON de pantalla se redondea a cinco decimales. Los originales y los cálculos no
se redondean ni se reemplazan por las copias visuales. El mapa no es apto para
mensura ni para localizar obras de detalle.

Salvo en la comparación de los totales de NBI 2010/2022, los cortes de Jenks se
calculan con classInt sobre los 13 valores completos,
hasta cinco clases por variable, con igualdad incluida en el intervalo inferior.
En fruticultura se distingue el cero. Sólo se redondean los rangos mostrados
en las referencias: se usa la centena para conteos cuando la separación de los
valores lo permite, y mayor precisión cuando evita cambiar el grupo de un valor.
Los intervalos discretos empiezan una unidad después del anterior; los continuos
indican la exclusión del extremo inferior con >. Los cortes analíticos y los colores
no cambian por ese formato. Las clases y los colores son propios de cada
variable, con la excepción explícita de los totales NBI 2010 y 2022, que comparten
intervalos y colores. Ninguna clasificación representa umbrales de riesgo.

Los límites y la simbología vial mantienen las convenciones IGN ya incorporadas.
Los recursos para su revisión están citados en Notas; las rutas son opcionales
y sus identificadores se regulan por zoom y colisiones. VMOS conserva su jerarquía
sobre la red vial. Se muestra un identificador por ruta y jurisdicción dentro de
cada vista, eligiendo entre candidatos del trazado unificado. El mapa bicontinental
retoma la proyección acimutal equiárea de Lambert del IGN, centrada en 40° S y 60° O,
que permite incluir el Polo Sur. La flecha se calcula con la dirección proyectada
del meridiano en el centro de la vista y cambia al desplazar o acercar el mapa.
Las capas de la presentación permanecen activas y las provincias, salvo Río Negro,
comparten el mismo tono pastel. La imagen de referencia queda incluida en assets.

`control_departamentos.csv`, `revision_atlas.json`, `revision_visualizacion.json`
y los registros previos documentan datos, decisiones y verificaciones. Para una
evaluación de efectos se sumarían establecimientos, cruces de obra y mediciones
antes/después de empleo, tránsito, agua y servicios. El atlas actual no simula impactos.

La capa departamental supera la máscara provincial anterior en 216,93 km², sin
huecos significativos. Se conservan ambas fuentes sin inventar una reasignación
jurisdiccional. La discrepancia se cuantifica en `revision_atlas.json`.

## Revisión del 23 de octubre de 2026

Se aplicaron las correcciones de presentación, población, NBI, producción y síntesis.
La conclusión desarrolla la función del atlas como apoyo al diagnóstico, planificación
y seguimiento territorial. Se retiraron las notas y secciones indicadas por el autor.
La firma y los créditos institucionales se presentan con la gráfica aportada y
composición HTML; el crédito docente corresponde a Lic. Andrea Marcela Silva.

## Segunda revisión del 23 de octubre de 2026

NBI 2010 y 2022 usan los límites 0, 5, 10, 15 y 20 %, con la misma paleta y cierre
a derecha. Los intervalos permanecen visibles aunque un año no tenga valores
en una clase. Las dimensiones de NBI mantienen sus clasificaciones propias.
Las secciones de análisis son Ambiente, Sociedad y producción e Infraestructuras
y territorios. La gráfica institucional se presenta completa, con el crédito
docente solicitado. Los value boxes ganaderos usan siluetas de oveja y vaca,
y los popups BAHRA conservan la distancia sin repetir la categoría de cercanía.

## Cierre de la versión final

Se retiraron las aclaraciones 3 y 4 de la presentación. Los indicadores ganaderos
quedaron como «cabezas ovinas - dato 2022» y «cabezas bovinas - datos 2021».
