# Ejecutar desde la carpeta del proyecto; requiere sf.
# Las originales no se modifican. Se escribe cada recorte en data/.
library(sf)
anterior <- sf_use_s2(FALSE)
tryCatch({
  provincia <- st_zm(st_read('data/provincia.geojson',quiet=TRUE))
  mascara <- st_union(st_make_valid(st_geometry(st_transform(provincia,4326))))
  for(nombre in c('vial_nacional','vial_provincial')) {
    original <- st_read(file.path('data','originales',paste0(nombre,'.geojson')),quiet=TRUE)
    original <- st_transform(st_zm(original),4326)
    candidatos <- lengths(st_intersects(original,mascara))>0
    recorte <- suppressWarnings(st_intersection(original[candidatos,],mascara))
    recorte <- recorte[!st_is_empty(recorte) & st_dimension(recorte)==1,]
    st_write(recorte,file.path('data',paste0(nombre,'.geojson')),delete_dsn=TRUE,quiet=TRUE)
    message(nombre,': ',nrow(recorte),' segmentos recortados.')
  }
},finally=sf_use_s2(anterior))
