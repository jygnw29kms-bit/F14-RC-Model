from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'references'/'UPC_Figure3_15_source_exact.png'
REG=ROOT/'analysis'/'original_front_sources'/'Navy_UPC_side_longitudinal_landmark_fit.json'
OUT=ROOT/'analysis'/'original_front_sources'/'UPC_side_NASA_antenna_FS_overlay.png'
r=json.loads(REG.read_text(encoding='utf-8'))['nominal_fit'];slope=float(r['slope_px_per_FS_in']);inter=float(r['FS0_x_px'])
pts=[('ILG',171,106.5),('ACLS',178,106.5),('UHAOT',191,166.5),('RDR/ALTR',207,123.5),('TOP411',411,192.3),('UDATA',511,177.5),('AFT663',663,95.0),('IFF3P',811,177.5)]
box=(350,2550,2113,2953);im=Image.open(SRC).convert('RGB').crop(box);d=ImageDraw.Draw(im)
for name,fs,wl in pts:
 x=inter+slope*fs;xx=x-box[0]
 if 0<=xx<im.width:
  d.line((xx,0,xx,im.height),fill=(255,0,0),width=2);d.text((xx+3,5),f'{name} FS{fs} WL{wl}',fill=(255,0,0))
im.save(OUT);print([(n,fs,wl,inter+slope*fs) for n,fs,wl in pts])
