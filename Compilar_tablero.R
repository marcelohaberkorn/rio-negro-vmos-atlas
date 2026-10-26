# Alternativa a Knit para reducir el pico de memoria.
# Ejecutar desde la carpeta que contiene Tablero_Rio_Negro.Rmd.
archivo <- normalizePath('Tablero_Rio_Negro.Rmd', mustWork=TRUE)
rscript <- file.path(R.home('bin'), if(.Platform$OS.type=='windows') 'Rscript.exe' else 'Rscript')
registro <- tempfile('rn-compilacion-',fileext='.rds')
paso1 <- tempfile('rn-calculo-',fileext='.R')
paso2 <- tempfile('rn-html-',fileext='.R')
texto_r <- function(x) paste(capture.output(dput(x)),collapse='\n')
writeLines(c(
  paste0('x <- rmarkdown::render(',texto_r(archivo),',run_pandoc=FALSE,clean=FALSE,quiet=FALSE)'),
  paste0('saveRDS(x,',texto_r(registro),')')
),paso1)
writeLines(c(
  paste0('x <- readRDS(',texto_r(registro),')'),
  paste0('rmarkdown::render(input=as.character(x),output_file="Tablero_Rio_Negro.html",',
         'knit_meta=attr(x,"knit_meta"),clean=FALSE,quiet=FALSE)')
),paso2)
resultado1 <- system2(rscript,c('--vanilla',shQuote(paso1)))
if(resultado1!=0) stop('Falló el cálculo del tablero. Revisá los mensajes anteriores.')
resultado2 <- system2(rscript,c('--vanilla',shQuote(paso2)))
if(resultado2!=0) stop('Falló la conversión a HTML. Se conservó el cálculo intermedio para revisar el error.')
intermedio <- as.character(readRDS(registro))
unlink(c(paso1,paso2,registro,intermedio))
message('Tablero_Rio_Negro.html generado. Mantené data y assets junto al Rmd para editarlo.')
