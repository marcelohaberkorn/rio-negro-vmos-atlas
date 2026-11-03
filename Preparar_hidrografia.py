"""Regenera la hidrografía suavizada y aplica la selección de dibujo revisada.

Requiere numpy, shapely >= 2 y pyproj. Ejecutar: python Preparar_hidrografia.py
No es necesario ejecutarlo para compilar el Rmd: los resultados se incluyen.
Conserva data/corrientes.geojson y escribe solamente su copia visual y controles.
"""
from pathlib import Path
import json,math,csv,hashlib
import numpy as np
from shapely.geometry import shape,mapping,LineString,MultiLineString,box
from shapely.ops import transform
from shapely.strtree import STRtree
from shapely.geometry import Point
from pyproj import Transformer
r=Path(__file__).resolve().parent;p=r/'data/corrientes.geojson'
fwd=Transformer.from_crs(4326,'+proj=aeqd +lat_0=-40 +lon_0=-67 +datum=WGS84 +units=m',always_xy=True).transform
inv=Transformer.from_crs('+proj=aeqd +lat_0=-40 +lon_0=-67 +datum=WGS84 +units=m',4326,always_xy=True).transform
d=json.loads(p.read_text());regiones=[('Choele Choel',box(-65.96,-39.43,-65.53,-39.16)),('General Roca',box(-67.9,-39.17,-67.35,-38.97))]
originales_metric=[transform(fwd,shape(f['geometry'])) for f in d['features']]
nodos=[]
for g in originales_metric:
 for parte in list(g.geoms) if g.geom_type=='MultiLineString' else [g]:
  nodos.extend([Point(parte.coords[0]),Point(parte.coords[-1])])
arbol_nodos=STRtree(nodos);cache_nodos={}
def es_nodo(c):
 llave=tuple(c)
 if llave not in cache_nodos:cache_nodos[llave]=bool(len(arbol_nodos.query(Point(c),predicate='dwithin',distance=.05)))
 return cache_nodos[llave]
def simplificar_con_nodos(g):
 if g.geom_type=='MultiLineString':return MultiLineString([simplificar_con_nodos(x) for x in g.geoms])
 c=list(g.coords);indices=[i for i,punto in enumerate(c) if i in (0,len(c)-1) or es_nodo(punto)];out=[]
 for a,b in zip(indices[:-1],indices[1:]):
  tramo=list(LineString(c[a:b+1]).simplify(5,preserve_topology=True).coords)
  out.extend(tramo if not out else tramo[1:])
 return LineString(out)
aux=[];report=[];maxdev=0;invalid=0;extremos=0;vertices=0
def suavizar_linea(g):
 if g.geom_type=='MultiLineString':return MultiLineString([suavizar_linea(x) for x in g.geoms])
 c=np.asarray(g.coords)[:,:2];out=[c[0]]
 for i in range(1,len(c)-1):
  a,b,z=c[i-1:i+2];ab=np.linalg.norm(a-b);bz=np.linalg.norm(z-b)
  if min(ab,bz)<1e-8:continue
  if es_nodo(b):out.append(b);continue
  recorte=min(140,.28*ab,.28*bz);q=b+(a-b)*recorte/ab;v=b+(z-b)*recorte/bz
  # Bézier cuadrática dentro del triángulo local: no introduce sobrepasos de spline.
  for t in [0,.25,.5,.75,1]:out.append((1-t)**2*q+2*t*(1-t)*b+t*t*v)
 out.append(c[-1]);return LineString(out)
