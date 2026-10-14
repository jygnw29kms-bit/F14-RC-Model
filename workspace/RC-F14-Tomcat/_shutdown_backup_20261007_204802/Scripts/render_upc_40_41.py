import pymupdf, os
pdf=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\UPC_F14_Structure_Report.pdf'
doc=pymupdf.open(pdf)
outdir=r'C:\Users\dezen\Desktop\135er-Spandau-Defeat\side-projects\F14_TOMCAT_RC\references\UPC_pages'
for pno in [39,40]:
    pix=doc[pno].get_pixmap(matrix=pymupdf.Matrix(2.5,2.5),alpha=False)
    out=os.path.join(outdir,f'UPC_page_{pno+1:03d}.png')
    pix.save(out)
    print(out)
