import fitz
from pathlib import Path
pdf=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/references/NASA_CR3992_F14_VSTFE.pdf")
doc=fitz.open(pdf)
out=Path(r"C:/Users/dezen/Desktop/JL1976/F14-Tomcat/F14-RC-Model/analysis/original_front_sources/CR3992_hi");out.mkdir(parents=True,exist_ok=True)
for pno,name in [(87,'page088_fig48_49'),(88,'page089_fig50')]:
 page=doc[pno];pix=page.get_pixmap(matrix=fitz.Matrix(4,4),alpha=False);path=out/(name+'.png');pix.save(path);print(path,pix.width,pix.height)
