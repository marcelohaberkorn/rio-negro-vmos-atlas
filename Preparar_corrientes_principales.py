"""Regenera la copia de dibujo aplicando la selección de tramos revisados.

Ejecutar después de Preparar_hidrografia.py. Requiere únicamente Python 3.
Los registros y las partes excluidos se documentan en el CSV de depuración.
La base original de análisis permanece intacta. No genera una capa auxiliar.
"""
from pathlib import Path
import json,csv
r=Path(__file__).resolve().parent
omit={(int(f['gid']),int(f['parte'])) for f in csv.DictReader((r/'data/depuracion_corrientes_20261103.csv').open())}
d=json.loads((r/'data/visual/corrientes.geojson').read_text());out=[]
for f in d['features']:
 g=f['geometry'];parts=g['coordinates'] if g['type']=='MultiLineString' else [g['coordinates']]
 for i,c in enumerate(parts):
  if (int(f['properties']['gid']),i) in omit:continue
  out.append({'type':'Feature','properties':dict(f['properties'],parte_original=i),'geometry':{'type':'LineString','coordinates':c}})
(r/'data/visual/corrientes_principales.geojson').write_text(json.dumps({'type':'FeatureCollection','features':out},ensure_ascii=False,separators=(',',':')))
print('Partes de dibujo:',len(out),'· partes excluidas:',len(omit))