for f in d['features']:
 original=shape(f['geometry']);g=transform(fwd,original);sg=simplificar_con_nodos(g)
 nuevo=suavizar_linea(sg);dev=g.hausdorff_distance(nuevo)
 if not nuevo.is_valid or dev>80:nuevo=sg;dev=g.hausdorff_distance(nuevo)
 invalid+=not nuevo.is_valid;maxdev=max(maxdev,dev)
 for antes,desp in zip(list(g.geoms) if g.geom_type=='MultiLineString' else [g],list(nuevo.geoms) if nuevo.geom_type=='MultiLineString' else [nuevo]):
  extremos+=int(np.linalg.norm(np.asarray(antes.coords)[0,:2]-np.asarray(desp.coords)[0,:2])>.001 or np.linalg.norm(np.asarray(antes.coords)[-1,:2]-np.asarray(desp.coords)[-1,:2])>.001)
  vertices+=len(desp.coords)
 nombre=f['properties'].get('fna');razon='';zona=''
 if original.geom_type=='LineString':
  for region,limite in regiones:
   if limite.covers(original):
    if original.is_ring:razon='Trazado cerrado en sector señalado: separado del dibujo principal para revisión'
    elif not nombre:razon='Trazado sin denominación en sector señalado: separado del dibujo principal para revisión'
    if razon:zona=region;break
 if razon:aux.append({'gid':f['properties']['gid'],'nombre':nombre or '', 'sector':zona,'motivo':razon,'longitud_original_m':round(g.length,2)})
 f['geometry']=mapping(transform(inv,nuevo))
# Detectar fragmentos pequeños que, tras separar los auxiliares, quedan aislados.
# Se usan los originales para medir la conectividad, no las líneas suavizadas.
raw=json.loads(p.read_text())['features'];metricas=[transform(fwd,shape(f['geometry'])) for f in raw]
ids_aux={x['gid'] for x in aux};visibles=[i for i,f in enumerate(raw) if f['properties']['gid'] not in ids_aux]
arbol=STRtree([metricas[i] for i in visibles])
for i in visibles:
 f=raw[i];g=metricas[i]
 if g.geom_type!='LineString' or g.length>200:continue
 zona=next((nom for nom,caja in regiones if caja.covers(shape(f['geometry']))),'')
 if not zona:continue
 conexiones=0
 for extremo in [g.coords[0],g.coords[-1]]:
  pt=Point(extremo)
  conexiones+=sum(visibles[int(j)]!=i and pt.distance(metricas[visibles[int(j)]])<5 for j in arbol.query(pt.buffer(5)))
 if not conexiones:aux.append({'gid':f['properties']['gid'],'nombre':f['properties'].get('fna') or '', 'sector':zona,'motivo':'Fragmento menor de 200 m sin conexión a otros trazados principales a 5 m: separado para revisión','longitud_original_m':round(g.length,2)})
(r/'data/visual/corrientes.geojson').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
with (r/'data/revision_hidrografia_20261103.csv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=['gid','nombre','sector','motivo','longitud_original_m']);w.writeheader();w.writerows(aux)
res={'fecha':'2026-11-03','fuente_original_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'registros_originales':len(d['features']),'registros_auxiliares':len(aux),'registros_dibujo_principal':len(d['features'])-len(aux),'detalle_auxiliares':aux,'criterio_auxiliares':'Sólo en las ventanas de revisión de General Roca y Choele Choel: trazados cerrados, sin denominación o menores de 200 m sin conexión al resto del dibujo principal a 5 m. No se visualizan en el tablero; no se afirma que sean cursos inexistentes ni se altera la base original.','suavizado':{'metodo':'Bézier cuadrática local tras simplificación de 5 m; extremos y vértices de conexión conservados; sin ajuste al mapa base','recorte_maximo_esquinas_m':140,'fraccion_maxima_de_segmento':.28,'desplazamiento_maximo_verificado_m':round(maxdev,3),'umbral_control_m':80,'geometrias_invalidas':invalid,'extremos_modificados':extremos,'vertices':vertices}}
(r/'revision_cartografica_20261103.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in res.items() if k!='detalle_auxiliares'},ensure_ascii=False,indent=2))

# Aplicar también la selección por partes de la última revisión.
import runpy
runpy.run_path(str(r/"Preparar_corrientes_principales.py"),run_name="__main__")
