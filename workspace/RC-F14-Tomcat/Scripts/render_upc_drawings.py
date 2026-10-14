import pymupdf, os
pdf=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\UPC_F14_Drawings.pdf'
doc=pymupdf.open(pdf)
out=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\UPC_drawings_pages'
os.makedirs(out,exist_ok=True)
for pno in range(17,23):
    pix=doc[pno].get_pixmap(matrix=pymupdf.Matrix(2.2,2.2),alpha=False)
    fn=os.path.join(out,f'draw_{pno+1:02d}.png')
    pix.save(fn); print(fn)
