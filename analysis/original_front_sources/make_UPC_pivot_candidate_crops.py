from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'references' / 'UPC_Figure3_15_source_exact.png'
OUT = ROOT / 'analysis' / 'original_front_sources'

im = Image.open(SRC)
print('source_size', im.size)
boxes = {
    'UPC_plan_pivot_candidate_crop.png': (1320, 1250, 1480, 2200),
    'UPC_side_pivot_candidate_crop.png': (1320, 2500, 1480, 2940),
}
for name, box in boxes.items():
    crop = im.crop(box)
    crop.save(OUT / name)
    print(name, box, crop.size)
