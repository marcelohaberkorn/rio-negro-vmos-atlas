"""Prepara la misma salida flexdashboard con datos de mapas en scripts externos.

Ejecutar tras Compilar_tablero.R: python Publicar_tablero.py
Conserva el HTML original en distribucion/Tablero_Rio_Negro.html.gz.
Los scripts defer se ejecutan antes de DOMContentLoaded, cuando htmlwidgets lee
los bloques JSON. Su texto se repone exactamente, sin redondear coordenadas.
"""
from pathlib import Path
import json,re,gzip,hashlib,shutil
R=Path(__file__).resolve().parent
source=R/'Tablero_Rio_Negro.html';text=source.read_text();payloads={}
folder=Path('Tablero_Rio_Negro_files/widget-data-20261103')
def separar(m):
 attrs,raw=m.group(1),m.group(2)
 if 'application/json' not in attrs or len(raw)<100000:return m.group(0)
 widget=re.search(r'data-for="([^"]+)"',attrs)
 if not widget:return m.group(0)
 wid=widget.group(1);rel=folder/(wid+'.js');path=R/rel;path.parent.mkdir(parents=True,exist_ok=True)
 # Una cadena JSON conserva el texto original del bloque sin reinterpretarlo.
 js='document.getElementById('+json.dumps(wid+'-data')+').textContent='+json.dumps(raw,ensure_ascii=False)+';\n'
 path.write_text(js);payloads[rel.as_posix()]=hashlib.sha256(js.encode()).hexdigest()
 return '<script'+attrs+' id="'+wid+'-data"></script>\n<script defer src="'+rel.as_posix()+'"></script>'
new=re.sub(r'<script\b([^>]*)>(.*?)</script>',separar,text,flags=re.S)
if not payloads:raise SystemExit('Primero compilar el HTML completo desde el Rmd; no se modifica una salida ya separada.')
archive=R/'distribucion/Tablero_Rio_Negro.html.gz';archive.parent.mkdir(exist_ok=True);archive.write_bytes(gzip.compress(source.read_bytes(),compresslevel=6,mtime=0))
source.write_text(new)
docs=R/'docs';docs.mkdir(exist_ok=True);(docs/'index.html').write_text(new)
for d in ['assets','Tablero_Rio_Negro_files']:shutil.copytree(R/d,docs/d,dirs_exist_ok=True)
(docs/'.nojekyll').write_text('')
manifest={'version':'2026-11-03-cierre','fecha':'2026-11-03','html_sha256':hashlib.sha256(new.encode()).hexdigest(),'html_original_sha256':hashlib.sha256(text.encode()).hexdigest(),'html_original_comprimido':'distribucion/Tablero_Rio_Negro.html.gz','rmd_sha256':hashlib.sha256((R/'Tablero_Rio_Negro.Rmd').read_bytes()).hexdigest(),'mapas_externos':payloads,'url':'https://marcelohaberkorn.github.io/rio-negro-vmos-atlas/','pestanas':10}
(docs/'version.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('Mapas preparados:',len(payloads),'· HTML original y datos preservados.')
