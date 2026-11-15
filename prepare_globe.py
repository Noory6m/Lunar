"""Optional regeneration. Install numpy and Pillow only when using this script.
Input: original NASA LRO LOLA PDS LDEM_4.IMG (included) and authoritative LBL.
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
a=np.fromfile(ROOT/'data/LDEM_4.IMG',dtype='<i2').reshape(720,1440).astype(float)*.5
a=np.roll(a,720,axis=1)
b=a.reshape(180,4,360,4).mean(axis=(1,3))
meta=dict(rows=180,cols=360,z=np.round(b,1).ravel().tolist(),units='m',radiusM=1737400,lonMin=-180,latMax=90,spacingDeg=1,nativeSpacingDeg=.25,source='NASA LRO LOLA LDEM_4',sourceUrl='https://imbrium.mit.edu/DATA/LOLA_GDR/CYLINDRICAL/IMG/',texture='lola-relief.jpg',textureType='LOLA topographic shaded relief, not optical imagery')
assets=ROOT/'frontend/assets';(assets/'globe-dem.json').write_text(json.dumps(meta,separators=(',',':')))
gy,gx=np.gradient(a);nx=-gx/4000;ny=-gy/4000
norm=np.sqrt(nx*nx+ny*ny+1);shade=np.clip((-.6*nx-.3*ny+.74)/norm,0,1)
gray=np.clip(65+shade*130+(a-a.mean())/600,0,255).astype('uint8')
Image.fromarray(gray).save(assets/'lola-relief.jpg',quality=92)
print('Recreated real-coordinate globe and data-derived relief.')
