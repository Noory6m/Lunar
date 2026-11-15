"""Optional polar-grid regeneration. Requires rasterio and numpy.
The application itself uses bundled prepared grids and needs neither package.
Usage: python tools/prepare_polar.py /path/to/Site01_final_adj_5mpp_surf.tif
NASA source: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site01/Site01_final_adj_5mpp_surf.tif
"""
import sys,json
from pathlib import Path
import rasterio,numpy as np
from rasterio.enums import Resampling
from rasterio.windows import from_bounds
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'frontend/assets'
def prepare(src,rows,cols,window=None):
 a=src.read(1,out_shape=(rows,cols),masked=True,resampling=Resampling.bilinear,window=window)
 bounds=src.bounds if window is None else rasterio.windows.bounds(window,src.transform)
 valid=~np.ma.getmaskarray(a)&np.isfinite(a.data);z=np.where(valid,a.data,0)
 return dict(rows=rows,cols=cols,z=np.round(z,2).ravel().tolist(),valid=valid.astype(int).ravel().tolist(),bounds=list(bounds),min=float(a.data[valid].min()),max=float(a.data[valid].max()))
if len(sys.argv)!=2:raise SystemExit(__doc__)
with rasterio.open(sys.argv[1]) as s:
 d=prepare(s,320,320);d.update(name='Connecting Ridge',site='Site 01',nativePixelM=5,previewPixelM=50,referenceRadiusM=1737400,frame='MOON_ME / DE421',sourceUrl='https://pgda.gsfc.nasa.gov/products/78')
 (out/'mission-terrain.json').write_text(json.dumps(d,separators=(',',':')))
url='https://pgda.gsfc.nasa.gov/data/LOLA_20mpp/LDEM_80S_80MPP_ADJ.TIF'
with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.TIF',GDAL_HTTP_TIMEOUT='60'):
 with rasterio.open(url) as s:
  window=from_bounds(-171000,-172000,149000,148000,transform=s.transform)
  d=prepare(s,320,320,window);d.update(name='Regional LOLA context',previewPixelM=1000,referenceRadiusM=1737400,sourceUrl='https://pgda.gsfc.nasa.gov/products/90')
  (out/'regional-terrain.json').write_text(json.dumps(d,separators=(',',':')))
print('Recreated local and regional polar meshes.')
